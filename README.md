# China vs. America: Global Trade Dominance Dashboard

## Project Description

This project presents a dynamic data visualization dashboard comparing the global trade trends between China and the United States from 2001 to 2024. The interactive dashboard allows users to explore and analyze how these two economic giants compete in global trade dominance through various metrics and visualizations.

Dive into the rivalry between the United States and China as they compete for global trade supremacy. This interactive trade map displays a time series capturing changing patterns of global trade with the world’s two largest economies.

## Dashboard Link

**[China versus America on global trade](https://global-trade-trend.streamlit.app/)**

## Key Features

* **Interactive World Map (Choropleth):** Displays trade dominance (US or China as the larger trading partner) per country, year by year.
    * Tooltips with detailed trade values.
    * Filter by trade flow type (Two-way trade, Imports, Exports).
    * Animation/Slider for year changes.
    * Zoom and Pan capabilities.
* **Trend Line Chart:**
    * Comparison of total export and import volume trends for the US vs. China over time (2001-2024).
    * Filter to view trends by Exports or Imports.
* **Dynamic Information Table:**
    * Displays a ranking of trading partner countries based on combined US and China trade volume.
    * Filter by year, continent, and trade flow type (Two-way trade, Imports, Exports).
    * Shows trade values for the US, China, and their total.
* **Miniature Pie Charts:** Integrated into the table to show the proportion of US vs. China trade for each partner country.
* **Responsive Design:** The dashboard is designed to be accessible on various screen sizes.
* **Global Filters:** Year selection and trade flow type selection that affect multiple dashboard components.

## Visualizations Used

* **Choropleth Map:** For geographical visualization of trade dominance.
* **Line Chart:** For displaying trade trends over time.
* **Data Table:** For presenting detailed information in a structured manner.
* **Pie Chart:** For showing trade composition per partner country.

## Data Source

The data used in this dashboard is sourced from the **IMF International Trade in Goods (by partner country) (IMTS)**, covering the period from 2001 to 2024.

## Technology Stack

* **Python:** Primary programming language.
* **Streamlit:** Framework for building interactive web applications and dashboards.
* **Pandas:** For data manipulation and analysis.
* **Plotly:** For creating interactive charts (Choropleth Map, Line Chart, Pie Chart).
* **HTML/CSS:** For custom styling and appearance.