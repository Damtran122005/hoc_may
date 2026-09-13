### Hướng dẫn tích hợp Máy chủ Cục bộ và Chiến lược Triển khai AI
#### Chủ đề: Thiết lập, Kiểm thử và Triển khai mô hình Naive Bayes (Naive Bayes Model Integration)

#### 1. Mục tiêu
* Vận hành đồng thời API Service Server và máy chủ AI sử dụng mô hình Naive Bayes ổn định trên máy tính cục bộ.
* Làm chủ hoàn toàn mã nguồn, đặc biệt là quy trình huấn luyện, tính xác suất và dự đoán của mô hình Naive Bayes.
* Thực hiện ảo hóa bằng Docker để đồng bộ môi trường chạy mô hình giữa môi trường phát triển cục bộ và Production.
* Đóng gói, kiểm thử Endpoint dự đoán, kiểm tra trạng thái hệ thống và triển khai mô hình Naive Bayes ổn định trên Production.

--------------------------------------------------------------------------------

### 2. Công nghệ bắt buộc
* Docker 
* Naive Bayes Model (Mô hình phân loại Naive Bayes)
* Model Training & Prediction (Huấn luyện và dự đoán)
* API Service Server (Máy chủ dịch vụ tích hợp)
* RESTful Endpoint
* Health Check Monitoring (Kiểm tra trạng thái hệ thống)
* Command Line Testing Tools (Kiểm thử qua dòng lệnh)

--------------------------------------------------------------------------------

### 3. Kiến trúc
Áp dụng kiến trúc đa cấu phần (Multi-component Architecture), trong đó API Server tiếp nhận dữ liệu đầu vào, chuyển dữ liệu cho tầng xử lý Naive Bayes và trả về lớp dự đoán cùng xác suất tương ứng.
```text
Hệ thống tích hợp (Local Integration Suite)

Cục bộ (Local machine) / Container:
 ├── Component 1 (API Endpoint)
 ├── Component 2 (Tiền xử lý dữ liệu)
 ├── Naive Bayes Model (Tính Prior & Likelihood)
 └── Docker Environment (Môi trường ảo hóa)
```
Tách riêng API, tiền xử lý và mô hình để có thể kiểm thử từng thành phần độc lập.

--------------------------------------------------------------------------------

### 4. Luồng hoạt động chi tiết
#### 4.1 Thiết kế cấu phần (Component Design)
* Dựng API Endpoint đầu tiên để nhận dữ liệu cần phân loại và chạy thử nghiệm độc lập.
* Phân tách riêng bước tiền xử lý dữ liệu, tính toán Naive Bayes và trả kết quả dự đoán để dễ kiểm thử.
* Khởi tạo Endpoint và xác định đường dẫn để API giao tiếp với tầng xử lý mô hình.

--------------------------------------------------------------------------------

#### 4.2 Kiểm thử tham số đầu vào (Parameter Testing)
* Hỗ trợ truyền dữ liệu đầu vào dưới dạng JSON, file hoặc chuỗi ký tự tùy theo đặc tả Endpoint.
* Kiểm tra dữ liệu đầu vào sau tiền xử lý trước khi đưa vào mô hình Naive Bayes.
* Kiểm tra mã trạng thái phản hồi của Endpoint, đồng thời đối chiếu lớp dự đoán và xác suất với kết quả mong đợi.
* Thực thi lệnh kiểm thử trực tiếp từ dòng lệnh để xác thực Endpoint và mô hình.

--------------------------------------------------------------------------------

#### 4.3 Tích hợp máy chủ AI cục bộ (Local AI Integration)
* Huấn luyện mô hình Naive Bayes từ tập dữ liệu đã chuẩn hóa và lưu các tham số cần thiết cho bước dự đoán.
* Khi có request, API Server thực hiện tiền xử lý dữ liệu rồi truyền dữ liệu vào mô hình Naive Bayes.
* Mô hình tính xác suất hậu nghiệm cho từng lớp và chọn lớp có xác suất cao nhất làm kết quả dự đoán.
* Vận hành API Server và mô hình Naive Bayes trên môi trường cục bộ để kiểm chứng toàn bộ luồng từ input đến prediction.

--------------------------------------------------------------------------------

#### 4.4 Đóng gói ảo hóa và Triển khai Production (Dockerization & Production)
* Sử dụng Docker để đóng gói API Server, mã nguồn mô hình và các dependency cần thiết.
* Thiết lập Health Check để kiểm tra API và trạng thái mô hình Naive Bayes đã sẵn sàng phục vụ dự đoán.
* Thực hiện đóng gói sản phẩm hoàn chỉnh và triển khai lên Production sau khi kiểm thử thành công.

--------------------------------------------------------------------------------

### 5. API Response mẫu
Phản hồi Endpoint dự đoán Naive Bayes thành công:
```json
{
  "success": true,
  "status": 200,
  "message": "Dự đoán Naive Bayes thành công",
  "data": {
    "model": "naive_bayes",
    "endpoint": "/api/v1/classify",
    "prediction": "spam",
    "probability": 0.94,
    "health_status": "healthy"
  }
}
```

#### API Response Samples for Invalid Requests

**Missing features:**
```json
{
  "success": false,
  "status": 400,
  "message": "Missing required field: features",
  "data": null
}
```

**Invalid features format:**
```json
{
  "success": false,
  "status": 400,
  "message": "The features field must be a non-empty array",
  "data": null
}
```

**Empty input:**
```json
{
  "success": false,
  "status": 400,
  "message": "Input data cannot be empty",
  "data": null
}
```

**Model unavailable:**
```json
{
  "success": false,
  "status": 503,
  "message": "Naive Bayes model is not available",
  "data": {
    "model": "naive_bayes",
    "health_status": "unhealthy"
  }
}
```

**Internal server error:**
```json
{
  "success": false,
  "status": 500,
  "message": "Internal server error during prediction",
  "data": null
}
```

--------------------------------------------------------------------------------

### 6. Thao tác Docker cơ bản
Tệp cấu hình chạy thử nghiệm cục bộ nhanh:
```bash
# Khởi chạy API Server và mô hình Naive Bayes bằng Docker
docker compose up --build

# Kiểm thử Endpoint dự đoán
curl -X POST http://localhost:3000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"features":["free","offer","click"]}'
```

--------------------------------------------------------------------------------
