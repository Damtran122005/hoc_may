# Local Naive Bayes API

This project implements a simple Naive Bayes classifier with a Flask API and Docker support.

Quick start (local python):

```bash
python -m pip install -r requirements.txt
python train.py
python app.py
```

Quick start (Docker):

```bash
docker compose up --build
```

Health check:

```bash
curl http://localhost:3000/health
```

Predict example:

```bash
curl -X POST http://localhost:3000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"features":["free","offer","click"]}'
```

Postman test cases
------------------

Below are focused test cases you can add to Postman. For each case create a request, set `Content-Type: application/json` where noted, paste the JSON body (raw), then assert the response status and JSON fields.

1) Health — service available

  - Request: `GET http://localhost:3000/health`
  - Expected status: `200`
  - Example response:

```json
{
  "success": true,
  "status": 200,
  "message": "Model health",
  "data": { "model": "naive_bayes", "health_status": "healthy" }
}
```

2) Predict — valid (likely `spam`)

  - Request: `POST http://localhost:3000/api/v1/classify`
  - Headers: `Content-Type: application/json`
  - Body:

```json
{ "features": ["free", "money", "offer"] }
```

  - Expected status: `200`
  - Key assertions: `success==true`, `data.prediction` exists, `data.probability` is a number

3) Predict — valid (likely `ham`)

  - Body:

```json
{ "features": ["project", "deadline", "update"] }
```

  - Expected status: `200`
  - Key assertions: `success==true`, `data.prediction` (should differ from spam case)

4) Predict — missing `features` field

  - Body:

```json
{}
```

  - Expected status: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "Missing required field: features",
  "data": null
}
```

5) Predict — empty `features` array

  - Body:

```json
{ "features": [] }
```

  - Expected status: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "The features field must be a non-empty array",
  "data": null
}
```

6) Predict — wrong type for `features` (string)

  - Body:

```json
{ "features": "free money" }
```

  - Expected status: `400`
  - Reason: server validates `features` must be an array

7) Predict — missing or wrong `Content-Type` (plain text / no body)

  - Send no body or omit header
  - Expected status: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "Input data cannot be empty",
  "data": null
}
```

8) Predict — malformed JSON

  - Body (invalid JSON):

```
{ "features": ["free", "offer"  
```

  - Expected status: `400`

9) Predict — model unavailable (server started without model file)

  - Expected status: `503`
  - Example response:

```json
{
  "success": false,
  "status": 503,
  "message": "Naive Bayes model is not available",
  "data": { "model": "naive_bayes", "health_status": "unhealthy" }
}
```

10) Predict — internal server error (unexpected exception)

  - This is harder to trigger intentionally; expected status: `500` with message `Internal server error during prediction`.

Quick Postman tips

- For each request add test scripts in Postman to assert `pm.response.code === 200` (or expected code) and to validate JSON fields, e.g. `pm.test("has prediction", () => pm.response.json().data.prediction);`.
- Optionally export a Postman Collection JSON from your workspace and keep it under a `postman/` folder for CI or sharing.

Run server locally before testing:

```bash
python -m pip install -r requirements.txt
python train.py
python app.py
```

# Phân loại hoa (Iris) — Các trường hợp kiểm thử

---

Các bài kiểm thử này giả định rằng endpoint nhận vào một vector đặc trưng dạng số để phân loại hoa Iris. Nếu model đang chạy của bạn yêu cầu các đặc trưng dạng token, bạn cần điều chỉnh server để chấp nhận mảng số (hoặc thêm một endpoint riêng).

Sử dụng `Content-Type: application/json` và gửi các đặc trưng dưới dạng một mảng theo thứ tự:

`[sepal_length, sepal_width, petal_length, petal_width]`

## 1) Iris-setosa (ví dụ)

* **Request:** `POST http://localhost:3000/api/v1/classify`
* **Headers:** `Content-Type: application/json`
* **Body:**

```json
{ "features": [5.1, 3.5, 1.4, 0.2] }
```

* **Status mong đợi:** `200`
* **Ví dụ response:**

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

## 2) Iris-versicolor (ví dụ)

* **Body:**

```json
{ "features": [6.0, 2.9, 4.5, 1.5] }
```

* **Status mong đợi:** `200`
* **Kết quả dự đoán:** `Iris-versicolor`

## 3) Iris-virginica (ví dụ)

* **Body:**

```json
{ "features": [6.3, 3.3, 6.0, 2.5] }
```

* **Status mong đợi:** `200`
* **Kết quả dự đoán:** `Iris-virginica`

## Ghi chú

* Nếu server hiện tại của bạn đang sử dụng các đặc trưng dạng token (danh sách từ), hãy triển khai một luồng xử lý đặc trưng dạng số hoặc tạo một endpoint riêng cho việc phân loại Iris.
* Bạn có thể thêm các bài kiểm thử trong Postman để kiểm tra:

  * `pm.response.code === 200`
  * `pm.expect(pm.response.json().data.prediction).to.eql("Iris-setosa")` (hoặc loài hoa tương ứng).
* Nếu muốn, tôi cũng có thể triển khai endpoint nhận đặc trưng dạng số và huấn luyện SVM trên bộ dữ liệu Iris ở local.

**Lựa chọn:**

* `tạo endpoint`
* `chỉ thêm test-case`


Files created:

- model.py: Naive Bayes implementation
- train.py: sample trainer that writes `model_params.json`
- app.py: Flask API server with `/api/v1/classify` and `/health`
- Dockerfile + docker-compose.yml
