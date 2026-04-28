import pandas as pd
from .prophet_model import run_prophet_forecast
from .xgboost_model import run_xgboost_forecast
from .lstm_model import run_lstm_forecast

def generate_ensemble_forecast(df, periods=30, date_col="Date", target_col="Modal_Price"):
    """
    Runs all 3 models and combines their predictions.
    Weights: Prophet 40%, LSTM 35%, XGBoost 25%
    """
    # 1. Prophet
    p_dates, p_yhat, p_lower, p_upper = run_prophet_forecast(df, periods, date_col, target_col)
    
    # 2. XGBoost
    x_dates, x_yhat = run_xgboost_forecast(df, periods, date_col, target_col)
    
    # 3. LSTM
    l_dates, l_yhat = run_lstm_forecast(df, periods, date_col, target_col)
    
    # Combine
    # Since dates might be out of order if not careful, we rely on them being exactly the same future periods.
    
    ensemble_yhat = (p_yhat * 0.40) + (l_yhat * 0.35) + (x_yhat * 0.25)
    
    # For confidence intervals, we'll center Prophet's intervals around the ensemble mean
    interval_range = (p_upper - p_lower) / 2
    ensemble_lower = ensemble_yhat - interval_range
    ensemble_upper = ensemble_yhat + interval_range
    
    return p_dates, ensemble_yhat, ensemble_lower, ensemble_upper

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from data.sample_data import generate_mock_data
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 365)
    dates, preds, lower, upper = generate_ensemble_forecast(df, 7)
    print("Ensemble Forecast:")
    print(preds.values)
