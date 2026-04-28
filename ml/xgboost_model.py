import pandas as pd
import numpy as np
import xgboost as xgb
from datetime import timedelta

def create_features(df, target_col="Modal_Price"):
    """Creates time series features for XGBoost."""
    df = df.copy()
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['season'] = df['Date'].dt.quarter
    
    df['lag_1'] = df[target_col].shift(1)
    df['lag_7'] = df[target_col].shift(7)
    df['lag_30'] = df[target_col].shift(30)
    
    df['rolling_mean_7'] = df[target_col].rolling(window=7).mean()
    df['rolling_std_30'] = df[target_col].rolling(window=30).std()
    
    df = df.bfill() # Backfill missing values from lags
    return df

def run_xgboost_forecast(df, periods=30, date_col="Date", target_col="Modal_Price"):
    """Runs XGBoost model recursively to forecast future prices."""
    feat_df = create_features(df, target_col)
    
    features = ['day_of_week', 'month', 'season', 'lag_1', 'lag_7', 'lag_30', 'rolling_mean_7', 'rolling_std_30']
    
    X = feat_df[features]
    y = feat_df[target_col]
    
    model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, objective='reg:squarederror')
    model.fit(X, y)
    
    # Recursive forecasting
    last_row = feat_df.iloc[-1].copy()
    last_date = pd.to_datetime(last_row[date_col])
    
    predictions = []
    dates = []
    
    current_df = feat_df.copy()
    
    for i in range(periods):
        next_date = last_date + timedelta(days=i+1)
        dates.append(next_date)
        
        # Need to recalculate features for the next day
        # For simplicity in this demo, we'll use the model to predict next step
        # and append it to our dataframe to recalculate rolling features
        
        # Create a dummy row for the next date
        new_row = pd.DataFrame({date_col: [next_date], target_col: [np.nan]})
        current_df = pd.concat([current_df, new_row], ignore_index=True)
        
        # Recalculate features
        current_df = create_features(current_df, target_col)
        
        # Get features for the row we just added
        X_pred = current_df.iloc[[-1]][features]
        pred_val = model.predict(X_pred)[0]
        
        predictions.append(pred_val)
        
        # Update the target col so next iteration can use it
        current_df.loc[current_df.index[-1], target_col] = pred_val

    return pd.Series(dates), pd.Series(predictions)

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from data.sample_data import generate_mock_data
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 365)
    ds, yhat = run_xgboost_forecast(df, 7)
    print("XGBoost Forecast:")
    print(yhat.values)
