import streamlit as st
import pandas as pd
from components import layout, map_plotter, line_chart_plotter, table_plotter
import config
import styles
import data_loader

def main():
    st.set_page_config(layout=config.LAYOUT, page_title=config.PAGE_TITLE)
    styles.load_global_css()

    layout.display_title()

    if 'active_trade_flow_display_map' not in st.session_state:
        st.session_state.active_trade_flow_display_map = config.DEFAULT_TRADE_FLOW_DISPLAY

    initial_years_for_map_default = config.YEARS_RANGE
    temp_df_dom, temp_avail_years = data_loader.load_trade_data()
    if temp_avail_years:
        initial_years_for_map_default = temp_avail_years

    if 'active_year_map' not in st.session_state:
        st.session_state.active_year_map = max(initial_years_for_map_default) if initial_years_for_map_default else config.YEARS_RANGE[-1]

    if 'selected_year_table' not in st.session_state:
        st.session_state.selected_year_table = config.DEFAULT_TABLE_YEAR
    if 'selected_continent_table' not in st.session_state:
        st.session_state.selected_continent_table = config.DEFAULT_TABLE_CONTINENT
    if 'selected_trade_flow_table' not in st.session_state:
        st.session_state.selected_trade_flow_table = config.DEFAULT_TRADE_FLOW_DISPLAY
    if 'sort_order_table' not in st.session_state:
        st.session_state.sort_order_table = config.DEFAULT_TABLE_SORT_ORDER
    if 'selected_view_line_chart' not in st.session_state:
        st.session_state.selected_view_line_chart = "Exports"

    df_dominance_all, available_years_all = data_loader.load_trade_data()
    if df_dominance_all.empty or not available_years_all:
        st.error("Failed to load main trade data. The application cannot proceed.")
        st.stop()
    df_table_prepared = data_loader.prepare_table_data(df_dominance_all)
    if df_table_prepared.empty and not df_dominance_all.empty:
        st.error("Failed to prepare data for the table.")

    st.markdown(
        "<h3 style='text-align: center; color: #E2E8F0; padding-top: 50px;'>🌍 Global Trade Dominance Map</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='color: #A0AEC0; font-size: 14px; margin-bottom: 10px; text-align: center;'>
            This choropleth map shows which countries are dominated by the US or China in terms of trade volume 
            (Exports or Imports) for the selected year. Use the slider to explore changes over time.
        </p>
        """,
        unsafe_allow_html=True
    )

    col_empty, col_map_filter_container, _ = st.columns([0.05, 0.15, 0.80])
    with col_map_filter_container:
        map_trade_flow_display_options = list(config.TRADE_FLOW_MAP.keys())
        selected_trade_flow_display_map_val = st.selectbox(
            "Trade Type:",
            options=map_trade_flow_display_options,
            index=map_trade_flow_display_options.index(st.session_state.active_trade_flow_display_map),
            key="map_trade_flow_filter"
        )
        st.session_state.active_trade_flow_display_map = selected_trade_flow_display_map_val

    current_selected_flow_key_map = config.TRADE_FLOW_MAP.get(
        st.session_state.active_trade_flow_display_map,
        config.TRADE_FLOW_MAP[config.DEFAULT_TRADE_FLOW_DISPLAY]
    )

    geojson_data = data_loader.get_geojson_data()
    if not df_dominance_all.empty and geojson_data and available_years_all:
        current_map_year = st.session_state.active_year_map
        if current_map_year not in available_years_all:
            current_map_year = max(available_years_all) if available_years_all else config.YEARS_RANGE[-1]
            st.session_state.active_year_map = current_map_year

        fig_map = map_plotter.create_choropleth_map(
            df_dominance_all, available_years_all, geojson_data,
            min(available_years_all), max(available_years_all),
            current_selected_year=current_map_year,
            selected_flow_key=current_selected_flow_key_map,
            selected_continent="World"
        )
        st.plotly_chart(fig_map, use_container_width=True, config=config.PLOTLY_CONFIG)
    else:
        st.warning("Data for the map is incomplete, the map cannot be displayed.")

    st.markdown("<br><hr style='margin-top: 0.5rem; margin-bottom: 0.5rem;'><br>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align: center; color: #E2E8F0; padding-top: 10px;'>📈 US vs China: Export & Import Trends</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='color: #A0AEC0; font-size: 14px; margin-bottom: 10px; text-align: center;'>
            Compare the export and import trends of the US and China over time. 
            Select 'Exports' or 'Imports' to see how their trade values have evolved.
        </p>
        """,
        unsafe_allow_html=True
    )
    col_empty, col_lc_filter_container, _ = st.columns([0.05, 0.1, 0.85])
    with col_lc_filter_container:
        line_chart_view_options = ["Exports", "Imports"]
        selected_view_lc_val = st.selectbox(
            "Trade Type:",
            options=line_chart_view_options,
            index=line_chart_view_options.index(st.session_state.selected_view_line_chart),
            key="line_chart_view_filter"
        )
        st.session_state.selected_view_line_chart = selected_view_lc_val

    df_line_chart_data = line_chart_plotter.load_line_chart_data()
    if not df_line_chart_data.empty:
        fig_line_chart = line_chart_plotter.create_trade_trend_line_chart(
            df_line_chart_data,
            selected_view=st.session_state.selected_view_line_chart
        )
        st.plotly_chart(fig_line_chart, use_container_width=True, config=config.PLOTLY_CONFIG)
    else:
        st.warning("Data for the trade trend line chart cannot be loaded.")

    st.markdown("<br><hr style='margin-top: 0.5rem; margin-bottom: 0.5rem;'><br>", unsafe_allow_html=True)

    st.markdown(
        f"<h3 style='text-align: center; color: #E2E8F0; padding-top: 10px;'>📊 Top {config.TOP_N_COUNTRIES} Trading Partners Analysis</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='color: #A0AEC0; font-size: 14px; margin-bottom: 10px; text-align: center; padding-bottom: 50px;'>
            This table highlights the top trading partners for the selected trade type, year, and continent, 
            showing the trade volumes with the US and China, along with their combined impact.
        </p>
        """,
        unsafe_allow_html=True
    )

    if df_table_prepared.empty:
        st.warning("Data for table analysis is not available.")
    else:
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
        with col_filter1:
            current_table_year_default = st.session_state.selected_year_table
            if current_table_year_default not in available_years_all:
                current_table_year_default = config.DEFAULT_TABLE_YEAR if config.DEFAULT_TABLE_YEAR in available_years_all else available_years_all[0]
            selected_year_table_val = st.selectbox("Year:", options=available_years_all, index=available_years_all.index(current_table_year_default), key="table_year_filter")
            st.session_state.selected_year_table = selected_year_table_val
        with col_filter2:
            continent_display_names = list(config.CONTINENT_OPTIONS.keys())
            selected_continent_display_table = st.selectbox("Continent:", options=continent_display_names, index=continent_display_names.index(st.session_state.selected_continent_table), key="table_continent_filter")
            st.session_state.selected_continent_table = selected_continent_display_table
        with col_filter3:
            trade_flow_display_options_table = list(config.TRADE_FLOW_MAP.keys())
            selected_trade_flow_display_table = st.selectbox("Trade Type:", options=trade_flow_display_options_table, index=trade_flow_display_options_table.index(st.session_state.selected_trade_flow_table), key="table_trade_flow_filter")
            st.session_state.selected_trade_flow_table = selected_trade_flow_display_table
        with col_filter4:
            selected_sort_order_table = st.selectbox("Sort (Total Trade):", options=config.SORT_ORDER_OPTIONS, index=config.SORT_ORDER_OPTIONS.index(st.session_state.sort_order_table), key="table_sort_order_filter")
            st.session_state.sort_order_table = selected_sort_order_table

        st.markdown("<div style='margin-bottom: 1.0rem;'></div>", unsafe_allow_html=True)

        current_year = st.session_state.selected_year_table
        current_continent_display = st.session_state.selected_continent_table
        current_trade_flow_display = st.session_state.selected_trade_flow_table
        current_sort_order = st.session_state.sort_order_table

        df_year_filtered = df_table_prepared[df_table_prepared['Year'] == current_year]
        current_trade_flow_key_table = config.TRADE_FLOW_MAP[current_trade_flow_display]
        df_flow_filtered = df_year_filtered[df_year_filtered['Trade_Flow_Type'] == current_trade_flow_key_table]

        if current_continent_display != "World":
            current_continent_code = config.CONTINENT_OPTIONS[current_continent_display]
            if 'Continent_Code' in df_flow_filtered.columns:
                 df_continent_filtered = df_flow_filtered[df_flow_filtered['Continent_Code'] == current_continent_code]
            else:
                st.warning("Column 'Continent_Code' not found for continent filtering.")
                df_continent_filtered = df_flow_filtered
        else:
            df_continent_filtered = df_flow_filtered
            if 'Continent_Code' in df_continent_filtered.columns:
                df_continent_filtered = df_continent_filtered[~df_continent_filtered['Continent_Code'].isin(["Unknown", "Group", ""])]

        if 'Total_US_China_Trade' in df_continent_filtered.columns:
            df_filtered_non_zero = df_continent_filtered[df_continent_filtered['Total_US_China_Trade'] > 0]
            df_to_sort = df_filtered_non_zero if not df_filtered_non_zero.empty else df_continent_filtered
            ascending_order = (current_sort_order == "Ascending")
            df_sorted = df_to_sort.sort_values(by='Total_US_China_Trade', ascending=ascending_order)
        else:
            st.warning("'Total_US_China_Trade' column is not found for table sorting.")
            df_sorted = df_continent_filtered

        df_top_n_raw = df_sorted.head(config.TOP_N_COUNTRIES)

        if df_top_n_raw.empty:
            st.info(f"There's no {current_trade_flow_display} to display in {current_year} (Continent: {current_continent_display}).")
        else:
            df_display_table, pie_figures = table_plotter.generate_trade_table_data_and_pies(df_top_n_raw)

            continent_title_part_display = f"Continent: {current_continent_display}" if current_continent_display != "World" else "Worldwide"
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 5px;">
                <h4 style="color: {config.TEXT_COLOR_PRIMARY}; margin-bottom: 0px;">Top {min(config.TOP_N_COUNTRIES, len(df_display_table))} Trading Partners</h4>
                <p style="color: {config.TEXT_COLOR_SECONDARY}; font-size: 12px; margin-top:0; margin-bottom: 15px;">
                    Type: {current_trade_flow_display} | Year: {current_year} | {continent_title_part_display}
                </p>
            </div>
            """, unsafe_allow_html=True)

            header_cols = st.columns([0.5, 2, 1.5, 1.5, 1.5, 1])
            headers = ["Rank", "Country", "US Trade", "China Trade", "Total (US+China)", "Proportion"]
            for col, header in zip(header_cols, headers):
                col.markdown(f"<p style='color: {config.TEXT_COLOR_PRIMARY}; font-weight: bold; font-size: 0.9em;'>{header}</p>", unsafe_allow_html=True)

            st.markdown("<hr style='margin-top: 0.1rem; margin-bottom: 0.5rem; border-color: #4A5568;'>", unsafe_allow_html=True)

            for i in range(len(df_display_table)):
                row_data = df_display_table.iloc[i]
                pie_fig_to_display = pie_figures[i]

                row_cols = st.columns([0.5, 2, 1.5, 1.5, 1.5, 1])

                with row_cols[0]:
                    st.markdown(f"<span style='color: {config.TEXT_COLOR_SECONDARY}; font-size: 0.9em;'>{row_data['Rank']}</span>", unsafe_allow_html=True)
                with row_cols[1]:
                    st.markdown(f"<span style='color: {config.TEXT_COLOR_SECONDARY}; font-size: 0.9em;'>{row_data['Country']}</span>", unsafe_allow_html=True)
                with row_cols[2]:
                    st.markdown(f"<span style='color: {config.TEXT_COLOR_SECONDARY}; font-size: 0.9em;'>{row_data['US Trade']}</span>", unsafe_allow_html=True)
                with row_cols[3]:
                    st.markdown(f"<span style='color: {config.TEXT_COLOR_SECONDARY}; font-size: 0.9em;'>{row_data['China Trade']}</span>", unsafe_allow_html=True)
                with row_cols[4]:
                    st.markdown(f"<span style='color: {config.TEXT_COLOR_SECONDARY}; font-size: 0.9em;'>{row_data['Total (US+China)']}</span>", unsafe_allow_html=True)
                with row_cols[5]:
                    if pie_fig_to_display:
                        st.plotly_chart(pie_fig_to_display, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.markdown(f"<div style='width:60px; height:60px; border-radius:50%; background-color:{config.HEX_COLOR_NO_DATA}; display:flex; align-items:center; justify-content:center; font-size:10px; color:white; margin:auto;'>N/A</div>", unsafe_allow_html=True)

                if i < len(df_display_table) - 1:
                    st.markdown("<hr style='margin-top: 0.2rem; margin-bottom: 0.2rem; border-style: dashed; border-color: #4A5568;'>", unsafe_allow_html=True)

    st.markdown("<br><hr style='margin-top: 0.5rem; margin-bottom: 0.5rem;'><br>", unsafe_allow_html=True)

    layout.display_key_findings()
    layout.display_authors()
if __name__ == "__main__":
    main()