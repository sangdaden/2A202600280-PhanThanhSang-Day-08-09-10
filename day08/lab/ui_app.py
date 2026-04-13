import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from rag_answer import rag_answer, suggest_followups


ROOT_DIR = Path(__file__).parent
UI_DIR = ROOT_DIR / "ui"
HOST = "127.0.0.1"
PORT = 8008

SUGGESTED_QUESTIONS = [
    "SLA xử lý ticket P1 là bao lâu?",
    "Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?",
    "Ai phải phê duyệt để cấp quyền Level 3?",
    "Approval Matrix để cấp quyền hệ thống là tài liệu nào?",
    "Nhân viên được làm remote tối đa mấy ngày mỗi tuần?",
    "ERR-403-AUTH là lỗi gì và cách xử lý?",
]


class RagUIHandler(BaseHTTPRequestHandler):
    server_version = "RagUILocal/1.0"

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
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
        if parsed.path in ("/", "/index.html"):
            self._send_file(UI_DIR / "index.html", "text/html")
            return

        if parsed.path == "/api/suggestions":
            self._send_json({"questions": SUGGESTED_QUESTIONS})
            return

        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/followups":
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, status=HTTPStatus.BAD_REQUEST)
                return
            question = (payload.get("question") or "").strip()
            answer   = (payload.get("answer")   or "").strip()
            if not question or not answer:
                self._send_json({"followups": []})
                return
            try:
                followups = suggest_followups(question, answer)
            except Exception:
                followups = []
            self._send_json({"followups": followups})
            return

        if parsed.path != "/api/ask":
            self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
            return

        question = (payload.get("question") or "").strip()
        retrieval_mode = (payload.get("retrieval_mode") or "dense").strip()
        use_rerank = bool(payload.get("use_rerank", False))

        if not question:
            self._send_json({"error": "Question is required"}, status=HTTPStatus.BAD_REQUEST)
            return

        try:
            result = rag_answer(
                query=question,
                retrieval_mode=retrieval_mode,
                use_rerank=use_rerank,
                verbose=False,
            )
        except Exception as exc:
            self._send_json(
                {"error": f"Không thể xử lý câu hỏi: {exc}"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        self._send_json(result)

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), RagUIHandler)
    print(f"RAG UI đang chạy tại: http://{HOST}:{PORT}")
    print("Nhấn Ctrl+C để dừng server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()