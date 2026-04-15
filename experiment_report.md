# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** 2A202600212

**Name:** Nguyễn Thi Thu Hiền

**Date:** 15/04/2026 

---

## 1. Ket qua thi nghiem

Chạy file `agent_simulation.py` với hai bộ dữ liệu khác nhau để kiểm tra khả năng phản hồi của Agent. Kết quả thu được như sau:

| Scenario | Agent Response | Accuracy (1-10) | Notes |
| :--- | :--- | :---: | :--- |
| **Clean Data** (`processed_data.csv`) | Based on my data, the best choice is Laptop at $1200 | 9 | Agent hoạt động hoàn hảo vì dữ liệu đã được chuẩn hóa (Title Case) và loại bỏ các giá trị âm/lỗi. |
| **Garbage Data** (`garbage_data.csv`) | Based on my data, the best choice is Nuclear Reactor at $999999. | 1 | Dữ liệu rác khiến Agent đưa ra thông tin sai lệch, thiếu thực tế khi xử lý. |

---

## 2. Phan tich & nhan xet

### Tai sao Agent tra loi sai khi dung Garbage Data?

Nguyên nhân chính khiến Agent đưa ra kết quả sai lệch là do hiện tượng **"Garbage In, Garbage Out"** (Đầu vào là rác thì đầu ra cũng là rác). Khi dữ liệu thô không được xử lý qua bước ETL, các vấn đề sau sẽ trực tiếp làm hại Agent:

* **Wrong Data Types (Sai kiểu dữ liệu):** Nếu cột giá tiền chứa chuỗi ký tự thay vì số, các hàm tính toán như tìm giá cao nhất (`idxmax`) hoặc tính chiết khấu sẽ bị lỗi hoặc trả về giá trị không xác định.
* **Outliers (Giá trị ngoại lai):** Những bản ghi có giá trị phi lý (như $999,999 cho một món đồ nhỏ) sẽ đánh lừa Agent, khiến nó đề xuất những lựa chọn kém chất lượng hoặc không thực tế.
* **Duplicate IDs (Trùng lặp ID):** Làm cho dữ liệu bị nhiễu, Agent có thể lấy nhầm các bản ghi cũ hoặc bản ghi lỗi thay vì dữ liệu cập nhật mới nhất.
* **Null Values (Giá trị rỗng):** Khi các trường quan trọng như `category` bị trống, Agent không thể lọc dữ liệu chính xác, dẫn đến việc bỏ sót sản phẩm phù hợp hoặc trả lời sai ngữ cảnh yêu cầu.

Tóm lại, bước **Validate** và **Transform** trong Pipeline ETL đóng vai trò là "màng lọc" bảo vệ Agent khỏi những thông tin sai lệch.

---

## 3. Ket luan

**Quality Data > Quality Prompt?** **Đồng ý hoàn toàn.**

**Giải thích ngắn gọn:** Dù chúng ta có viết một câu lệnh (Prompt) thông minh hay tinh tế đến đâu, nhưng nếu nền tảng kiến thức (Data) mà AI truy cập vào bị sai, thiếu hoặc lỗi thời, thì kết quả đầu ra vẫn sẽ là thông tin sai lệch. Một Prompt đơn giản dựa trên một nguồn dữ liệu sạch, có cấu trúc tốt sẽ luôn mang lại giá trị cao hơn và đáng tin cậy hơn so với một Prompt phức tạp chạy trên một tập dữ liệu "rác". Dữ liệu chính là linh hồn của hệ thống AI.
