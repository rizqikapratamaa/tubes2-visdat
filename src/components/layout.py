import streamlit as st
import config

def display_legend():
    st.markdown(f"""
    <div class="map-controls">
        <div class="legend-container" style="display: flex; flex-direction: row; align-items: center; margin-top: 5px;">
            <span style="font-size: 13px; color: #A0A0A0; margin-right: 10px; font-weight: 500;">Who is the larger trading partner?</span>
            <div class="legend-item"><div class="legend-swatch" style="background-color:{config.HEX_COLOR_US_DOMINANT};"></div>US</div>
            <div class="legend-item"><div class="legend-swatch" style="background-color:{config.HEX_COLOR_EQUAL_TRADE};"></div>Equal</div>
            <div class="legend-item"><div class="legend-swatch" style="background-color:{config.HEX_COLOR_CHINA_DOMINANT};"></div>China</div>
            <div class="legend-item"><div class="legend-swatch" style="background-color:{config.HEX_COLOR_NO_DATA};"></div>No data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_source_info(): # Contoh komponen lain jika diperlukan
    st.markdown(
        f"""
        <div class="source-text" style="margin-top:20px;">
            Data source: Your Data Source Name | 
            <a href="your_link_here" target="_blank">More info</a>
        </div>
        """, unsafe_allow_html=True
    )