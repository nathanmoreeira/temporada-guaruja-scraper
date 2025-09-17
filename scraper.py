import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente (se existirem)
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Conectando ao Supabase (se as chaves foram fornecidas)
if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client, Client
    print("Conectando ao banco de dados Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Conexão bem-sucedida!")
else:
    supabase = None
    print("Credenciais do Supabase não encontradas. Os dados serão apenas impressos e salvos em CSV.")

url = 'https://www.temporadalivre.com/aluguel-temporada/brasil/sao-paulo/guaruja'

print("Iniciando o navegador com Selenium...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

print("Aguardando o conteúdo da página carregar (5 segundos)...")
time.sleep(5) 

html_content = driver.page_source
print("Conteúdo HTML capturado!")
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# --- AQUI ESTÁ A MUDANÇA FINAL ---
# Usando a coordenada mais completa que você encontrou!
anuncios = soup.find_all('a', class_='show-details')

print(f"\nEncontramos {len(anuncios)} anúncios na primeira página.\n---")

lista_imoveis = []
total_inserido = 0

for anuncio in anuncios:
    link = "https://www.temporadalivre.com" + anuncio['href']
    
    # As informações de texto estão dentro da tag <div class="property">
    propriedade = anuncio.find('div', class_='property')
    
    if propriedade:
        titulo = propriedade.find('span', class_='title').text.strip()
        localizacao = propriedade.find('div', class_='location').text.strip()
        
        preco_tag = propriedade.find('span', attrs={'data-behavior': 'rate'})
        preco = preco_tag.text.strip() if preco_tag else "A consultar"
        
        imovel_data = {
            'titulo': titulo,
            'preco_diaria': f"R$ {preco}",
            'localizacao': localizacao,
            'link': link
        }
        lista_imoveis.append(imovel_data)

        # Se a conexão com o Supabase existir, insere os dados
        if supabase:
            try:
                data, count = supabase.table('imoveis').insert(imovel_data).execute()
                print(f"Inserido no DB: {titulo}")
                total_inserido += 1
            except Exception as e:
                print(f"Falha ao inserir o imóvel '{titulo}'. Erro: {e}")
        else:
            print(f"Título: {titulo} | Preço: R$ {preco}")

# Salvando em CSV como backup
if lista_imoveis:
    df_imoveis = pd.DataFrame(lista_imoveis)
    df_imoveis.to_csv('imoveis_guaruja.csv', index=False, encoding='utf-8-sig')
    print("\nDados salvos com sucesso no arquivo 'imoveis_guaruja.csv'!")

if supabase:
    print(f"\n--- FIM DA EXECUÇÃO ---\nTotal de {total_inserido} novos imóveis inseridos no banco de dados.")