import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

def generate_mock_data(n_samples=500):
    np.random.seed(42)
    data = []
    
    for _ in range(n_samples):
        # Features
        hour_of_day = np.random.randint(9, 16)
        volume_normalized = np.random.uniform(0.5, 2.5)
        risk_reward_ratio = np.random.uniform(0.5, 3.5)
        volatility_index = np.random.uniform(10, 40)
        emotion_score = np.random.randint(1, 100) # Higher is worse (e.g., greedy/fearful)
        trend_strength = np.random.uniform(-1, 1) # -1 strong downtrend, 1 strong uptrend
        
        # Outcome logic (mocking patterns)
        # Winning more likely if R:R > 1.5, low volatility, trend is strong
        score = (risk_reward_ratio * 2) - (volatility_index * 0.05) + (abs(trend_strength) * 2) - (emotion_score * 0.02)
        
        # Adding some "pattern detection" signals requested by the user
        if hour_of_day >= 14: # "Win rate drops after 2 PM"
            score -= 1.5
            
        prob = 1 / (1 + np.exp(-score)) # Sigmoid
        outcome = 1 if np.random.random() < prob else 0
        
        data.append({
            "hour_of_day": hour_of_day,
            "volume_normalized": volume_normalized,
            "risk_reward_ratio": risk_reward_ratio,
            "volatility_index": volatility_index,
            "emotion_score": emotion_score,
            "trend_strength": trend_strength,
            "outcome": outcome
        })
        
    return pd.DataFrame(data)

def main():
    print("Generating mock trading data...")
    df = generate_mock_data(1000)
    
    X = df.drop("outcome", axis=1)
    y = df["outcome"]
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2%}")
    
    os.makedirs("../models", exist_ok=True)
    
    # Save the model and scaler
    model_path = "../models/trade_predictor.joblib"
    scaler_path = "../models/scaler.joblib"
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Saved model to {model_path}")
    print(f"Saved scaler to {scaler_path}")

if __name__ == "__main__":
    main()
