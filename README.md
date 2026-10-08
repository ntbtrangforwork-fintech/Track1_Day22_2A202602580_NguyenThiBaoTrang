# Day 22 Monetization and GTM

- **Họ và tên:** Nguyễn Thị Bảo Trang
- **MSSV:** 2A202602580
- **Lớp:** Track 1
- **Ngành:** Y tế
- **Sản phẩm giả định:** MediNote VN, trợ lý AI tạo bản nháp ghi chú khám bệnh cho phòng khám tư ngoại trú tại Việt Nam

> Mọi số vận hành chưa qua pilot được ghi là giả định. Giá nhà cung cấp và đối thủ được kiểm tra ngày 08/10/2026. Sản phẩm không chẩn đoán và không tự ghi vào hồ sơ bệnh án; bác sĩ luôn duyệt đầu ra.

## One Pager

### 1. Pricing

**Định vị đã chọn.** MediNote VN hoàn thành bản nháp ghi chú SOAP sau mỗi phiên khám để bác sĩ chỉ cần rà soát và duyệt, thay vì tự chép lại toàn bộ hội thoại. Người duyệt mua là chủ phòng khám hoặc giám đốc chuyên môn; tiền đến từ ngân sách vận hành/nhân sự vì sản phẩm cạnh tranh với thời gian hành chính của bác sĩ và trợ lý.

**Định nghĩa một Job.** Một phiên khám tối đa 20 phút tạo ra bản nháp SOAP và được bác sĩ duyệt/lưu trong 24 giờ. Phiên bị hủy, âm thanh không đủ chất lượng, lỗi kỹ thuật, hoặc bản nháp chưa được duyệt không được tính là Job hoàn tất.

**Value Metric.** Hybrid theo outcome: phí tối thiểu **1.990.000 VND/clinician/tháng** bao gồm 200 Job đầu; từ Job 201 tính **10.000 VND/Job**. Đây là mức chi tiêu tối thiểu có bao gồm sản lượng, không phải phí nền cộng tiền lại từ Job đầu tiên.

- Attribution **8/10**: hệ thống ghi được chuỗi `generated -> edited -> approved -> saved` và diff của bác sĩ.
- Autonomy **5/10**: AI tự tạo bản nháp, nhưng bác sĩ bắt buộc duyệt trước khi lưu EHR.
- Market override: không dùng outcome thuần vì phòng khám SME cần hóa đơn dự đoán được; gói tối thiểu tạo sự ổn định, overage giúp doanh thu tăng theo giá trị.

**Benchmark cùng Job.** [Freed](https://www.getfreed.ai/pricing) niêm yết Starter $39/tháng cho tối đa 40 note, Core $79/tháng cho note không giới hạn. [PatientNotes](https://patientnotes.ai/pricing) niêm yết $50/user/tháng khi trả năm hoặc $70 khi trả tháng, không giới hạn visit. Hai sản phẩm chủ yếu neo giá theo seat/gói; MediNote VN thêm outcome overage để giới hạn rủi ro khi sử dụng cao.

| Chỉ số bắt buộc | Kết quả base case |
| --- | ---: |
| Cost/Job | **2.760 VND** |
| Giá sàn 3 x Cost/Job | **8.279 VND/Job** |
| Giá bán đề xuất | **1.990.000 VND/tháng gồm 200 Job; 10.000 VND/Job vượt gói** |
| Giá hiệu dụng tại 360 Job | **9.972 VND/Job** |
| Gross Margin | **72,3%** |
| Breakeven completion để GM đạt 60% | **63,8%** |
| Completion hiện tại | **92% mục tiêu pilot, chưa được xác minh** |

**Neo giá trần.** 360 Job tiết kiệm khoảng 48 giờ/tháng. Với giá trị giờ bác sĩ giả định 400.000 VND, giá trị tạo ra là 19,2 triệu VND/tháng; dải 10-25% là 1,92-4,8 triệu. So với lương admin y tế giả định 8 triệu/tháng, dải 50-70% là 4,0-5,6 triệu. Doanh thu điển hình 3,59 triệu/tháng nằm dưới hai mốc trần, nhưng các giả định lương và thời gian tiết kiệm phải được xác nhận bằng phỏng vấn.

**Chi phí.** Base case dùng 1.000 lượt thử/tháng, completion 92%, audio 12 phút/lượt, OpenAI gpt-transcribe $0,0045/phút và GPT-5.4 mini $0,75 input / $0,075 cached input / $4,50 output cho mỗi 1M token. Cost/Attempt là $0,09765; chia trên 920 Job hoàn tất thành $0,10614/Job. Retry 8%, infra, observability và QA nội bộ đều đã được tính. Review lâm sàng của bác sĩ không vào COGS vì MediNote VN là phần mềm, không phải managed service.

**Stress test.** Ở completion 50%, GM còn 49,0%; 60% là 57,5%; 70% là 63,5%; 80% là 68,1%; 90% là 71,6%. Biến có thể phá mô hình nhanh nhất là thời lượng audio nhân với giá STT, vì STT chiếm khoảng 55% Cost/Attempt. Batch có thể giảm gần một nửa chi phí LLM nhưng chỉ giảm khoảng 5,3% tổng COGS và không phù hợp mục tiêu trả note trong 60 giây.

### 2. GTM

**Kênh 90 ngày:** founder-led Sales. Sản phẩm y tế cần tạo niềm tin, thu dữ liệu sửa note và hỗ trợ tích hợp EHR; PLG không đủ để học nhanh, còn partner-led chưa có partner đã xác nhận.

| Affordability Test | Kết quả |
| --- | ---: |
| ARPU tại 360 Job | 3.590.000 VND/tháng |
| Ngân sách CAC = ARPU x GM x 12 tháng | 31.158.514 VND/khách |
| CAC bottom-up = 2.250.000/opportunity / 30% win rate | 7.500.000 VND/khách |
| Khoảng đệm ngân sách / CAC | 4,15 lần |
| ACV | 43.080.000 VND |
| Deal/AE/ngày với quota 2,4 tỷ/năm | 0,23 |
| LTV:CAC với lifetime giả định 18 tháng | 6,23 lần |

Benchmark sales có rep quốc tế trong đề cho ra CAC khoảng $25.200-$44.800, vượt xa ngân sách. Vì vậy 90 ngày đầu chỉ dùng founder-led Sales với chi phí bottom-up nội địa; chưa tuyển đội AE trả lương đầy đủ.

**Pain Moment.** 17:30 sau ca khám cuối, bác sĩ vẫn đang chép nội dung hội thoại vào EHR trên trình duyệt để hoàn tất hồ sơ trước khi rời phòng khám.

**Điểm nhúng.** Chrome extension và nút “Tạo ghi chú” ngay trong EHR; không yêu cầu bác sĩ mở một website riêng.

| Giai đoạn | Mục tiêu | Hoạt động và dữ liệu | KPI quyết định | Owner |
| --- | --- | --- | --- | --- |
| 12/10-08/11/2026 | 3 phòng khám, 10 bác sĩ | Pilot tận tay; 300 cặp note AI/note đã sửa; 2 phỏng vấn mỗi bác sĩ | Completion >=80%; 0 hallucination nghiêm trọng; review median <=3 phút | Nguyễn Thị Bảo Trang |
| 09/11/2026-10/01/2027 | 8 khách trả phí, 30 bác sĩ | Chuẩn hóa onboarding, template và tích hợp EHR; lấy referral | 8.000 note; completion >=90%; GM >=65%; CAC <=10 triệu | Nguyễn Thị Bảo Trang |
| Từ 11/01/2027 | Mở thêm một chuyên khoa | Chọn nhi hoặc da liễu theo accuracy và retention tốt nhất | 90-day retention >=80%; major-edit rate <=15% | Nguyễn Thị Bảo Trang |

### 3. Evidence

| Tài sản | Hiện có | Khoảng trống và deadline |
| --- | --- | --- |
| Eval Results | Chưa có | Nguyễn Thị Bảo Trang hoàn thành 08/11/2026 trên 300 consultation đã khử định danh; 0 lỗi lâm sàng nghiêm trọng, field accuracy >=95%, major-edit <=15% |
| Procurement Q&A | Đã có bản nháp 3 câu trọng yếu | Hoàn thành data-flow, DPA, retention, deletion và exit runbook trước 25/10/2026 |
| Pilot Report | Chưa có | Báo cáo 8.000 note, completion, review time, accuracy, GM và CAC trước 10/01/2027 |

Chi tiết nằm trong [Evidence Pack](docs/EVIDENCE_PACK.md). Nếu eval có lỗi nghiêm trọng hoặc completion dưới 64%, không mở rộng bán hàng; giảm phạm vi specialty, sửa workflow, tăng giá hoặc đổi mô hình HITL trước.

## Cách chạy và kiểm tra

```bash
python -m src.monetization_model
python -m src.monetization_model --json
python -m unittest discover -s tests -v
```

Workbook có công thức và toàn bộ nguồn: [Day22_Monetization_GTM_Model.xlsx](artifacts/Day22_Monetization_GTM_Model.xlsx).

## Nguồn công khai

- OpenAI transcription pricing: https://platform.openai.com/pricing
- OpenAI GPT-5.4 mini pricing: https://developers.openai.com/api/docs/models/gpt-5.4-mini
- OpenAI enterprise privacy: https://openai.com/enterprise-privacy/
- Deepgram list and promotional pricing: https://deepgram.com/pricing
- Freed pricing: https://www.getfreed.ai/pricing
- PatientNotes pricing: https://patientnotes.ai/pricing

