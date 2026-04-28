import pandas as pd
from datetime import timedelta

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

def run_prophet_forecast(df, periods=30, date_col="Date", target_col="Modal_Price"):
    """Runs Prophet model to forecast future prices."""
    if not PROPHET_AVAILABLE:
        print("Prophet not available. Please install 'prophet'.")
        # Dummy fallback
        last_date = pd.to_datetime(df[date_col].iloc[-1])
        dates = [last_date + timedelta(days=i+1) for i in range(periods)]
        last_val = df[target_col].iloc[-1]
        return pd.Series(dates), pd.Series([last_val]*periods), pd.Series([last_val*0.9]*periods), pd.Series([last_val*1.1]*periods)

    prophet_df = df[[date_col, target_col]].rename(columns={date_col: 'ds', target_col: 'y'})
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(prophet_df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Return only the future predictions
    future_forecast = forecast.iloc[-periods:]
    
    return future_forecast['ds'].reset_index(drop=True), future_forecast['yhat'].reset_index(drop=True), future_forecast['yhat_lower'].reset_index(drop=True), future_forecast['yhat_upper'].reset_index(drop=True)

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from data.sample_data import generate_mock_data
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 365)
    ds, yhat, lower, upper = run_prophet_forecast(df, 7)
    print("Forecast dates:", ds.head().values)
    print("Forecast values:", yhat.head().values)
