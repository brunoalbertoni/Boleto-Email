import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './CSS/email.css';

function Email() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const text = queryParams.get('text') || 'Usuário';

  const handleLogin = async (event) => {
    event.preventDefault();
    console.log('Iniciando requisição OPTIONS...');

    try {
      const optionsResponse = await fetch('http://127.0.0.1:5000/boleto', {
        method: 'OPTIONS',
      });

      if (optionsResponse.ok) {
        console.log('Requisição OPTIONS bem-sucedida');

        console.log('Iniciando requisição POST...');
        alert('Login bem-sucedido! Continue');
        const postResponse = await fetch('http://127.0.0.1:5000/boleto', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });

        if (postResponse.ok) {
          const boletosData = await postResponse.json();
          const nomeUsuario = name.trim() !== '' ? name : 'Usuário';
          console.log('Requisição POST bem-sucedida. Dados recebidos:', boletosData);

          console.log('Redirecionando para /app...');
          navigate('/app');
          
          // Exibir mensagem de sucesso
          
          ;
        } else {
          const errorData = await postResponse.json();
          console.error('Falha na requisição POST', errorData);
     
        }
      } else {
        console.error('Falha na requisição OPTIONS');
        ;
      }
    } catch (error) {
      console.error('Erro durante a requisição:', error);
      ;
    }
  };

  return (
    <div className='body'>
      <div className="containr">
        <h2>Seja bem-vindo, {text}!</h2>
        <form onSubmit={handleLogin}>
          <div className="label-container">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <label>Email:</label>
          </div>
          <div className="label-container">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <label>Senha:</label>
          </div>
          <button type="submit">Login</button>
          <button type="button" className="btn_cont" onClick={() => navigate('/app')}>
            Continuar
          </button>
        </form>
      </div>
    </div>
  );
}

export default Email;
