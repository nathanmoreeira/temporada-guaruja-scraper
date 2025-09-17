import os
from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env que está na pasta raiz do projeto
load_dotenv()

# Pega as credenciais do Supabase do arquivo .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validação para garantir que as chaves foram carregadas
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Credenciais do Supabase não encontradas. Verifique seu arquivo .env na raiz do projeto.")

# Inicializa o aplicativo Flask e o cliente Supabase
app = Flask(__name__)
CORS(app)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("API conectada ao Supabase com sucesso!")

# Definindo o endpoint principal para buscar os imóveis
@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    try:
        # Seleciona todos os dados (*) da tabela 'imoveis', ordenados pelos mais recentes, com um limite de 100
        response = supabase.table('imoveis').select('*').order('created_at', desc=True).limit(100).execute()
        
        # A biblioteca do Supabase retorna os dados dentro de um atributo 'data'
        dados = response.data
        
        print(f"Encontrados {len(dados)} imóveis no banco de dados.")
        
        # Retorna os dados encontrados em formato JSON
        return jsonify(dados)

    except Exception as e:
        # Retorna uma mensagem de erro em formato JSON se algo der errado
        return jsonify({"error": str(e)}), 500

# Ponto de entrada para rodar a aplicação
if __name__ == '__main__':
    # Usando a porta 8000 para não conflitar com outras aplicações
    app.run(host='0.0.0.0', port=8000)