
# --- HTTPServer-based UI backend (Day 09 Multi-Agent) ---
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from graph import run_graph
from mcp_server import list_tools

ROOT_DIR = Path(__file__).parent
UI_DIR = ROOT_DIR / "ui"
HOST = "127.0.0.1"
PORT = 8008

# Câu hỏi gợi ý — bao gồm cả grading questions chính
SUGGESTED_QUESTIONS = [
    "SLA xử lý ticket P1 là bao lâu?",
    "Ticket P1 lúc 22:47 — ai nhận thông báo đầu tiên, qua kênh nào, escalation lúc mấy giờ?",
    "Khách hàng Flash Sale yêu cầu hoàn tiền vì sản phẩm lỗi — được không?",
    "Sản phẩm kỹ thuật số (license key) có được hoàn tiền không?",
    "Ai phải phê duyệt để cấp quyền Level 3? Bao nhiêu người?",
    "Store credit khi hoàn tiền có giá trị bao nhiêu so với tiền gốc?",
    "Nhân viên vừa vào thử việc muốn làm remote — điều kiện là gì?",
    "Mức phạt tài chính khi vi phạm SLA P1 là bao nhiêu?",
    "Ticket P1 lúc 2am + cần cấp quyền Level 2 tạm thời cho contractor — quy trình cả hai?",
    "ERR-403-AUTH là lỗi gì và cách xử lý?",
]


def format_trace(history: list) -> list:
    """Chuyển history list thành structured trace steps."""
    trace = []
    for step in history:
        if not isinstance(step, str):
            continue
        if "]" in step:
            agent, action = step.split("]", 1)
            trace.append({"agent": agent.strip("[ "), "action": action.strip()})
        else:
            trace.append({"agent": "system", "action": step})
    return trace


def format_mcp_tools(mcp_tools_used: list) -> list:
    """Format MCP tool call list để gửi về UI."""
    out = []
    for call in mcp_tools_used:
        if not isinstance(call, dict):
            continue
        out.append({
            "tool": call.get("tool", "unknown"),
            "timestamp": call.get("timestamp", ""),
            "success": call.get("error") is None,
            "error": call.get("error"),
        })
    return out


class RagUIHandler(BaseHTTPRequestHandler):
    server_version = "Day09MultiAgent/1.0"

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: Path, content_type: str) -> None:
        body = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._send_file(UI_DIR / "index.html", "text/html")
            return

        if path == "/api/suggestions":
            self._send_json({"questions": SUGGESTED_QUESTIONS})
            return

        # MCP tools discovery — dùng để hiển thị trong UI
        if path == "/api/tools":
            tools = list_tools()
            self._send_json({"tools": [
                {"name": t["name"], "description": t["description"]}
                for t in tools
            ]})
            return

        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/ask":
            self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self._send_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
            return

        question = (payload.get("question") or "").strip()
        if not question:
            self._send_json({"error": "Câu hỏi không được để trống."}, status=HTTPStatus.BAD_REQUEST)
            return

        try:
            result = run_graph(question)

            # Tất cả trường day09 quan trọng đều được trả về
            response = {
                # Kết quả chính
                "final_answer": result.get("final_answer", ""),
                "sources": result.get("sources") or result.get("retrieved_sources", []),
                "confidence": result.get("confidence", 0.0),

                # Supervisor decision — key day09 fields
                "supervisor_route": result.get("supervisor_route", "unknown"),
                "route_reason": result.get("route_reason", ""),
                "risk_high": result.get("risk_high", False),
                "needs_tool": result.get("needs_tool", False),

                # Workers invoked
                "workers_called": result.get("workers_called", []),

                # MCP tools
                "mcp_tools_used": format_mcp_tools(result.get("mcp_tools_used", [])),

                # HITL
                "hitl_triggered": result.get("hitl_triggered", False),

                # Perf
                "latency_ms": result.get("latency_ms"),
                "run_id": result.get("run_id", ""),

                # Full trace
                "trace": format_trace(result.get("history", [])),
            }
            self._send_json(response)

        except Exception as exc:
            self._send_json(
                {"error": f"Pipeline error: {exc}"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def log_message(self, format: str, *args) -> None:
        return  # tắt access log để console sạch


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), RagUIHandler)
    print(f"Day 09 Multi-Agent UI: http://{HOST}:{PORT}")
    print("Ctrl+C de dung server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
