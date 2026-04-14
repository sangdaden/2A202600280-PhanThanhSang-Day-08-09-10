# Báo Cáo Nhóm — Lab Day 09: Multi-Agent Orchestration

**Tên nhóm:** ___________  
**Thành viên:**
| Tên | Vai trò | Email |
|-----|---------|-------|
| ___ | Supervisor Owner | ___ |
| ___ | Worker Owner | ___ |
| ___ | MCP Owner | ___ |
| ___ | Trace & Docs Owner | ___ |

**Ngày nộp:** ___________  
**Repo:** ___________  
**Độ dài khuyến nghị:** 600–1000 từ

---

> **Hướng dẫn nộp group report:**
> 
> - File này nộp tại: `reports/group_report.md`
> - Deadline: Được phép commit **sau 18:00** (xem SCORING.md)
> - Tập trung vào **quyết định kỹ thuật cấp nhóm** — không trùng lặp với individual reports
> - Phải có **bằng chứng từ code/trace** — không mô tả chung chung
> - Mỗi mục phải có ít nhất 1 ví dụ cụ thể từ code hoặc trace thực tế của nhóm

---

## 1. Kiến trúc nhóm đã xây dựng (Sprint 2)

**Hệ thống tổng quan:**
Nhóm đã xây dựng hệ Supervisor-Worker gồm 3 worker chính: retrieval_worker, policy_tool_worker, synthesis_worker. Supervisor chịu trách nhiệm phân tích task và route đến worker phù hợp. Các worker thực hiện domain skill riêng biệt, giao tiếp qua AgentState và tuân thủ contract định nghĩa trong `contracts/worker_contracts.yaml`.

**Routing logic cốt lõi:**
Supervisor sử dụng keyword-based routing để quyết định chuyển task đến retrieval_worker hoặc policy_tool_worker. Điều này giúp giảm độ trễ và tăng tính minh bạch khi debug trace.

**MCP tools đã tích hợp:**
- `search_kb`: Được gọi bởi policy_tool_worker khi cần kiểm tra policy hoặc tìm thông tin bổ sung.
- `get_ticket_info`: Được sử dụng khi cần truy xuất thông tin ticket đặc biệt.

Ví dụ trace: Khi supervisor nhận task liên quan đến "hoàn tiền", sẽ route sang policy_tool_worker, worker này có thể gọi MCP tool `search_kb` để kiểm tra policy hoàn tiền.

---

## 2. Quyết định kỹ thuật quan trọng nhất (Sprint 2)

**Quyết định:**
Nhóm chọn tách rõ 3 worker với contract input/output cụ thể thay vì gộp logic vào một pipeline lớn.

**Bối cảnh vấn đề:**
Khi pipeline cũ (Day 08) bị quá tải, khó trace lỗi và không thể mở rộng từng phần riêng biệt. Việc tách worker giúp dễ kiểm thử, dễ debug và mỗi thành viên có thể phụ trách một module độc lập.

**Các phương án cân nhắc:**
- Gộp logic vào 1 file lớn (dễ triển khai nhanh nhưng khó bảo trì)
- Tách thành các worker độc lập (phức tạp hơn nhưng rõ ràng, dễ mở rộng)

**Lý do chọn:**
- Dễ trace, dễ kiểm thử từng worker
- Đảm bảo tuân thủ contract, dễ thay thế hoặc nâng cấp từng worker

**Bằng chứng:**
- File: `workers/retrieval.py`, `workers/policy_tool.py`, `workers/synthesis.py` đều có docstring mô tả contract rõ ràng
- File: `contracts/worker_contracts.yaml` định nghĩa input/output cho từng worker
- Khi chạy pipeline, trace log cho thấy từng worker nhận và trả kết quả đúng contract

---

## 3. Kết quả grading questions (150–200 từ)

> Sau khi chạy pipeline với grading_questions.json (public lúc 17:00):
> - Nhóm đạt bao nhiêu điểm raw?
> - Câu nào pipeline xử lý tốt nhất?
> - Câu nào pipeline fail hoặc gặp khó khăn?

**Tổng điểm raw ước tính:** ___ / 96

**Câu pipeline xử lý tốt nhất:**
- ID: ___ — Lý do tốt: ___________________

**Câu pipeline fail hoặc partial:**
- ID: ___ — Fail ở đâu: ___________________  
  Root cause: ___________________

**Câu gq07 (abstain):** Nhóm xử lý thế nào?

_________________

**Câu gq09 (multi-hop khó nhất):** Trace ghi được 2 workers không? Kết quả thế nào?

_________________

---

## 4. So sánh Day 08 vs Day 09 — Điều nhóm quan sát được (150–200 từ)

> Dựa vào `docs/single_vs_multi_comparison.md` — trích kết quả thực tế.

**Metric thay đổi rõ nhất (có số liệu):**

_________________

**Điều nhóm bất ngờ nhất khi chuyển từ single sang multi-agent:**

_________________

**Trường hợp multi-agent KHÔNG giúp ích hoặc làm chậm hệ thống:**

_________________

---

## 5. Phân công và đánh giá nhóm (100–150 từ)

> Đánh giá trung thực về quá trình làm việc nhóm.

**Phân công thực tế:**

| Thành viên | Phần đã làm | Sprint |
|------------|-------------|--------|
| ___ | ___________________ | ___ |
| ___ | ___________________ | ___ |
| ___ | ___________________ | ___ |
| ___ | ___________________ | ___ |

**Điều nhóm làm tốt:**

_________________

**Điều nhóm làm chưa tốt hoặc gặp vấn đề về phối hợp:**

_________________

**Nếu làm lại, nhóm sẽ thay đổi gì trong cách tổ chức?**

_________________

---

## 6. Nếu có thêm 1 ngày, nhóm sẽ làm gì? (50–100 từ)

> 1–2 cải tiến cụ thể với lý do có bằng chứng từ trace/scorecard.

_________________

---

*File này lưu tại: `reports/group_report.md`*  
*Commit sau 18:00 được phép theo SCORING.md*
