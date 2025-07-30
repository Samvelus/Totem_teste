import streamlit as st

import time

def repetir(func):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            time.sleep(10)  # Espera 60 segundos antes de repetir
    return wrapper

def side_bar():

    colsd1, colsd2 = st.sidebar.columns([1,1])
    with colsd1:
        st.sidebar.image("Logo 10 anos - Letra preta (1).png")
    with colsd2:
        st.sidebar.image("logo_ufmt.png")
    # Sidebar para navegação
    st.sidebar.title("Menu de Navegação")
    
    # Exemplo de um item de menu
    st.sidebar.subheader("Opções")
    # st.sidebar.button("Guia do Estudante", use_container_width=True)
    # st.sidebar.page_link("https://wiki.ufmt.br/Guia_do_Estudante_de_Gradua%C3%A7%C3%A3o", label="Guia do Estudante", use_container_width=True)
    st.sidebar.button("Início", use_container_width=True)
    st.sidebar.button("Mapa do Campus", on_click=page_mapa.mapa, use_container_width=True)
    st.sidebar.button("Configurações", use_container_width=True)
    st.sidebar.button("Ajuda", use_container_width=True)
    
    # Exemplo de um seletor de idioma
    language = st.sidebar.selectbox("Selecione o idioma", ["Português", "Inglês", "Espanhol"])
    
    return language

def config_page():
    # Configurações iniciais do Streamlit
    st.set_page_config(
        page_title="Totem Web Interface",
        page_icon="Logo 10 anos - Letra branca (1).png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Configurações de tema (CSS)
    st.markdown("""
    <style> 
    body {
        background-color: #f0f2f5;  
        color: #333;
    }           
    </style>
    """, unsafe_allow_html=True)


def cabeçalho():
    # Cabeçalho da página
    st.markdown("""
    <h1 style='text-align: center; color: #003366;'>Universidade Federal de Mato Grosso</h1>
    <p style='text-align: center;'>Bem-vindo ao Totem da UFMT!</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""<hr style='border: 1px solid #003366;'/>""", unsafe_allow_html=True)


def menu():
    
    with st.container():
        # Linha 1: Mapa e Horários
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            # st.markdown("""
            #  <button class="big-button mapa" onclick="window.location.href='https://wiki.ufmt.br/Guia_do_Estudante_de_Gradua%C3%A7%C3%A3o'">
            #    🔍\n Mapa </button>
            #     """, unsafe_allow_html=True)
            # if st.button("🔍\nMapa", key="mapa",on_click=page_mapa.mapa, help="Encontre salas e laboratórios", use_container_width=True):
            #     st.switch_page("Site/page_mapa.py")
            st.button("🔍\nMapa", key="mapa",on_click=page_mapa.mapa, help="Encontre salas e laboratórios", use_container_width=True)
        with col2:
            if st.button("📋\nHorários", key="horarios", help="Veja os horários das aulas", use_container_width=True):
                st.success("Você clicou em Horários")
        with col3:
            if st.button("📰\nAvisos", key="avisos", help="Leia os avisos recentes", use_container_width=True):
                st.success("Você clicou em Avisos")

        # Linha 2: Contatos, FAQ, Ajuda
        col4, col5, col6 = st.columns(3, gap="medium")

        with col4:
            if st.button("📞\nContatos", key="contatos", help="Veja os contatos úteis", use_container_width=True):
                st.success("Você clicou em Contatos")

        with col5:
            if st.button("❓\nFAQ", key="faq", help="Perguntas frequentes", use_container_width=True):
                st.success("Você clicou em FAQ")
        with col6:
            if st.button("🆘\nAjuda", key="ajuda", help="Peça ajuda", use_container_width=True):
                st.success("Você clicou em Ajuda")
