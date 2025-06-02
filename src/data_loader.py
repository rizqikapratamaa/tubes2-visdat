# streamlit_app/data_loader.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
# from . import config # Jika menjalankan dari luar streamlit_app/
import config # Jika menjalankan streamlit run app.py dari dalam streamlit_app/

@st.cache_data
def load_trade_data():
    try:
        df = pd.read_csv(config.TRADE_DATA_PATH)
    except FileNotFoundError:
        st.error(f"File '{config.TRADE_DATA_PATH}' tidak ditemukan.")
        return pd.DataFrame(), []

    df_pivot = df.pivot_table(index=['Partner', 'Country'],
                              columns='Trade_Type',
                              values=[str(y) for y in config.YEARS_RANGE],
                              aggfunc='sum').fillna(0)
    
    new_cols = []
    for col_tuple in df_pivot.columns:
        # Kolom sekarang adalah tuple seperti ('2001', 'Export') atau ('2001', 'Import')
        # Atau jika aggfunc hanya 'sum' tanpa kolom Trade_Type, bisa jadi hanya tahun
        if isinstance(col_tuple, tuple) and len(col_tuple) == 2:
            year_val, trade_type_val = col_tuple
            new_cols.append(f"{year_val}_{trade_type_val}")
        else: # Fallback jika struktur kolom berbeda
            new_cols.append(str(col_tuple)) 
    df_pivot.columns = new_cols
    df_pivot = df_pivot.reset_index()

    years_range_str = [str(y) for y in config.YEARS_RANGE]
    
    # Hitung total perdagangan (ekspor + impor) untuk setiap tahun jika belum ada
    for year_col_num in years_range_str:
        export_col = f'{year_col_num}_Export'
        import_col = f'{year_col_num}_Import'
        
        # Pastikan kolom ada sebelum dijumlahkan
        df_pivot[export_col] = df_pivot.get(export_col, pd.Series(0, index=df_pivot.index))
        df_pivot[import_col] = df_pivot.get(import_col, pd.Series(0, index=df_pivot.index))
        
        df_pivot[f'{year_col_num}_Total'] = df_pivot[export_col] + df_pivot[import_col]

    trade_dominance_records = []
    
    # Tipe aliran perdagangan yang akan kita proses
    # Kunci adalah yang akan disimpan di DataFrame, nilai adalah suffix kolom di df_pivot
    trade_flow_processing_map = {
        "Total": "_Total",
        "Import": "_Import",
        "Export": "_Export"
    }

    for partner in df_pivot['Partner'].unique():
        df_partner_country = df_pivot[df_pivot['Partner'] == partner]
        for year_str in years_range_str:
            for flow_type_key, col_suffix in trade_flow_processing_map.items():
                data_col_name = f'{year_str}{col_suffix}' # e.g., '2001_Total', '2001_Import'
                
                us_trade_series = df_partner_country[df_partner_country['Country'] == 'United States'].get(data_col_name)
                china_trade_series = df_partner_country[df_partner_country['Country'] == 'China'].get(data_col_name)
                
                us_trade_val = us_trade_series.iloc[0] if us_trade_series is not None and not us_trade_series.empty else 0
                china_trade_val = china_trade_series.iloc[0] if china_trade_series is not None and not china_trade_series.empty else 0
                
                total_us_china_trade = us_trade_val + china_trade_val
                current_ratio = np.nan
                if total_us_china_trade > 0:
                    current_ratio = china_trade_val / total_us_china_trade
                
                trade_dominance_records.append({
                    'Partner': partner, 
                    'Year': int(year_str), 
                    'Trade_Flow_Type': flow_type_key, # Menyimpan jenis aliran
                    'Ratio': current_ratio,
                    'US_Trade': us_trade_val,
                    'China_Trade': china_trade_val
                })
            
    df_processed_dominance = pd.DataFrame(trade_dominance_records)

    name_mapping = {
        'Falkland Islands (Malvinas)': 'Falkland Islands', 'Equatorial Guinea, Republic of': 'Equatorial Guinea',
        'Brunei Darussalam': 'Brunei', 'Congo, Democratic Republic of the': 'Democratic Republic of the Congo',
        'Congo, Rep.': 'Republic of Congo', "Côte d'Ivoire": "Ivory Coast",
        'Iran, Islamic Rep. of': 'Iran', "Korea, Democratic People's Republic of": 'North Korea',
        'Korea, Republic of': 'South Korea', 'Lao PDR': 'Laos', 'Russian Federation': 'Russia',
        'Syrian Arab Republic': 'Syria', 'Taiwan, China': 'Taiwan',
        'Tanzania, United Republic of': 'Tanzania', 'Timor-Leste, Dem. Rep. of': 'Timor-Leste',
        'Venezuela, Rep. Bolivariana de': 'Venezuela', 'Viet Nam': 'Vietnam', 'Yemen, Rep. of': 'Yemen',
        'Egypt, Arab Rep.': 'Egypt', 'Gambia, The': 'Gambia', 'Kyrgyz Republic': 'Kyrgyzstan',
        'Slovak Republic': 'Slovakia', 'Micronesia, Fed. Sts. of': 'Federated States of Micronesia',
        'Bahamas, The': 'The Bahamas', 'Czech Republic': 'Czechia', 'Swaziland': 'Eswatini',
        'United States': 'United States of America', 'Uzbekistan, Republic of': 'Uzbekistan',
        'Kazakhstan, Republic of': 'Kazakhstan', 'Kyrgyz Republic' : 'Kyrgyzstan', 'Mauritania, Islamic Republic of': 'Mauritania',
        'Poland, Republic of': 'Poland', 'Estonia, Republic of': 'Estonia', 'Madagascar, Republic of' : 'Madagascar',
        'Belarus, Republic of' : 'Belarus', 'Netherlands, The' : 'Netherlands', 'Lithuania, Republic of': 'Lithuania', 
        'Latvia, Republic of' : 'Latvia', 'Türkiye, Republic of' : 'Turkey', 'Moldova, Republic of' : 'Moldova',
        'North Macedonia, Republic of': 'North Macedonia', 'Kosovo, Republic of' : 'Kosovo', 'Serbia, Republic of': 'Serbia',
        'Slovenia, Republic of': 'Slovenia', 'Croatia, Republic of' : 'Croatia', 'Czech Republic': 'Czechia', 'Timor-Leste, Democratic Republic of' : 'Timor-Leste',
        'Taiwan Province of China' : 'Taiwan', 'Egypt, Arab Republic of' : 'Egypt', "Lao People's Democratic Republic" : 'Laos', 'Armenia, Republic of' : 'Armenia',
        'Azerbaijan, Republic of' : 'Azerbaijan', 'Syrian Arab Republic' : 'Syria', 'West Bank and Gaza' : 'West Bank', 'Iran, Islamic Republic of' : 'Iran',
        'Afghanistan, Islamic Republic of' : 'Afghanistan', 'Tajikistan, Republic of' : 'Tajikistan', 'Yemen, Republic of' : 'Yemen', 'Ethiopia, The Federal Democratic Republic of' : 'Ethiopia', 
        'South Sudan, Republic of' : 'South Sudan', 'Mozambique, Republic of': 'Mozambique',
        'Lesotho, Kingdom of': 'Lesotho', 'Sub-Saharan Africa (SSA)' : 'Western Sahara'
    }
    df_processed_dominance['Partner'] = df_processed_dominance['Partner'].replace(name_mapping)
    
    # Rasio dominasi untuk US dan China sebagai Partner tetap 0 dan 1 untuk pewarnaan peta,
    # berlaku untuk semua Trade_Flow_Type. Nilai aktual US_Trade dan China_Trade akan tetap spesifik per flow.
    df_processed_dominance.loc[df_processed_dominance['Partner'] == 'United States of America', 'Ratio'] = 0.0
    df_processed_dominance.loc[df_processed_dominance['Partner'] == 'China', 'Ratio'] = 1.0
    
    available_years = sorted(df_processed_dominance['Year'].unique())
    if not available_years:
        st.warning("Tidak ada data tahun yang valid.")
        return pd.DataFrame(), []
        
    return df_processed_dominance, available_years

@st.cache_data
def get_geojson_data():
    try:
        response = requests.get(config.GEOJSON_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data GeoJSON: {e}")
        return None