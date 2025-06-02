import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import config
from data_loader import format_trade_value

def generate_trade_table_data_and_pies(df_filtered_table):
    if df_filtered_table.empty:
        return pd.DataFrame(), []

    table_data_records = []
    pie_chart_figures = []

    for index, row in df_filtered_table.iterrows():
        rank = df_filtered_table.index.get_loc(index) + 1
        country = row['Partner']
        us_trade_val = row['US_Trade']
        china_trade_val = row['China_Trade']
        total_trade_val = row['Total_US_China_Trade']

        # Data untuk DataFrame tabel
        table_data_records.append({
            "Rank": rank,
            "Country": country,
            "US Trade": format_trade_value(us_trade_val),
            "China Trade": format_trade_value(china_trade_val),
            "Total (US+China)": format_trade_value(total_trade_val)
        })

        labels = []
        values = []
        colors = []
        pie_fig = None

        if us_trade_val > 0:
            labels.append('US')
            values.append(us_trade_val)
            colors.append(config.COLOR_US_REF)
        if china_trade_val > 0:
            labels.append('China')
            values.append(china_trade_val)
            colors.append(config.COLOR_CHINA_REF)
        
        if values:
            pie_fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                marker_colors=colors,
                hole=0.4, 
                hoverinfo='label+percent', 
                textinfo='none', 
                sort=False,
                automargin=True
            )])
            pie_fig.update_layout(
                showlegend=False, 
                width=60, height=60,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)'
            )
        
        pie_chart_figures.append(pie_fig)

    df_display_table = pd.DataFrame(table_data_records)
    return df_display_table, pie_chart_figures