import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations(master_data_path, output_folder):

    # 1. Loading the master dataset
    if not os.path.exists(master_data_path):
        print(f"Error: {master_data_path} not found. Run the merge script first!")
        return
        
    df = pd.read_csv(master_data_path)
    os.makedirs(output_folder, exist_ok=True)

    sns.set_theme(style="whitegrid")

    # --- CHART 1: Correlation Heatmap ---
    plt.figure(figsize=(10, 8))    #Showing the mathematical relationship between all variables.
    cols_to_corr = ['T2M_MAX', 'RH2M', 'PRECTOTCORR', 'Total Generation', 'Coal', 'Solar']
    corr = df[cols_to_corr].corr()
    sns.heatmap(corr, annot=True, cmap='YlGnBu', fmt=".2f")
    plt.title('Correlation Matrix: Weather Factors vs. Energy Production')
    plt.savefig(f"{output_folder}/01_correlation_heatmap.png")
    
    # --- CHART 2: Temperature vs. Demand Regression ---
    plt.figure(figsize=(10, 6)) #To prove the "Heat Island" impact on power usage.
    sns.regplot(data=df, x='T2M_MAX', y='Total Generation', 
                scatter_kws={'alpha':0.3, 'color':'teal'}, 
                line_kws={'color':'orange'})
    plt.title('Impact of Temperature on Electricity Generation in India (2024)')
    plt.xlabel('Average Max Temperature (°C)')
    plt.ylabel('Total Generation (GWh)')
    plt.savefig(f"{output_folder}/02_temp_vs_generation.png")

    # --- CHART 3: Energy Source Comparison (Stacked Area) ---
    target_state = 'Maharashtra'
    state_df = df[df['state'] == target_state].sort_values(['year', 'month'])
    state_df['Date'] = pd.to_datetime(state_df[['year', 'month']].assign(day=1))
    
    plt.figure(figsize=(12, 6))
    plt.stackplot(state_df['Date'], state_df['Coal'], state_df['Solar'], 
                  labels=['Coal (Fossil)', 'Solar (Renewable)'], alpha=0.7)
    plt.title(f'Energy Generation Mix Trend: {target_state}')
    plt.ylabel('Generation (GWh)')
    plt.legend(loc='upper left')
    plt.savefig(f"{output_folder}/03_energy_mix_trend.png")

    print(f"charts saved in {output_folder}")

if __name__ == "__main__":
    generate_visualizations('data/processed/india_master_data.csv', 'output/visualizations')