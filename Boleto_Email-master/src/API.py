from flask import Flask, request, jsonify
from imap_tools import MailBox
from PyPDF2 import PdfReader
from datetime import datetime
import os
import re
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)  # Adiciona suporte ao CORS para todos os endpoints

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///boletos.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Boleto(Base):
    __tablename__ = 'boletos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(String, nullable=False)
    vencimento = Column(String, nullable=False)
    beneficiario = Column(String, nullable=False)
    status = Column(Boolean, default=False)

Base.metadata.create_all(engine)

def fetch_boletos(username, password):
    try:
        with MailBox("imap.gmail.com").login(username, password, initial_folder="INBOX") as mailbox:
            for email in mailbox.fetch(reverse=True):
                if email.attachments:
                    for attachment in email.attachments:
                        if attachment.filename.lower().endswith(".pdf") and "boleto" in attachment.filename.lower():
                            with open("temporario.pdf", "wb") as arquivo_pdf:
                                arquivo_pdf.write(attachment.payload)

                            try:
                                with open("temporario.pdf", "rb") as arquivo_pdf:
                                    leitor_pdf = PdfReader(arquivo_pdf)
                                    texto = ""
                                    for page in leitor_pdf.pages:
                                        texto += page.extract_text()

                                padrao_codigo_barra=re.compile(r"\d+\.\d+.+\d+\.\d+.+\d+\.\d+.+\d.+\d+")
                                codigo_barra=re.finditer(padrao_codigo_barra,texto)
                                for item in codigo_barra:
                                    codigo_barra=item
                                padrao_mais=re.compile(r'\(\+\)')
                                mais=re.finditer(padrao_mais,texto)
                                for item in mais:
                                    mais=item
                                if codigo_barra.start()>mais.end():
                                    codigo_barra=re.search(padrao_codigo_barra,texto)
                                subtexto=texto[codigo_barra.start():]

                                padrao_valor=re.compile(r'.?\d.+,\d+')
                                Valor = re.findall(padrao_valor, subtexto)

                                primeiro_valor = Valor[0] if Valor else 'Nenhum valor monetário encontrado.'

                                padrao_data = r'\d{2}/\d{2}/\d{4}'
                                datas_encontradas = re.findall(padrao_data, subtexto)

                                datas_convertidas = [datetime.strptime(data, '%d/%m/%Y') for data in datas_encontradas]
                                vencimento = max(datas_convertidas).strftime('%d/%m/%Y') if datas_convertidas else 'Nenhuma data encontrada.'
                                    
                                padrao_beneficiario = re.compile(r'[bB][eE][nN][eE][fF][iI][cC][iI][aáAÁ][rR][iI][oO]')
                                beneficiario_match = re.search(padrao_beneficiario, texto)
                                    
                                padrao_beneficiario = re.compile(r'[bB][eE][nN][eE][fF][iI][cC][iI][aáAÁ][rR][iI][oO]')
                                beneficiario_match = re.search(padrao_beneficiario, texto)

                                if beneficiario_match:
                                    benef_txt = texto[beneficiario_match.end():]
                                    padrao_beneficiario_nome = re.compile(r'[A-ZÇÃÁÚ/ ]+')
                                    beneficiarios = re.findall(padrao_beneficiario_nome, benef_txt)

                                    beneficiario2 = [nome for nome in beneficiarios if len(nome) > 4 and 'CPF' not in nome]

                                    if len(beneficiario2) > 1:
                                        if len(beneficiario2[0]) > len(beneficiario2[1]):
                                            beneficiario_final = beneficiario2[0]
                                        else:
                                            beneficiario_final = beneficiario2[1]
                                    elif beneficiario2:
                                        beneficiario_final = beneficiario2[0]
                                    else:
                                        beneficiario_final = 'Beneficiário não encontrado'
                                else:
                                    beneficiario_final = 'Beneficiário não encontrado'
                            finally:
                                os.remove("temporario.pdf")

                            # Verifica se o boleto já existe no banco de dados
                            existing_boleto = session.query(Boleto).filter_by(
                                valor=primeiro_valor,
                                vencimento=vencimento,
                                beneficiario=beneficiario_final
                            ).first()

                            if not existing_boleto:
                                boleto = Boleto(
                                    valor=primeiro_valor,
                                    vencimento=vencimento,
                                    beneficiario=beneficiario_final
                                )
                                session.add(boleto)
                                session.commit()
                                print('E-mail processado com sucesso. Valor do Documento:', primeiro_valor, 'Vencimento:', vencimento, 'Beneficiário:', beneficiario_final)
                            else:
                                print('Boleto já existe no banco de dados. Ignorando duplicata...')
    except Exception as e:
        print("Erro ao fazer login:", e)
        return {'error': 'Erro ao acessar o e-mail. Verifique suas credenciais ou as configurações do servidor de e-mail.'}, 401

@app.route('/boleto', methods=['POST'])
def fetch_boletos_route():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Por favor, forneça nome de usuário e senha do e-mail'}), 400

    username = data['username']
    password = data['password']

    result = fetch_boletos(username, password)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({'message': 'Boletos fetched successfully'}), 200

@app.route('/boleto', methods=['GET'])
def get_boleto_info():
    boletos = session.query(Boleto).all()
    response = jsonify([{
        'id': boleto.id,
        'Valor do Documento': boleto.valor,
        'Vencimento': boleto.vencimento,
        'Beneficiário': boleto.beneficiario,
        'status': boleto.status
    } for boleto in boletos])
    response.headers.add('Access-Control-Allow-Origin', '*')  # Adiciona o cabeçalho CORS
    return response

@app.route('/boleto/<int:id>', methods=['PUT'])
def update_boleto_status(id):
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': 'Por favor, forneça o status do boleto'}), 400

    boleto = session.query(Boleto).filter_by(id=id).first()
    if not boleto:
        return jsonify({'error': 'Boleto não encontrado'}), 404

    boleto.status = data['status']
    session.commit()
    return jsonify({'message': 'Status do boleto atualizado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
