
# India Urban Climate & Energy Risk Analysis

#### *End-to-End Data Science Pipeline: Weather Impact on Power Grids*



## 📌 Project Overview
As climate change accelerates, India faces record-breaking heatwaves. This project investigates the direct relationship between rising surface temperatures and electricity demand across 29 Indian States and UTs. By merging NASA satellite weather data with official energy generation statistics, this project provides a data-driven look at climate-induced energy risks.
## 🛠️ Tech Stack

- **Data Engineering:** Python, Pandas, NumPy (Pivoting, Linear Interpolation).

- **Visualization:** Matplotlib, Seaborn, Plotly (Interactive Charts)

- **Interface:** Streamlit (Web Dashboard).
- **Data Sources:** NASA POWER API (Weather) & Ember Climate Data (Energy).


## 📂 Project Structure
```text
Urban_Climate_Analysis/
├── data/
│   ├── raw/                
│   └── processed/   
├── output/
│   ├── visualization/         
├── src/                    
│   ├── preprocessing.py       
│   ├── data_loader.py     
│   ├── energy_processing.py 
│   ├── main_merge.py       
│   └── visualization.py    
├── app.py                  
├── requirements.txt        
└── README.md   
```
## 🔍 Key Data Science Methodologies

1. **Data Cleaning & Linear Interpolation**
Satellite data often contains missing entries or noise (flagged as -999).

- **Methodology**: I implemented Linear Interpolation to fill gaps in the time-series weather data.

- **Rationale**: Unlike "Mean Imputation," which flattens variance, linear interpolation preserves the trend between data points, which is critical for seasonal climate analysis.

2. **Feature Engineering: Long-to-Wide Transformation**
The raw energy data was provided in a "Long Format" (Tidy Data), which is efficient for storage but difficult for correlation analysis.

- **Methodology**: I utilized Pandas Pivot Tables to reshape the dataset.

- **Result**: I transformed the Variable column (containing Solar, Coal, etc.) into separate feature columns. This reshaped the data into a "Wide Format," allowing for row-wise mathematical operations between weather and energy variables.

3. **Statistical Analysis**: Pearson CorrelationTo quantify the impact of heat on the power grid, I conducted a state-wise correlation analysis.
- **Methodology**: Calculated the Pearson Correlation Coefficient (r) between T2M_MAX (Max Temperature) and Total Generation.

- **Finding**: A strong positive correlation ($r > 0.8$) was identified in urbanized regions, statistically proving that temperature spikes are the primary driver of grid load during Indian summers.

4. **Modular Pipeline Architecture**
Following industry best practices for Reproducibility (Rule 13), I moved away from monolithic notebooks.

- **Methodology**: Encapsulated data logic into modular .py scripts.

- **Impact**: This allows for automated data updates and ensures that the preprocessing logic is "Production-Ready" and easy to debug.


## 📊 Sample Insights
- **Heat Sensitivity**: For every 1°C rise in average monthly temperature above 30°C, energy demand increases significantly in states with high AC penetration.

- **Renewable Buffer**: Solar energy production peaks during the same months as peak demand, highlighting its role as a critical buffer for the Indian grid.
## 🚀 Installation & Usage

1. Clone the repository:

```bash
git clone [https://github.com/NamanNair18/India-Urban-Climate-Energy-Risk-Analysis]
cd india-climate-energy
```
2.Install Dependencies:

```bash
pip install -r requirements.txt
```
3. Run the Dashboard:

```bash
streamlit run app.py
```

## Author

- [@NamanNair18](https://github.com/NamanNair18)

