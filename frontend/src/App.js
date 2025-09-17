import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [imoveis, setImoveis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // useEffect é um "hook" do React que executa uma função
  // logo depois que o componente é renderizado na tela.
  // É o lugar perfeito para fazer nossa chamada de API.
  useEffect(() => {
    const fetchImoveis = async () => {
      try {
        // Chama a nossa API backend para buscar os imóveis
        const response = await axios.get('http://127.0.0.1:8000/imoveis');
        setImoveis(response.data); // Guarda a lista de imóveis no nosso estado
      } catch (err) {
        setError('Falha ao buscar dados da API. O backend (api/app.py) está rodando?');
        console.error(err);
      } finally {
        setLoading(false); // Para de carregar, independentemente do resultado
      }
    };

    fetchImoveis();
  }, []); // O array vazio [] garante que o useEffect rode apenas uma vez

  if (loading) {
    return <div className="App"><h1>Carregando anúncios...</h1></div>;
  }

  if (error) {
    return <div className="App"><h1>Erro: {error}</h1></div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporada Guarujá 🏖️</h1>
        <p>Últimos anúncios de aluguel de temporada encontrados para o Guarujá-SP.</p>
      </header>
      <main className="grid-container">
        {imoveis.map(imovel => (
          <div className="card" key={imovel.id}>
            <h2>{imovel.titulo}</h2>
            <p className="price">{imovel.preco_diaria}</p>
            <p className="location">{imovel.localizacao}</p>
            <a href={imovel.link} target="_blank" rel="noopener noreferrer" className="card-button">
              Ver Anúncio Original
            </a>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;