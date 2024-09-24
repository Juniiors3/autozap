from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import urllib
import datetime as dt
from datetime import date,datetime,timedelta
import logging
import os
#Criado por Júniors3
logging.basicConfig(level=logging.INFO,filename="Log.log", format='%(asctime)s - %(levelname)s - %(message)s')
hora_ent = str(input('Digite a hora:  '))
min_ent = str(input('Digite os minutos:  '))
logging.info('entrada da hora') 
contato = pd.read_excel(r"G:\PROGRAMACAO2\AUTOMACAO V1.3 0209\BDCLIENTES.xlsx")#caminho onde ficará o arquivo bd(excel)
logging.info('importação do arquivo')
navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")
logging.info('abertura do navegador')


h1 = hora_ent
h2 = min_ent
tempo = h1+':'+h2
agora = ''
print('Aguardando...')
c = 0

while agora <= tempo:
    c +=1
    #print(c)
    time.sleep(1)
    agora = datetime.now().strftime('%H:%M:%S')
    #print(agora)

while len(navegador.find_elements(By.ID, 'side')) <1:
    time.sleep(1)
time.sleep(2)
logging.info('Carregamento com sucesso!')
print('Deu certo')

for i, mensagem in enumerate(contato['MENSAGEM']):
    pessoa = contato.loc[i,'PESSOA']
    numero = contato.loc[i,'TELEFONE']
    arquivo = contato.loc[i,'ARQUIVO']
    texto = urllib.parse.quote(f"{pessoa} {mensagem}") # type: ignore
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    time.sleep(2)
    while len(navegador.find_elements(By.ID, 'side')) <1:
        time.sleep(1)
    time.sleep(2)

    if len(navegador.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) == 0: #verifica se o numero ta ok
        print('conferencia ok')
        time.sleep(5)
        print( len(navegador.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')))
        if len(navegador.find_elements(By.XPATH,'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) > 0:
            print('Numero errado')
        navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click()
        print(f'Enviado com Sucesso!{pessoa},{arquivo}')
        time.sleep(5)

        if arquivo != 'N':
            caminho_completo = os.path.abspath(f"G:\PROGRAMACAO2\AUTOMACAO V1.3 0209\{arquivo}")
            print(f'Pessoa{pessoa}')
            navegador.find_element(By.XPATH,
                                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span').click() # clicar no menu (anexo)
            print('clicou em anexo')
            time.sleep(4)
            #navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[4]/li/div/input').send_keys(caminho_completo)# caminho do arquivo documento)
            navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/input').send_keys(caminho_completo)# caminho do arquivo de foto)

            print('busca o anexo')                      
            time.sleep(10)

            #navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span').send_keys(Keys.ENTER)
            
            
            navegador.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div').click()#envia msg e anexo
            print('envia a msg e anexo')
            print(f'enviado para {pessoa}')
            time.sleep(5)



navegador.quit()
