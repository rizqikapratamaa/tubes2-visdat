import pandas as pd

data = pd.read_csv("raw_trade_data.csv")

data = data.drop(columns=['DATASET', 'SERIES_CODE', 'OBS_MEASURE'])

country_map = {
    'United States': 'United States',
    "China, People's Republic of": 'China'
}

trade_map = {
    'Exports of goods, Free on board (FOB), US dollar': 'Export',
    'Imports of goods, Cost insurance freight (CIF), US dollar': 'Import'
}

data['COUNTRY'] = data['COUNTRY'].replace(country_map)
data['COUNTERPART_COUNTRY'] = data['COUNTERPART_COUNTRY'].replace(country_map)
data['INDICATOR'] = data['INDICATOR'].replace(trade_map)

data = data.rename(columns={
    'COUNTRY': 'Country',
    'COUNTERPART_COUNTRY': 'Partner',
    'INDICATOR': 'Trade_Type'
})

data.to_csv("cleaned_trade_data.csv", index=False)