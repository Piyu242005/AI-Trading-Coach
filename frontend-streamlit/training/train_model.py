"""Train the demo classifier on synthetic data (research/demo use only).

This script intentionally labels the dataset as synthetic. Its metrics must not be
presented as evidence of real-world trading performance.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

FEATURES = [
    "hour_of_day",
    "volume_normalized",
    "risk_reward_ratio",
    "volatility_index",
    "emotion_score",
    "trend_strength",
]
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"


def generate_mock_data(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """Generate deterministic synthetic examples for a demo pipeline."""
    rng = np.random.default_rng(random_state)
    hour = rng.integers(9, 16, n_samples)
    volume = rng.uniform(0.5, 2.5, n_samples)
    risk_reward = rng.uniform(0.5, 3.5, n_samples)
    volatility = rng.uniform(10, 40, n_samples)
    emotion = rng.integers(1, 100, n_samples)
    trend = rng.uniform(-1, 1, n_samples)

    score = (
        risk_reward * 2
        - volatility * 0.05
        + np.abs(trend) * 2
        - emotion * 0.02
        - np.where(hour >= 14, 1.5, 0)
    )
    probability = 1 / (1 + np.exp(-score))
    outcome = (rng.random(n_samples) < probability).astype(int)
    return pd.DataFrame(
        {
            "hour_of_day": hour,
            "volume_normalized": volume,
            "risk_reward_ratio": risk_reward,
            "volatility_index": volatility,
            "emotion_score": emotion,
            "trend_strength": trend,
            "outcome": outcome,
        }
    )


def main() -> None:
    print("Training demo model on SYNTHETIC data only; metrics do not indicate real-market performance.")
    data = generate_mock_data()
    x = data[FEATURES]
    y = data["outcome"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    # Fit preprocessing on training data only to avoid test-set leakage.
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(x_train_scaled, y_train)
    predictions = model.predict(x_test_scaled)
    probabilities = model.predict_proba(x_test_scaled)[:, 1]

    print("Holdout metrics on synthetic data:")
    print(f"  Accuracy:  {accuracy_score(y_test, predictions):.3f}")
    print(f"  Precision: {precision_score(y_test, predictions, zero_division=0):.3f}")
    print(f"  Recall:    {recall_score(y_test, predictions, zero_division=0):.3f}")
    print(f"  F1:        {f1_score(y_test, predictions, zero_division=0):.3f}")
    try:
        print(f"  ROC AUC:   {roc_auc_score(y_test, probabilities):.3f}")
    except ValueError:
        print("  ROC AUC:   unavailable for this holdout split")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "trade_predictor.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    print(f"Saved model and scaler to {MODEL_DIR}")


if __name__ == "__main__":
    main()
