# streamlit_app/styles.py
import streamlit as st
import config

def load_global_css():
    st.markdown(
        f"""
        <style>
        /* --- Global Styles --- */
        html, body, [class*="st-"], .main {{
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: {config.PAGE_BG_COLOR} !important;
        }}
        
        .main {{ 
            color: {config.TEXT_COLOR_PRIMARY}; 
        }}
        
        h1, h2, h3, h4, h5, h6 {{ 
            color: {config.TEXT_COLOR_PRIMARY}; 
            font-weight: bold; 
        }}
        
        p, li, label, .stMarkdown, .stMarkdown p {{ 
            color: {config.TEXT_COLOR_SECONDARY}; 
            font-size: 14px; 
            line-height: 1.6; 
        }}
        
        hr {{ 
            border-top: 1px solid #444; 
        }}

        /* --- App Specific Utility Classes (JIKA MASIH DIGUNAKAN) --- */
        /* Jika .map-controls, .year-display-container, .play-pause-buttons, etc. */
        /* adalah untuk elemen Streamlit kustom, biarkan. Jika tidak, bisa dihapus. */
        /* Untuk sekarang, saya akan biarkan yang tampaknya tidak terkait langsung dengan Plotly updatemenus */

        .map-controls {{ 
            padding: 10px 20px; 
            margin-bottom: -10px; 
            position: relative; 
            z-index: 10; 
        }}
        
        .year-display-container {{ 
            text-align: left; 
            margin-bottom: 5px; 
        }}
        
        /* Tombol Play/Pause Streamlit (jika ada, bukan yang Plotly) */
        .play-pause-buttons button {{
            background-color: transparent !important; 
            color: {config.TEXT_COLOR_PRIMARY} !important;
            border: none !important; 
            padding: 5px !important;
            font-size: 24px !important; 
            font-weight: bold;
            margin-right: 10px;
        }}
        .play-pause-buttons button:hover {{ 
            color: {config.TEXT_COLOR_SECONDARY} !important; 
        }}
        
        .legend-container {{ 
            margin-top: 5px; 
        }}
        .legend-item {{ 
            display: flex; 
            align-items: center; 
            margin-right: 15px; 
            font-size: 12px; 
            color: {config.TEXT_COLOR_SECONDARY}; 
        }}
        .legend-swatch {{ 
            width: 30px; 
            height: 8px; 
            margin-right: 5px; 
            border: 1px solid rgba(255,255,255,0.3); 
        }}
        
        .source-text {{ 
            font-size: 11px; 
            color: {config.TEXT_COLOR_TERTIARY}; 
            text-align: right; 
        }}
        .source-text a {{ 
            color: {config.TEXT_COLOR_TERTIARY}; 
            text-decoration: underline; 
        }}
        .source-text a:hover {{ 
            color: {config.TEXT_COLOR_SECONDARY}; 
        }}
        
        .control-container {{ 
            display: flex; 
            flex-direction: column; 
            align-items: flex-start; 
            margin-top: 10px; 
        }}
        .slider-container {{ 
            width: 100%; 
            margin-top: 10px; 
        }}

        /* --- Plotly Specific Styles --- */
        /* HAPUS ATAU KOMENTARI ATURAN YANG MUNGKIN BERKONFLIK DENGAN UPDATEMENUS */
        
        /* Ini untuk slider Plotly, seharusnya aman */
        .plotly .slider {{
            /* background-color: #333333 !important; */ /* Biarkan Plotly yang atur dari layout fig */
            /* border-color: #444444 !important; */ /* Biarkan Plotly yang atur dari layout fig */
        }}
        .plotly .slider .handle {{
             /* background-color: #555555 !important; */ /* Biarkan Plotly yang atur */
        }}
        .plotly .slider text {{
            /* fill: {config.TEXT_COLOR_PRIMARY} !important; */ /* Biarkan Plotly yang atur */
        }}
        
        /* Ini untuk tombol modebar Plotly (zoom, pan, etc.), seharusnya aman */
        /* Jika Anda tidak menampilkan modebar, ini tidak relevan */
        .plotly .modebar-btn svg {{
            /* fill: {config.TEXT_COLOR_PRIMARY} !important; */ /* Biarkan Plotly yang atur */
        }}

        /* PERHATIKAN BAGIAN INI: .plotly .updatemenu-button */
        /* Jika kode di map_plotter.py sudah mengatur font color, ini mungkin redundan atau konflik */
        /* Mari kita coba hapus sementara untuk melihat efeknya pada fill hover */
        /*
        .plotly .updatemenu-button text {{
            fill: {config.TEXT_COLOR_PRIMARY} !important; 
            font-size: 20px !important; 
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        }}
        */

        /* --- Nav Button Styles (UNTUK TOMBOL STREAMLIT KUSTOM, BUKAN PLOTLY UPDATEMENU) --- */
        /* Jika .nav-button, .nav-button:hover, .nav-button.active BUKAN untuk tombol Plotly updatemenu, */
        /* maka biarkan. Jika Anda mencurigainya memengaruhi Plotly, komentari juga. */
        /* Untuk sekarang, saya asumsikan ini untuk tombol Streamlit lain. */
        .nav-button-container {{
            display: flex;
            flex-direction: row;
            gap: 0px;
            margin-bottom: 10px;
            border: 1px solid #4A5568;
            border-radius: 0.375rem;
            overflow: hidden;
        }}

        .nav-button {{
            padding: 8px 16px;
            color: {config.TEXT_COLOR_SECONDARY};
            background-color: transparent;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s ease, color 0.2s ease;
            border-right: 1px solid #4A5568;
        }}
        
        .nav-button:last-child {{
            border-right: none;
        }}

        .nav-button:hover {{
            background-color: #2D3748; 
            color: {config.TEXT_COLOR_PRIMARY};
        }}

        .nav-button.active {{
            background-color: {config.COLOR_US_REF}; 
            color: {config.TEXT_COLOR_PRIMARY}; 
            font-weight: 700; 
            border-right: 1px solid {config.COLOR_US_REF}; 
        }}
        
        .nav-button.active:last-child {{
            border-right: none;
        }}

        .nav-button a {{
            text-decoration: none !important;
            color: inherit !important; 
        }}

        /* Hilangkan margin dan padding default untuk elemen utama */
        .main > .block-container {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        
        }}
        /* Target selectbox untuk map filter */
        div[data-testid="stSelectbox"][key="map_trade_flow_filter"] {{
            max-width: 200px;
        }}
        /* Gaya lain yang sudah ada */
        body {{
            background-color: #1A202C;
            color: #E2E8F0;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )