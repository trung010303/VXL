#include <Wire.h>
#include <MAX30105.h>
#include "heartRate.h"
#include <SD.h>
#include <SPI.h>

// Khởi tạo MAX30102
MAX30105 particleSensor;

// SD card
const int chipSelect = 5;  // GPIO5 cho CS
File dataFile;

// Biến toàn cục
uint32_t irValue, redValue;
int beatsPerMinute = 0;
int spO2 = 0;
int validSignal = 0;
int sampleCount = 0;
unsigned long startTime = 0;

// Mảng để lưu IR và Red
const int BUFFER_SIZE = 100;
uint32_t irBuffer[BUFFER_SIZE];
uint32_t redBuffer[BUFFER_SIZE];
int bufferIndex = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n========================================");
  Serial.println("     MAX30102 Heart Rate & SpO2 Test");
  Serial.println("========================================\n");

  // Khởi tạo I2C
  Wire.begin(21, 22);  // SDA=GPIO21, SCL=GPIO22
  Serial.println("[1/4] Initializing I2C...");
  
  // Khởi tạo MAX30102
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("ERROR: MAX30102 not found!");
    while (1);
  }
  Serial.println("OK - MAX30102 detected");

  // Cấu hình MAX30102
  particleSensor.setup(255, 4, 2, 100, 411, 4096);  // LED power, averaging, sample avg, pulse width, sample rate, ADC range
  Serial.println("OK - MAX30102 configured\n");

  // Khởi tạo SD card
  Serial.println("[2/4] Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("ERROR: SD card not found!");
    while (1);
  }
  Serial.println("OK - SD card detected\n");

  // Tạo file CSV
  Serial.println("[3/4] Creating CSV file...");
  
  // Xóa file cũ nếu tồn tại
  if (SD.exists("max30102_test_1.csv")) {
    SD.remove("max30102_test_1.csv");
    Serial.println("Removed old file");
  }
  
  // Tạo file mới
  dataFile = SD.open("max30102_test_1.csv", FILE_WRITE);
  if (!dataFile) {
    Serial.println("ERROR: Cannot create CSV file!");
    while (1);
  }
  
  // Ghi header
  dataFile.println("Time_ms,IR_Value,Red_Value,Valid,HR_bpm,SpO2_percent");
  dataFile.flush();
  Serial.println("OK - CSV file created\n");

  // Bắt đầu đếm thời gian
  Serial.println("[4/4] Starting measurement...");
  Serial.println("Place your finger on the sensor and wait!\n");
  startTime = millis();

  delay(2000);
}

void loop() {
  // Đọc dữ liệu từ FIFO
  bufferIndex = 0;
  
  // Lấy mẫu từ FIFO buffer
  while (particleSensor.available() && bufferIndex < BUFFER_SIZE) {
    irBuffer[bufferIndex] = particleSensor.getIR();
    redBuffer[bufferIndex] = particleSensor.getRed();
    particleSensor.nextSample();
    bufferIndex++;
  }

  // Xử lý từng mẫu
  for (int i = 0; i < bufferIndex; i++) {
    irValue = irBuffer[i];
    redValue = redBuffer[i];
    
    // Kiểm tra tín hiệu hợp lệ (IR phải > 50000 LSB)
    if (irValue > 50000) {
      validSignal = 1;
    } else {
      validSignal = 0;
    }

    // Tính BPM từ IR signal
    if (validSignal) {
      // Sử dụng hàm từ heartRate.h (nếu có)
      checkForBeat(irValue);
      long delta = millis() - startTime;
      if (checkForBeat(irValue)) {
        // Phát hiện được nhịp
        long deltas = delta;
        beatsPerMinute = 60000 / deltas;
      }
    } else {
      beatsPerMinute = 0;
    }

    // Tính SpO2 từ công thức
    if (validSignal && redValue > 0) {
      float ratio = (float)redValue / (float)irValue;
      spO2 = (int)(104 - 27 * ratio);
      
      // Giới hạn SpO2 trong khoảng hợp lệ
      if (spO2 < 0) spO2 = 0;
      if (spO2 > 100) spO2 = 100;
    } else {
      spO2 = 0;
    }

    // Lấy thời gian hiện tại
    unsigned long currentTime = millis() - startTime;
    sampleCount++;

    // Ghi vào SD card
    if (dataFile) {
      // Định dạng: Time_ms,IR_Value,Red_Value,Valid,HR_bpm,SpO2_percent
      dataFile.print(currentTime);
      dataFile.print(",");
      dataFile.print(irValue);
      dataFile.print(",");
      dataFile.print(redValue);
      dataFile.print(",");
      dataFile.print(validSignal);
      dataFile.print(",");
      dataFile.print(beatsPerMinute);
      dataFile.print(",");
      dataFile.println(spO2);
      
      // Flush mỗi 10 mẫu
      if (sampleCount % 10 == 0) {
        dataFile.flush();
      }
    }

    // In ra console
    if (sampleCount % 10 == 0) {
      Serial.print("Sample: ");
      Serial.print(sampleCount);
      Serial.print(" | Time: ");
      Serial.print(currentTime);
      Serial.print("ms | IR: ");
      Serial.print(irValue);
      Serial.print(" | Red: ");
      Serial.print(redValue);
      Serial.print(" | BPM: ");
      Serial.print(beatsPerMinute);
      Serial.print(" | SpO2: ");
      Serial.print(spO2);
      Serial.print("% | Valid: ");
      Serial.println(validSignal);
    }

    // Dừng sau 60 mẫu (khoảng 6 giây với 100 Hz)
    if (sampleCount >= 60) {
      Serial.println("\n========================================");
      Serial.println("Measurement complete!");
      Serial.print("Total samples: ");
      Serial.println(sampleCount);
      Serial.println("Data saved to: max30102_test_1.csv");
      Serial.println("========================================\n");
      
      // Đóng file
      if (dataFile) {
        dataFile.close();
      }
      
      // Chờ vĩnh viễn
      while (1) {
        delay(1000);
      }
    }

    delay(10);  // Delay 10ms giữa các mẫu
  }
}

// Hàm phát hiện nhịp (đơn giản)
boolean checkForBeat(long sample) {
  static int lastSample = 0;
  static int beatCount = 0;
  
  if (sample > lastSample + 5000) {  // Phát hiện peak
    beatCount++;
    lastSample = sample;
    return true;
  }
  lastSample = sample;
  return false;
}
