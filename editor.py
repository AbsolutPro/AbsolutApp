import streamlit as st
import strings as literais
from streamlit_ace import st_ace
import os
from os import listdir
from os.path import isfile, join

st.set_page_config(
	 page_title='Ace Editor',
	 layout='wide',
	 initial_sidebar_state='expanded',
	 page_icon=literais.apple_dragon_icon, #"favicon.png" #expanded / collapsed
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)
coluna_esquerda, coluna_direita = st.columns(2)

# Display editor's content as you type

def retornar_lista_arquivo_python():
    cwd = os.getcwd()
    onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

    print(f'DIRETORIO {cwd}\n {onlyfiles}')
    return onlyfiles
def file_leitor(arquivo):
    with open(arquivo, 'r') as arqv:
        tudo = arqv.read()
    return tudo

with coluna_direita:
    st.header("A dog")
    arquivo_selecionado = st.selectbox('scripts', retornar_lista_arquivo_python())
    content = st_ace(value=file_leitor(arquivo_selecionado),height=400)

with coluna_esquerda:
    st.header("Observador")
    mostrar = st.button('mostar')
    if mostrar:
        st.code(content)
        #chama essa funcao só de passagem, então ao ler o botao enviar e depois ler o botao confirmar em dois rounds de script
        #quando o botao confirmar chamar sua rotina padrão on_click 
        # o loop anterior onde o botao enviar estava ativado (porque foi ele[enviar] quem ativou o botao confirmar)
        #vai continuar existindo. e por isso essa linha aqui funciona com  on_click
        #mas não funciona dentro do contexto do botao confirmar.
        if st.button('confirmar', on_click=print('retorna antes de ser acionado e se acionado e anterior nao, não executa')):
            print('estanho?')
            st.write(content)
            #print(f'salvar no arquivo {content}') #aqui não vai ser executado quando você clicar esse botao
            #