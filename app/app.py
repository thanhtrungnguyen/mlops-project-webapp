import os
import joblib
import logging
from typing import Any, Dict, List, Optional

import pandas as pd
from flask import Flask, request, jsonify, render_template, Response
from flask.typing import ResponseReturnValue
from huggingface_hub import hf_hub_download
from sklearn.base import BaseEstimator

app: Flask = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

# Environment variables for configuration
HF_REPO_ID: str = os.getenv("HF_REPO_ID", "trungngnthanh/mlops-project")
MODEL_FILENAME: str = os.getenv("MODEL_FILENAME", "model.joblib")
HF_REVISION: str = os.getenv("HF_REVISION", "main")

# Global model variable, initially None.
model: Optional[BaseEstimator] = None

try:
    logger.info("Downloading model from Hugging Face Hub...")
    model_path: str = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=MODEL_FILENAME,
        revision=HF_REVISION
    )
    model = joblib.load(model_path)
    logger.info("Model loaded successfully from Hugging Face Hub.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

@app.route("/")
def index() -> str:
    """Render the home page."""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict() -> ResponseReturnValue:
    """
    Predict endpoint that accepts a JSON payload with a "data" key.
    Converts the received data to a DataFrame with valid feature names if needed
    and returns the prediction result as JSON.
    """
    if model is None:
        return jsonify({"error": "Model not available."}), 500

    data: Optional[Dict[str, Any]] = request.get_json()
    if not data or "data" not in data:
        return jsonify({"error": "Missing 'data' in request payload."}), 400

    try:
        # Expected input: a list of samples (list of lists of feature values)
        input_data: List[Any] = data["data"]

        # If model was trained with feature names, convert input_data to a DataFrame.
        if hasattr(model, "feature_names_in_"):
            feature_names = model.feature_names_in_
            # Assume input_data is list of samples. Convert using pandas DataFrame.
            input_df = pd.DataFrame(input_data, columns=feature_names)
            predictions: List[Any] = model.predict(input_df).tolist()
        else:
            predictions = model.predict(input_data).tolist()

        return jsonify({"predictions": predictions})
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port: int = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
    
