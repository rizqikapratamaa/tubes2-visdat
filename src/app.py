# streamlit_app/app.py
import streamlit as st
import config 
import styles
import data_loader # Untuk peta
import map_plotter # Untuk peta
import line_chart_plotter # Impor modul baru kita

def main():
    st.set_page_config(layout=config.LAYOUT, page_title=config.PAGE_TITLE)
    styles.load_global_css()

    # --- INISIALISASI SESSION STATE UNTUK PETA ---
    if 'active_trade_flow_display' not in st.session_state:
        st.session_state.active_trade_flow_display = config.DEFAULT_TRADE_FLOW_DISPLAY
    
    df_dominance, available_years_init = data_loader.load_trade_data()
    if df_dominance.empty or not available_years_init:
        st.error("Tidak dapat memuat data perdagangan awal untuk peta.")
        # Pertimbangkan apakah akan st.stop() atau hanya menampilkan pesan error peta
    
    default_active_year = max(available_years_init) if available_years_init else config.YEARS_RANGE[-1]
    if 'active_year' not in st.session_state:
        st.session_state.active_year = default_active_year
    
    # --- DATA UNTUK PETA ---
    initial_active_flow_key = config.TRADE_FLOW_MAP.get(
        st.session_state.active_trade_flow_display,
        config.TRADE_FLOW_MAP[config.DEFAULT_TRADE_FLOW_DISPLAY]
    )
    geojson_data = data_loader.get_geojson_data()

    min_year_data_map = min(available_years_init) if available_years_init else config.YEARS_RANGE[0]
    max_year_data_map = max(available_years_init) if available_years_init else config.YEARS_RANGE[-1]

    if st.session_state.active_year not in available_years_init and available_years_init:
        st.session_state.active_year = max_year_data_map
    
    # --- TAMPILKAN PETA CHOROPLETH ---
    st.markdown("## Global Trade Dominance: US vs China", unsafe_allow_html=True) # Judul untuk peta
    if not df_dominance.empty and geojson_data and available_years_init:
        fig_map = map_plotter.create_choropleth_map(
            df_dominance,
            available_years_init, 
            geojson_data,
            min_year_data_map,
            max_year_data_map,
            current_selected_year=st.session_state.active_year,
            initial_active_flow_key=initial_active_flow_key,
            selected_continent="World"
        )
        st.plotly_chart(fig_map, use_container_width=True, config=config.PLOTLY_CONFIG)
    else:
        st.warning("Data untuk peta tidak lengkap, peta tidak dapat ditampilkan.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True) # Pemisah

    # --- DATA DAN TAMPILKAN LINE CHART ---
    st.markdown("## US vs China: Export & Import Trends", unsafe_allow_html=True) # Judul untuk line chart
    
    df_line_chart_data = line_chart_plotter.load_line_chart_data()
    
    if not df_line_chart_data.empty:
        fig_line_chart = line_chart_plotter.create_trade_trend_line_chart(df_line_chart_data)
        st.plotly_chart(fig_line_chart, use_container_width=True, config=config.PLOTLY_CONFIG)
    else:
        st.warning("Data untuk line chart tren perdagangan tidak dapat dimuat.")

if __name__ == "__main__":
    main()