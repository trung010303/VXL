# MAX30102 Raw Reader — Hệ thống đo và phân tích nhịp tim & oxyhóa máu

Hệ thống gồm 3 thành phần hoạt động nối tiếp nhau: MAX30102 thu tín hiệu từ ngón tay, ESP32 xử lý và lưu vào SD card, Python nhận dữ liệu và vẽ đồ thị phân tích.

---

## 📋 Mô tả dự án

### Mục tiêu
- Đo nhịp tim và oxyhóa máu bằng cảm biến MAX30102 trên ESP32
- Lưu dữ liệu thô vào SD card (định dạng CSV)
- Phân tích dữ liệu bằng Python để đánh giá độ chính xác
- So sánh với giá trị tham chiếu tiêu chuẩn (bình thường)

### Kết quả kỳ vọng
- Sai số BPM ≤ ±5 (nhịp/phút)
- Sai số SpO2 ≤ ±2 (%)
- Valid rate ≥ 95%

---

## 🏗️ Tổng quan kiến trúc

```
[MAX30102] --I2C--> [ESP32] --SPI--> [SD Card] --CSV--> [analyze_data.py]
  Thu nhịp tim        Xử lý số      Lưu file        Phân tích       Vẽ đồ thị
```

---

## 📁 Cấu trúc Folder & File

```
max30102 test/
│
├── 📂 Code (Python Scripts)
│   ├── MASTER.py                 → Chạy phân tích chính
│   ├── PLOT_DETAILED.py          → Vẽ 6 biểu đồ chi tiết
│   └── ADVANCED_ANALYSIS.py      → Phân tích nâng cao (Correlation + ANOVA)
│
├── 📂 Data (Dữ liệu đo được)
│   ├── max30102_test_1.csv       → Dữ liệu lần test 1 (60 mẫu)
│   ├── max30102_test_2.csv       → Dữ liệu lần test 2 (60 mẫu)
│   └── reference_data.csv        → Dữ liệu tham chiếu (10 người bình thường)
│
├── 📂 Results (Kết quả phân tích)
│   ├── [Biểu đồ cơ bản]
│   │   ├── 01_HR_Test1.png           (Nhịp tim lần 1)
│   │   ├── 02_HR_Test2.png           (Nhịp tim lần 2)
│   │   ├── 03_SpO2_Test1.png         (Oxyhóa lần 1)
│   │   ├── 04_SpO2_Test2.png         (Oxyhóa lần 2)
│   │   ├── 05_IR_Red_Test1.png       (Tín hiệu LED lần 1)
│   │   ├── 06_IR_Red_Test2.png       (Tín hiệu LED lần 2)
│   │   └── MAX30102_FULL_ANALYSIS.png (Tổng hợp 6 panel)
│   │
│   ├── [Biểu đồ phân tích nâng cao]
│   │   ├── ADVANCED_01_Correlation.png (Scatter plot + Correlation)
│   │   └── ADVANCED_02_ANOVA.png       (Box plot + ANOVA)
│   │
│   └── [Kết quả số liệu]
│       ├── MAX30102_RESULT.txt    (Báo cáo chi tiết)
│       └── evaluation_result.txt  (Đánh giá PASS/FAIL)
│
└── README.md (File hướng dẫn)
```

---

## 🚀 Cách chạy từng script

### Yêu cầu
```bash
# Cài đặt thư viện cần thiết (nếu chưa có)
pip install pandas matplotlib scipy numpy
```

### Bước 1: Chạy MASTER.py (Phân tích chính)
```bash
cd "Desktop\max30102 test"
python MASTER.py
```

**Kết quả:**
- In ra console: BPM, SpO2, sai số, độ chính xác
- Tạo file: `MAX30102_FULL_ANALYSIS.png` (biểu đồ 6 panel)
- Tạo file: `MAX30102_RESULT.txt` (báo cáo chi tiết)

---

### Bước 2: Chạy PLOT_DETAILED.py (Vẽ biểu đồ chi tiết)
```bash
python PLOT_DETAILED.py
```

**Kết quả:**
- Hiển thị 6 biểu đồ từng cái một
- Lưu 6 file PNG (01-06)

---

### Bước 3: Chạy ADVANCED_ANALYSIS.py (Phân tích nâng cao - Tùy chọn)
```bash
python ADVANCED_ANALYSIS.py
```

**Kết quả:**
- Correlation analysis (mối quan hệ IR vs Red, HR vs SpO2)
- ANOVA analysis (so sánh 3 nhóm)
- Lưu 2 file PNG (ADVANCED_01, ADVANCED_02)

---

## 📊 Hiểu biểu đồ kết quả

### Biểu đồ HR (Nhịp tim)
- Trục ngang: Thời gian (giây)
- Trục dọc: BPM (nhịp/phút)
- Đường xanh: Dữ liệu đo được
- Vùng xanh: Khoảng chấp nhận (±5 BPM)
- **Nếu trong vùng → PASS ✅**

### Biểu đồ SpO2 (Oxyhóa máu)
- Trục ngang: Thời gian (giây)
- Trục dọc: SpO2 (%)
- Đường đỏ/cam: Dữ liệu đo được
- Vùng xanh: Khoảng chấp nhận (±2%)
- **Nếu ổn định → PASS ✅**

### Biểu đồ IR & Red (Tín hiệu LED)
- Đường tím: Tín hiệu IR (hồng ngoại)
- Đường nâu: Tín hiệu Red (đỏ)
- **Hai đường tương tự → Tốt ✅**

### Biểu đồ Correlation (Phân tích nâng cao)
- Scatter plot: Mối quan hệ giữa 2 biến
- Correlation > 0.9 = Rất mạnh (gần như tuyến tính)

### Biểu đồ ANOVA (Phân tích nâng cao)
- Box plot: So sánh 3 nhóm (Test1, Test2, Ref)
- P-value < 0.05 = 3 nhóm có khác nhau

---

## 📈 Giải thích kết quả số liệu

### Ví dụ kết quả:
```
NHIP TIM (BPM):
  Test 1: 75.3 BPM vs Tham chieu 72.0 BPM
    → Sai so: ±3.3 BPM (Do chinh xac: 95.4%) → PASS ✓

  Test 2: 70.3 BPM vs Tham chieu 72.0 BPM
    → Sai so: ±1.7 BPM (Do chinh xac: 97.6%) → PASS ✓

OXYBOA MAU (SpO2):
  Test 1: 97.86% vs Tham chieu 98.01%
    → Sai so: ±0.15% (Do chinh xac: 99.8%) → PASS ✓

  Test 2: 96.96% vs Tham chieu 98.01%
    → Sai so: ±1.05% (Do chinh xac: 98.9%) → PASS ✓

DANH GIA:
  Overall: EXCELLENT (Tất cả test PASSED)
```

---

## 🔬 Tiêu chuẩn đánh giá

| Chỉ tiêu | Tiêu chuẩn | Kết quả | Trạng thái |
|----------|-----------|--------|-----------|
| **BPM Sai số** | ≤ ±5 | ±1.7 - ±3.3 | ✅ PASS |
| **SpO2 Sai số** | ≤ ±2 | ±0.15 - ±1.05 | ✅ PASS |
| **Valid Rate** | ≥ 95% | 98.3% | ✅ EXCELLENT |

---

## 🔬 Lý thuyết hoạt động

### Cảm biến MAX30102

**Hoạt động:**
1. Phát xạ 2 LED (IR + Red) chiếu vào ngón tay
2. Photodiode đo ánh sáng phản xạ
3. ADC chuyển thành số (18-bit, 100 Hz)
4. Tính BPM từ biến động IR/Red
5. Tính SpO2 = 104 - 27×(Red/IR)
6. Gửi qua I2C tới ESP32

**Tại sao IR & Red?**
- Máu chứa hemoglobin (Hb)
- O2Hb (có oxy): phản xạ ít Red, hấp thụ nhiều IR
- Hb (thiếu oxy): phản xạ nhiều Red, hấp thụ ít IR
- So sánh Red/IR → % oxy trong máu = SpO2

---

## 🛠️ Lỗi thường gặp

| Lỗi | Cách sửa |
|-----|---------|
| `No such file` | Kiểm tra file CSV tồn tại |
| `ModuleNotFoundError` | `pip install pandas matplotlib scipy numpy` |
| Sai thư mục | `cd "Desktop\max30102 test"` |
| Biểu đồ không hiển thị | `pip install pyqt5` |

---

## ✅ Checklist trước nộp

```
☑ 2 file CSV dữ liệu (test_1, test_2)
☑ MASTER.py, PLOT_DETAILED.py, ADVANCED_ANALYSIS.py
☑ 6 file PNG biểu đồ chi tiết (01-06)
☑ 2 file PNG nâng cao (ADVANCED_01, 02)
☑ MAX30102_RESULT.txt
☑ Tất cả test PASSED
☑ Đánh giá: EXCELLENT
☑ README.md trong folder
```

---

## 👨‍💻 Thông tin dự án

- **Người thực hiện**: Trung (ĐHBK Hà Nội)
- **Ngày**: 27/05/2026
- **Môn**: Circuit Theory (ET2050)
- **Trường**: Hanoi University of Science and Technology

---

**Chúc bạn trình bày tốt! 🎓**
