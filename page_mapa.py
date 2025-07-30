import streamlit as st
import modulo_web as mw
import streamlit_folium as st_fol
import geopandas as gpd
import folium as fol
import mapas
import time
import json

# Configurações iniciais:
mw.config_page()

# Título e descrição da página
st.title("Mapa do Campus")
st.write("Explore o mapa do campus para encontrar locais importantes.")

# ==== Carregar dados ====

# salas = gpd.read_file("Mapa/salas_1.geojson")
# rotas = gpd.read_file("Mapa/rotas.geojson")
# floor_1 = gpd.read_file("Mapa/floor_1_unido.geojson")
# floor_1 = gpd.read_file("Mapa\\floor_1_unido.geojson")
# rotas_acessiveis = gpd.read_file("Mapa/rotas.geojson")


# Abrir os arquivos GeoJSON como dicionários Python
with open("Mapa/salas_1.geojson", "r", encoding="utf-8") as f:
    salas = json.load(f)

with open("Mapa/rotas.geojson", "r", encoding="utf-8") as f:
    rotas = json.load(f)

with open("Mapa/floor_1_unido.geojson", "r", encoding="utf-8") as f:
    floor_1 = json.load(f)

# === Corrigir colunas com Timestamp (converter para string) ===
# for gdf in [salas, rotas_normais, rotas_acessiveis, floor_1]:
#     for col in gdf.columns:
#         if gdf[col].dtype == "datetime64[ns]":
#             gdf[col] = gdf[col].astype(str)

# Limites do mapa
min_lon, max_lon = -56.06187707154574, -56.07384725735446
min_lat, max_lat = -15.606074048769116, -15.61345366988482
centro_mapa = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]

# Tipo de tile
tiles_dict = {
    "Normal": "CartoDB Positron",
    "Híbrido": "Stamen Toner",
    "Satélite": "Stamen Terrain"
}


# Interface lateral
col1, col2 = st.columns([3, 1])

with col2:
    #nomes_salas = sorted(salas["nome"].dropna().unique())
    # Extrai os nomes das salas a partir das propriedades
    nomes_salas = sorted(
        list(
            set(
                feature["properties"].get("nome")
                for feature in salas["features"]
                if feature["properties"].get("nome")  # ignora valores None ou vazios
            )
        )
    )
    sala_escolhida = st.selectbox("PESQUISA LOCAL:", nomes_salas, placeholder="Digite ou selecione o local..." )
    acessibilidade = st.checkbox("Preciso de acessibilidade")
    mostrar_rota = st.button("Como chegar?")

    tile_escolhido = st.selectbox("Tipo de Mapa:", list(tiles_dict.keys()), index=0)
    mostrar_pontos = st.checkbox("Mostrar Pontos de Interesse", value=True)
    mostrar_rotas = st.checkbox("Mostrar Rotas", value=False)
    mostrar_info = st.checkbox("Mostrar Informações do Local", value=True)
    
# Definir tile escolhido
tile_escolhido = tiles_dict.get(tile_escolhido, "CartoDB Positron")
# Define centro do mapa: se sala for escolhida, centraliza nela
if sala_escolhida:
    sala_alvo = salas[salas["nome"] == sala_escolhida]
    if not sala_alvo.empty:
        centro = sala_alvo.geometry.unary_union.centroid
        centro_mapa = [centro.y, centro.x]

# Criar o mapa
mapa = fol.Map(
    max_bounds=True,
    location=centro_mapa,
    zoom_start=20,
    tiles=tile_escolhido,
    min_zoom=16,
    max_zoom=25
)

# Adicionar pontos de interesse
if mostrar_pontos:
    for _, row in salas.iterrows():
        nome = row.get("nome", "Sala sem nome")
        descricao = row.get("descricao", "Sem descrição")
        imagem = row.get("imagem", "")

        # HTML do popup
        html_popup = f"""
        <b>{nome}</b><br>
        {descricao}<br>
        {"<img src='" + imagem + "' width='200'>" if imagem else ""}
        """

        fol.GeoJson(
            row["geometry"],
            style_function=lambda x: {
                "fillColor": "gray",
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.6
            },
            tooltip=nome if mostrar_info else None,
            popup=fol.Popup(html_popup, max_width=300)
        ).add_to(mapa)

# Adicionar camada de fundo do mapa
fol.TileLayer(
    tiles=tile_escolhido,
    name="Mapa Base",
    control=False
).add_to(mapa)
# Adicionar camada de piso
fol.GeoJson(
    floor_1,
    name="Piso 1",
    style_function=lambda x: {'fillColor': 'gray', 'color': 'black', 'weight': 1, 'fillOpacity': 0.8},
    tooltip="Piso 1"
).add_to(mapa)


# Desenhar salas no mapa
def cor_preenchimento(nome):
    return 'red' if nome == sala_escolhida else 'black'

for _, row in salas.iterrows():

    nome = row.get("nome", "Sala sem nome")
    descricao = row.get("descricao", "Sem descrição")
    imagem = row.get("imagem", "")

    # HTML do popup
    html_popup = f"""
    <b>{nome}</b><br>
    {descricao}<br>
    {"<img src='" + imagem + "' width='200'>" if imagem else ""}
    """

    estilo = {
        'fillColor': cor_preenchimento(row["nome"]),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    }
    fol.GeoJson(
        row["geometry"],
        name=row["nome"],
        tooltip=row["nome"] if mostrar_info else None,
        popup=fol.Popup(html_popup, max_width=300),
        style_function=lambda x, estilo=estilo: estilo
    ).add_to(mapa)

# Mostrar rota, se houver
if mostrar_rota and sala_escolhida:
    # rotas_usar = rotas_acessiveis if acessibilidade else rotas_normais
    # rota_para_sala = rotas_usar[rotas_usar["destino"] == sala_escolhida]
    if acessibilidade:
        rota_usar = rotas[rotas["acessibilidade"] == "true"]
    else:
        rota_usar = rotas[rotas["acessibilidade"] == "false"]

    rota_para_sala = rota_usar[rota_usar["destino"] == sala_escolhida]

    if not rota_para_sala.empty:
        fol.GeoJson(
            rota_para_sala,
            name="Rota",
            style_function=lambda x: {'color': 'blue', 'weight': 5, 'opacity': 0.9},
            tooltip="Rota até " + sala_escolhida
        ).add_to(mapa)
    else:
        st.warning("Nenhuma rota encontrada para esta sala com o perfil escolhido.")

fol.LayerControl().add_to(mapa)

# Mostrar mapa na interface
with col1:
    st_fol.folium_static(mapa, width=1200, height=700)
