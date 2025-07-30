import geopandas as gpd
import folium as fol
from folium import GeoJson  
import streamlit as st
from streamlit_folium import folium_static


def mapa_ufmt():
    """
    Cria um mapa interativo da UFMT com pontos de interesse e polígonos.
    """
    min_lon, max_lon = -56.06187707154574, -56.07384725735446
    min_lat, max_lat = -15.606074048769116, -15.61345366988482


    mapa = fol.Map(
        max_bounds=True,
        location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2],
        zoom_start=12,
        tiles="CartoDB Positron",
        min_zoom=16,
        max_zoom=25,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon
    )

    # Carregar dados
    salas = gpd.read_file("Mapa\\salas_1.geojson")
    floor_1 = gpd.read_file("Mapa\\floor_1.geojson")
    rotas = gpd.read_file("Mapa\\rotas.geojson")
    banheiros = gpd.read_file("Mapa\\banheiros.geojson")

    # for _, row in floor_1.iterrows():
    #     estilo = {
    #         'color': 'gray',   
    #         'weight': 1,
    #         'fillOpacity': 0.8
    #     }
    #     fol.GeoJson(
    #         row["geometry"],
    #         style_function=lambda x, estilo=estilo: estilo
    #     ).add_to(mapa)


    # for _, row in salas.iterrows():
    #     estilo = {
    #         'color': 'black',
    #         'weight': 1,
    #         'fillOpacity': 0.6,
    #     }
    #     fol.GeoJson(
    #         row["geometry"],
    #         name=row["nome"],
    #         tooltip=row["nome"],
    #         style_function=lambda x, estilo=estilo: estilo
    #     ).add_to(mapa)

    # Configurações do mapa
    #fol.LayerControl().add_to(mapa)
    
    return mapa



def mostrar_banheiros(mapa):
    """
    Adiciona marcadores de banheiros ao mapa.
    """
    banheiros = gpd.read_file("Mapa\\banheiros.geojson")

    for _, row in banheiros.iterrows():
        fol.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row["nome"],
            icon=fol.Icon(color="green", icon="toilet")
        ).add_to(mapa)  
    return mapa