import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_base_price(crop):
    base_prices = {
        "Tomato": 1800,
        "Onion": 1200,
        "Potato": 900,
        "Wheat": 2100,
        "Rice": 2400,
        "Soybean": 4500,
        "Cotton": 6000,
        "Sugarcane": 300,
        "Chilli": 15000,
        "Garlic": 8000
    }
    return base_prices.get(crop, 2000)

def generate_mock_data(crop, state, market, days=365):
    """Generates realistic mock daily prices using sine wave and noise."""
    base = get_base_price(crop)
    
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    dates.reverse()
    
    prices = []
    for i in range(days):
        # Base + trend (slight upward) + seasonality (sine wave over 365 days) + noise
        trend = i * (base * 0.0001)
        seasonality = (base * 0.2) * np.sin(2 * np.pi * i / 365.0)
        noise = np.random.normal(0, base * 0.05)
        
        price = base + trend + seasonality + noise
        
        # Clamp between 50% and 200%
        price = max(base * 0.5, min(price, base * 2.0))
        prices.append(price)
        
    df = pd.DataFrame({
        "Date": dates,
        "Crop": [crop] * days,
        "State": [state] * days,
        "Market": [market] * days,
        "Modal_Price": prices
    })
    return df

if __name__ == "__main__":
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 30)
    print(df.head())
