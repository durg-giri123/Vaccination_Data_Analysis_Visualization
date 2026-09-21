import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Vaccination Data Dashboard", layout="wide")

st.title("🌍 Global Vaccination & Public Health Dashboard")
st.markdown("This interactive dashboard provides insights into vaccination coverage, reported cases, and disease incidence rates globally. (Alternative to Power BI/Tableau)")

@st.cache_data
def load_data():
    db_path = Path("data/vaccination.db")
    if not db_path.exists():
        st.error("Database not found! Please run `python run_pipeline.py` first.")
        return None, None
    
    conn = sqlite3.connect(db_path)
    
    # Load coverage
    query_cov = """
    SELECT c.name as country_name, c.who_region, v.year, a.antigen, v.coverage
    FROM fact_vaccination_coverage v
    JOIN dim_country c ON v.country_id = c.country_id
    JOIN dim_vaccine a ON v.vaccine_id = a.vaccine_id
    """
    df_cov = pd.read_sql(query_cov, conn)
    
    # Load cases
    query_cases = """
    SELECT c.name as country_name, c.who_region, r.year, d.disease, r.cases
    FROM fact_reported_cases r
    JOIN dim_country c ON r.country_id = c.country_id
    JOIN dim_disease d ON r.disease_id = d.disease_id
    """
    df_cases = pd.read_sql(query_cases, conn)
    
    conn.close()
    return df_cov, df_cases

df_cov, df_cases = load_data()

if df_cov is not None and not df_cov.empty:
    st.sidebar.header("Filters")
    
    # Year slider
    min_year, max_year = int(df_cov['year'].min()), int(df_cov['year'].max())
    selected_year = st.sidebar.slider("Select Year", min_year, max_year, max_year)
    
    # Region filter
    regions = ['All'] + list(df_cov['who_region'].dropna().unique())
    selected_region = st.sidebar.selectbox("Select WHO Region", regions)
    
    # Filter data
    df_cov_filtered = df_cov[df_cov['year'] == selected_year]
    df_cases_filtered = df_cases[df_cases['year'] == selected_year]
    
    if selected_region != 'All':
        df_cov_filtered = df_cov_filtered[df_cov_filtered['who_region'] == selected_region]
        df_cases_filtered = df_cases_filtered[df_cases_filtered['who_region'] == selected_region]

    # KPIs
    st.markdown("### Key Performance Indicators (KPIs)")
    col1, col2, col3 = st.columns(3)
    avg_cov = df_cov_filtered['coverage'].mean()
    total_cases = df_cases_filtered['cases'].sum()
    countries_reporting = df_cov_filtered['country_name'].nunique()
    
    col1.metric("Average Vaccination Coverage", f"{avg_cov:.1f}%" if pd.notnull(avg_cov) else "N/A")
    col2.metric("Total Reported Disease Cases", f"{total_cases:,.0f}" if pd.notnull(total_cases) else "N/A")
    col3.metric("Countries Reporting", f"{countries_reporting}")

    st.markdown("---")
    
    # Row 1: Maps and Distributions
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Global Vaccination Coverage Map")
        map_data = df_cov_filtered.groupby('country_name')['coverage'].mean().reset_index()
        fig_map = px.choropleth(map_data, locations="country_name", locationmode="country names", 
                                color="coverage", hover_name="country_name", 
                                color_continuous_scale=px.colors.sequential.YlGnBu,
                                range_color=(0, 100))
        st.plotly_chart(fig_map, use_container_width=True)

    with col_b:
        st.subheader("Reported Cases by Disease (Pie)")
        pie_data = df_cases_filtered.groupby('disease')['cases'].sum().reset_index()
        # Group small values into 'Other'
        threshold = pie_data['cases'].sum() * 0.02
        pie_data.loc[pie_data['cases'] < threshold, 'disease'] = 'Other'
        pie_data = pie_data.groupby('disease')['cases'].sum().reset_index()
        fig_pie = px.pie(pie_data, names='disease', values='cases', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Row 2: Trend Lines
    st.markdown("---")
    st.subheader("Historical Trends (All Years)")
    col_c, col_d = st.columns(2)
    
    with col_c:
        trend_cov = df_cov.groupby('year')['coverage'].mean().reset_index()
        fig_trend_cov = px.line(trend_cov, x='year', y='coverage', title='Global Average Coverage Over Time', markers=True)
        st.plotly_chart(fig_trend_cov, use_container_width=True)

    with col_d:
        trend_cases = df_cases.groupby('year')['cases'].sum().reset_index()
        fig_trend_cases = px.line(trend_cases, x='year', y='cases', title='Global Total Reported Cases Over Time', markers=True, color_discrete_sequence=['red'])
        st.plotly_chart(fig_trend_cases, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Raw Data Explorer")
    st.dataframe(df_cov_filtered.head(100))
