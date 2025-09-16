import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.temporadalivre.com/aluguel-temporada/brasil/sao-paulo/guaruja'

print("Iniciando o navegador com Selenium...")
# Configura e inicia o navegador Chrome de forma automatizada
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Acessa a URL
driver.get(url)

# --- PONTO CRUCIAL ---
# Espera 5 segundos para dar tempo do JavaScript do site carregar os anúncios
print("Aguardando o conteúdo da página carregar (5 segundos)...")
time.sleep(5) 

# Pega o HTML da página DEPOIS que o JavaScript já rodou
html_content = driver.page_source
print("Conteúdo HTML capturado!")

# Fecha o navegador que o Selenium abriu
driver.quit()

# Agora o resto é o mesmo que já fizemos, mas com o HTML correto
soup = BeautifulSoup(html_content, 'html.parser')

# Usando o seletor que você mesmo descobriu, que sabemos que é parte do anúncio
anuncios = soup.find_all('div', class_='description_container')

print(f"\nEncontramos {len(anuncios)} anúncios na primeira página.\n---")

lista_imoveis = []

for anuncio in anuncios:
    titulo = anuncio.find('span', class_='title').text.strip()
    localizacao = anuncio.find('div', class_='location').text.strip()
    
    preco_tag = anuncio.find('span', attrs={'data-behavior': 'rate'})
    preco = preco_tag.text.strip() if preco_tag else "A consultar"
    
    # O link é mais difícil de pegar agora, pois não está dentro deste container.
    # Vamos focar em pegar os dados de texto primeiro. Deixaremos o link para depois.
    
    imovel = {
        'titulo': titulo,
        'preco_diaria': preco,
        'localizacao': localizacao
    }
    lista_imoveis.append(imovel)
    
    print(f"Título: {titulo}")
    print(f"Preço: R$ {preco} a diária")
    print(f"Localização: {localizacao}\n---")

if lista_imoveis:
    df_imoveis = pd.DataFrame(lista_imoveis)
    df_imoveis.to_csv('imoveis_guaruja.csv', index=False, encoding='utf-8-sig')
    print("Dados salvos com sucesso no arquivo 'imoveis_guaruja.csv'!")