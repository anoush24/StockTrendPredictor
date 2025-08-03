import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def predict_trend(data, forecast_days=5):
    """Improved prediction with trend analysis"""
    df = data.copy()
    df['Days'] = np.arange(len(df))

    # Feature engineering
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_21'] = df['Close'].rolling(window=21).mean()
    df = df.dropna()

    X = df[['Days', 'MA_7', 'MA_21']].values
    y = df['Close'].values

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future
    last_day = df['Days'].iloc[-1]
    future_days = np.array(range(last_day + 1, last_day + 1 + forecast_days))
    future_ma7 = df['MA_7'].iloc[-forecast_days:].values
    future_ma21 = df['MA_21'].iloc[-forecast_days:].values

    future_features = np.column_stack([future_days, future_ma7, future_ma21])
    return model.predict(future_features)