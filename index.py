import time
import pandas as pd
import openai  # Importa a biblioteca OpenAI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Configurar a chave de API do OpenAI
# openai.api_key = ''  # Substitua pela sua chave de API do OpenAI

# Função para abrir o navegador Chrome e acessar o YouTube
def abrir_youtube():
    # Inicializa o driver do Chrome
    driver = webdriver.Chrome()

    # Abre o YouTube
    driver.get("https://www.youtube.com")

    # Espera alguns segundos para o YouTube carregar completamente
    time.sleep(15)

    return driver

# Função para abrir a playlist do YouTube e clicar em "Reproduzir tudo"
def abrir_playlist_e_reproduzir(driver, url_playlist):
    # Navega para a URL da playlist do YouTube
    driver.get(url_playlist)

    # Espera alguns segundos para a playlist carregar completamente
    time.sleep(15)

    # Desce até o final da página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Encontra o botão "Reproduzir tudo" e clica nele
    try:
        play_all_button = driver.find_element_by_xpath("//*[contains(text(), 'Reproduzir tudo')]")
        play_all_button.click()
    except:
        print("Botão 'Reproduzir tudo' não encontrado.")

    # Espera alguns segundos para começar a reprodução
    time.sleep(10)

# Função para clicar no botão "TRANSCRIPT" e copiar a transcrição
def clicar_transcript_e_transcrever(driver):
    # Encontra o botão "TRANSCRIPT" e clica nele
    try:
        transcript_button = driver.find_element_by_xpath("//*[contains(text(), 'TRANSCRIPT')]")
        transcript_button.click()
    except:
        print("Botão 'TRANSCRIPT' não encontrado.")

    # Espera alguns segundos para a transcrição carregar
    time.sleep(15)

    # Seleciona todo o texto da transcrição
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'a')

    # Copia o texto selecionado
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'c')

    # Espera alguns segundos para a cópia
    time.sleep(5)

    # Cole o texto no ChatGPT
    transcrição = driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'v')

    # Espera alguns segundos
    time.sleep(5)

    # Envia a pergunta para o ChatGPT
    driver.find_element_by_tag_name('body').send_keys("Este texto está em acordo com todas as normas e leis brasileiras atuais?")
    driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)

    # Espera alguns segundos para a resposta do ChatGPT
    time.sleep(15)

    return transcrição

# Função para salvar os resultados em uma planilha Excel
def salvar_resultados(nome_video, transcrição, resposta_gpt):
    resultados = pd.DataFrame({
        "Nome do Vídeo": [nome_video],
        "Transcrição": [transcrição],
        "Resposta do GPT": [resposta_gpt]
    })
    resultados.to_excel("resultados.xlsx", index=False)

# URL da playlist do YouTube
url_playlist = "https://www.youtube.com/playlist?list=PL-AkrwhsMLD6IoC4HFISmsw8ZO4nJr27Y"

# Execução do processo completo
driver = abrir_youtube()
abrir_playlist_e_reproduzir(driver, url_playlist)
transcrição = clicar_transcript_e_transcrever(driver)
salvar_resultados("Nome do Vídeo", transcrição, "Resposta do GPT")
