import streamlit as st
import pandas as pd
import numpy as np
import requests
import config
import base64

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image file '{image_path}' is not found.")
        return ""
    
def format_trade_value(value):
    if pd.isna(value) or value == 0:
        return "$0"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}T"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}B"
    return f"${value:.2f}M"

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
        if isinstance(col_tuple, tuple) and len(col_tuple) == 2:
            year_val, trade_type_val = col_tuple
            new_cols.append(f"{year_val}_{trade_type_val}")
        else: 
            new_cols.append(str(col_tuple)) 
    df_pivot.columns = new_cols
    df_pivot = df_pivot.reset_index()

    years_range_str = [str(y) for y in config.YEARS_RANGE]
    
    for year_col_num in years_range_str:
        export_col = f'{year_col_num}_Export'
        import_col = f'{year_col_num}_Import'
        
        df_pivot[export_col] = df_pivot.get(export_col, pd.Series(0, index=df_pivot.index))
        df_pivot[import_col] = df_pivot.get(import_col, pd.Series(0, index=df_pivot.index))
        
        df_pivot[f'{year_col_num}_Total'] = df_pivot[export_col] + df_pivot[import_col]

    trade_dominance_records = []
    trade_flow_processing_map = {
        "Total": "_Total", "Import": "_Import", "Export": "_Export"
    }

    for partner_country_raw in df_pivot['Partner'].unique():
        df_partner_country_data = df_pivot[df_pivot['Partner'] == partner_country_raw]
        for year_str in years_range_str:
            for flow_type_key, col_suffix in trade_flow_processing_map.items():
                data_col_name = f'{year_str}{col_suffix}'
                
                us_trade_series = df_partner_country_data[df_partner_country_data['Country'] == 'United States'].get(data_col_name)
                china_trade_series = df_partner_country_data[df_partner_country_data['Country'] == 'China'].get(data_col_name)
                
                us_trade_val = us_trade_series.iloc[0] if us_trade_series is not None and not us_trade_series.empty else 0
                china_trade_val = china_trade_series.iloc[0] if china_trade_series is not None and not china_trade_series.empty else 0
                
                total_us_china_trade = us_trade_val + china_trade_val
                current_ratio = np.nan
                if total_us_china_trade > 0:
                    current_ratio = china_trade_val / total_us_china_trade
                
                trade_dominance_records.append({
                    'Partner_Raw': partner_country_raw,
                    'Year': int(year_str), 
                    'Trade_Flow_Type': flow_type_key,
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
        'Venezuela, Rep. Bolivariana de': 'Venezuela',
        'Viet Nam': 'Vietnam', 'Yemen, Rep. of': 'Yemen',
        'Egypt, Arab Rep.': 'Egypt', 'Gambia, The': 'Gambia', 'Kyrgyz Republic': 'Kyrgyzstan',
        'Slovak Republic': 'Slovakia', 'Micronesia, Fed. Sts. of': 'Federated States of Micronesia',
        'Bahamas, The': 'The Bahamas', 'Czech Republic': 'Czechia', 'Swaziland': 'Eswatini',
        'United States': 'United States of America',
        'Uzbekistan, Republic of': 'Uzbekistan',
        'Kazakhstan, Republic of': 'Kazakhstan',
        'Mauritania, Islamic Republic of': 'Mauritania',
        'Poland, Republic of': 'Poland', 'Estonia, Republic of': 'Estonia', 
        'Madagascar, Republic of' : 'Madagascar', 'Belarus, Republic of' : 'Belarus', 
        'Netherlands, The' : 'Netherlands', 'Lithuania, Republic of': 'Lithuania', 
        'Latvia, Republic of' : 'Latvia', 'Türkiye, Republic of' : 'Turkey', 
        'Moldova, Republic of' : 'Moldova', 'North Macedonia, Republic of': 'North Macedonia', 
        'Kosovo, Republic of' : 'Kosovo', 'Serbia, Republic of': 'Serbia',
        'Slovenia, Republic of': 'Slovenia', 'Croatia, Republic of' : 'Croatia', 
        'Timor-Leste, Democratic Republic of' : 'Timor-Leste',
        'Taiwan Province of China' : 'Taiwan',
        'Egypt, Arab Republic of' : 'Egypt', 
        "Lao People's Democratic Republic" : 'Laos', 
        'Armenia, Republic of' : 'Armenia',
        'Azerbaijan, Republic of' : 'Azerbaijan', 
        'Afghanistan, Islamic Republic of' : 'Afghanistan', 
        'Tajikistan, Republic of' : 'Tajikistan', 
        'Ethiopia, The Federal Democratic Republic of' : 'Ethiopia', 
        'South Sudan, Republic of' : 'South Sudan', 
        'Mozambique, Republic of': 'Mozambique',
        'Lesotho, Kingdom of': 'Lesotho', 
        'Sub-Saharan Africa (SSA)' : 'Western Sahara',
        'Comoros, Union of the': 'Comoros',
        'Eritrea, The State of': 'Eritrea',
        'Eswatini, Kingdom of': 'Eswatini',
        'Fiji, Republic of': 'Fiji',
        'Marshall Islands, Republic of the': 'Marshall Islands',
        'Nauru, Republic of': 'Nauru',
        'Palau, Republic of': 'Palau',
        'San Marino, Republic of': 'San Marino',
        'São Tomé and Príncipe, Democratic Republic of': 'Sao Tome and Principe',
        'Venezuela, República Bolivariana de': 'Venezuela',
        'West Bank and Gaza': 'West Bank'
    }
    df_processed_dominance['Partner'] = df_processed_dominance['Partner_Raw'].replace(name_mapping)

    df_processed_dominance.loc[df_processed_dominance['Partner'] == 'United States of America', 'Ratio'] = 0.0
    df_processed_dominance.loc[df_processed_dominance['Partner'] == 'China', 'Ratio'] = 1.0
    
    available_years = sorted(df_processed_dominance['Year'].unique())
    if not available_years:
        st.warning("There's no valid year data.")
        return pd.DataFrame(), []
        
    return df_processed_dominance, available_years

@st.cache_data
def get_geojson_data():
    try:
        response = requests.get(config.GEOJSON_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch GeoJSON data: {e}")
        return None

@st.cache_data
def prepare_table_data(df_dominance):
    if df_dominance.empty:
        return pd.DataFrame()

    df_table_ready = df_dominance.copy()
    df_table_ready['Total_US_China_Trade'] = df_table_ready['US_Trade'] + df_table_ready['China_Trade']

    def get_continent_info(country_name):
        return config.COUNTRY_TO_CONTINENT_MAP.get(country_name, ("Unknown", "Unknown"))

    continent_data = df_table_ready['Partner'].apply(lambda x: pd.Series(get_continent_info(x), index=['Continent_Code', 'Continent_Name']))
    
    df_table_ready = pd.concat([df_table_ready, continent_data], axis=1)

    cols_to_keep = ['Partner', 'Year', 'Trade_Flow_Type', 'Ratio', 'US_Trade', 'China_Trade', 'Total_US_China_Trade', 'Continent_Code', 'Continent_Name']
    existing_cols = [col for col in cols_to_keep if col in df_table_ready.columns]
    
    if len(existing_cols) < len(cols_to_keep) -2 :
         st.warning("Beberapa kolom penting hilang saat menyiapkan data tabel. Tabel mungkin tidak lengkap.")
         return df_table_ready[existing_cols] if existing_cols else pd.DataFrame()
        
    return df_table_ready[existing_cols]