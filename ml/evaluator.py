import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error

def evaluate_model(y_true, y_pred):
    """Calculates MAPE, RMSE, and MAE."""
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    
    return {
        "MAPE": mape,
        "RMSE": rmse,
        "MAE": mae
    }

if __name__ == "__main__":
    y_true = np.array([100, 150, 200])
    y_pred = np.array([110, 140, 210])
    metrics = evaluate_model(y_true, y_pred)
    print("Metrics:", metrics)
