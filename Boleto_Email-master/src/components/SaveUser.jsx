import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../CSS/SaveUser.css';
import logo from '../logo512.png';  // Ajuste o caminho conforme necessário

function SaveUser() {
  const [text, setText] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    localStorage.setItem('user', text);
    navigate(`/Email?text=${encodeURIComponent(text)}`);
  };

  return (
    <div className="contain">
      <div className="header">
        <img src={logo} alt="Logo" className="logo" />
        <h1 className="site-name">BANKSLY</h1>
      </div>
      <div className="content">
        <p>
          Nosso objetivo é ajudar você a gerenciar e organizar todos os boletos que você recebe por email. Sabemos que é fácil deixar esses documentos importantes de lado, especialmente quando eles chegam com frequência.
        </p>
        <p>
          Com nosso site, você pode:
        </p>
        <ul>
          <li><strong>Centralizar os Boletos:</strong> Visualize todos os seus boletos em um só lugar.</li>
          <li><strong>Facilitar o Acesso:</strong> Consulte os detalhes dos boletos rapidamente, sem precisar procurar em sua caixa de entrada.</li>
        </ul>
        <p>
          Comece agora mesmo! Cadastre seus boletos ou envie os detalhes dos boletos que você deseja organizar. Estamos aqui para simplificar sua vida financeira.
        </p>
        <div className="form-container">
          <p>Por favor, digite seu nome abaixo e clique em "Enviar" para continuar.</p>
          <form onSubmit={handleSubmit}>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Digite seu nome aqui..."
            />
            <button type="submit">Enviar</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SaveUser;
