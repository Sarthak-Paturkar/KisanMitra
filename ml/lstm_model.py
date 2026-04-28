import pandas as pd
import numpy as np
from datetime import timedelta
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def run_lstm_forecast(df, periods=30, date_col="Date", target_col="Modal_Price", seq_length=30):
    """Runs LSTM model to forecast future prices."""
    # Ensure data is sorted
    df = df.sort_values(by=date_col).reset_index(drop=True)
    
    # Scale data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[[target_col]])
    
    # Create sequences
    X, y = create_sequences(scaled_data, seq_length)
    
    # Build model
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(seq_length, 1)),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    
    # Train model
    early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
    model.fit(X, y, epochs=20, batch_size=32, verbose=0, callbacks=[early_stop]) # Keep epochs low for demo speed
    
    # Forecast
    last_seq = scaled_data[-seq_length:]
    current_seq = last_seq.reshape(1, seq_length, 1)
    
    predictions = []
    for _ in range(periods):
        pred = model.predict(current_seq, verbose=0)[0]
        predictions.append(pred)
        current_seq = np.append(current_seq[:, 1:, :], [[pred]], axis=1)
        
    # Inverse transform
    inv_predictions = scaler.inverse_transform(predictions).flatten()
    
    # Generate dates
    last_date = pd.to_datetime(df[date_col].iloc[-1])
    dates = [last_date + timedelta(days=i+1) for i in range(periods)]
    
    return pd.Series(dates), pd.Series(inv_predictions)

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from data.sample_data import generate_mock_data
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 365)
    ds, yhat = run_lstm_forecast(df, 7)
    print("LSTM Forecast:")
    print(yhat.values)
