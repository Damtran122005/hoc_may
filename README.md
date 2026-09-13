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

Use the requests below in Postman (set method, url, headers, and raw JSON body). Expected responses are shown so you can assert status and body in tests.

- Health check

  - Request: `GET http://localhost:3000/health`
  - Expected: `200`
  - Example response:

```json
{
  "success": true,
  "status": 200,
  "message": "Model health",
  "data": { "model": "naive_bayes", "health_status": "healthy" }
}
```

- Predict — valid features

  - Request: `POST http://localhost:3000/api/v1/classify`
  - Headers: `Content-Type: application/json`
  - Body (raw JSON):

```json
{
  "features": ["free", "offer", "click"]
}
```

  - Expected: `200`
  - Example response shape (values will vary):

```json
{
  "success": true,
  "status": 200,
  "message": "Dự đoán Naive Bayes thành công",
  "data": {
    "model": "naive_bayes",
    "endpoint": "/api/v1/classify",
    "prediction": "spam",
    "probability": 0.8421,
    "health_status": "healthy"
  }
}
```

- Predict — missing `features` field

  - Body:

```json
{}
```

  - Expected: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "Missing required field: features",
  "data": null
}
```

- Predict — empty `features` array

  - Body:

```json
{ "features": [] }
```

  - Expected: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "The features field must be a non-empty array",
  "data": null
}
```

- Predict — empty or invalid JSON body

  - Send no body or malformed JSON
  - Expected: `400`
  - Example response:

```json
{
  "success": false,
  "status": 400,
  "message": "Input data cannot be empty",
  "data": null
}
```

- Predict — model unavailable (service start without `model_params.json`)

  - Expected: `503`
  - Example response:

```json
{
  "success": false,
  "status": 503,
  "message": "Naive Bayes model is not available",
  "data": { "model": "naive_bayes", "health_status": "unhealthy" }
}
```

Files created:

- model.py: Naive Bayes implementation
- train.py: sample trainer that writes `model_params.json`
- app.py: Flask API server with `/api/v1/classify` and `/health`
- Dockerfile + docker-compose.yml
