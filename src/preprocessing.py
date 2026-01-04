import pandas as pd
import numpy as np
import os

def clean_and_aggregate_weather(input_path, output_path):

    # 1. Loading the data
    df = pd.read_csv(input_path)
    print(f"Processing {len(df)} rows of data....")

    # 2. Converting Integer Date to Real Datetime
    # Why? '20240101' -> '2024-01-01'. This allows for time-series math.
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')

    # 3. Handle 'Hidden' Nulls 
    df = df.replace(-999, np.nan)
    df = df.interpolate(method='linear')

    # 4. Extracting Month and Year for Aggregation
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # 5. AGGREGATION: Convert Daily to Monthly
    monthly_df = df.groupby(['state', 'year', 'month']).agg({
        'T2M_MAX': 'mean',
        'T2M_MIN': 'mean',
        'RH2M': 'mean',
        'PRECTOTCORR': 'sum' # Rainfall is cumulative
    }).reset_index()

    # 6. Saving the Processed Data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    monthly_df.to_csv(output_path, index=False)
    
    print(f"Cleaned and Aggregated data saved to: {output_path}")
    return monthly_df

if __name__ == "__main__":
    clean_and_aggregate_weather(
        input_path='data/raw/india_weather_2024_2025.csv',
        output_path='data/processed/india_monthly_weather.csv'
    )