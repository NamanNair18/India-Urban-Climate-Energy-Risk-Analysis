# India Urban Climate & Energy Risk Analysis
### *End-to-End Data Science Pipeline: Weather Impact on Power Grids*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge.svg)](https://share.streamlit.io/) 
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 📌 Project Overview
As climate change accelerates, India faces record-breaking heatwaves. This project investigates the direct relationship between rising surface temperatures and electricity demand across 29 Indian States and UTs. By merging NASA satellite weather data with official energy generation statistics, this project provides a data-driven look at climate-induced energy risks.

## 🛠️ Tech Stack
- **Data Engineering:** Python, Pandas, NumPy (Pivoting, Linear Interpolation).
- **Visualization:** Matplotlib, Seaborn, Plotly (Interactive Charts).
- **Interface:** Streamlit (Web Dashboard).
- **Data Sources:** NASA POWER API (Weather) & Ember Climate Data (Energy).

## 📂 Project Structure
```text
Urban_Climate_Analysis/
├── data/
│   ├── raw/                # Original CSVs from NASA & Ember
│   └── processed/          # Merged Master Dataset (Cleaned)
├── src/                    # Modular Python Scripts
│   ├── processing.py       # Weather data cleaning
│   ├── energy_processing.py # Long-to-Wide format pivoting
│   ├── main_merge.py       # Data joining logic
│   └── visualization.py    # Static chart generation
├── app.py                  # Streamlit Web Application
├── requirements.txt        # Reproducibility config
└── README.md               # Project documentation