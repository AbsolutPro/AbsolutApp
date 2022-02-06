#region IMPORTS
from base64 import b64decode
import pandas as pd
import streamlit as st
from streamlit_quill import st_quill as text_editor
import os
if os.name == 'nt':
	import win32clipboard
	from PIL import Image
	from io import BytesIO
	def send_to_clipboard(img_path):
		image = Image.open(img_path)#path
		output = BytesIO()
		image.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		#print(data)
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
import strings as literais
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#endregion

st.set_page_config(
	 page_title='Unidades',
	 layout='centered',
	 initial_sidebar_state='expanded',
	 page_icon=literais.apple_dragon_icon, #"favicon.png" #expanded / collapsed
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)

if "contatos_salvos" not in st.session_state: st.session_state["contatos_salvos"] = pd.DataFrame([''], columns=['contatos'])

if "contatos_list" not in st.session_state: st.session_state["contatos_list"] = []

if "contatos_see_info" not in st.session_state: st.session_state["contatos_see_info"] = []

def html_to_wppedit(raw_html):
	negrito = re.compile('(<strong>|</strong>)')
	clean_negrito_text = negrito.sub('*', raw_html)

	italico = re.compile('(<em>|</em>)')
	clean_negrito_text = italico.sub('_', clean_negrito_text)

	cutted = re.compile('(<s>|</s>)')
	clean_negrito_text = cutted.sub('~', clean_negrito_text)

	monoletter = re.compile(r'(<span class="ql-font-monospace">|</span>)')
	clean_negrito_text = monoletter.sub('```', clean_negrito_text)

	CLEANR = re.compile('<.*?>')
	cleantext = re.sub(CLEANR, '', clean_negrito_text)
	return cleantext

def listar_nomes_desc(content):
	desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="fd365im1', content)
	return desc_

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)

def ui_login():
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	#opts.add_argument("---headless")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless executable_path='chromedriver.exe', 
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 999)

	palavra_beta = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/header/div[1]/div[2]/b')))

	if palavra_beta:
		return palavra_beta.text
	else:
		return 'error'

def ui_lista_chat():
	chat_ctts = []
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	#opts.add_argument("---headless")
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)

	btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
	btn_search.send_keys("")
	chat_bloco = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[2]')))
	time.sleep(1)
	#barra de busca
	btn_search.send_keys(Keys.ARROW_DOWN)
	#PRIMEIRA CONVERSA SELECIONADA
	ctt_anterior = ''

	is_chat_not_end = True
	while is_chat_not_end:
		#time.sleep(1)
		ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
		selected_name = listar_nomes(str(ctt_selected.get_attribute('innerHTML')))
		chat_ctts += selected_name
		print(f' \nSELECIONADO > {selected_name[0]}\n ')
		print(f' \ctt anterior > {ctt_anterior}\n ')
		if selected_name[0] != ctt_anterior:
			ctt_anterior = selected_name[0]
		else:
			is_chat_not_end = False
		chat_bloco.send_keys(Keys.ARROW_DOWN)

	chat_ctts = list(dict.fromkeys(chat_ctts))
	return chat_ctts

def ui_buscar(contatos_):
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)
	contagem = 0
	ate_o_fim = True

	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:
			driver.get('https://web.whatsapp.com/')
			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(.51)
		except Exception as e:
			print(f'envia_msg -- ERROR {e}')
		finally:
			time.sleep(0.21)
			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			btn_clear.click()
			contagem +=1
			time.sleep(.21)
	driver.quit()
	


	btn_search.send_keys(Keys.ARROW_DOWN)
	time.sleep(3)
	ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
	ctt_selected.click()
	time.sleep(1)
	btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
	#CLEAR_BUTTON
	btn_clear.click()
	espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
	#TEXT_BOX_CHAT
	espaco_enviar.send_keys('')

	time.sleep(1)

	actions = ActionChains(driver)
	actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	time.sleep(5)
	driver.quit()

def ui_enviar_imagem(contatos_,mensagem):
	ate_o_fim = True
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
	texto_p_enviar = html_to_wppedit(mensagem)
	wait = WebDriverWait(driver, 60)
	contagem = 0

	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:
			driver.get('https://web.whatsapp.com/')
			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])

			info_ultimo_contato = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_1i_wG')))
			print(f'{contatos_["contatos"][contagem]} < ULTIMA conversa > {info_ultimo_contato.text}')
			btn_search.send_keys(Keys.ARROW_DOWN)
			ctt_selecionado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))

			time.sleep(1)
			ctt_selecionado.click()

			if bool(listar_imgs):
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
				espaco_enviar.send_keys('')
				actions = ActionChains(driver)
				actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
				time.sleep(5)
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')))
				espaco_enviar.send_keys(texto_p_enviar) #texto para enviar
				time.sleep(5)
				botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
				botao_enviar.click()
			else:
				espaco_enviar = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
				espaco_enviar.send_keys('')
				espaco_enviar.send_keys(texto_p_enviar)
				botao_enviar_menor = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')))
				botao_enviar_menor.click()

		except Exception as e:
			print(f'envia_msg -- ERROR {e}')
		finally:
			time.sleep(1)

			

			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))

			btn_clear.click()

			contagem +=1

			time.sleep(.5)

	time.sleep(1)
	driver.quit()

def ui_lista_contatos():
	contatos = []
	contato_anterior = ''
	descricao_anterior = ''
	fim_da_lista_contatos = True

	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)

	icone_ctts = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')))
	icone_ctts.click()

	box_lista_ctt = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div')))

	conteudo_list_ctt = str(box_lista_ctt.get_attribute('innerHTML'))

	contatos = listar_nomes(conteudo_list_ctt)

	ctt_blc = wait.until(EC.presence_of_element_located((By.XPATH , '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]')))

	lista_inter = contatos

	while fim_da_lista_contatos:
		ctt_blc.send_keys(Keys.ARROW_DOWN)

		ctt_selecionado = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))

		nome_selecionado = listar_nomes(str(ctt_selecionado.get_attribute('innerHTML')))

		descricao_nome_selecionado = listar_nomes_desc(str(ctt_selecionado.get_attribute('innerHTML')))

		lista_inter += nome_selecionado

		if descricao_nome_selecionado:
			print(f'\n\n descrição tem conteudo {descricao_nome_selecionado[0]}')
		else:
			descricao_nome_selecionado.append(str(f'descrição ausente-{str(nome_selecionado[0])[:2]}'))
			print(f'\n\n NAO TEM descrição {nome_selecionado[0]}')
		
		if nome_selecionado[0] != contato_anterior or descricao_nome_selecionado[0] != descricao_anterior:
			contato_anterior = nome_selecionado[0]
			descricao_anterior = descricao_nome_selecionado[0]
		else:
			fim_da_lista_contatos = False
	
	back_to_main = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/header/div/div[1]/button')))
	back_to_main.click()
	contatos = list(dict.fromkeys(lista_inter))
	return contatos

def ui_ultima_conversa( contatos_):#dataframe['contatos'], text-img.txt
	ate_o_fim = True
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	

	#contatos_['contatos']#contato1,contato2 LIST
	#for cada in contatos_['contatos']:
	#	pass

	wait = WebDriverWait(driver, 60)
	contagem = 0

	while ate_o_fim:
		if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
		try:#abrir janela clicar em pesquisa. esperar item carregado
			driver.get('https://web.whatsapp.com/')

			btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
			btn_search.click()
			btn_search.send_keys(contatos_['contatos'][contagem])
			time.sleep(.1)
			
		except Exception as e:
			print(f'envia_msg -- ERROR {e}')
		finally:
			time.sleep(0.1)

			info_ultimo_contato = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_1i_wG')))
			print(f'{contatos_["contatos"][contagem]} < ULTIMA conversa > {info_ultimo_contato.text}')
			btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
			btn_clear.click()
			contagem +=1
			time.sleep(.1)
	driver.quit()

with st.container():
	caixa = st.container()
	caixa.subheader("Mensagem")
	content = text_editor(placeholder="Escreva seu Newsletter Personalizado",html=caixa.checkbox("Entregar como HTML", True),readonly=caixa.checkbox("Apenas leitura", False),key="quill",)
	listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{content}')
	st.subheader('Contatos')
	st.write(st.session_state.contatos_salvos)
	print(st.session_state.contatos_list)
	if st.sidebar.button('LOGIN', ):
		#on_click=send_to_clipboard('imagem-0.png')
		
		st.sidebar.info(f'Login : {ui_login()}')

	if st.sidebar.button('CHAT LISTA',):
		st.sidebar.info('Executando Chrome')

		st.session_state.contatos_list += ui_lista_chat()

		st.session_state.contatos_list = list(dict.fromkeys(st.session_state.contatos_list))
		
		st.session_state.contatos_salvos = pd.DataFrame(st.session_state.contatos_list, columns=['contatos'])

		st.experimental_rerun()

	if st.sidebar.button('CONTATOS SALVOS LISTA',):
		st.sidebar.info('Executando Chrome')

		st.session_state.contatos_list += ui_lista_contatos()

		st.session_state.contatos_list = list(dict.fromkeys(st.session_state.contatos_list))

		st.session_state.contatos_salvos = pd.DataFrame(st.session_state.contatos_list, columns=['contatos'])

		st.experimental_rerun()

	if st.sidebar.button('BUSCA CONTATO',):
		st.sidebar.info('Executando Chrome')
		ui_buscar(st.session_state.contatos_salvos)


	enviar = st.sidebar.button('ENVIA msg IMAGEM',)
	if enviar:
		st.sidebar.info('Executando Chrome')
		ui_enviar_imagem(st.session_state.contatos_salvos,content)
	
	if len(listar_imgs) > 0  and not enviar:
		with open(f"imagem-{0}.{listar_imgs[0][0]}", 'wb') as wrb:
			wrb.write(b64decode(listar_imgs[0][1]))
		send_to_clipboard(f"imagem-0.{listar_imgs[0][0]}")
	
	if st.sidebar.button('ULTIMA CONVERSA',):
		st.sidebar.info('Executando Chrome')
		st.write(ui_ultima_conversa(st.session_state.contatos_salvos))