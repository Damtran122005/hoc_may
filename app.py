from flask import Flask, request, jsonify
from model import NaiveBayesModel
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_params.joblib")

app = Flask(__name__)


def load_model():
    try:
        from model import SVMModel

        model = SVMModel.load(MODEL_PATH)
        return model
    except Exception:
        return None


model = load_model()


@app.route("/health", methods=["GET"])
def health():
    status = "healthy" if model is not None else "unhealthy"
    code = 200 if model is not None else 503
    return jsonify({
        "success": model is not None,
        "status": code,
        "message": "Model health",
        "data": {"model": "naive_bayes", "health_status": status},
    }), code


@app.route("/api/v1/classify", methods=["POST"])
def classify():
    if model is None:
        return jsonify({
            "success": False,
            "status": 503,
            "message": "SVM model is not available",
            "data": {"model": "svm", "health_status": "unhealthy"},
        }), 503

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({
            "success": False,
            "status": 400,
            "message": "Input data cannot be empty",
            "data": None,
        }), 400

    features = payload.get("features")
    if features is None:
        return jsonify({
            "success": False,
            "status": 400,
            "message": "Missing required field: features",
            "data": None,
        }), 400

    if not isinstance(features, list) or len(features) == 0:
        return jsonify({
            "success": False,
            "status": 400,
            "message": "The features field must be a non-empty array",
            "data": None,
        }), 400

    try:
        prediction, prob = model.predict(features)
        return jsonify({
            "success": True,
            "status": 200,
            "message": "Prediction successful",
            "data": {
                "model": "svm",
                "endpoint": "/api/v1/classify",
                "prediction": prediction,
                "probability": round(prob, 4),
                "health_status": "healthy",
            },
        }), 200
    except Exception:
        return jsonify({
            "success": False,
            "status": 500,
            "message": "Internal server error during prediction",
            "data": None,
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
