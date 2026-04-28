import pandas as pd
import numpy as np

def remove_outliers(df, column="Modal_Price"):
    """Removes outliers using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Cap outliers instead of removing to maintain time sequence
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    return df

def smooth_prices(df, column="Modal_Price", window=7):
    """Smooths prices using a rolling median."""
    df[column] = df[column].rolling(window=window, min_periods=1).median()
    return df

def interpolate_missing(df, column="Modal_Price"):
    """Interpolates missing values using time interpolation."""
    df[column] = df[column].interpolate(method='linear', limit_direction='both')
    return df

def preprocess(df, date_col="Date", target_col="Modal_Price"):
    """Full preprocessing pipeline."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col).reset_index(drop=True)
    
    df = interpolate_missing(df, target_col)
    df = remove_outliers(df, target_col)
    df = smooth_prices(df, target_col)
    
    return df

if __name__ == "__main__":
    from data.sample_data import generate_mock_data
    df = generate_mock_data("Tomato", "Maharashtra", "Pune", 30)
    print("Before:", df['Modal_Price'].head().values)
    df_clean = preprocess(df)
    print("After:", df_clean['Modal_Price'].head().values)
