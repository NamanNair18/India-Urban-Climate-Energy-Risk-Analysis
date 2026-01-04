import pandas as pd
import os

def create_master_dataset(weather_path, energy_path, output_path):

    # 1. Loading the processed files
    df_weather = pd.read_csv(weather_path)
    df_energy = pd.read_csv(energy_path)

    # 2. THE INNER JOIN 
    df_energy = df_energy.rename(columns={'State': 'state'})    # matching rows where BOTH the state and the time (year/month) are identical.
    
    master_df = pd.merge(
        df_weather, 
        df_energy, 
        on=['state', 'year', 'month'], 
        how='inner'
    )

    # 3. Checking the Qulaity of the File
    print(f"Merge Complete!")
    print(f"Total Rows: {master_df.shape[0]}")
    print(f"Columns available for AI/Analysis: {master_df.columns.tolist()}")

    # 4. Saving the Master File
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    master_df.to_csv(output_path, index=False)
    
    return master_df

if __name__ == "__main__":
    create_master_dataset(
        weather_path='data/processed/india_monthly_weather.csv',
        energy_path='data/processed/india_energy_wide.csv',
        output_path='data/processed/india_master_data.csv'
    )