import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './CSS/App.css';

function BoletosAseremPagos({ boletos }) {
  return (
    <div className="contas-hoje">
      <h2>Boletos a serem pagos hoje</h2>
      {boletos.map((boleto, index) => (
        <div key={index} className="conta-hoje">
          <div className="data">{boleto['Vencimento']}</div>
          <div className="detalhes">
            <p>{boleto['Beneficiário']}</p>
            <p>{boleto['Valor do Documento']}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

function BoletoInfo() {
  const location = useLocation();
  const nomeUsuario = location.state?.name || 'Usuário';

  const [boletos, setBoletos] = useState(location.state?.boletos || []);
  const [contasHoje, setContasHoje] = useState([]);
  const [totalBoletos, setTotalBoletos] = useState(0);
  const [boletosPagos, setBoletosPagos] = useState(0);
  const [boletosNaoPagos, setBoletosNaoPagos] = useState(0);

  const obterDataHoje = () => {
    const hoje = new Date();
    const dia = String(hoje.getDate()).padStart(2, '0');
    const mes = String(hoje.getMonth() + 1).padStart(2, '0');
    const ano = hoje.getFullYear();
    return `${dia}/${mes}/${ano}`;
  };

  useEffect(() => {
    fetch('http://127.0.0.1:5000/boleto')
      .then(response => response.json())
      .then(data => {
        setBoletos(data);
        const hoje = obterDataHoje();
        const contasDoDia = data.filter(boleto => boleto['Vencimento'] === hoje);
        setContasHoje(contasDoDia);

        const boletosPagosCount = data.filter(boleto => boleto.status).length;
        setTotalBoletos(data.length);
        setBoletosPagos(boletosPagosCount);
        setBoletosNaoPagos(data.length - boletosPagosCount);
      })
      .catch(error => console.error('Erro ao buscar informações do boleto:', error));
  }, []);

  const handleStatusChange = (index) => {
    const updatedBoletos = [...boletos];
    updatedBoletos[index].status = !updatedBoletos[index].status;

    // Atualiza o estado local
    setBoletos(updatedBoletos);

    // Envia a atualização para o backend
    fetch(`http://127.0.0.1:5000/boleto/${updatedBoletos[index].id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: updatedBoletos[index].status }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error('Erro ao atualizar o status do boleto:', data.error);
        } else {
          console.log('Status do boleto atualizado com sucesso:', data.message);
        }
      })
      .catch(error => console.error('Erro ao enviar atualização para o backend:', error));
  };

  return (
    <div className="container">
      <div className="left-section">
        <h1>BANKSLY</h1>
        <div className="resumo">
          <div className="numero">
            <h2>Total de Boletos</h2>
            <p>{totalBoletos}</p>
          </div>
          <div className="numero">
            <h2>Contas a Pagar</h2>
            <p>{boletosNaoPagos}</p>
          </div>
          <div className="numero">
            <h2>Contas Pagas</h2>
            <p>{boletosPagos}</p>
          </div>
        </div>
        <div className="tabela-boletos">
          <h2>Todas as Contas</h2>
          {boletos.length > 0 ? (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Beneficiário</th>
                    <th>Vencimento</th>
                    <th>Valor do Documento</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {boletos.map((boleto, index) => (
                    <tr key={index}>
                      <td>{boleto['Beneficiário']}</td>
                      <td>{boleto['Vencimento']}</td>
                      <td>{boleto['Valor do Documento']}</td>
                      <td>
                        <button
                          className={boleto.status ? 'status-button pago' : 'status-button nao-pago'}
                          onClick={() => handleStatusChange(index)}
                        >
                          {boleto.status ? 'Pago' : 'Não pago'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>Nenhum boleto encontrado.</p>
          )}
        </div>
      </div>
      <div className="right-section">
        <BoletosAseremPagos boletos={contasHoje} />
      </div>
    </div>
  );
}

export default BoletoInfo;
