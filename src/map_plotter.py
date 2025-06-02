# streamlit_app/map_plotter.py
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import config
import streamlit as st

# Fungsi format_trade_value (pastikan sudah benar)
def format_trade_value(value):
    if pd.isna(value) or value == 0:
        return "$0"
    if abs(value) >= 1_000_000_000_000: # Trillion
        return f"${value / 1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000: # Billion
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000: # Million
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000: # Thousand
        return f"${value / 1_000:.2f}K"
    return f"${value:.2f}"

def create_choropleth_map(df_dominance_all_flows, available_years, geojson_data, min_year, max_year, current_selected_year, initial_active_flow_key="Total", selected_continent="World"):

    if df_dominance_all_flows.empty or not available_years or geojson_data is None:
        return go.Figure()

    map_countries_in_geojson = [feature['properties']['name'] for feature in geojson_data['features']]
    
    fig = go.Figure()
    
    flow_keys_ordered = [config.TRADE_FLOW_MAP[display_name] for display_name in config.TRADE_FLOW_OPTIONS_DISPLAY]

    initial_year_to_display = current_selected_year 
    if initial_year_to_display not in available_years:
        initial_year_to_display = max(available_years) if available_years else min_year

    # --- Tambahkan Traces Awal ---
    for i, flow_key in enumerate(flow_keys_ordered):
        df_flow_specific = df_dominance_all_flows[df_dominance_all_flows['Trade_Flow_Type'] == flow_key]
        df_initial_year_flow = df_flow_specific[df_flow_specific['Year'] == initial_year_to_display]
        
        ratio_dict = pd.Series(df_initial_year_flow.Ratio.values, index=df_initial_year_flow.Partner).to_dict()
        us_trade_dict = pd.Series(df_initial_year_flow.US_Trade.values, index=df_initial_year_flow.Partner).to_dict()
        china_trade_dict = pd.Series(df_initial_year_flow.China_Trade.values, index=df_initial_year_flow.Partner).to_dict()
        
        z_values, hover_texts, locations = [], [], []
        for country_name_geojson in map_countries_in_geojson:
            locations.append(country_name_geojson)
            ratio = ratio_dict.get(country_name_geojson, np.nan)
            us_trade = us_trade_dict.get(country_name_geojson, 0) 
            china_trade = china_trade_dict.get(country_name_geojson, 0)
            
            z_values.append(ratio)
            
            country_display_name = country_name_geojson
            trade_details_text = ""
            if pd.isna(ratio): trade_details_text = "Data: Not available"
            elif country_name_geojson == "United States of America": trade_details_text = f"US Trade: {format_trade_value(us_trade)}<br>China Trade: {format_trade_value(china_trade)}<br>(Dominant: US)"
            elif country_name_geojson == "China": trade_details_text = f"US Trade: {format_trade_value(us_trade)}<br>China Trade: {format_trade_value(china_trade)}<br>(Dominant: China)"
            else: trade_details_text = (f"US Trade: {format_trade_value(us_trade)}<br>"
                                      f"China Trade: {format_trade_value(china_trade)}")
            hover_texts.append(f"<b>{country_display_name}</b><br>Year: {initial_year_to_display}<br>Type: {flow_key}<br>{trade_details_text}")

        is_visible = (flow_key == initial_active_flow_key)

        fig.add_trace(
            go.Choropleth(
                name=flow_key,
                geojson=geojson_data,
                locations=locations,
                z=z_values,
                featureidkey="properties.name",
                colorscale=[[0, config.HEX_COLOR_US_DOMINANT], 
                            [0.5, config.HEX_COLOR_EQUAL_TRADE], 
                            [1, config.HEX_COLOR_CHINA_DOMINANT]],
                zmin=0, zmax=1,
                hovertext=hover_texts,
                hovertemplate="%{hovertext}<extra></extra>",
                marker_line_color=config.COLOR_BORDER,
                marker_line_width=0.3,
                showscale=False,
                visible=is_visible
            )
        )

    # --- Buat Frames untuk Animasi Tahun ---
    frames = []
    for year in available_years:
        frame_data_list = [] 
        for flow_key in flow_keys_ordered:
            df_flow_specific = df_dominance_all_flows[df_dominance_all_flows['Trade_Flow_Type'] == flow_key]
            df_year_flow_filtered = df_flow_specific[df_flow_specific['Year'] == year]
            
            ratio_dict_year = pd.Series(df_year_flow_filtered.Ratio.values, index=df_year_flow_filtered.Partner).to_dict()
            us_trade_dict_year = pd.Series(df_year_flow_filtered.US_Trade.values, index=df_year_flow_filtered.Partner).to_dict()
            china_trade_dict_year = pd.Series(df_year_flow_filtered.China_Trade.values, index=df_year_flow_filtered.Partner).to_dict()
            
            current_z_values, current_hover_texts = [], []
            for country_name_geojson in map_countries_in_geojson:
                ratio = ratio_dict_year.get(country_name_geojson, np.nan)
                us_trade = us_trade_dict_year.get(country_name_geojson, 0)
                china_trade = china_trade_dict_year.get(country_name_geojson, 0)
                current_z_values.append(ratio)
                
                country_display_name = country_name_geojson
                trade_details_text = ""
                if pd.isna(ratio): trade_details_text = "Data: Not available"
                elif country_name_geojson == "United States of America": trade_details_text = f"US Trade: {format_trade_value(us_trade)}<br>China Trade: {format_trade_value(china_trade)}<br>(Dominant: US)"
                elif country_name_geojson == "China": trade_details_text = f"US Trade: {format_trade_value(us_trade)}<br>China Trade: {format_trade_value(china_trade)}<br>(Dominant: China)"
                else: trade_details_text = (f"US Trade: {format_trade_value(us_trade)}<br>"
                                          f"China Trade: {format_trade_value(china_trade)}")
                current_hover_texts.append(f"<b>{country_display_name}</b><br>Year: {year}<br>Type: {flow_key}<br>{trade_details_text}")
            
            frame_data_list.append(go.Choropleth(z=current_z_values, hovertext=current_hover_texts))

        frames.append(go.Frame(
            name=str(year),
            data=frame_data_list, 
        ))
    fig.frames = frames

    slider_steps = []
    for year_val in available_years:
        slider_steps.append(
            dict(label=str(year_val),
                 method="animate",
                 args=[[str(year_val)], 
                       {"frame": {"duration": 200, "redraw": True}, 
                        "mode": "immediate", 
                        "transition": {"duration": 100, "easing": "linear"}}])
        )

    # --- Geo Settings ---
    current_geo_settings = dict(
        showframe=False, showcoastlines=False,
        projection_type='miller',
        bgcolor='rgba(0,0,0,0)',
        landcolor=config.HEX_COLOR_NO_DATA,
        showocean=True, oceancolor=config.OCEAN_COLOR, lakecolor=config.OCEAN_COLOR,
        subunitcolor=config.COLOR_BORDER,
        lataxis_range=[-60, 90], 
        lonaxis_range=[-180, 180] 
    )
    if selected_continent != "World" and selected_continent in config.CONTINENT_BOUNDS:
        bounds = config.CONTINENT_BOUNDS[selected_continent]
        current_geo_settings['lataxis_range'] = [bounds['lat_min'], bounds['lat_max']]
        current_geo_settings['lonaxis_range'] = [bounds['lon_min'], bounds['lon_max']]

    # --- Updatemenus untuk Tipe Perdagangan ---
    updatemenu_buttons = []
    num_traces = len(flow_keys_ordered)

    for i, display_name in enumerate(config.TRADE_FLOW_OPTIONS_DISPLAY):
        visibility_array = [False] * num_traces
        visibility_array[i] = True
        
        # Untuk setiap tombol, kita akan atur style dasarnya
        # Plotly akan mencoba mencerahkan 'bgcolor' saat hover dan untuk tombol 'active'
        # Kita set 'bordercolor' agar tidak terlihat
        button_style = dict(
            label=display_name,
            method="restyle",
            args=[{"visible": visibility_array}, list(range(num_traces))],
            # Tidak ada styling eksplisit di sini, akan diambil dari updatemenu dict
        )
        updatemenu_buttons.append(button_style)
    
    initial_active_button_index = flow_keys_ordered.index(initial_active_flow_key) if initial_active_flow_key in flow_keys_ordered else 0


    fig.update_layout(
        dragmode=False,
        geo=current_geo_settings,
        sliders=[dict(
            active=available_years.index(initial_year_to_display) if initial_year_to_display in available_years else 0,
            currentvalue={
                "font": {"size": 28, "color": config.TEXT_COLOR_PRIMARY, "family": '"Helvetica Neue", Helvetica, Arial, sans-serif'},
                "prefix": "",
                "visible": True,
                "xanchor": "left",
            },
            x=0, 
            y=0.10, 
            xanchor="left", 
            yanchor="top",
            pad={"t": 20, "b": 10, "l": 20, "r": 20},
            activebgcolor=config.TEXT_COLOR_TERTIARY, # Warna saat slider aktif/ditarik
            tickcolor=config.TEXT_COLOR_PRIMARY,
            bgcolor=config.TEXT_COLOR_PRIMARY,
            bordercolor=config.PAGE_BG_COLOR, # Atau 'rgba(0,0,0,0)'
            borderwidth=0, # Atau 1 jika bordercolor=config.PAGE_BG_COLOR
            tickwidth=1,
            font=dict(color=config.TEXT_COLOR_PRIMARY, size=12),
            steps=slider_steps,
        )],
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=updatemenu_buttons,
                active=initial_active_button_index,
                x=0.01,
                xanchor="left",
                y=1.02,
                yanchor="bottom",
                
                # Biarkan Plotly menangani bgcolor saat hover/active.
                # Jika PAGE_BG_COLOR gelap, Plotly akan mencerahkannya (bisa jadi putih/terang).
                bgcolor=config.PAGE_BG_COLOR, 
                
                bordercolor=config.PAGE_BG_COLOR,    # Border tidak terlihat
                borderwidth=0,                       # Tidak ada ketebalan border visual
                
                # Teks berwarna PUTIH
                font=dict(color=config.TEXT_COLOR_PRIMARY, size=12), 
                
                pad={"r": 7, "l": 7, "t": 4, "b": 4},
                showactive=True# Biarkan Plotly menandai tombol aktif (kemungkinan dengan fill terang)
            ),
            dict( # Tombol Play/Pause
                type="buttons",
                direction="right",
                buttons=[
                    dict(label="❮", method="animate", args=[[None], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}, "args2": ["prev"]}]),
                    dict(label="▶", method="animate", args=[None, {"frame": {"duration": 800, "redraw": True}, "fromcurrent": True, "transition": {"duration": 400, "easing": "linear"}, "mode": "immediate"}]),
                    dict(label="⏸", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                    dict(label="❯", method="animate", args=[[None], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}, "args2": ["next"]}]),
                ],
                x=0.12, 
                y=-0.10, 
                xanchor="left", 
                yanchor="top", 
                pad={"t": 18, "r": 5, "l": 5}, 
                showactive=False, # Tidak perlu menonjolkan tombol play/pause yang aktif
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)',
                font=dict(size=20, color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif')
        )],
        height=750,
        margin={"r":0, "t":0, "l":0, "b":120},
        paper_bgcolor=config.PAGE_BG_COLOR,
        plot_bgcolor=config.PAGE_BG_COLOR,
        font=dict(color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif'),
        annotations=[
            dict(
                x=0.01, y=0.05,
                xref='paper', yref='paper',
                showarrow=False,
                align='left',
                text=(
                    "<span style='font-size:13px; color:#A0A0A0; font-weight:500;'>Who is the larger trading partner?</span>   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_US_DOMINANT};'>■</span> US   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_EQUAL_TRADE};'>■</span> Equal   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_CHINA_DOMINANT};'>■</span> China   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_NO_DATA};'>■</span> No data"
                ),
            )
        ],
    )
    return fig