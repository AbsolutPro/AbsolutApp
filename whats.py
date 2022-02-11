import re
import os
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import win32clipboard
from PIL import Image
from base64 import b64decode
from io import BytesIO
from selenium.common.exceptions import TimeoutException
import time

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

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

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)

def listar_nomes_desc(content):
	desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="fd365im1', content)
	return desc_

def nome_localizado(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.search(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.search(r'<span dir="auto" title="(.*?)" class="gg', texto)

def extrair_info_ultima_conversa(texto):
	try:
		info_last_talk = re.search(r'<div class="_1i_wG">(.*?)</div>',texto)
	except Exception as e:
		print(f'Não achou nenhuma ultima conversa: {e}')
		return ""
	finally:
		if info_last_talk:
			return info_last_talk
		else: return ""

def desistir_localizado(contato, texto):
	#fr'{contato}: "><div class="_1Gy50"><span dir="ltr" class="i0jNr selectable-text copyable-text"><span>(.*?)<'
	ctt = contato.replace('+', '\+')
	frases = re.findall(fr'{ctt}: "><div class="_1Gy50"><span dir="ltr" class="i0jNr selectable-text copyable-text"><span>(.*?)<', texto)
	#
	for cada in frases:
		print(f'CADA UNIDADE {cada}')
	str_match = [s for s in frases if 'Desistir' in s]
	#print(f'PESSOA {contato} ENCONTRADO--> {str_match}\n\n')
	#print(f'FRASES VISTA--> {frases}\n\n')
	if str_match != []:
	#	print(f'AQUI--> {frases}')
		return contato
	else:
		return False

#options = Options()
#options.add_argument("--user-data-dir=C:\\Users\\Victor\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4")
class Cliente:
	"""
		Faz login no whats
		param driver: The selenium driver
		type driver: object
	"""
	google = None
	URL = 'https://web.whatsapp.com/'

	def __init__(self, google=None):
		"""
		param driver The selenium driver
		type driver object
		"""
		self.google = google

	def login(self):

		self.google.get(self.URL)
		self.google.maximize_window()

		wait = WebDriverWait(self.google, 999)
		try:
			wnd = wait.until(EC.visibility_of_element_located(GetLocator.O_BETA))
		except TimeoutException:
			self.google.quit()
			return "você precisa ler o QR CODE. Tente denovo"

		if wnd:
			return wnd.text
		else:
			return "algo diferente de nao ter lido BETA no tempo certo."

	def contatos(self):
		cttss = []
		ctt_nome_anterior = ''
		desc_nome_anterior = ''
		is_ctt_not_end = True
		wait = WebDriverWait(self.google, 999)
		try:
			btn_ctt = wait.until(EC.presence_of_element_located(GetLocator.BTN_CHAT))
			btn_ctt.click()
			time.sleep(1)
			
			
			ctt_blc = wait.until(EC.presence_of_element_located(GetLocator.CTT_BLOC))
			ctt_blc.send_keys(Keys.ARROW_DOWN)
			ctt_blc.send_keys(Keys.ARROW_UP)
			
			
			while is_ctt_not_end:
				time.sleep(.1)

				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))

				nome_selecionado = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))

				selec_desc_name = listar_nomes_desc(str(ctt_selected.get_attribute('innerHTML')))
				
				cttss.append(str(nome_selecionado.group(1)).replace(',', ''))

				if selec_desc_name:
					print(f'\n\n  {nome_selecionado} :descrição: {selec_desc_name.group(1)}')
				else:
					selec_desc_name.append(str(f'descrição ausente-{str(nome_selecionado.group(1))[:2]}'))
					print(f'\n\n NAO TEM descrição tem conteudo {str(nome_selecionado.group(1))}')


				if nome_selecionado.group(1) != ctt_nome_anterior or selec_desc_name.group(1) != desc_nome_anterior:
					ctt_nome_anterior = nome_selecionado.group(1)
					desc_nome_anterior = selec_desc_name.group(1)
				else:
					is_ctt_not_end = False
				ctt_blc.send_keys(Keys.ARROW_DOWN)

			back_to_main = wait.until(EC.presence_of_element_located(GetLocator.BACK_BTN))
			back_to_main.click()
			cttss = list(dict.fromkeys(cttss))
			return cttss

		except Exception as e:
			print(f">ERRO:  {e}")
			time.sleep(99999)
			return cttss

	def chats_ctt(self):
		chat_ctts = []
		wait = WebDriverWait(self.google, 999)
		fast = WebDriverWait(self.google, 1)
		try:
			btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
			btn_search.send_keys('')
			time.sleep(1)
			ctt_nome_anterior = ''
			btn_search.send_keys(Keys.ARROW_DOWN)
			try:
				chat_bloco = fast.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]')))#GetLocator.CHAT_BLOC))
			except:
				chat_bloco = fast.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[2]')))
			is_chat_not_end = True
			while is_chat_not_end:
				time.sleep(0.1)
				chat_ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
				selected_name = nome_localizado(str(chat_ctt_selected.get_attribute('innerHTML')))
				
				chat_ctts.append(str(selected_name.group(1)).replace(',', ''))
				
				if selected_name.group(1) != ctt_nome_anterior:
					ctt_nome_anterior = selected_name.group(1)
				else:
					is_chat_not_end = False
				chat_bloco.send_keys(Keys.ARROW_DOWN)
			chat_ctts = list(dict.fromkeys(chat_ctts))
			return chat_ctts
		except Exception as e:
			print(f'\n\n\n\n\n\n\nFALHA {e}')
			time.sleep(99999)
			return chat_ctts

	def envia_msg(self, contatos_, mensagem):#dataframe['contatos'], text-img.txt
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()
		lista_contatos_info = []
		lista_contatos_ = []
		lista_negra = []
		listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
		texto_p_enviar = html_to_wppedit(mensagem)
		#lista_imgs_ext = []
		if os.name == 'nt':

			if bool(listar_imgs):
				
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					self.google.get(self.URL)
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					
					btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()
					nome_de_fato = str(contatos_['contatos'][contagem])
					btn_search.send_keys(nome_de_fato)
					btn_search.click()
					print(f"CONTATO {contatos_['contatos'][contagem]}")
					time.sleep(.53)

					btn_search.send_keys(Keys.ARROW_DOWN)

					ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
					time.sleep(.53)
					ctt_selected.click()
					selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
					info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
					lista_contatos_info.append(str(info_ultimo_contato.group(1)))
					lista_contatos_.append(str(selected_name.group(1)).replace(',', ''))
					print(f'{selected_name.group(1)} < ULTIMA CONVERSA > {str(info_ultimo_contato.group(1))}')
					tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
					se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))
					if se_desistente_ != False:
						lista_negra.append(se_desistente_)
					time.sleep(.51)
					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))

					
					btn_clear.click()

					try:
						espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
						espaco_enviar.click()
						time.sleep(1)

						pos = 0
						for _ in listar_imgs:
							img_name = f"imagem-{pos}.{listar_imgs[pos][0]}"
							print(f'NOME DAS IMAGENS: {img_name} ')
							time.sleep(1)
							actions = ActionChains(self.google)
							actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
							time.sleep(1)
					except:
						print(f'FALHA AO ANEXAR UMA IMAGEM {e}')
					try:
						
						espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.ENTRADA_ENVIAR_MSG))
						espaco_enviar.send_keys(texto_p_enviar)

						botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
						botao_enviar.click()
						time.sleep(3)

					except Exception as e:
						print(f'FALHA AO DIGITAR MENSAGEM {e}')

					contagem += 1
					print(f'contagem de contatos {contagem}')

				self.google.quit()
				return lista_contatos_info, lista_contatos_

			else:
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					try:

						btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
						btn_search.click()

						btn_search.send_keys(contatos_['contatos'][contagem])

						time.sleep(1)
						btn_search.send_keys(Keys.ARROW_DOWN)
						ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
						ctt_selected.click()
						selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
						info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))

						lista_contatos_info.append(str(info_ultimo_contato.group(1)))
						lista_contatos_.append(str(selected_name.group(1)).replace(',', ''))

						print(f'{selected_name.group(1)} < ULTIMA CONVERSA > {str(info_ultimo_contato.group(1))}')
						tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
						se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))
						if se_desistente_ != False:
							lista_negra.append(se_desistente_)
						time.sleep(.1)

						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()

						time.sleep(1)

						try:
							espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							espaco_enviar.send_keys(texto_p_enviar)

							box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
							box_buscador.click()
						except Exception as e:
							print(f'FALHA AO ABRIR CHAT {e}')
					except Exception as e:
						print(f'FALHA  App Whats. Não achei algum elemento {e}')

					contagem +=1
					time.sleep(1)
				self.google.quit()
			
				return lista_contatos_info, lista_contatos_, lista_negra
			#self.google.maximize_window()
		elif os.name == 'posix':
			wait = WebDriverWait(self.google, 5)
			contagem = 0

			while ate_o_fim:
				if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
				try:#abrir janela clicar em pesquisa. esperar item carregado
					
					#click em pesquisar
					btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()

					btn_search.send_keys(contatos_['contatos'][contagem])
					# insere nome do contato

					time.sleep(1)
					btn_search.send_keys(Keys.ARROW_DOWN)
					ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
					selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
					info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
					ctt_selected.click()
					time.sleep(1)
					#abre contato selecionado
					lista_contatos_info.append(str(info_ultimo_contato.group(1)))
					lista_contatos_.append(str(selected_name.group(1)).replace(',', ''))

					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
					tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
					se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))
					if se_desistente_ != False:
						lista_negra.append(se_desistente_)
					btn_clear.click()
					
					time.sleep(1)
					#apaga busca anterior
					try:
						espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
						espaco_enviar.send_keys(texto_p_enviar) #texto para enviar
						#BOTAO enviar
						box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
						box_buscador.click()
					except Exception as e:
						print(f'FALHA AO ABRIR CHAT {e}')
					finally:
						pass
				except Exception as e:
					print(f'FALHA  App Whats. Não achei algum elemento {e}')
				finally:
					time.sleep(2)

				contagem +=1
				time.sleep(1)
			self.google.quit()
			return lista_contatos_info, lista_contatos_, lista_negra
	
	def envia_msg_fake(self, contatos_, mensagem):#dataframe['contatos'], text-img.txt
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()
		lista_contatos_info = []
		lista_contatos_ = []
		lista_negra = []

		listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
		texto_p_enviar = html_to_wppedit(mensagem)
		#lista_imgs_ext = []
		if os.name == 'nt':

			if bool(listar_imgs):
				
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					#self.google.get(self.URL)
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					
					btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()
					#regrex_pattern = re.compile(pattern = "["u"\U0001F600-\U0001F64F" 
					#	u"\U0001F600-\U0001F64F"
					#	u"\U0001F300-\U0001F5FF"
					#	u"\U0001F680-\U0001F6FF"
					#	u"\U0001F1E0-\U0001F1FF"
					#	"]+", flags = re.UNICODE)
					#pesqisar = regrex_pattern.sub(r'',contatos_['contatos'][contagem])
					pesqisar = remove_emojis(contatos_['contatos'][contagem])

					#pesqisar = re.sub(r'\W+ ', '', contatos_['contatos'][contagem])
					
					btn_search.send_keys(pesqisar)
					
					print(f"CONTATO {contatos_['contatos'][contagem]}")
					time.sleep(.53)

					btn_search.send_keys(Keys.ARROW_DOWN)

					ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
					time.sleep(.53)
					ctt_selected.click()
					selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
					info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
					lista_contatos_info.append(str(info_ultimo_contato.group(1)))
					lista_contatos_.append(str(selected_name.group(1)).replace(',', ''))
					print(f"{str(selected_name.group(1)).replace(',', '')} < ULTIMA CONVERSA > {str(info_ultimo_contato.group(1))}")
					tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
					se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))
					if se_desistente_ != False:
						lista_negra.append(se_desistente_)
					time.sleep(1)
					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
					#btn_clear = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
					
					btn_clear.click()

					try:
						pass
						#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
						#espaco_enviar.click()
						time.sleep(1)

						#pos = 0
						#for _ in listar_imgs:
						#	img_name = f"imagem-{pos}.{listar_imgs[pos][0]}"
						#	print(f'NOME DAS IMAGENS: {img_name} ')
						#	time.sleep(1)
						#	actions = ActionChains(self.google)
						#	actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
						#	time.sleep(1)
					except:
						print(f'FALHA NA SELEÇÃO UNITÁRIA RÁPIDA  {e}')
					try:
						pass
						#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.ENTRADA_ENVIAR_MSG))
						#espaco_enviar.send_keys(texto_p_enviar)

						#botao_enviar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')))
						#botao_enviar.click()
						time.sleep(3)

					except Exception as e:
						print(f'FALHA AO DIGITAR MENSAGEM {e}')

					contagem += 1
					print(f'contagem de contatos {contagem}')

				self.google.quit()
				return lista_contatos_info, lista_contatos_
					
				

			else:
				wait = WebDriverWait(self.google, 999)
				contagem = 0

				while ate_o_fim:
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					try:

						btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
						btn_search.click()
						regrex_pattern = re.compile(pattern = "["u"\U0001F600-\U0001F64F" 
						 u"\U0001F600-\U0001F64F"
						 u"\U0001F300-\U0001F5FF"
						 u"\U0001F680-\U0001F6FF"
						 u"\U0001F1E0-\U0001F1FF"
						 "]+", flags = re.UNICODE)
						#pesqisar = regrex_pattern.sub(r'',contatos_['contatos'][contagem])
						pesqisar = remove_emojis(contatos_['contatos'][contagem])

						#pesqisar = re.sub(r'\W+ ', '', contatos_['contatos'][contagem])
						btn_search.send_keys(pesqisar)

						time.sleep(1)
						btn_search.send_keys(Keys.ARROW_DOWN)
						ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
						ctt_selected.click()
						selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
						info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))

						lista_contatos_info.append(str(info_ultimo_contato.group(1)))
						lista_contatos_.append(str(selected_name.group(1)).replace(',', ''))

						print(f'{selected_name.group(1)} < ULTIMA CONVERSA > {str(info_ultimo_contato.group(1))}')
						tela_atual = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div[3]/div/div[2]/div[3]')))
						se_desistente_ = desistir_localizado(contatos_['contatos'][contagem],tela_atual.get_attribute('innerHTML'))
						if se_desistente_ != False:
							lista_negra.append(se_desistente_)

						time.sleep(1)

						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()

						time.sleep(1)

						try:
							pass
							#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							#espaco_enviar.send_keys(texto_p_enviar)

							#box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
							#box_buscador.click()
						except Exception as e:
							print(f'FALHA AO ABRIR CHAT {e}')
							self.google.quit()
					except Exception as e:
						print(f'FALHA  App Whats. Não achei algum elemento {e}')
						self.google.quit()

					contagem +=1
					time.sleep(1)
				self.google.quit()
				return lista_contatos_info, lista_contatos_, lista_negra
			#self.google.maximize_window()

class GetLocator(object):

	"""
		:Getter: 'Web Element'
	"""
	
	O_BETA = (By.XPATH, '//*[@id="side"]/header/div[1]/div[2]/b')
	"""
		span: TEXT 'beta'
	"""
	
	BTN_CHAT = (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')
	"""
		button: DIV
	"""
	#tab_index_contact_key     //*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]
	CTT_LIST_BOX = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div')
	"""
		block: DIV
	"""

	CTT_BLOC = (By.XPATH , '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]')
	"""
		block: DIV
	"""

	SEARCH_INPUT = (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
	"""
		input: DIV
	"""
	CHAT_BLOC = (By.XPATH, '//*[@id="pane-side"]/div[2]')
	"""
		block: DIV
	"""
	BACK_BTN = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/header/div/div[1]/button')
	
	"""
		input: BUTTON
	"""
	CLEAR_BUTTON = (By.XPATH, '//*[@id="side"]/div[1]/div/button')
	"""
		input: BUTTON
	"""

	TEXT_BOX_CHAT = (By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
	
	"""
		block: DIV
	"""
	ENTRADA_ENVIAR_MSG = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
	"""
		input: DIV
	"""