# Phân công công việc cho 5 người - Lab Day 09

Ngày tạo: 2026-04-13

## Mục tiêu
Phân công 5 thành viên để:
- Đáp ứng đầy đủ vai trò bắt buộc: Supervisor, Worker, MCP, Trace-Docs.
- Có bằng chứng đóng góp rõ ràng cho từng cá nhân.
- Giảm rủi ro mất điểm do thiếu trace, sai contract, hoặc report không khớp code.

## Phân vai đề xuất (thay M1..M5 bằng tên thật)

| Thành viên | Vai chính | Sprint lead | File chịu trách nhiệm | Đầu ra bắt buộc |
|---|---|---|---|---|
| M1 | Supervisor Owner + Integrator | Sprint 1 | graph.py | Route đúng ít nhất 2 loại task, route_reason rõ ràng, state đầy đủ |
| M2 | Worker Owner A (Retrieval) | Sprint 2 | workers/retrieval.py | Worker chạy độc lập, ghi retrieved_chunks và worker_io_log |
| M3 | Worker Owner B (Policy + Contracts) | Sprint 2 | workers/policy_tool.py, contracts/worker_contracts.yaml | Xử lý ít nhất 1 exception case (Flash Sale hoặc digital), I/O khớp contract |
| M4 | MCP Owner | Sprint 3 | mcp_server.py, phối hợp workers/policy_tool.py | Có ít nhất 2 tools, policy worker gọi MCP thay vì direct call |
| M5 | Trace & Docs Owner + QA Release | Sprint 4 | eval_trace.py, docs/*.md, artifacts/grading_run.jsonl | Chạy 15 test end-to-end, trace đủ field, docs có số liệu thật |

## Timeline thực hiện (4 sprint)

### Sprint 1 (60 phút)
- M1:
  - Hoàn thành AgentState và supervisor routing trong graph.py.
  - Có route_reason cụ thể cho mỗi route.
- M5:
  - Chuẩn bị mẫu trace field trong eval_trace.py để đồng bộ với graph.

### Sprint 2 (60 phút)
- M2:
  - Hoàn thành retrieval worker + test độc lập.
- M3:
  - Hoàn thành policy worker + exception case + contract yaml.
- M1:
  - Tích hợp retrieval/policy vào graph.

### Sprint 3 (60 phút)
- M4:
  - Implement mcp_server với 2 tools tối thiểu: search_kb, get_ticket_info.
- M3:
  - Nối policy worker sang MCP client.
- M5:
  - Kiểm tra trace có mcp_tool_called, mcp_result.

### Sprint 4 (60 phút)
- M5:
  - Chạy full 15 test questions, sinh trace và metrics.
  - Điền 3 file docs: system_architecture, routing_decisions, single_vs_multi_comparison.
- M1, M2, M3, M4:
  - Sửa lỗi theo trace, chốt output.

## Ma trận owner theo deliverables

| Deliverable | Owner chính | Owner dự phòng |
|---|---|---|
| graph.py | M1 | M5 |
| workers/retrieval.py | M2 | M3 |
| workers/policy_tool.py | M3 | M4 |
| workers/synthesis.py | M2 | M1 |
| mcp_server.py | M4 | M1 |
| contracts/worker_contracts.yaml | M3 | M2 |
| eval_trace.py | M5 | M1 |
| artifacts/grading_run.jsonl | M5 | M4 |
| docs/system_architecture.md | M5 | M1 |
| docs/routing_decisions.md | M5 | M3 |
| docs/single_vs_multi_comparison.md | M5 | M2 |
| reports/group_report.md | M5 | M1 |
| reports/individual/*.md | Từng thành viên | Không áp dụng |

## Điều kiện bắt buộc để tránh mất điểm

1. Tất cả code, trace, docs liên quan deadline 18:00 phải commit trước 18:00.
2. Mỗi người phải có bằng chứng đóng góp trùng khớp:
   - File code thực sự đã sửa.
   - Trace field liên quan đến module phụ trách.
   - Báo cáo cá nhân mô tả đúng phần việc đã làm.
3. Không được claim phần việc không thực hiện, tránh 0/40 điểm cá nhân.
4. Không hallucinate trong grading questions, ưu tiên abstain đúng cách khi thiếu evidence.

## Checklist Done trước 18:00

- [ ] graph.py chạy và route được ít nhất 2 nhóm câu hỏi.
- [ ] 3 workers test độc lập được và khớp contracts.
- [ ] policy worker xử lý ít nhất 1 exception case.
- [ ] mcp_server có >= 2 tools và được gọi thực tế.
- [ ] eval_trace.py chạy end-to-end 15 câu hỏi không crash.
- [ ] grading_run.jsonl có đủ các trường bắt buộc.
- [ ] 3 file docs đã điền dữ liệu thật từ trace.
- [ ] Mỗi thành viên có file báo cáo cá nhân riêng.

## Mẫu thay tên nhanh

- M1 = __________________
- M2 = __________________
- M3 = __________________
- M4 = __________________
- M5 = __________________

Sau khi thay tên, đổi lại tên file nếu cần để nộp bài nội bộ.
