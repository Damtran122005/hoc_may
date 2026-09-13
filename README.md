# Local SVM API

Dự án triển khai mô hình **Support Vector Machine (SVM)** để phân loại hoa Iris thông qua **Flask REST API**, đồng thời hỗ trợ chạy bằng **Docker**.

Mô hình sử dụng bộ dữ liệu **Iris Dataset** để phân loại hoa thành 3 lớp:

* `Iris-setosa`
* `Iris-versicolor`
* `Iris-virginica`

---

# 1. Tổng quan dự án

Hệ thống hoạt động theo quy trình:

```text
Dữ liệu đầu vào
      ↓
Flask API
      ↓
Kiểm tra dữ liệu đầu vào
      ↓
Mô hình SVM
      ↓
Dự đoán + Xác suất
      ↓
JSON Response
```

API nhận vào 4 đặc trưng của một bông hoa Iris:

```text
[sepal_length, sepal_width, petal_length, petal_width]
```

Ví dụ:

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

---

# 2. Input

Endpoint `/api/v1/classify` nhận dữ liệu JSON gồm một trường `features`.

## Định dạng Input

```json
{
  "features": [
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
  ]
}
```

Các giá trị trong `features` phải là **số** và phải có đúng **4 giá trị**.

### Ví dụ

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

## Ý nghĩa các đặc trưng

| Đặc trưng      | Ý nghĩa                  |
| -------------- | ------------------------ |
| `sepal_length` | Chiều dài đài hoa (cm)   |
| `sepal_width`  | Chiều rộng đài hoa (cm)  |
| `petal_length` | Chiều dài cánh hoa (cm)  |
| `petal_width`  | Chiều rộng cánh hoa (cm) |

---

# 3. Output

Khi dự đoán thành công, API trả về HTTP Status `200`.

### Ví dụ Response

```json
{
  "success": true,
  "status": 200,
  "message": "Prediction successful",
  "data": {
    "model": "svm",
    "endpoint": "/api/v1/classify",
    "prediction": "Iris-setosa",
    "probability": 0.99,
    "health_status": "healthy"
  }
}
```

## Ý nghĩa các trường Output

| Trường               | Ý nghĩa                                  |
| -------------------- | ---------------------------------------- |
| `success`            | Cho biết request có thành công hay không |
| `status`             | HTTP status code                         |
| `message`            | Thông báo kết quả                        |
| `data.model`         | Mô hình Machine Learning được sử dụng    |
| `data.endpoint`      | Endpoint thực hiện dự đoán               |
| `data.prediction`    | Loài hoa được dự đoán                    |
| `data.probability`   | Xác suất của kết quả dự đoán             |
| `data.health_status` | Trạng thái của model                     |

---

# 4. Algorithm (Must)

Thuật toán bắt buộc của dự án là:

## Support Vector Machine (SVM)

**SVM (Support Vector Machine)** là một thuật toán Machine Learning có giám sát, thường được sử dụng cho các bài toán phân loại.

Trong dự án này, SVM được sử dụng để phân loại dữ liệu hoa Iris thành 3 lớp:

```text
Iris-setosa
Iris-versicolor
Iris-virginica
```

## Quy trình huấn luyện

```text
Iris Dataset
     ↓
Đọc dữ liệu
     ↓
Tách Features và Labels
     ↓
Huấn luyện mô hình SVM
     ↓
Lưu model
     ↓
Flask API
     ↓
Nhận Features
     ↓
SVM dự đoán
     ↓
Trả về kết quả
```

## Các Features sử dụng

Mỗi mẫu dữ liệu Iris gồm 4 đặc trưng:

```text
1. Sepal Length
2. Sepal Width
3. Petal Length
4. Petal Width
```

Ví dụ:

```text
[5.1, 3.5, 1.4, 0.2]
```

Model SVM sử dụng 4 giá trị này để xác định loài hoa.

---

# 5. API Endpoints

## 5.1. Kiểm tra trạng thái Server

### Request

```http
GET /health
```

### URL

```text
http://localhost:3000/health
```

### Ví dụ sử dụng

```bash
curl http://localhost:3000/health
```

### Response

```json
{
  "success": true,
  "status": 200,
  "message": "Model health",
  "data": {
    "model": "svm",
    "health_status": "healthy"
  }
}
```

---

# 5.2. Phân loại hoa Iris

### Request

```http
POST /api/v1/classify
```

### URL

```text
http://localhost:3000/api/v1/classify
```

### Header

```http
Content-Type: application/json
```

### Body

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

### Sử dụng bằng cURL

```bash
curl -X POST http://localhost:3000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d "{\"features\":[5.1,3.5,1.4,0.2]}"
```

---

# 6. Các trường hợp dự đoán

## 6.1. Iris-setosa

### Input

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

### Kết quả mong đợi

```text
Iris-setosa
```

---

## 6.2. Iris-versicolor

### Input

```json
{
  "features": [6.0, 2.9, 4.5, 1.5]
}
```

### Kết quả mong đợi

```text
Iris-versicolor
```

---

## 6.3. Iris-virginica

### Input

```json
{
  "features": [6.3, 3.3, 6.0, 2.5]
}
```

### Kết quả mong đợi

```text
Iris-virginica
```

---

# 7. Xử lý lỗi

API thực hiện kiểm tra dữ liệu trước khi đưa dữ liệu vào model SVM.

## 7.1. Thiếu trường `features`

### Request

```json
{}
```

### Status mong đợi

```text
400 Bad Request
```

### Response

```json
{
  "success": false,
  "status": 400,
  "message": "Missing required field: features",
  "data": null
}
```

---

## 7.2. `features` là mảng rỗng

### Request

```json
{
  "features": []
}
```

### Status mong đợi

```text
400 Bad Request
```

### Response

```json
{
  "success": false,
  "status": 400,
  "message": "The features field must be a non-empty array",
  "data": null
}
```

---

## 7.3. `features` sai kiểu dữ liệu

### Request

```json
{
  "features": "5.1,3.5,1.4,0.2"
}
```

### Status mong đợi

```text
400 Bad Request
```

Server phải từ chối request vì `features` phải là một mảng.

---

## 7.4. Không đủ số lượng Features

Model Iris yêu cầu chính xác 4 features.

### Request không hợp lệ

```json
{
  "features": [5.1, 3.5]
}
```

### Status mong đợi

```text
400 Bad Request
```

---

## 7.5. Features không phải số

### Request không hợp lệ

```json
{
  "features": ["small", "medium", "large", "small"]
}
```

### Status mong đợi

```text
400 Bad Request
```

Server phải từ chối vì các features phải có kiểu số.

---

## 7.6. JSON không hợp lệ

### Request

```text
{ "features": [5.1, 3.5, 1.4
```

### Status mong đợi

```text
400 Bad Request
```

---

## 7.7. Model không khả dụng

Nếu model SVM không tồn tại hoặc không thể load, API trả về:

```text
503 Service Unavailable
```

### Response

```json
{
  "success": false,
  "status": 503,
  "message": "SVM model is not available",
  "data": {
    "model": "svm",
    "health_status": "unhealthy"
  }
}
```

---

# 8. Kiểm thử bằng Postman

Có thể tạo các request sau trong Postman để kiểm thử API.

## Test Case 1 — Health Check

### Request

```http
GET http://localhost:3000/health
```

### Kết quả mong đợi

```text
Status: 200
```

### Postman Test

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Model is SVM", function () {
    const json = pm.response.json();
    pm.expect(json.data.model).to.eql("svm");
});
```

---

## Test Case 2 — Iris-setosa

### Request

```http
POST http://localhost:3000/api/v1/classify
```

### Body

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

### Kết quả mong đợi

```text
Status: 200
Prediction: Iris-setosa
```

### Postman Test

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Prediction is Iris-setosa", function () {
    const json = pm.response.json();
    pm.expect(json.data.prediction).to.eql("Iris-setosa");
});
```

---

## Test Case 3 — Iris-versicolor

### Body

```json
{
  "features": [6.0, 2.9, 4.5, 1.5]
}
```

### Kết quả mong đợi

```text
Status: 200
Prediction: Iris-versicolor
```

---

## Test Case 4 — Iris-virginica

### Body

```json
{
  "features": [6.3, 3.3, 6.0, 2.5]
}
```

### Kết quả mong đợi

```text
Status: 200
Prediction: Iris-virginica
```

---

## Test Case 5 — Thiếu `features`

### Body

```json
{}
```

### Kết quả mong đợi

```text
Status: 400
```

---

## Test Case 6 — `features` rỗng

### Body

```json
{
  "features": []
}
```

### Kết quả mong đợi

```text
Status: 400
```

---

## Test Case 7 — Sai kiểu `features`

### Body

```json
{
  "features": "5.1,3.5,1.4,0.2"
}
```

### Kết quả mong đợi

```text
Status: 400
```

---

## Test Case 8 — Sai số lượng Features

### Body

```json
{
  "features": [5.1, 3.5, 1.4]
}
```

### Kết quả mong đợi

```text
Status: 400
```

---

# 9. Chạy Server bằng Python

Cài đặt các thư viện cần thiết:

```bash
python -m pip install -r requirements.txt
```

Huấn luyện model SVM:

```bash
python train.py
```

Sau khi train thành công, chạy Flask server:

```bash
python app.py
```

Server sẽ chạy tại:

```text
http://localhost:3000
```

---

# 10. Chạy bằng Docker

Build và chạy project:

```bash
docker compose up --build
```

Sau khi container khởi động, API có thể được truy cập tại:

```text
http://localhost:3000
```

Dừng container:

```bash
docker compose down
```

---

# 11. Kiểm tra Server

Sau khi server được khởi động:

```bash
curl http://localhost:3000/health
```

Nếu server và model hoạt động bình thường, kết quả phải có:

```json
{
  "success": true,
  "status": 200,
  "message": "Model health",
  "data": {
    "model": "svm",
    "health_status": "healthy"
  }
}
```

---

# 12. Cấu trúc Project

```text
local-svm-api/
│
├── app.py
├── train.py
├── model.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
└── model_params.json
```

## Chức năng của từng file

| File                 | Chức năng                           |
| -------------------- | ----------------------------------- |
| `app.py`             | Flask REST API server               |
| `train.py`           | Huấn luyện model SVM                |
| `model.py`           | Cài đặt/xử lý model SVM             |
| `requirements.txt`   | Danh sách thư viện Python           |
| `Dockerfile`         | Cấu hình Docker image               |
| `docker-compose.yml` | Cấu hình Docker Compose             |
| `model_params.json`  | Thông tin/model parameters được lưu |
| `README.md`          | Tài liệu hướng dẫn project          |

---

# 13. Yêu cầu hệ thống

Project yêu cầu:

* Python 3.x
* Flask
* NumPy
* scikit-learn
* Docker
* Docker Compose
* Postman (tùy chọn)

Cài đặt dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# 14. Tổng kết

Project xây dựng một **Local AI Server** sử dụng thuật toán **Support Vector Machine (SVM)** để phân loại hoa Iris.

Hệ thống thực hiện các chức năng:

1. Đọc và xử lý dữ liệu Iris.
2. Huấn luyện model SVM.
3. Lưu model sau khi huấn luyện.
4. Khởi động Flask REST API.
5. Nhận 4 đặc trưng số của hoa Iris.
6. Sử dụng SVM để dự đoán loài hoa.
7. Trả về kết quả dự đoán và xác suất.
8. Cung cấp API `/health` để kiểm tra trạng thái model.
9. Hỗ trợ chạy local bằng Python.
10. Hỗ trợ chạy bằng Docker.
11. Hỗ trợ kiểm thử API bằng Postman.

## Thuật toán bắt buộc

```text
Support Vector Machine (SVM)
```

## API chính

```http
POST http://localhost:3000/api/v1/classify
```

## Health Check

```http
GET http://localhost:3000/health
```
