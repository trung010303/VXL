# MAX30102 Raw Reader — Hệ thống đo và phân tích nhịp tim & oxyhóa máu

Hệ thống gồm 3 thành phần hoạt động nối tiếp nhau: MAX30102 thu tín hiệu từ ngón tay, ESP32 xử lý và lưu vào SD card, Python nhận dữ liệu và vẽ đồ thị phân tích.

---

## Tổng quan kiến trúc

MAX30102 thu dữ liệu nhịp tim qua I2C, ESP32 xử lý số liệu và lưu vào SD card dưới dạng CSV, sau đó Python đọc file CSV để thực hiện phân tích thống kê, so sánh với dữ liệu tham chiếu và vẽ biểu đồ minh họa.

---

## File 1 — `MAX30102_Test_SD_Card.ino` (chạy trên ESP32)

### Nhiệm vụ

Thu dữ liệu nhịp tim từ MAX30102 qua giao thức I2C, xử lý để tính BPM và SpO2, rồi ghi toàn bộ vào SD card dưới dạng CSV để Python tiếp nhận.

---

## File 2 — SD Card (lưu trữ dữ liệu)

### Nhiệm vụ

Lưu trữ dữ liệu thô từ cảm biến (IR, Red, BPM, SpO2) vào file CSV định dạng chuẩn, cho phép lấy dữ liệu từ ESP32 về máy tính để phân tích.

Định dạng CSV:
```
Time_ms, IR_Value, Red_Value, Valid, HR_bpm, SpO2_percent
```

---

## File 3 — Python Scripts (chạy trên máy tính)

### MASTER.py — Phân tích chính

Đọc file CSV từ SD card và thực hiện các tác vụ phân tích:
- Tính toán thống kê BPM, SpO2 (mean, std, min, max)
- So sánh với thiết bị tham chiếu để tính sai số
- Vẽ biểu đồ tín hiệu IR, Red, BPM, SpO2 theo thời gian
- Phân tích tỉ lệ Red/IR và đánh giá chất lượng dữ liệu

Cách chạy:
```
python MASTER.py
```

Kết quả: Biểu đồ tổng hợp (MAX30102_FULL_ANALYSIS.png) và báo cáo chi tiết (MAX30102_RESULT.txt)

### PLOT_DETAILED.py — Vẽ biểu đồ chi tiết

Vẽ 6 biểu đồ riêng biệt, từng cái một, để dễ quan sát:
- 2 biểu đồ nhịp tim (Test 1, Test 2)
- 2 biểu đồ oxyhóa máu (Test 1, Test 2)
- 2 biểu đồ tín hiệu LED (IR & Red, Test 1, Test 2)

Cách chạy:
```
python PLOT_DETAILED.py
```

Kết quả: 6 file PNG (01_HR_Test1.png đến 06_IR_Red_Test2.png)

### ADVANCED_ANALYSIS.py — Phân tích nâng cao (tùy chọn)

Thực hiện phân tích nâng cao:
- Correlation: Xem mối quan hệ giữa IR vs Red, HR vs SpO2, Thời gian vs HR
- ANOVA: So sánh sự khác nhau giữa 3 nhóm (Test 1, Test 2, Tham chiếu)

Cách chạy:
```
python ADVANCED_ANALYSIS.py
```

Kết quả: 2 file PNG (ADVANCED_01_Correlation.png, ADVANCED_02_ANOVA.png)

---

## Cấu trúc folder

```
max30102 test/
├── MASTER.py
├── PLOT_DETAILED.py
├── ADVANCED_ANALYSIS.py
├── max30102_test_1.csv
├── max30102_test_2.csv
├── reference_data.csv
├── 01_HR_Test1.png
├── 02_HR_Test2.png
├── 03_SpO2_Test1.png
├── 04_SpO2_Test2.png
├── 05_IR_Red_Test1.png
├── 06_IR_Red_Test2.png
├── ADVANCED_01_Correlation.png
├── ADVANCED_02_ANOVA.png
├── MAX30102_FULL_ANALYSIS.png
├── MAX30102_RESULT.txt
└── README.md
```

---

## Cách chạy

### Bước 1: Chuẩn bị
```
cd "Desktop\max30102 test"
pip install pandas matplotlib scipy numpy
```

### Bước 2: Chạy phân tích chính
```
python MASTER.py
```

Kết quả sẽ hiển thị trên console: BPM, SpO2, sai số, độ chính xác, và tạo 2 file (biểu đồ + báo cáo).

### Bước 3: Vẽ biểu đồ chi tiết (nếu muốn)
```
python PLOT_DETAILED.py
```

Sẽ hiển thị 6 biểu đồ từng cái một. Đóng mỗi cái để xem cái tiếp theo.

### Bước 4: Phân tích nâng cao (nếu muốn)
```
python ADVANCED_ANALYSIS.py
```

Tính Correlation và ANOVA, lưu 2 file PNG nâng cao.

---

## Kết quả phân tích

### Nhịp tim (BPM)

Mỗi biểu đồ HR hiển thị:
- Dữ liệu BPM được đo qua thời gian (đường màu)
- Trung bình BPM của test (gạch ngang)
- Giá trị tham chiếu bình thường (gạch ngang đỏ)
- Khoảng chấp nhận ±5 BPM

Tiêu chuẩn: Sai số ≤ ±5 BPM → PASS

### Oxyhóa máu (SpO2)

Mỗi biểu đồ SpO2 hiển thị:
- Dữ liệu SpO2 được đo qua thời gian
- Trung bình SpO2 của test
- Giá trị tham chiếu bình thường
- Khoảng chấp nhận ±2%

Tiêu chuẩn: Sai số ≤ ±2% → PASS

### Tín hiệu LED (IR & Red)

Mỗi biểu đồ IR & Red hiển thị:
- Tín hiệu IR (hồng ngoại) theo thời gian
- Tín hiệu Red (đỏ) theo thời gian
- Tỉ lệ Red/IR nên nằm trong khoảng 0.4-0.6

Tiêu chuẩn: Hai tín hiệu có xu hướng tương tự, tỉ lệ trong khoảng

### Correlation (phân tích nâng cao)

Hiển thị scatter plot giữa các cặp biến:
- IR vs Red: Xem mối quan hệ giữa 2 tín hiệu
- HR vs SpO2: Xem mối quan hệ giữa nhịp tim và oxyhóa
- Thời gian vs HR: Xem HR có thay đổi theo thời gian không

Correlation > 0.9 = Rất mạnh (gần như tuyến tính)

### ANOVA (phân tích nâng cao)

So sánh phân bố dữ liệu của 3 nhóm (Test 1, Test 2, Tham chiếu):
- Box plot: Thể hiện phân vị, trung bình, min, max
- P-value < 0.05: 3 nhóm có khác nhau có ý nghĩa thống kê
- P-value ≥ 0.05: 3 nhóm không khác nhau

---

## Giải thích kết quả

### Ví dụ kết quả từ MASTER.py:

Test 1: BPM = 75.3 ± 0.58 (trung bình ± độ lệch chuẩn)
Tham chiếu: BPM = 72.0
Sai số: ±3.3 BPM
Độ chính xác: 95.4%
Kết luận: PASS (sai số < 5 BPM)

Test 2: SpO2 = 97.86%
Tham chiếu: SpO2 = 98.01%
Sai số: ±0.15%
Độ chính xác: 99.8%
Kết luận: PASS (sai số < 2%)

---

## Tiêu chuẩn đánh giá

Chỉ tiêu | Tiêu chuẩn | Kết quả | Trạng thái
---|---|---|---
BPM Sai số | ≤ ±5 | ±1.7 - ±3.3 | PASS
SpO2 Sai số | ≤ ±2 | ±0.15 - ±1.05 | PASS
Valid Rate | ≥ 95% | 98.3% | EXCELLENT
Correlation IR-Red | > 0.9 | 0.9995 | RẤT MẠNH

---

## Lý thuyết hoạt động

### Cảm biến MAX30102

MAX30102 là cảm biến SpO2 và heart rate sử dụng 2 LED (hồng ngoại IR và đỏ Red) để đo độ oxyhóa máu. Nguyên lý hoạt động:

1. Phát xạ ánh sáng: 2 LED phát ánh sáng vào ngón tay
2. Phản xạ ánh sáng: Máu phản xạ ánh sáng tùy theo nồng độ oxy
3. Nhạy cảm: Photodiode trong MAX30102 nhạy cảm với ánh sáng phản xạ
4. Chuyển đổi: ADC 18-bit chuyển tín hiệu analog thành số, lấy mẫu 100 Hz
5. Tính toán: Phát hiện nhịp từ biến động IR/Red, tính SpO2 từ công thức

Công thức tính SpO2:
```
SpO2 = 104 - 27 × (Red/IR)
```

### Tại sao IR và Red lại quan trọng?

Hemoglobin (Hb) trong máu có 2 dạng:
- O2Hb (oxyhemoglobin): Hb có oxy, phản xạ ít ánh sáng Red, hấp thụ nhiều IR
- Hb (deoxyhemoglobin): Hb thiếu oxy, phản xạ nhiều Red, hấp thụ ít IR

Bằng cách so sánh cường độ tín hiệu Red và IR, ta có thể tính được % oxy trong máu (SpO2).

### Luồng dữ liệu

Ánh sáng từ ngón tay → Photodiode → Tín hiệu analog → ADC → Xuất I2C → ESP32 xử lý → Lưu SD card (CSV) → Python đọc và phân tích → Vẽ biểu đồ

---

## Lỗi thường gặp

Lỗi | Nguyên nhân | Cách sửa
---|---|---
No such file or directory | Thiếu file CSV | Kiểm tra max30102_test_1.csv, max30102_test_2.csv tồn tại
ModuleNotFoundError | Thiếu thư viện | pip install pandas matplotlib scipy numpy
FileNotFoundError | Chạy từ sai thư mục | cd "Desktop\max30102 test"
Biểu đồ không hiển thị | Vấn đề backend matplotlib | pip install pyqt5

---

## Checklist trước nộp

- Có 2 file CSV dữ liệu (test_1.csv, test_2.csv)
- Có file reference_data.csv
- Chạy MASTER.py thành công
- Chạy PLOT_DETAILED.py thành công
- Có 6 file PNG biểu đồ chi tiết (01-06)
- Có file MAX30102_RESULT.txt
- Code (MASTER.py, PLOT_DETAILED.py, ...) được giữ lại
- Folder sạch sẽ, dễ hiểu
- Tất cả test PASSED
- Đánh giá: EXCELLENT

---

## Tham khảo

- MAX30102 Datasheet: Công thức tính SpO2, thông số kỹ thuật
- ESP32 I2C Guide: Giao tiếp với cảm biến qua I2C
- Python Data Analysis: pandas, matplotlib, scipy
- Tiêu chuẩn y tế: FDA, ISO 80601 (pulse oximeter accuracy)



