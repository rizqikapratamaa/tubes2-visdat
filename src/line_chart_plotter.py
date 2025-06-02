# streamlit_app/line_chart_plotter.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import config

# from map_plotter import format_trade_value # Jika masih diperlukan

@st.cache_data
def load_line_chart_data():
    """
    Memuat dan memproses data perdagangan untuk line chart.
    Fokus pada total ekspor/impor AS dan China.
    """
    try:
        df = pd.read_csv(config.TRADE_DATA_PATH)
    except FileNotFoundError:
        st.error(f"File '{config.TRADE_DATA_PATH}' tidak ditemukan untuk line chart.")
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
    
    return df_aggregated

def create_trade_trend_line_chart(df_trend_data):
    """
    Membuat line chart tren perdagangan untuk AS dan China.
    """
    if df_trend_data.empty:
        return go.Figure()

    fig = go.Figure()

    countries = ['United States', 'China']
    country_colors = {
        'United States': config.COLOR_US_REF,
        'China': config.COLOR_CHINA_REF
    }

    # --- Tambahkan Traces untuk Ekspor (visible by default) ---
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
            line=dict(color=country_colors[country], width=2.5), # Garis solid
            marker=dict(size=6),
            hovertemplate=(
                f"<b>{country} Exports</b><br>"
                "Year: %{x}<br>"
                "Value: %{y:$,.0f}<extra></extra>"
            ),
            visible=True 
        ))

    # --- Tambahkan Traces untuk Impor (initially hidden) ---
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
            line=dict(color=country_colors[country], width=2.5), # PERUBAHAN: Garis solid (hapus dash='dash')
            marker=dict(size=6, symbol='circle'), # Ganti simbol marker jika mau, misal kembali ke 'circle' atau biarkan default
            hovertemplate=(
                f"<b>{country} Imports</b><br>"
                "Year: %{x}<br>"
                "Value: %{y:$,.0f}<extra></extra>"
            ),
            visible=False 
        ))

    # --- Updatemenus untuk memilih Ekspor/Impor ---
    # Args tetap sama: [visible_export_us, visible_export_cn, visible_import_us, visible_import_cn]
    updatemenu_buttons_list = [
        dict(
            label="Exports",
            method="restyle",
            args=[{"visible": [True, True, False, False]}], 
        ),
        dict(
            label="Imports",
            method="restyle",
            args=[{"visible": [False, False, True, True]}],
        )
    ]

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
        margin=dict(l=90, r=50, t=100, b=80), 
        updatemenus=[
            dict(
                type="dropdown", # PERUBAHAN: dari "buttons" menjadi "dropdown"
                direction="down", # Arah dropdown (bisa juga "right", "left", "up")
                active=0, # Item pertama ("Exports") aktif secara default
                buttons=updatemenu_buttons_list, # Menggunakan list tombol yang sudah ada
                x=0.01, 
                xanchor="left",
                y=1.15,  
                yanchor="top",
                bgcolor=config.PAGE_BG_COLOR, 
                bordercolor=config.TEXT_COLOR_TERTIARY,
                font=dict(color=config.TEXT_COLOR_PRIMARY, size=12), # Font untuk teks dropdown
                pad={"r": 10, "l": 10, "t": 5, "b": 5} # Sesuaikan padding jika perlu
            )
        ]
    )
    return fig