# streamlit_app/app.py
import streamlit as st
import config 
import styles
import data_loader
import map_plotter

# Fungsi callback untuk tombol tipe perdagangan TIDAK DIPERLUKAN LAGI UNTUK MAP
# def set_active_trade_flow(flow_name):
#     st.session_state.active_trade_flow_display = flow_name
    # Tidak perlu mengubah tahun di sini, biarkan slider yang menanganinya

def main():
    st.set_page_config(layout=config.LAYOUT, page_title=config.PAGE_TITLE)
    styles.load_global_css() # Pastikan CSS tidak mengganggu layout Plotly

    # --- INISIALISASI SESSION STATE ---
    if 'active_trade_flow_display' not in st.session_state:
        st.session_state.active_trade_flow_display = config.DEFAULT_TRADE_FLOW_DISPLAY
    
    df_dominance, available_years_init = data_loader.load_trade_data()
    if df_dominance.empty or not available_years_init:
        st.error("Tidak dapat memuat data perdagangan awal.")
        st.stop()
    
    default_active_year = max(available_years_init)
    if 'active_year' not in st.session_state:
        st.session_state.active_year = default_active_year
    
    # --- KONTROL UI (HAPUS TOMBOL STREAMLIT UNTUK TIPE TRADE) ---
    # st.markdown(""" ... CSS untuk top-controls-container ... """, unsafe_allow_html=True)
    # st.markdown('<div class="top-controls-container">', unsafe_allow_html=True)

    # Bagian Kiri: Pilihan Tipe Perdagangan (DIHAPUS, DIGANTI Plotly updatemenu)
    # ... (kode st.button atau st.radio dihapus) ...

    # Bagian Kanan: Filter Benua (BISA DIPERTAHANKAN JIKA MAU, TAPI SEDERHANAKAN DULU)
    # Untuk saat ini, kita fokus pada trade flow. Filter benua bisa ditambahkan kembali nanti.
    # Jika ingin mempertahankan, pastikan tidak menyebabkan rerun yang tidak perlu.
    # selected_continent_code = "World" # Default
    # ... (kode selectbox benua, jika ada, perlu ditinjau agar tidak rerun peta) ...

    # st.markdown('</div>', unsafe_allow_html=True) # Tutup top-controls-container
    
    # Dapatkan kunci data untuk flow yang aktif secara default (dari config)
    initial_active_flow_key = config.TRADE_FLOW_MAP.get(
        st.session_state.active_trade_flow_display, # Ini display name
        config.TRADE_FLOW_MAP[config.DEFAULT_TRADE_FLOW_DISPLAY] # Fallback ke default key
    )

    # --- Data Loading (df_dominance sudah dimuat di atas) ---
    geojson_data = data_loader.get_geojson_data()
    if geojson_data is None:
        st.error("Data GeoJSON tidak dapat dimuat.")
        st.stop()

    min_year_data = min(available_years_init)
    max_year_data = max(available_years_init)

    if st.session_state.active_year not in available_years_init:
        st.session_state.active_year = max_year_data
    
    # --- Generate and Display Plotly Figure ---
    # Kirim seluruh df_dominance, dan flow awal yang aktif
    fig = map_plotter.create_choropleth_map(
        df_dominance,  # Data semua flow
        available_years_init, 
        geojson_data,
        min_year_data,
        max_year_data,
        current_selected_year=st.session_state.active_year,
        initial_active_flow_key=initial_active_flow_key, # Kunci data seperti "Total", "Import"
        selected_continent="World" # Atau dari filter benua jika ada
    )
    
    st.plotly_chart(fig, use_container_width=True, config=config.PLOTLY_CONFIG)

    # Slider Streamlit untuk tahun mungkin tidak diperlukan lagi jika slider Plotly sudah cukup.
    # Jika tetap mau ada slider Streamlit yang mengontrol tahun di Plotly:
    # selected_year_from_st_slider = st.slider(
    #     "Select Year (Streamlit Control):", 
    #     min_value=min_year_data, 
    #     max_value=max_year_data, 
    #     value=st.session_state.active_year,
    #     key="year_slider_st_control"
    # )
    # if selected_year_from_st_slider != st.session_state.active_year:
    #     st.session_state.active_year = selected_year_from_st_slider
    #     # Ini akan menyebabkan rerun dan peta diregenerate dengan tahun baru dari slider Streamlit
    #     # Slider Plotly akan diset ulang ke tahun ini.
    #     st.experimental_rerun() 


if __name__ == "__main__":
    main()