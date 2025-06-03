# Page Configuration
PAGE_TITLE = "China vs. America: Global Trade Dominance"
LAYOUT = "wide"

# Color Definitions
PAGE_BG_COLOR = "#0B1A3B"
TEXT_COLOR_PRIMARY = "#FFFFFF"
TEXT_COLOR_SECONDARY = "#CCCCCC"
TEXT_COLOR_TERTIARY = "#A0A0A0"

COLOR_US_REF = "#0067B1"
COLOR_CHINA_REF = "#E60000"
HEX_COLOR_EQUAL_TRADE = "#D8D8D8"
HEX_COLOR_NO_DATA = "#000000"

HEX_COLOR_US_DOMINANT = COLOR_US_REF
HEX_COLOR_CHINA_DOMINANT = COLOR_CHINA_REF

COLOR_BORDER = '#181818'
OCEAN_COLOR = PAGE_BG_COLOR

# Data Paths
TRADE_DATA_PATH = 'src/data/cleaned_trade_data.csv'
GEOJSON_URL = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'

# Map Settings
INITIAL_YEAR_OFFSET = 0 # 0 untuk tahun terakhir, 1 untuk tahun kedua terakhir, dst.
YEARS_RANGE = range(2001, 2025)


# --- Trade Flow Options ---
TRADE_FLOW_OPTIONS_DISPLAY = ["Two-way trade", "Imports", "Exports"]
TRADE_FLOW_MAP = {
    "Two-way trade": "Total",
    "Imports": "Import",
    "Exports": "Export"
}
DEFAULT_TRADE_FLOW_DISPLAY = "Two-way trade"

SORT_ORDER_OPTIONS = ["Descending", "Ascending"]

# Default Table Settings
DEFAULT_TABLE_YEAR = 2024
DEFAULT_TABLE_CONTINENT = "World"
DEFAULT_TABLE_SORT_ORDER = "Descending"
TOP_N_COUNTRIES = 10

# Continent Bounds (lon_min, lon_max, lat_min, lat_max)
CONTINENT_BOUNDS = {
    "AS": {"lon_min": 35, "lon_max": 165, "lat_min": -10, "lat_max": 75},
    "EU": {"lon_min": -20, "lon_max": 50, "lat_min": 35, "lat_max": 75},
    "AF": {"lon_min": -20, "lon_max": 55, "lat_min": -35, "lat_max": 37}, 
    "NA": {"lon_min": -165, "lon_max": -55, "lat_min": 10, "lat_max": 80}, 
    "SA": {"lon_min": -85, "lon_max": -35, "lat_min": -55, "lat_max": 12}, 
    "OC": {"lon_min": 112, "lon_max": 178, "lat_min": -48, "lat_max": -5}
}

CONTINENT_NAME_TO_CODE = {
    "World": "World",
    "Asia": "AS",
    "Europe": "EU",
    "Africa": "AF",
    "North America": "NA",
    "South America": "SA"
}

CONTINENT_OPTIONS = {
    "World": "World",
    "Asia": "AS",
    "Europe": "EU",
    "Africa": "AF",
    "North America": "NA",
    "South America": "SA",
    "Oceania": "OC"
}

COUNTRY_TO_CONTINENT_MAP = {
    # Asia (AS)
    "Afghanistan": ("AS", "Asia"), # Dari GeoJSON, 'Afghanistan, Islamic Republic of' di df_dominance setelah mapping jadi 'Afghanistan'
    "Bahrain, Kingdom of": ("AS", "Asia"), # Contoh, perlu disesuaikan
    "Bangladesh": ("AS", "Asia"),
    "Bhutan": ("AS", "Asia"),
    "Brunei": ("AS", "Asia"), # 'Brunei Darussalam' -> 'Brunei'
    "Cambodia": ("AS", "Asia"),
    "China": ("AS", "Asia"),
    "Cyprus": ("AS", "Asia"), # Geografis di Asia, politik bisa EU
    "Georgia": ("AS", "Asia"), # Bisa juga Eropa
    "India": ("AS", "Asia"),
    "Indonesia": ("AS", "Asia"),
    "Iran": ("AS", "Asia"), # 'Iran, Islamic Republic of' -> 'Iran'
    "Iraq": ("AS", "Asia"),
    "Israel": ("AS", "Asia"),
    "Japan": ("AS", "Asia"),
    "Jordan": ("AS", "Asia"),
    "Kazakhstan": ("AS", "Asia"), # 'Kazakhstan, Republic of' -> 'Kazakhstan' (sebagian di Eropa)
    "North Korea": ("AS", "Asia"), # "Korea, Democratic People's Republic of" -> "North Korea"
    "South Korea": ("AS", "Asia"), # "Korea, Republic of" -> "South Korea"
    "Kuwait": ("AS", "Asia"),
    "Kyrgyzstan": ("AS", "Asia"), # 'Kyrgyz Republic' -> 'Kyrgyzstan'
    "Laos": ("AS", "Asia"), # "Lao People's Democratic Republic" -> "Laos"
    "Lebanon": ("AS", "Asia"),
    "Malaysia": ("AS", "Asia"),
    "Maldives": ("AS", "Asia"),
    "Mongolia": ("AS", "Asia"),
    "Myanmar": ("AS", "Asia"), # Dulu Burma
    "Nepal": ("AS", "Asia"),
    "Oman": ("AS", "Asia"),
    "Pakistan": ("AS", "Asia"),
    "Philippines": ("AS", "Asia"),
    "Qatar": ("AS", "Asia"),
    "Saudi Arabia": ("AS", "Asia"),
    "Singapore": ("AS", "Asia"),
    "Sri Lanka": ("AS", "Asia"),
    "Syria": ("AS", "Asia"), # 'Syrian Arab Republic' -> 'Syria'
    "Taiwan": ("AS", "Asia"), # 'Taiwan Province of China' -> 'Taiwan'
    "Tajikistan": ("AS", "Asia"), # 'Tajikistan, Republic of' -> 'Tajikistan'
    "Thailand": ("AS", "Asia"),
    "Timor-Leste": ("AS", "Asia"), # 'Timor-Leste, Democratic Republic of' -> 'Timor-Leste' (Oceania?)
    "Turkey": ("AS", "Asia"), # 'Türkiye, Republic of' -> 'Turkey' (sebagian di Eropa)
    "Turkmenistan": ("AS", "Asia"),
    "United Arab Emirates": ("AS", "Asia"),
    "Uzbekistan": ("AS", "Asia"), # 'Uzbekistan, Republic of' -> 'Uzbekistan'
    "Vietnam": ("AS", "Asia"),
    "Yemen": ("AS", "Asia"), # 'Yemen, Republic of' -> 'Yemen'
    "West Bank and Gaza": ("AS", "Asia"), # Atau "West Bank" saja tergantung mapping GeoJSON Anda

    # Eropa (EU)
    "Albania": ("EU", "Europe"),
    "Armenia": ("EU", "Europe"), # 'Armenia, Republic of' -> 'Armenia' (bisa juga Asia)
    "Austria": ("EU", "Europe"),
    "Azerbaijan": ("EU", "Europe"), # 'Azerbaijan, Republic of' -> 'Azerbaijan' (bisa juga Asia)
    "Belarus": ("EU", "Europe"), # 'Belarus, Republic of' -> 'Belarus'
    "Belgium": ("EU", "Europe"),
    "Bosnia and Herzegovina": ("EU", "Europe"),
    "Bulgaria": ("EU", "Europe"),
    "Croatia": ("EU", "Europe"), # 'Croatia, Republic of' -> 'Croatia'
    "Czechia": ("EU", "Europe"), # 'Czech Republic' -> 'Czechia'
    "Denmark": ("EU", "Europe"),
    "Estonia": ("EU", "Europe"), # 'Estonia, Republic of' -> 'Estonia'
    "Faroe Islands": ("EU", "Europe"), # Bagian dari Denmark
    "Finland": ("EU", "Europe"),
    "France": ("EU", "Europe"),
    "Germany": ("EU", "Europe"),
    "Gibraltar": ("EU", "Europe"), # Wilayah Inggris
    "Greece": ("EU", "Europe"),
    "Hungary": ("EU", "Europe"),
    "Iceland": ("EU", "Europe"),
    "Ireland": ("EU", "Europe"),
    "Italy": ("EU", "Europe"),
    "Kosovo": ("EU", "Europe"), # 'Kosovo, Republic of' -> 'Kosovo'
    "Latvia": ("EU", "Europe"), # 'Latvia, Republic of' -> 'Latvia'
    "Lithuania": ("EU", "Europe"), # 'Lithuania, Republic of' -> 'Lithuania'
    "Luxembourg": ("EU", "Europe"),
    "Malta": ("EU", "Europe"),
    "Moldova": ("EU", "Europe"), # 'Moldova, Republic of' -> 'Moldova'
    "Montenegro": ("EU", "Europe"),
    "Netherlands": ("EU", "Europe"), # 'Netherlands, The' -> 'Netherlands'
    "North Macedonia": ("EU", "Europe"), # 'North Macedonia, Republic of' -> 'North Macedonia' (Macedonia di GeoJSON?)
    "Norway": ("EU", "Europe"),
    "Poland": ("EU", "Europe"), # 'Poland, Republic of' -> 'Poland'
    "Portugal": ("EU", "Europe"),
    "Romania": ("EU", "Europe"),
    "Russia": ("EU", "Europe"), # 'Russian Federation' -> 'Russia' (sebagian besar Asia)
    "San Marino, Republic of": ("EU", "Europe"), # San Marino di GeoJSON
    "Serbia": ("EU", "Europe"), # 'Serbia, Republic of' -> 'Serbia'
    "Slovakia": ("EU", "Europe"), # 'Slovak Republic' -> 'Slovakia'
    "Slovenia": ("EU", "Europe"), # 'Slovenia, Republic of' -> 'Slovenia'
    "Spain": ("EU", "Europe"),
    "Sweden": ("EU", "Europe"),
    "Switzerland": ("EU", "Europe"),
    "Ukraine": ("EU", "Europe"),
    "United Kingdom": ("EU", "Europe"),
    "Holy See": ("EU", "Europe"), # Vatikan

    # Afrika (AF)
    "Algeria": ("AF", "Africa"),
    "Angola": ("AF", "Africa"),
    "Benin": ("AF", "Africa"),
    "Botswana": ("AF", "Africa"),
    "Burkina Faso": ("AF", "Africa"),
    "Burundi": ("AF", "Africa"),
    "Cabo Verde": ("AF", "Africa"),
    "Cameroon": ("AF", "Africa"),
    "Central African Republic": ("AF", "Africa"),
    "Chad": ("AF", "Africa"),
    "Comoros, Union of the": ("AF", "Africa"), # Comoros di GeoJSON
    "Democratic Republic of the Congo": ("AF", "Africa"), # 'Congo, Democratic Republic of the' -> 'Democratic Republic of the Congo'
    "Republic of Congo": ("AF", "Africa"), # 'Congo, Republic of' -> 'Republic of Congo'
    "Ivory Coast": ("AF", "Africa"), # "Côte d'Ivoire" -> "Ivory Coast"
    "Djibouti": ("AF", "Africa"),
    "Egypt": ("AF", "Africa"), # 'Egypt, Arab Republic of' -> 'Egypt'
    "Equatorial Guinea": ("AF", "Africa"),
    "Eritrea": ("AF", "Africa"), # 'Eritrea, The State of' -> 'Eritrea'
    "Eswatini": ("AF", "Africa"), # 'Eswatini, Kingdom of' -> 'Eswatini' (dulu Swaziland)
    "Ethiopia": ("AF", "Africa"), # 'Ethiopia, The Federal Democratic Republic of' -> 'Ethiopia'
    "Gabon": ("AF", "Africa"),
    "Gambia": ("AF", "Africa"),
    "Ghana": ("AF", "Africa"),
    "Guinea": ("AF", "Africa"),
    "Guinea-Bissau": ("AF", "Africa"), # Guinea Bissau di GeoJSON
    "Kenya": ("AF", "Africa"),
    "Lesotho": ("AF", "Africa"), # 'Lesotho, Kingdom of' -> 'Lesotho'
    "Liberia": ("AF", "Africa"),
    "Libya": ("AF", "Africa"),
    "Madagascar": ("AF", "Africa"), # 'Madagascar, Republic of' -> 'Madagascar'
    "Malawi": ("AF", "Africa"),
    "Mali": ("AF", "Africa"),
    "Mauritania": ("AF", "Africa"), # 'Mauritania, Islamic Republic of' -> 'Mauritania'
    "Mauritius": ("AF", "Africa"),
    "Morocco": ("AF", "Africa"),
    "Mozambique": ("AF", "Africa"), # 'Mozambique, Republic of' -> 'Mozambique'
    "Namibia": ("AF", "Africa"),
    "Niger": ("AF", "Africa"),
    "Nigeria": ("AF", "Africa"),
    "Rwanda": ("AF", "Africa"),
    "São Tomé and Príncipe, Democratic Republic of": ("AF", "Africa"), # Sao Tome and Principe di GeoJSON
    "Senegal": ("AF", "Africa"),
    "Seychelles": ("AF", "Africa"),
    "Sierra Leone": ("AF", "Africa"),
    "Somalia": ("AF", "Africa"),
    "South Africa": ("AF", "Africa"),
    "South Sudan": ("AF", "Africa"), # 'South Sudan, Republic of' -> 'South Sudan'
    "Sudan": ("AF", "Africa"),
    "Tanzania": ("AF", "Africa"), # 'Tanzania, United Republic of' -> 'Tanzania'
    "Togo": ("AF", "Africa"),
    "Tunisia": ("AF", "Africa"),
    "Uganda": ("AF", "Africa"),
    "Zambia": ("AF", "Africa"),
    "Zimbabwe": ("AF", "Africa"),
    "Western Sahara": ("AF", "Africa"), # Mungkin ada di data Anda

    # Amerika Utara (NA)
    "Antigua and Barbuda": ("NA", "North America"),
    "The Bahamas": ("NA", "North America"), # 'Bahamas, The' -> 'The Bahamas'
    "Barbados": ("NA", "North America"),
    "Belize": ("NA", "North America"),
    "Canada": ("NA", "North America"),
    "Costa Rica": ("NA", "North America"),
    "Cuba": ("NA", "North America"),
    "Dominica": ("NA", "North America"),
    "Dominican Republic": ("NA", "North America"),
    "El Salvador": ("NA", "North America"),
    "Greenland": ("NA", "North America"), # Bagian dari Denmark
    "Grenada": ("NA", "North America"),
    "Guatemala": ("NA", "North America"),
    "Haiti": ("NA", "North America"),
    "Honduras": ("NA", "North America"),
    "Jamaica": ("NA", "North America"),
    "Mexico": ("NA", "North America"),
    "Nicaragua": ("NA", "North America"),
    "Panama": ("NA", "North America"),
    "St. Kitts and Nevis": ("NA", "North America"),
    "St. Lucia": ("NA", "North America"),
    "St. Vincent and the Grenadines": ("NA", "North America"),
    "Trinidad and Tobago": ("NA", "North America"),
    "United States of America": ("NA", "North America"), # 'United States' -> 'United States of America'

    # Amerika Selatan (SA)
    "Argentina": ("SA", "South America"),
    "Bolivia": ("SA", "South America"),
    "Brazil": ("SA", "South America"),
    "Chile": ("SA", "South America"),
    "Colombia": ("SA", "South America"),
    "Ecuador": ("SA", "South America"),
    "Guyana": ("SA", "South America"),
    "Paraguay": ("SA", "South America"),
    "Peru": ("SA", "South America"),
    "Suriname": ("SA", "South America"),
    "Uruguay": ("SA", "South America"),
    "Venezuela": ("SA", "South America"), # 'Venezuela, República Bolivariana de' -> 'Venezuela'
    "Falkland Islands": ("SA", "South America"), # 'Falkland Islands (Malvinas)' -> 'Falkland Islands'

    # Oceania (OC)
    "Australia": ("OC", "Oceania"),
    "Fiji": ("OC", "Oceania"),
    "Kiribati": ("OC", "Oceania"),
    "Marshall Islands, Republic of the": ("OC", "Oceania"),
    "Federated States of Micronesia": ("OC", "Oceania"),
    "Nauru, Republic of": ("OC", "Oceania"),
    "New Caledonia": ("OC", "Oceania"),
    "New Zealand": ("OC", "Oceania"),
    "Palau, Republic of": ("OC", "Oceania"),
    "Papua New Guinea": ("OC", "Oceania"),
    "Samoa": ("OC", "Oceania"),
    "Solomon Islands": ("OC", "Oceania"),
    "Tonga": ("OC", "Oceania"),
    "Tuvalu": ("OC", "Oceania"),
    "Vanuatu": ("OC", "Oceania"),
}

PLOTLY_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'doubleClick': 'reset',
}