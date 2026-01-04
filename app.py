import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="India Climate-Energy Analysis", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Ensure this path is correct in your local folder
    return pd.read_csv('data/processed/india_master_data.csv')

# --- MAIN APP LOGIC ---
st.title("🇮🇳 India Climate & Energy Risk Dashboard")
st.markdown("""
    This application analyzes the correlation between **Surface Temperature** and 
    **Electricity Generation** across different Indian states for the 2024-2025 period.
""")

try:
    # 1. Load data first
    df = load_data()

    # 2. Sidebar Filters (Define 'selected_state' here)
    st.sidebar.header("Navigation")
    state_list = sorted(df['state'].unique())
    selected_state = st.sidebar.selectbox("Select State/UT", state_list)
    
    # 3. Filter Data for the selected state
    state_df = df[df['state'] == selected_state].sort_values(['year', 'month']).copy()
    state_df['Date'] = pd.to_datetime(state_df[['year', 'month']].assign(day=1))

    # 4. DATA INTEGRITY FIX: Handle the 'Goa Anomaly'
    # Calculate Solar Share using epsilon to avoid division by zero
    state_df['Solar_Share'] = (state_df['Solar'] / (state_df['Total Generation'] + 1e-6)) * 100

    # Check for anomalies (>100%)
    is_anomaly = state_df['Solar_Share'].max() > 100
    if is_anomaly:
        st.warning(f" Note: In {selected_state}, internal solar data exceeds reported generation. Share has been capped at 100% for analysis.")
        state_df.loc[state_df['Solar_Share'] > 100, 'Solar_Share'] = 100

    # --- ROW 1: KEY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Max Temp", f"{state_df['T2M_MAX'].mean():.1f} °C")
    col2.metric("Total Power Gen", f"{state_df['Total Generation'].sum():,.0f} GWh")
    
    # Use the cleaned solar share for the metric
    avg_solar_contribution = (state_df['Solar'].sum() / (state_df['Total Generation'].sum() + 1e-6)) * 100
    # Cap displayed metric at 100%
    display_solar = min(avg_solar_contribution, 100.0)
    col3.metric("Solar Contribution", f"{display_solar:.1f}%")
    
    col4.metric("Avg Humidity", f"{state_df['RH2M'].mean():.1f}%")

    # --- ROW 2: MAIN VISUALS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Temperature vs. Energy Demand")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=state_df['Date'], y=state_df['T2M_MAX'], name="Max Temp (°C)", yaxis="y1", line=dict(color="#FF4B4B")))
        fig.add_trace(go.Bar(x=state_df['Date'], y=state_df['Total Generation'], name="Gen (GWh)", yaxis="y2", opacity=0.3, marker_color="#0068C9"))
        
        fig.update_layout(
            yaxis=dict(
                title=dict(text="Temperature (°C)", font=dict(color="#FF4B4B")),
                tickfont=dict(color="#FF4B4B")
            ),
            yaxis2=dict(
                title=dict(text="Generation (GWh)", font=dict(color="#0068C9")),
                tickfont=dict(color="#0068C9"),
                overlaying="y",
                side="right"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Energy Mix Over Time")
        # Ensure we only plot existing columns to avoid errors
        available_cols = [c for c in ['Coal', 'Solar', 'Wind', 'Hydro'] if c in state_df.columns]
        fig_mix = px.area(state_df, x='Date', y=available_cols, 
                         labels={"value": "GWh", "variable": "Source"},
                         color_discrete_map={"Coal": "#454545", "Solar": "#FFD700", "Wind": "#00CC96", "Hydro": "#636EFA"})
        st.plotly_chart(fig_mix, use_container_width=True)

    # --- ROW 3: CORRELATION INSIGHT ---
    st.divider()
    st.subheader("Correlation Analysis")
    correlation = state_df['T2M_MAX'].corr(state_df['Total Generation'])
    
    # Handling NaN correlation (if data is constant)
    if pd.isna(correlation):
        st.info("Insufficient variance in data to calculate Pearson correlation.")
    else:
        st.write(f"The Pearson Correlation between Heat and Energy Demand in **{selected_state}** is **{correlation:.2f}**.")
        
        if correlation > 0.7:
            st.success(" **High Correlation:** Energy demand is strongly driven by temperature spikes (likely high AC/Cooling usage).")
        elif correlation > 0.4:
            st.warning(" **Moderate Correlation:** Temperature is a significant factor, but industrial cycles or seasonal shifts also play a role.")
        else:
            st.info(" **Low Correlation:** Energy demand in this state appears driven by industrial activity or base load rather than weather fluctuations.")

except FileNotFoundError:
    st.error(" **File Not Found:** Please ensure `data/processed/india_master_data.csv` exists. Run your processing scripts first!")
except Exception as e:
    st.error(f" **Application Error:** {e}")