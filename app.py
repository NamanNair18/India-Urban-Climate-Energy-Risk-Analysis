import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="India Climate-Energy Analysis", layout="wide")# Setting page to wide mode for better charts

# Title and Description
st.title("India Climate & Energy Risk Dashboard")
st.markdown("""
    This application analyzes the correlation between **Surface Temperature** and 
    **Electricity Generation** across different Indian states for the 2024-2025 period.
""")

@st.cache_data
def load_data():
    return pd.read_csv('data/processed/india_master_data.csv')

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Navigation")
    state_list = sorted(df['state'].unique())
    selected_state = st.sidebar.selectbox("Select State/UT", state_list)
    
    # Filter Data
    state_df = df[df['state'] == selected_state].sort_values(['year', 'month'])
    state_df['Date'] = pd.to_datetime(state_df[['year', 'month']].assign(day=1))

    # --- ROW 1: KEY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Max Temp", f"{state_df['T2M_MAX'].mean():.1f} °C")
    col2.metric("Total Power Gen", f"{state_df['Total Generation'].sum():,.0f} GWh")
    col3.metric("Solar Contribution", f"{(state_df['Solar'].sum()/state_df['Total Generation'].sum()*100):.1f}%")
    col4.metric("Avg Humidity", f"{state_df['RH2M'].mean():.1f}%")

    # --- ROW 2: MAIN VISUALS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Temperature vs. Energy Demand")
        # Dual axis chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=state_df['Date'], y=state_df['T2M_MAX'], name="Max Temp (°C)", yaxis="y1"))
        fig.add_trace(go.Bar(x=state_df['Date'], y=state_df['Total Generation'], name="Gen (GWh)", yaxis="y2", opacity=0.5))
        
        fig.update_layout(
            yaxis=dict(title="Temperature (°C)"),
            yaxis2=dict(title="Generation (GWh)", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Energy Mix Over Time")
        fig_mix = px.area(state_df, x='Date', y=['Coal', 'Solar'], 
                         labels={"value": "GWh", "variable": "Source"},
                         color_discrete_map={"Coal": "#454545", "Solar": "#FFD700"})
        st.plotly_chart(fig_mix, use_container_width=True)

    # --- ROW 3: CORRELATION INSIGHT ---
    st.divider()
    st.subheader("Correlation Analysis")
    correlation = state_df['T2M_MAX'].corr(state_df['Total Generation'])
    st.write(f"The Pearson Correlation between Heat and Energy Demand in **{selected_state}** is **{correlation:.2f}**.")
    
    if correlation > 0.7:
        st.success("High Correlation: Energy demand is strongly driven by temperature spikes (likely AC usage).")
    elif correlation > 0.4:
        st.warning("Moderate Correlation: Temperature is a significant factor but other seasonal factors exist.")
    else:
        st.info("Low Correlation: Energy demand in this state may be driven more by industrial activity than weather.")

except Exception as e:
    st.error(f"Please ensure 'data/processed/india_master_data.csv' is created. Error: {e}")