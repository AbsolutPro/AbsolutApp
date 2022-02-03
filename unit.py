import time
import streamlit as st
import win32clipboard
from PIL import Image
from io import BytesIO
import strings as literais
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

def ui_automation():
	#send_to_clipboard(f'imagem-0.png')
	opts = Options()
	opts.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
	driver = webdriver.Chrome(options=opts)#options=opts ---headless
	driver.get('https://web.whatsapp.com/')
	driver.maximize_window()
	wait = WebDriverWait(driver, 60)

	btn_search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
	#SEARCH_INPUT
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


st.markdown(literais.css_botao_boneca_russa, unsafe_allow_html=True)

with st.container():
	
	if st.button('Enviar', on_click=send_to_clipboard('imagem-0.png')):
		
		st.info('imagem anexada')

	if st.button('confirma', on_click=send_to_clipboard('imagem-0.png')):
		
		ui_automation()
		




