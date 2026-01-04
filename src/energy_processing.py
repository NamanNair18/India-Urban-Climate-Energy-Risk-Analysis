import pandas as pd
import numpy as np
import os

def process_ember_energy_data(input_path, output_path):

    # 1. Loading the dataset
    df = pd.read_csv(input_path)
    
    # 2. Filtering for relevant data 
    interesting_variables = ['Total Generation', 'Coal', 'Solar', 'Wind']
    df_filtered = df[
        (df['Category'] == 'Electricity generation') & 
        (df['Variable'].isin(interesting_variables)) #keeping 'Total Generation', 'Coal', 'Wind' and 'Solar' to see the 'Green Energy' transition.
    ].copy()

    # 3. Converting the Date to datetime objects 
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])
    df_filtered['year'] = df_filtered['Date'].dt.year
    df_filtered['month'] = df_filtered['Date'].dt.month

    # 4. THE PIVOT: 
    df_wide = df_filtered.pivot_table(   #turning the 'Variable' column values into their own columns.
        index=['State', 'year', 'month'], 
        columns='Variable', 
        values='Value'
    ).reset_index()

    # 5. Handling Missing Values
    df_wide[['Solar', 'Wind', 'Coal']] = df_wide[['Solar', 'Wind', 'Coal']].fillna(0)
    df_wide['Total Generation'] = df_wide['Total Generation'].interpolate()

    # 6. Saving the Processed Energy Data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_wide.to_csv(output_path, index=False)
    
    print(f"Energy data reshaped! Saved to: {output_path}")
    print(f"Columns created: {df_wide.columns.tolist()}")
    return df_wide

if __name__ == "__main__":
    process_ember_energy_data(
        input_path='data/raw/india_monthly_full_release_long_format.csv',
        output_path='data/processed/india_energy_wide.csv'
    )