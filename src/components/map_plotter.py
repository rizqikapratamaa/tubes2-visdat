import plotly.graph_objects as go
import pandas as pd
import numpy as np
import config
from data_loader import format_trade_value

def create_choropleth_map(df_dominance_all_flows, available_years, geojson_data,
                          min_year, max_year, current_selected_year,
                          selected_flow_key,
                          selected_continent="World"):

    if df_dominance_all_flows.empty or not available_years or geojson_data is None:
        return go.Figure()

    map_countries_in_geojson = [feature['properties']['name'] for feature in geojson_data['features']]
    fig = go.Figure()
    flow_keys_ordered = [config.TRADE_FLOW_MAP[display_name] for display_name in config.TRADE_FLOW_OPTIONS_DISPLAY]

    initial_year_to_display = current_selected_year
    if initial_year_to_display not in available_years:
        initial_year_to_display = max(available_years) if available_years else min_year

    for i, flow_key_trace in enumerate(flow_keys_ordered):
        df_flow_specific = df_dominance_all_flows[df_dominance_all_flows['Trade_Flow_Type'] == flow_key_trace]
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

            flow_display_name_trace = [dn for dn, fk in config.TRADE_FLOW_MAP.items() if fk == flow_key_trace][0]
            hover_texts.append(f"<b>{country_display_name}</b><br>Year: {initial_year_to_display}<br>Type: {flow_display_name_trace}<br>{trade_details_text}")

        is_visible = (flow_key_trace == selected_flow_key)

        fig.add_trace(
            go.Choropleth(
                name=flow_key_trace,
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

    frames = []
    for year in available_years:
        frame_data_list = []
        for flow_key_trace_frame in flow_keys_ordered: # Iterasi untuk setiap tipe flow dalam frame
            df_flow_specific = df_dominance_all_flows[df_dominance_all_flows['Trade_Flow_Type'] == flow_key_trace_frame]
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
                flow_display_name_frame = [dn for dn, fk in config.TRADE_FLOW_MAP.items() if fk == flow_key_trace_frame][0]
                current_hover_texts.append(f"<b>{country_display_name}</b><br>Year: {year}<br>Type: {flow_display_name_frame}<br>{trade_details_text}")

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

    fig.update_layout(
        dragmode="zoom",
        modebar=dict(
            add=['zoomInGeo', 'zoomOutGeo', 'resetGeo']
            # remove=['lasso2d', 'select2d'] # Contoh jika ingin menghapus tombol lain
            # active=True # Defaultnya True, modebar akan muncul jika ada tombol
        ),
        showlegend=True,
        geo=current_geo_settings,
        sliders=[dict(
            active=available_years.index(initial_year_to_display) if initial_year_to_display in available_years else 0,
            currentvalue={
                "font": {"size": 28, "color": config.TEXT_COLOR_PRIMARY, "family": '"Helvetica Neue", Helvetica, Arial, sans-serif'},
                "prefix": "",
                "visible": True,
                "xanchor": "left",
            },
            x=0.01,
            y=0.10, # Disesuaikan agar tidak terlalu bawah
            xanchor="left",
            yanchor="top",
            len=0.98,
            pad={"t": 20, "b": 10, "l": 20, "r":20},
            activebgcolor=config.TEXT_COLOR_TERTIARY,
            tickcolor=config.TEXT_COLOR_PRIMARY,
            bgcolor=config.TEXT_COLOR_PRIMARY,
            bordercolor=config.PAGE_BG_COLOR,
            borderwidth=0,
            tickwidth=1,
            font=dict(color=config.TEXT_COLOR_PRIMARY, size=12),
            steps=slider_steps,
        )],

        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=[
                    dict(label="▶", method="animate", args=[None, {"frame": {"duration": 800, "redraw": True}, "fromcurrent": True, "transition": {"duration": 400, "easing": "linear"}, "mode": "immediate"}]),
                    dict(label="⏸", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]),
                ],
                x=0.095,
                xanchor="center",
                y=-0.015,
                yanchor="bottom",
                pad={"t": 5, "r": 2, "l": 2, "b": 5},
                showactive=False,
                bordercolor='rgba(0,0,0,0)',
                font=dict(size=20, color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif')
            )
        ],
        height=750,
        margin={"r":10, "t":15, "l":10, "b":120},
        paper_bgcolor=config.PAGE_BG_COLOR,
        plot_bgcolor=config.PAGE_BG_COLOR,
        font=dict(color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif'),
        annotations=[
            dict(
                x=0.5,
                y=0.05,
                xref='paper',
                yref='paper',
                xanchor='center',
                showarrow=False,
                align='center',
                text=(
                    "<span style='font-size:13px; color:#A0A0A0; font-weight:500;'>Who is the larger trading partner?</span>   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_US_DOMINANT};'>■</span> US   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_EQUAL_TRADE};'>■</span> Equal   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_CHINA_DOMINANT};'>■</span> China   "
                    f"<span style='font-size:16px; color:{config.HEX_COLOR_NO_DATA};'>■</span> No data"
                ),
            )
        ],
    )
    return fig