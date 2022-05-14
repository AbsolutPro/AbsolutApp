from sympy import EX
import strings
import re
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command
import time
from contextlib import contextmanager
@contextmanager
def try_catch(fail_info):
	try:
		yield
	except Exception as e:
		print(f"{fail_info}")
		with open('unique_out.txt', 'a') as uf:
			uf.write(f'{fail_info}\n')
    #else:
        #print("case everthig works inside the with")
    #finally:
        #print("FINAL always")
        # whatever your common handling is

def html_to_wppedit(raw_html):
	#image_tag = re.compile(r'<img.*?/>').search(raw_html).group()
	#with open("input_editor.txt", "w") as f:
	#	f.write(raw_html)
	#raw_html = raw_html.replace(image_tag, '')
	#f = open("input_editor.txt", "w")
	#f.write(raw_html)
	#f.close()
	#print("\n\n\n"+raw_html+"\n\n\n")
	negrito = re.compile('(<strong>|</strong>)')
	clean_negrito_text = negrito.sub('*', raw_html)

	italico = re.compile('(<em>|</em>)')
	clean_negrito_text = italico.sub('_', clean_negrito_text)

	cutted = re.compile('(<s>|</s>)')
	clean_negrito_text = cutted.sub('~', clean_negrito_text)

	monoletter = re.compile(r'(<span class="ql-font-monospace">|</span>)')
	clean_negrito_text = monoletter.sub('```', clean_negrito_text)

	#test to reamove new line
	new_line = re.compile(r'(<br>)')
	clean_negrito_text = new_line.sub(' /n ', clean_negrito_text)

	CLEANR = re.compile('<.*?>')
	cleantext = re.sub(CLEANR, '', clean_negrito_text)
	#print(f'\n\n\n HTML TO WPP >>> {cleantext} \n\n\n')

	#time.sleep(1000)
	return cleantext

def listar_nomes(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` 
	title_name = re.findall(r'"_3q9s6"><span dir="auto" title="(.*?)" class="g', texto)
	if title_name:
		return title_name
	else:
		return re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)

def listar_nomes_desc(content):
	#desc_ = re.findall(r'_1qB8f"><span dir="auto" title="(.*?)" class="', content)
	desc_ = re.search(r'_1qB8f"><span dir="auto" title="(.*?)" class="', content)
	return desc_

def nome_localizado(texto):
	#print(f'O TEXTO \n\n\n {texto}') '' "" `` _3vPI2
	try:
		title_name = re.findall(r'"><span dir="auto" title="(.*?)" class="g', texto)
		if title_name is not None:
			return title_name[0]
		else:
			title_alt = re.findall(r'<span dir="auto" title="(.*?)" class="gg', texto)
			return title_alt[1]
	except Exception as e: 
		print(f"FALHA NO REGULAR EXPRESSION {e}")

def extrair_info_ultima_conversa(texto):
	try:
		info_last_talk = re.findall(r'<div class="_1i_wG">(.*?)</div>',texto)
	except Exception as e:
		print(f'Não achou nenhuma ultima conversa: {e}')
		return ""
	finally:
		if info_last_talk:
			return info_last_talk[0]
		else: return ""

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

	def consultar(self): #
		self.google.get(self.URL)
		self.google.maximize_window()
		try:
			while self.google.title:
				try:
					self.google.execute(Command.STATUS)
				except Exception as e:
					self.google.quit()
		except Exception as e:
			print(f"Could not login {e}")

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
			return ''# wnd.text
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
			time.sleep(.51)
			
			#//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]
			ctt_blc = wait.until(EC.presence_of_element_located(GetLocator.CTT_BLOC))#//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div/div[10]
			ctt_blc.send_keys(Keys.ARROW_DOWN)
			ctt_blc.send_keys(Keys.ARROW_UP)
			
			
			while is_ctt_not_end:
				time.sleep(.1)

				ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))#OK
				
				#print(f"\n\nULTIMO COMANDO {ctt_selected.get_attribute('innerHTML')}??????\n\n")
				
				nome_selecionado = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))#RETORNA UMA OBJETO MATCH COM A PROPRIEDADE GROUP
				#***CASO DESCRIÇÃO NAO EXISTA
				selec_desc_name = listar_nomes_desc(str(ctt_selected.get_attribute('innerHTML')))
				
				
				time.sleep(.1)
				#print(f"\n\nULTIMO COMANDO {nome_selecionado}   ??????\n\n")
				cttss.append(str(nome_selecionado.group(1)).replace(',', ''))
				#cttss.append(str(nome_selecionado[0]).replace(',', ''))

				if selec_desc_name:
					print(f'\n\n  {nome_selecionado} :descrição: {selec_desc_name.group(1)}')
				else:
					
					selec_desc_name = nome_selecionado#.append(str(f'descrição ausente-{str(nome_selecionado.group(1))[:2]}'))
					print(f'\n\n NAO TEM descrição tem conteudo {str(nome_selecionado.group(1))}')


				if nome_selecionado.group(1) != ctt_nome_anterior or selec_desc_name.group(1) != desc_nome_anterior:
					ctt_nome_anterior = nome_selecionado.group(1)
					if selec_desc_name:
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
			time.sleep(99)
			return cttss

	def chats_ctt(self):
		chat_ctts = []
		wait = WebDriverWait(self.google, 90)
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
			time.sleep(99)
			return chat_ctts

	def envia_msg(self, contatos_, mensagem):#dataframe['contatos'], text-img.txt
		ate_o_fim = True
		self.google.get(self.URL)
		self.google.maximize_window()
		lista_contatos_info = []
		lista_contatos_ = []
		lista_negra = []
		listar_imgs = re.findall( r'src="data:image/(.*?);base64,(.*?)"', fr'{mensagem}')
		#remove image tag
		image_tag = re.compile(r'<img.*?>').search(mensagem).group()
		mensagem = mensagem.replace(image_tag, '') 

		texto_p_enviar = html_to_wppedit(mensagem)
		#lista_imgs_ext = []
		if os.name == 'nt':

			if bool(listar_imgs):
				
				wait = WebDriverWait(self.google, 10)
				contagem = 0

				while ate_o_fim:
					#self.google.get(self.URL)
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					
					btn_search = wait.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()
					nome_de_fato = str(contatos_['contatos'][contagem])
					btn_search.send_keys(nome_de_fato)
					btn_search.click()
					#************************************************************
					#PAUSE INFINITO
					time.sleep(.53)

					btn_search.send_keys(Keys.TAB)#firefox
					try: 
						#SE EXISTE NA BUSCA
						self.google.find_element_by_class_name('_2_TVt')
						ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
						selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
						info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
						time.sleep(.53)
						ctt_selected.click()
						if selected_name is None: selected_name = nome_de_fato
						if info_ultimo_contato is None: info_ultimo_contato = ""
						lista_contatos_info.append(str(info_ultimo_contato))

						lista_contatos_.append(  str(selected_name).replace(',', '')  ) 
						
						try:
							# the only way to check is waiting for texto box
							
							espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							#self.google.find_element_by_xpath(GetLocator.TEXT_BOX_CHAT)
							# #wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							espaco_enviar.click()
							time.sleep(1)

							pos = 0
							for _ in listar_imgs:
								#img_name = f"imagem-{pos}.{listar_imgs[pos][0]}"
								#print(f'NOME DAS IMAGENS: {img_name} ')
								time.sleep(1)
								actions = ActionChains(self.google)
								actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
								time.sleep(1)
						except Exception as e:
							print(f'{contatos_["contatos"][contagem]}')
						try:
							#INPUT TEXT => ENVIAR_MSG
							espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.ESPACO_ENVIAR_MSG ))
							#espaco_enviar = self.google.find_element_by_xpath(GetLocator.ENTRADA_ENVIAR_MSG)
							#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.ENTRADA_ENVIAR_MSG))
							#time.sleep(100)
							#print(f'\n\n\n\n{texto_p_enviar}\n\n\n\n')
							for part in texto_p_enviar.split('/n'):
								try:
									espaco_enviar.send_keys(part)
								except Exception as exp:
									#print(f"{exp}")
									time.sleep(1)
								ActionChains(self.google).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
								time.sleep(1)
							#espaco_enviar.send_keys(texto_p_enviar)

							botao_enviar = wait.until(EC.presence_of_element_located(GetLocator.BOTAO_ENVIAR_IMG))
							botao_enviar.click()
							time.sleep(1)

						except Exception as e:
							print(f"{nome_de_fato}")

						contagem += 1
						#print(f'contagem de contatos {contagem}', end='')

					except Exception as e:
						print(f"{nome_de_fato}")


						contagem += 1
						#print(f'{contagem}')
						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()
						time.sleep(2)
					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
					btn_clear.click()

					

				self.google.quit()
				return lista_contatos_info, lista_contatos_

			else:#SE NAO TIVER IMAGEM NOVA ROTINA DE ENVIO DE MSG
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

						lista_contatos_info.append(str(info_ultimo_contato))
						lista_contatos_.append(str(selected_name).replace(',', ''))

						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()

						time.sleep(1)

						try:
							espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							for part in texto_p_enviar.split('/n'):
								try:
									espaco_enviar.send_keys(texto_p_enviar)
								except: pass
							box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
							box_buscador.click()
						except Exception as e:
							time.sleep(1)#print(f'FALHA AO ABRIR CHAT {e}')
					except Exception as e:
						print(f"{contatos_['contatos'][contagem]}")

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
		image_tag = re.compile(r'<img.*?>').search(mensagem).group()
		mensagem = mensagem.replace(image_tag, '')
		texto_p_enviar = html_to_wppedit(mensagem)#only text format for whatsapp OUTPUT
		if os.name == 'nt':

			if bool(listar_imgs):
				
				wait = WebDriverWait(self.google, 9) #culd be not founded ...short
				wait_long = WebDriverWait(self.google, 9999)#certainly will find ...wait
				wait_short = WebDriverWait(self.google, 5)
				wait_short_l = WebDriverWait(self.google, 7)
				contagem = 0

				while ate_o_fim:
					#self.google.get(self.URL)
					if contagem >= len(contatos_['contatos']) - 1: ate_o_fim = False
					
					btn_search = wait_long.until(EC.presence_of_element_located(GetLocator.SEARCH_INPUT))
					btn_search.click()
					
					btn_search.send_keys(contatos_['contatos'][contagem])
					btn_search.click()
					#************************************************************
					#PAUSE INFINITO
					#print('OK ATE AQUI?')
					time.sleep(2)

					btn_search.send_keys(Keys.TAB)#firefox
					try:
						#SE EXISTE NA BUSCA
						time.sleep(2)
						#self.google.find_element_by_class_name('_2_TVt')#chrome
						ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
						selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
						info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))
						time.sleep(1)
						ctt_selected.click()
						
						if selected_name is None: selected_name = contatos_['contatos'][contagem]
						if info_ultimo_contato is None: info_ultimo_contato = ""

						lista_contatos_info.append(str(info_ultimo_contato))
						lista_contatos_.append(  str(selected_name).replace(',', ''))
						
						CLEANR = re.compile('<.*?>')
						clean_mensagem = re.sub(CLEANR, '', mensagem)
						clean_mensagem = clean_mensagem.replace("/n", '')
						#print(f'clean_mensagem {clean_mensagem}')
						try:
							tela_atual = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'_2gzeB')))
							#print(tela_atual.get_attribute('innerHTML'))
							

							CLEANR = re.compile(r'<.*?>')#\d(.*)\d\d \w\w ADD NEW LINES
							CLEANR_rmv_src = re.compile(r's.*>')
							CLEANR_rmv_nl_nl = re.compile(r'<.*\n.*\n.*"')
							CLEANR_ = re.compile(r'\n.*\n')
							#remove nested new lines from regex img
							#CLEANR_tg_add_nl = re.compile('\d\d:\d\d')
							CLEANR_rmv_single = re.compile('^\S+$')#remove single words in one line
							CLEANR_all_az09 = re.compile(r'[^A-Za-z0-9 ]+')#allow char
							

							remover_alert = " mensagens são protegidas com a criptografia de ponta a ponta e ficam somente entre você e os participantes desta conversa. Nem mesmo o WhatsApp pode ler ou ouvi-las. Clique para saber mais."
							mensagem_instance = re.sub(CLEANR, '', str(tela_atual.get_attribute('innerHTML')))
							mensagem_instance = re.sub(CLEANR_rmv_src, '', mensagem_instance)
							mensagem_instance = re.sub(CLEANR_rmv_nl_nl, '', mensagem_instance)
							mensagem_instance = re.sub(CLEANR_, '', mensagem_instance)

							mensagem_instance = mensagem_instance.replace('"', '')
							mensagem_instance = mensagem_instance.replace('*', '')
							mensagem_instance = mensagem_instance.replace('_', '')
							mensagem_instance = mensagem_instance.replace('```', '')
							mensagem_instance = mensagem_instance.replace(remover_alert, ' ')
							mensagem_instance = re.sub(CLEANR_rmv_single, '', mensagem_instance)
							#mensagem_instance = re.sub(CLEANR_all_az09, '', CLEANR_rmv_single)
							#clean_mensagem = re.sub(CLEANR_all_az09, '', clean_mensagem)

							mensagem_instance = mensagem_instance.replace(' ', '')
							clean_mensagem = clean_mensagem.replace(' ', '')

							#mensagem_instance = '\n'.join(mensagem_instance)
							with open('regrex.html', 'w', encoding="utf-8") as f:
								f.write(mensagem_instance)
							
							print(mensagem_instance)
							print('--------------------------------------------------------')
							print(clean_mensagem[0-6])
							print('\n-search----------------------------------------------------')

							print(re.search(clean_mensagem, mensagem_instance))
							find_already_sent = re.search(clean_mensagem, mensagem_instance)
							if find_already_sent is not None:
								print('HOLY SHIT')
								
								time.sleep(10)
							else:
								print('message not found')
								time.sleep(10)
								#METODO CAPTURE SPACE
								with try_catch(f'{contatos_["contatos"][contagem]}'):
									espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
									espaco_enviar.click()
									time.sleep(1)
									for _ in listar_imgs:
										time.sleep(1)
										actions = ActionChains(self.google)
										actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
										time.sleep(1)
								#METODO ENVIA TEXTO
								with try_catch(f"{contatos_['contatos'][contagem]}"):
									espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.ESPACO_ENVIAR_MSG))
									for part in texto_p_enviar.split('/n'):
										with try_catch(f"{contatos_['contatos'][contagem]}"):
											espaco_enviar.send_keys(part)
											time.sleep(1)
										ActionChains(self.google).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
										time.sleep(1)
									botao_enviar = wait.until(EC.presence_of_element_located(GetLocator.BOTAO_ENVIAR_IMG))
									botao_enviar.click()
									time.sleep(1)
						except Exception as e:
							print(f'is not to came here {e}')
							with open('unique_out.txt', 'w') as f:
								f.write(f"{contatos_['contatos'][contagem]}")
						

						contagem += 1

					except Exception as e:
						#print(f"{contatos_['contatos'][contagem]}")
						with open('unique_out.txt', 'a') as ef:
							ef.write(f"{contatos_['contatos'][contagem]}")
						#PULAR ERRO. NAO ENCONTROU contato
						contagem += 1
						#print(f'contagem de contatos {contagem}')
						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()
						time.sleep(2)
					btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
					btn_clear.click()

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
						
						contatos_['contatos'][contagem] = str(contatos_['contatos'][contagem])

						btn_search.send_keys(contatos_['contatos'][contagem])
						#************************************************************
						#PAUSE INFINITO
						time.sleep(.53)
						btn_search.send_keys(Keys.ARROW_DOWN)

						if (self.google.find_element_by_class_name('_2_TVt')):
							pass
							#print(f"\nCONTATO Achado {contatos_['contatos'][contagem]}")
						else:
							pass
							#print(f"{contatos_['contatos'][contagem]}")
						ctt_selected = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2_TVt')))
						ctt_selected.click()
						selected_name = nome_localizado(str(ctt_selected.get_attribute('innerHTML')))
						info_ultimo_contato = extrair_info_ultima_conversa(str(ctt_selected.get_attribute('innerHTML')))

						lista_contatos_info.append(str(info_ultimo_contato))
						lista_contatos_.append(str(selected_name).replace(',', ''))
						time.sleep(1)
						btn_clear = wait.until(EC.presence_of_element_located(GetLocator.CLEAR_BUTTON))
						btn_clear.click()

						time.sleep(5)

						try:
							pass
							#espaco_enviar = wait.until(EC.presence_of_element_located(GetLocator.TEXT_BOX_CHAT))
							#espaco_enviar.send_keys(texto_p_enviar)

							#box_buscador = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
							#box_buscador.click()
						except Exception as e:
							#pass
							#print(f'FALHA AO ABRIR CHAT {e}')
							self.google.quit()
					except Exception as e:
						#pass
						#print(f'FALHA  App Whats. Não achei algum elemento {e}')
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
	
	O_BETA = (By.XPATH, '//*[@id="side"]/header/div[1]/div')#'//*[@id="side"]/header/div[1]/div[2]/b')
	"""
		span: TEXT 'beta'
	"""
	
	BTN_CHAT = (By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[2]/div')
	"""
		button: DIV
	"""
	#tab_index_contact_key N USADO AINDA
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
	ENTRADA_ENVIAR_MSG = (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
	"""
		block: DIV
	"""
	TEXTO_TELA_PRINCIPAL_MSG = (By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]')

	"""
		INPUT: BUTTON
	"""
	BOTAO_ENVIAR_IMG = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')
	"""
		block: DIV
	"""
	ESPACO_ENVIAR_MSG = (By.XPATH,'//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')

	"""
	
	"""
	BOTAO_CANCELAR_IMG = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[1]/div[1]')