# streamlit_app/treemap_plotter.py
import plotly.graph_objects as go
import pandas as pd
import numpy as np # Untuk np.nan_to_num
import config 
import streamlit as st

def format_trade_value(value):
    if pd.isna(value) or value == 0:
        return "$0"
    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:.2f}"

def create_treemap_chart(df_all_data, selected_year, selected_trade_flow_key):
    # Hapus atau komentari st.write untuk versi produksi
    # st.subheader("Debugging Treemap Plotter")
    # st.write(f"Masuk create_treemap_chart dengan Tahun: {selected_year}, Flow Key: {selected_trade_flow_key}")
    # st.write(f"Dimensi df_all_data: {df_all_data.shape if not df_all_data.empty else 'Kosong'}")

    if df_all_data.empty:
        # st.warning("df_all_data kosong saat masuk create_treemap_chart.")
        fig = go.Figure()
        fig.add_annotation(text="No data available for treemap (initial data empty).", showarrow=False, font=dict(size=16, color=config.TEXT_COLOR_PRIMARY))
        fig.update_layout(paper_bgcolor=config.TREEMAP_BG_COLOR, plot_bgcolor=config.TREEMAP_BG_COLOR, height=400)
        return fig

    df_filtered = df_all_data[
        (df_all_data['Year'] == selected_year) &
        (df_all_data['Trade_Flow_Type'] == selected_trade_flow_key)
    ].copy()

    # st.write(f"Dimensi df_filtered setelah filter tahun & flow: {df_filtered.shape}")

    if df_filtered.empty:
        # st.warning(f"Tidak ada data mentah untuk {selected_trade_flow_key} di tahun {selected_year}.")
        fig = go.Figure()
        fig.add_annotation(text=f"No raw data for {selected_trade_flow_key} in {selected_year}.", showarrow=False, font=dict(size=16, color=config.TEXT_COLOR_PRIMARY))
        fig.update_layout(paper_bgcolor=config.TREEMAP_BG_COLOR, plot_bgcolor=config.TREEMAP_BG_COLOR, height=400)
        return fig

    # Hitung Value: US_Trade + China_Trade. Pastikan tidak ada NaN yang merusak.
    # Ganti NaN dengan 0 sebelum menjumlahkan untuk 'Value'
    df_filtered['US_Trade_Clean'] = np.nan_to_num(df_filtered['US_Trade'])
    df_filtered['China_Trade_Clean'] = np.nan_to_num(df_filtered['China_Trade'])
    df_filtered['Value'] = df_filtered['US_Trade_Clean'] + df_filtered['China_Trade_Clean']
    
    # Filter negara/partner yang tidak memiliki benua valid atau nama partner valid (seharusnya sudah ditangani di data_loader)
    df_filtered = df_filtered.dropna(subset=['Partner', 'Continent'])
    df_filtered = df_filtered[df_filtered['Partner'] != ""]
    df_filtered = df_filtered[df_filtered['Continent'] != ""]

    # Kita tetap memerlukan setidaknya beberapa data dengan Value > 0 untuk membuat treemap yang berarti
    # Jika semua Value adalah 0, treemap akan kosong.
    # Namun, jangan terlalu agresif memfilter jika data memang kecil.
    # Filter utama adalah bahwa negara itu sendiri memiliki data perdagangan.
    df_display = df_filtered[df_filtered['Value'] > 0].copy() # Hanya tampilkan yang ada nilai perdagangannya

    # st.write(f"Dimensi df_display setelah filter Value > 0: {df_display.shape}")
    # if not df_display.empty:
    #     st.write("Contoh df_display (5 baris pertama):", df_display.head())
    # else:
    #     st.warning("df_display kosong setelah filter Value > 0.")

    if df_display.empty:
        # st.warning(f"Tidak ada data perdagangan > 0 untuk {selected_trade_flow_key} di tahun {selected_year} setelah pembersihan.")
        fig = go.Figure()
        fig.add_annotation(text=f"No trade value > 0 for {selected_trade_flow_key} in {selected_year}.", showarrow=False, font=dict(size=16, color=config.TEXT_COLOR_PRIMARY))
        fig.update_layout(paper_bgcolor=config.TREEMAP_BG_COLOR, plot_bgcolor=config.TREEMAP_BG_COLOR, height=400)
        return fig

    ids = ["Global Trade"]
    labels = ["Global Trade"]
    parents = [""]
    total_global_value = df_display['Value'].sum()
    values = [total_global_value if total_global_value > 0 else 1] # Plotly butuh value > 0 untuk root jika ada children
    customdata = [f"Total Global: {format_trade_value(total_global_value)}"]
    marker_colors_list = [config.PAGE_BG_COLOR] 


    continents_data = df_display.groupby('Continent')['Value'].sum().reset_index()
    continents_data = continents_data[continents_data['Value'] > 0] # Hanya benua dengan nilai

    for _, row in continents_data.iterrows():
        continent_name = row['Continent']
        ids.append(continent_name)
        labels.append(continent_name)
        parents.append("Global Trade")
        values.append(row['Value'])
        customdata.append(f"Total for {continent_name}: {format_trade_value(row['Value'])}")
        marker_colors_list.append(config.CONTINENT_COLORS.get(continent_name, config.CONTINENT_COLORS["Other"]))

    for _, row in df_display.iterrows(): # Iterasi pada df_display yang sudah difilter Value > 0
        partner_name = row['Partner']
        continent_name_for_partner = row['Continent']
        
        # Pastikan parent (benua) ada di IDs sebelum menambahkan negara
        if continent_name_for_partner not in ids:
            # st.warning(f"Benua '{continent_name_for_partner}' untuk partner '{partner_name}' tidak ditemukan di IDs benua. Partner dilewati.")
            continue

        ids.append(partner_name)
        labels.append(partner_name)
        parents.append(continent_name_for_partner)
        values.append(row['Value']) # Value sudah dipastikan > 0 dari filter df_display
        
        hover_detail = (f"Partner: {partner_name}<br>"
                        f"Continent: {continent_name_for_partner}<br>"
                        f"Total Trade (US+China): {format_trade_value(row['Value'])}<br>"
                        f"US Trade: {format_trade_value(row['US_Trade'])}<br>" # Tampilkan nilai asli US_Trade
                        f"China Trade: {format_trade_value(row['China_Trade'])}") # Tampilkan nilai asli China_Trade
        customdata.append(hover_detail)
        marker_colors_list.append(config.CONTINENT_COLORS.get(continent_name_for_partner, config.CONTINENT_COLORS["Other"]))

    # st.write("Final Treemap Data IDs count:", len(ids))

    if len(ids) <= 1 : 
        # st.warning("Hanya data root yang tersedia untuk treemap. Tidak cukup untuk visualisasi.")
        fig = go.Figure()
        fig.add_annotation(text="Not enough data to display in treemap (only root or no children).", showarrow=False, font=dict(size=16, color=config.TEXT_COLOR_PRIMARY))
        fig.update_layout(paper_bgcolor=config.TREEMAP_BG_COLOR, plot_bgcolor=config.TREEMAP_BG_COLOR, height=400)
        return fig

    fig = go.Figure(go.Treemap(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        customdata=customdata,
        hovertemplate="<b>%{label}</b><br>%{customdata}<extra></extra>",
        branchvalues="total", 
        marker=dict(
            colors=marker_colors_list,
            # line=dict(width=0.5, color=config.PAGE_BG_COLOR) # Opsi garis tipis
        ),
        pathbar=dict(
            visible=True,
            thickness=20,
            textfont=dict(color=config.TEXT_COLOR_PRIMARY, size=12, family='"Helvetica Neue", Helvetica, Arial, sans-serif'),
            edgeshape='>',
        ),
        textfont=dict(color=config.TEXT_COLOR_PRIMARY, family='"Helvetica Neue", Helvetica, Arial, sans-serif', size=11),
        hoverlabel=dict(
            bgcolor=config.PAGE_BG_COLOR,
            font_size=12,
            font_family='"Helvetica Neue", Helvetica, Arial, sans-serif',
            font_color=config.TEXT_COLOR_PRIMARY,
            bordercolor="rgba(255,255,255,0.5)"
        ),
        tiling=dict( # Coba algoritma tiling berbeda jika ada overlap teks
            packing='squarify', # 'slice', 'dice', 'slice-dice', 'squarify', 'binary'
            # pad=1 # Sedikit padding antar tile
        )
    ))

    fig.update_layout(
        height=650, 
        margin=dict(t=35, l=10, r=10, b=10), 
        paper_bgcolor=config.TREEMAP_BG_COLOR,
        plot_bgcolor=config.TREEMAP_BG_COLOR,
        font=dict(color=config.TREEMAP_TEXT_COLOR, family='"Helvetica Neue", Helvetica, Arial, sans-serif')
    )
    # st.success("Figur treemap berhasil dibuat.")
    return fig