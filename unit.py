
import streamlit as st
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

st.set_page_config(
	 page_title='MKT',
	 layout='wide',
	 initial_sidebar_state='expanded',
	 page_icon=literais.apple_dragon_icon, #"favicon.png" #expanded / collapsed
	 menu_items={
		 'Get help': 'https://github.com/jvcss',
		 'Report a bug': "https://github.com/jvcss",
		 'About': "App para automação whatsapp"
	}
)

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)


def ui_caminhar_chat():
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
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

	is_chat_not_end = True
	while is_chat_not_end:
		time.sleep(1)
		ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
		selected_name = listar_nomes(str(ctt_selected.get_attribute('innerHTML')))

		chat_bloco.send_keys(Keys.ARROW_DOWN)
		print(f' \nSELECIONADO > {selected_name[0]}\n\n\n ')


	time.sleep(3)


def ui_buscar():
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)

	btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
	btn_search.click()
	btn_search.send_keys("Salvando")
	time.sleep(1)
	


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

	time.sleep(5)

	actions = ActionChains(driver)
	actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	time.sleep(10)


st.markdown(literais.css_botao_boneca_russa, unsafe_allow_html=True)

with st.container():
	
	if st.button('Enviar', on_click=send_to_clipboard('imagem-0.png')):
		
		st.info('imagem anexada')

	if st.button('confirma',):
		st.info('Executando Chrome')
		ui_caminhar_chat()
		




