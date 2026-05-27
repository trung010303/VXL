# MAX30102 Raw Reader — Hệ thống đo và phân tích nhịp tim & oxyhóa máu

Hệ thống gồm 3 thành phần hoạt động nối tiếp nhau: MAX30102 thu tín hiệu từ ngón tay, ESP32 xử lý và lưu vào SD card, Python nhận dữ liệu và vẽ đồ thị phân tích.

---

## Tổng quan kiến trúc

```
[MAX30102] --I2C--> [ESP32] --SPI--> [SD Card] --CSV--> [analyze_data.py]
  Thu nhịp tim        Xử lý số      Lưu file        Phân tích       Vẽ đồ thị
```

---

## File 1 — `MAX30102_Test_SD_Card.ino` (chạy trên ESP32)

### Nhiệm vụ

Thu dữ liệu nhịp tim từ MAX30102 qua giao thức I2C, xử lý để tính BPM và SpO2, rồi ghi toàn bộ vào SD card dưới dạng CSV để Python tiếp nhận.

## File 2 — SD Card (lưu trữ dữ liệu)

### Nhiệm vụ

Lưu trữ dữ liệu thô từ cảm biến (IR, Red, BPM, SpO2) vào file `heart_data.csv` định dạng CSV, cho phép lấy dữ liệu từ ESP32 về máy tính để phân tích.

---

## File 3 — `analyze_data.py` (chạy trên máy tính)

### Nhiệm vụ

Đọc file CSV từ SD card và thực hiện các tác vụ phân tích:
- Tính toán thống kê BPM, SpO2 (mean, std, min, max)
- So sánh với thiết bị tham chiếu để tính sai số
- Vẽ biểu đồ tín hiệu IR, Red, BPM, SpO2 theo thời gian
- Phân tích tỉ lệ Red/IR và phát hiện chuyển động

## Luồng dữ liệu đầy đủ

```
Ánh sáng hồng ngoại từ ngón tay (liên tục)
        │
        ▼
Photodiode bên trong MAX30102 nhạy cảm với ánh sáng
Phát xạ ánh sáng → đo lượng ánh sáng phản xạ lại
        │
        ▼
Tín hiệu analog từ 2 LED (IR + Red)
        │
        ▼
ADC bên trong MAX30102
Lấy mẫu 100 lần/giây → 18-bit/mẫu
        │
        ▼
Xuất qua I2C: SDA (dữ liệu) + SCL (clock)
        │
        ▼
ESP32 đọc qua Wire library
Xử lý tín hiệu → tính nhịp tim (BPM) từ detector beat
Tính SpO2 từ công thức: SpO2 = 104 - 27×(Red/IR)
        │
        ▼
Ghi qua SPI vào SD card 460800 baud dạng CSV
        │
        ▼
Lấy file heart_data.csv từ SD card về máy tính
        │
        ▼
analyze_data.py đọc CSV, tính toán thống kê
So sánh với giá trị tham chiếu → sai số (%)
        │
        ▼
Vẽ biểu đồ: IR/Red theo thời gian, BPM trend, SpO2 trend
Vẽ tỉ lệ Red/IR, phát hiện motion
```
