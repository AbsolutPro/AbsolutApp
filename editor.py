#!/usr/bin/env python3
import streamlit as st
import strings as literais
from streamlit_ace import st_ace
import os
from os import listdir
from os.path import isfile, join

st.set_page_config(page_title='Ace Editor', layout='wide',initial_sidebar_state='expanded', page_icon=literais.apple_dragon_icon, 
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)
THEMES = ["ambiance", "chaos", "chrome", "clouds", "clouds_midnight", "cobalt", "crimson_editor", "dawn", "dracula", "dreamweaver", "eclipse", "github", "gob", "gruvbox", "idle_fingers", "iplastic","katzenmilch", "kr_theme", "kuroir", "merbivore", "merbivore_soft", "mono_industrial", "monokai", "nord_dark", "pastel_on_dark", "solarized_dark", "solarized_light", "sqlserver", "terminal","textmate", "tomorrow", "tomorrow_night", "tomorrow_night_blue", "tomorrow_night_bright", "tomorrow_night_eighties", "twilight", "vibrant_ink", "xcode"]

my_theme = st.sidebar.selectbox('themes', THEMES)
# Display editor's content as you type

def list_files():
    cwd = os.getcwd()
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

    #print(f'DIRETORIO {cwd}\n {onlyfiles}')
    return onlyfiles
def file_reader(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arqv:
        tudo = arqv.read()
    return tudo

st.header("Aws dog editor")
arquivo_selecionado = st.selectbox('list python scripts', list_files())
content = st_ace(value=file_reader(arquivo_selecionado),height=800,theme=my_theme,language="python",)


st.sidebar.header("Observador")
salvar = st.sidebar.button('salvar')
if salvar:
    with open(arquivo_selecionado, 'w', encoding='utf-8') as arquivo:
        arquivo.write(content)
    
    #st.code(content)