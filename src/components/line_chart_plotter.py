import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import config
from data_loader import format_trade_value

@st.cache_data
def load_line_chart_data():
    try:
        df = pd.read_csv(config.TRADE_DATA_PATH)
    except FileNotFoundError:
        st.error(f"File '{config.TRADE_DATA_PATH}' not found for line chart.")
        return pd.DataFrame()

    df_us_china = df[df['Country'].isin(['United States', 'China'])].copy()
    year_columns = [str(y) for y in config.YEARS_RANGE if str(y) in df_us_china.columns]

    df_melted = df_us_china.melt(
        id_vars=['Country', 'Trade_Type', 'Partner'],
        value_vars=year_columns,
        var_name='Year',
        value_name='Value'
    )

    df_melted['Year'] = pd.to_numeric(df_melted['Year'])
    df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce').fillna(0)

    df_aggregated = df_melted.groupby(['Country', 'Trade_Type', 'Year'])['Value'].sum().reset_index()

    df_aggregated['Formatted_Value'] = df_aggregated['Value'].apply(format_trade_value)

    return df_aggregated

def create_trade_trend_line_chart(df_trend_data, selected_view="Exports"):
    if df_trend_data.empty:
        return go.Figure()

    fig = go.Figure()

    countries = ['United States', 'China']
    country_colors = {
        'United States': config.COLOR_US_REF,
        'China': config.COLOR_CHINA_REF
    }

    show_exports = (selected_view == "Exports")
    show_imports = (selected_view == "Imports")

    for country in countries:
        df_country_export = df_trend_data[
            (df_trend_data['Country'] == country) &
            (df_trend_data['Trade_Type'] == 'Export')
        ]
        fig.add_trace(go.Scatter(
            x=df_country_export['Year'],
            y=df_country_export['Value'],
            name=f'{country} Exports',
            mode='lines+markers',
            line=dict(color=country_colors[country], width=2.5),
            marker=dict(size=6),
            customdata=df_country_export['Formatted_Value'],
            hovertemplate=(
                f"<b>{country} Exports</b><br>"
                "Year: %{x}<br>"
                "Value: %{customdata}<extra></extra>"
            ),
            visible=show_exports
        ))

    for country in countries:
        df_country_import = df_trend_data[
            (df_trend_data['Country'] == country) &
            (df_trend_data['Trade_Type'] == 'Import')
        ]
        fig.add_trace(go.Scatter(
            x=df_country_import['Year'],
            y=df_country_import['Value'],
            name=f'{country} Imports',
            mode='lines+markers',
            line=dict(color=country_colors[country], width=2.5),
            marker=dict(size=6, symbol='circle'),
            customdata=df_country_import['Formatted_Value'],
            hovertemplate=(
                f"<b>{country} Imports</b><br>"
                "Year: %{x}<br>"
                "Value: %{customdata}<extra></extra>"
            ),
            visible=show_imports
        ))

    fig.update_layout(
        title=dict(
            text="US vs China Trade Trends",
            x=0.5,
            xanchor='center',
            font=dict(size=20, color=config.TEXT_COLOR_PRIMARY)
        ),
        xaxis=dict(
            title=dict(
                text="Year",
                font=dict(color=config.TEXT_COLOR_PRIMARY, size=14)
            ),
            showgrid=True,
            gridcolor='#4A5568',
            zeroline=False,
            tickfont=dict(color=config.TEXT_COLOR_SECONDARY),
        ),
        yaxis=dict(
            title=dict(
                text="Trade Value (USD)",
                font=dict(color=config.TEXT_COLOR_PRIMARY, size=14)
            ),
            showgrid=True,
            gridcolor='#4A5568',
            zeroline=False,
            tickfont=dict(color=config.TEXT_COLOR_SECONDARY),
            tickformat="$,.0f"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor='rgba(0,0,0,0)',
            font=dict(color=config.TEXT_COLOR_SECONDARY)
        ),
        paper_bgcolor=config.PAGE_BG_COLOR,
        plot_bgcolor=config.PAGE_BG_COLOR,
        font=dict(color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif'),
        height=500,
        margin=dict(l=90, r=50, t=100, b=80)
    )
    return fig