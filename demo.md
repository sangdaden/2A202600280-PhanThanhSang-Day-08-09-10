# Demo Brief — RAG Assistant (CS + IT Helpdesk)

## 1. Mục tiêu demo
- Trình bày hệ RAG trả lời câu hỏi nội bộ dựa trên tài liệu thật.
- Chứng minh câu trả lời có dẫn nguồn và giảm hallucination.
- Thể hiện cách hệ xử lý câu hỏi ngoài phạm vi bằng phản hồi an toàn.

## 2. Bài toán
Hệ thống hỗ trợ hỏi đáp cho CS + IT Helpdesk:
- SLA xử lý sự cố
- Chính sách hoàn tiền
- Quy trình cấp quyền
- IT FAQ
- HR leave policy

## 3. Kiến trúc tổng quan
- Indexing: preprocess, chunk theo section và paragraph, gắn metadata.
- Retrieval: dense hoặc hybrid (dense + BM25), có thể bật rerank.
- Generation: grounded prompting với citation.
- Evaluation: scorecard theo 4 metric.

Pipeline:
Raw docs -> Indexing -> Vector store -> Retrieval -> Prompt grounded -> Answer + Citation

## 4. Thành phần chính
- index.py: build index, chunking, embedding, lưu ChromaDB.
- rag_answer.py: retrieve, rerank, build prompt, gọi LLM, trả answer.
- eval.py: chạy bộ test và chấm scorecard.

## 5. Cấu hình kỹ thuật nổi bật
- Embedding: text-embedding-3-small (hoặc fallback local).
- Vector store: ChromaDB.
- Retrieval baseline: dense, top_k_search 10, top_k_select 3.
- Variant: hybrid + rerank.
- Prompt rule: chỉ trả lời từ context; thiếu dữ liệu thì abstain.
- Follow-up: 2 câu liên quan + 1 câu khác chủ đề nhưng đúng phạm vi nội bộ.

## 5.1 So sánh Dense, Sparse, Hybrid và Hybrid + Rerank

### Mục tiêu phần này trong demo
- Cho thấy mỗi chiến lược retrieval mạnh ở loại câu hỏi khác nhau.
- Giải thích vì sao nhóm chọn variant cuối là Hybrid + Rerank.

### Bảng so sánh nhanh

| Chiến lược | Cách hoạt động ngắn gọn | Điểm mạnh | Điểm yếu | Khi nên dùng |
|---|---|---|---|---|
| Dense | So khớp embedding theo ngữ nghĩa | Tốt cho câu hỏi diễn đạt tự nhiên, paraphrase | Dễ hụt keyword đặc thù, mã lỗi, alias | Baseline nhanh, câu hỏi ngôn ngữ tự nhiên |
| Sparse (BM25) | So khớp từ khóa theo tần suất token | Bắt tốt keyword chính xác: P1, ERR-403, Level 3 | Hụt ý nghĩa khi query diễn đạt khác từ trong tài liệu | Câu hỏi có mã lỗi, tên riêng, thuật ngữ cố định |
| Hybrid | Kết hợp Dense + Sparse bằng RRF | Cân bằng ngữ nghĩa và exact match, tăng recall | Có thể kéo thêm chunk nhiễu | Corpus pha trộn policy + FAQ + mã lỗi |
| Hybrid + Rerank | Hybrid rồi chấm lại top chunks theo độ liên quan | Tăng precision, giảm nhiễu context trước khi generate | Tốn thêm compute/latency | Bản demo chính cần câu trả lời ổn định |

### Ví dụ minh họa để demo trực tiếp

1. Câu hỏi thiên ngữ nghĩa (Dense thường tốt)
- Query: Approval Matrix để cấp quyền là tài liệu nào?
- Kỳ vọng:
  - Dense: thường tìm đúng Access Control SOP dù câu hỏi dùng alias Approval Matrix.
  - Sparse: có thể hụt nếu tài liệu không chứa đúng cụm từ Approval Matrix.
  - Hybrid: ổn định hơn dense khi alias xuất hiện rải rác.

2. Câu hỏi thiên keyword chính xác (Sparse/Hybrid tốt)
- Query: ERR-403-AUTH là lỗi gì và xử lý thế nào?
- Kỳ vọng:
  - Dense: có thể trả về chunk liên quan login/auth nhưng thiếu đúng mã lỗi.
  - Sparse: ưu tiên chunk chứa đúng token ERR-403-AUTH.
  - Hybrid: giữ được chunk đúng mã lỗi và vẫn có ngữ cảnh xử lý.

3. Câu hỏi có nhiều chi tiết định lượng (Hybrid + Rerank tốt)
- Query: SLA P1 phản hồi bao lâu và resolve trong bao lâu?
- Kỳ vọng:
  - Dense/Sparse: đôi lúc trả về đúng một phần nhưng lẫn thêm chunk không cần thiết.
  - Hybrid: tăng khả năng lấy đúng section SLA theo mức ưu tiên.
  - Hybrid + Rerank: thường cho câu trả lời gọn và đủ 2 mốc thời gian (first response, resolution).

4. Câu hỏi ngoài phạm vi (tất cả đều phải an toàn)
- Query: Số lượng người dùng tăng hay giảm?
- Kỳ vọng:
  - Không chiến lược nào được bịa số liệu.
  - Hệ thống trả về không có thông tin trong tài liệu và gợi ý câu hỏi trong phạm vi.

### Script nói nhanh khi demo (30-45 giây)
- Dense là baseline mạnh về ngữ nghĩa.
- Sparse mạnh khi cần bắt đúng từ khóa đặc thù.
- Hybrid kết hợp cả hai để tăng recall.
- Thêm rerank để lọc nhiễu và tăng độ chính xác chunk trước khi generate.
- Vì vậy nhóm chọn Hybrid + Rerank làm cấu hình trình diễn chính.

## 6. Kịch bản demo 8-10 phút

### Bước 1: Khởi động
- Chạy index.
- Chạy UI.
- Mở trình duyệt tại http://127.0.0.1:8008.

### Bước 2: Demo câu hỏi trong phạm vi
- SLA xử lý ticket P1 là bao lâu?
- Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?
- Ai phải phê duyệt để cấp quyền Level 3?

Kỳ vọng:
- Trả lời ngắn gọn.
- Có nguồn trích dẫn.

### Bước 3: Demo câu hỏi ngoài phạm vi
- Số lượng người dùng tăng hay giảm?

Kỳ vọng:
- Hệ thống trả lời không có thông tin trong tài liệu hiện có.
- Gợi ý người dùng hỏi lại trong phạm vi RAG.

### Bước 4: Demo follow-up
- Sau mỗi câu trả lời: hiện 3 gợi ý.
- Cấu trúc: 2 câu bám sát + 1 câu mở rộng chủ đề khác.

### Bước 5: Kết bằng số liệu
- Trình bày scorecard baseline và variant.
- Nêu rõ cải thiện và lý do chọn variant.

## 7. Bộ câu hỏi demo đề xuất
1. SLA ticket P1 phản hồi ban đầu và thời gian xử lý là bao nhiêu?
2. Chính sách refund có ngoại lệ nào không được hoàn tiền?
3. Điều kiện cấp quyền Level 3 là gì?
4. ERR-403-AUTH là lỗi gì và xử lý thế nào?
5. Nhân viên được remote tối đa bao nhiêu ngày mỗi tuần?
6. Câu hỏi ngoài phạm vi: số lượng người dùng tăng hay giảm?

## 8. FAQ khi giảng viên hỏi

1. Vì sao hệ này đáng tin hơn chatbot thường?
- Vì chỉ trả lời từ evidence retrieve được và có citation.

2. Chunking strategy đang dùng là gì?
- Section-first, sau đó paragraph-first, có overlap để giữ ngữ cảnh.

3. Score retrieval tính sao?
- Dense: similarity từ khoảng cách cosine.
- Hybrid: RRF kết hợp rank dense và sparse.

4. Đánh giá chất lượng bằng gì?
- Faithfulness, Relevance, Context Recall, Completeness.

5. Khi nào hệ abstain?
- Khi không có thông tin liên quan đủ mạnh trong corpus.

6. Điểm khác biệt của variant so với baseline?
- Variant dùng hybrid/rerank để tăng recall và giảm nhiễu context.

## 9. Rủi ro và hướng cải tiến
- Rủi ro: query mơ hồ, alias khác từ tài liệu, retrieval kéo nhầm chunk.
- Cải tiến:
  - Query expansion theo từ điển thuật ngữ nội bộ.
  - Out-of-scope detection trước bước generation.
  - Tối ưu ngưỡng chọn chunk và chiến lược rerank.

## 10. Kết luận ngắn cho slide cuối
Hệ RAG đã đạt mục tiêu vận hành cơ bản: trả lời grounded, có citation, có đánh giá định lượng, và có cơ chế an toàn khi câu hỏi vượt phạm vi tài liệu.
