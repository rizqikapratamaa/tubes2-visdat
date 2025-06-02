# Page Configuration
PAGE_TITLE = "Global Trade Dominance - Interactive Hover"
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
TRADE_DATA_PATH = 'data/cleaned_trade_data.csv'
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

# Continent Bounds (lon_min, lon_max, lat_min, lat_max)
CONTINENT_BOUNDS = {
    "AS": {"lon_min": 35, "lon_max": 165, "lat_min": -10, "lat_max": 75},    # Asia (lebih ketat)
    "EU": {"lon_min": -20, "lon_max": 50, "lat_min": 35, "lat_max": 75},      # Eropa (lebih ketat)
    "AF": {"lon_min": -20, "lon_max": 55, "lat_min": -35, "lat_max": 37},      # Afrika (sedikit lebih ketat)
    "NA": {"lon_min": -165, "lon_max": -55, "lat_min": 10, "lat_max": 80},     # Amerika Utara (lebih ketat)
    "SA": {"lon_min": -85, "lon_max": -35, "lat_min": -55, "lat_max": 12},     # Amerika Selatan (lebih ketat)
    "OC": {"lon_min": 112, "lon_max": 178, "lat_min": -48, "lat_max": -5}     # Oceania
}

CONTINENT_NAME_TO_CODE = {
    "World": "World",
    "Asia": "AS",
    "Europe": "EU",
    "Africa": "AF",
    "North America": "NA",
    "South America": "SA"
}

# Plotly Figure Config
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'doubleClick': 'reset',
}