from glob import glob
import re
import flet as ft
import PyPDF2
import os
from PyPDF2 import PdfReader
from imap_tools import MailBox
from datetime import datetime

lista=[]       
def banco_codigo_barra():
    banco_final=''
    lista_bancos={'Banco do Brasil':1, 'Banco Santander':33, 'Caixa Econômica Federal':104, 'Banco Bradesco':237,
                'Banco Itaú':341,
                'Banco Mercantil do Brasil':389,'Banco Safra':422,'Banco Rural':453,'Banco Rendimento':633,
                'Banco Citibank':745, 'Banco ABC':246,
                'Banrisul':41}

    padrao_codigo_barra=re.compile(r"\d{5}\.\d{5}.+\d{5}\.\d{5}.+\d{5}\.\d{5}.+\d{1}.+\d")


    codigo_barra=re.findall(padrao_codigo_barra,texto)
    codigo_barra=codigo_barra[0]
    if '-' in codigo_barra:
        codigo_barra=codigo_barra[:-5]


    codigo_barra=str(codigo_barra)
    padrao_banco=re.compile(r'^\d{3}')
    banco=re.search(padrao_banco,codigo_barra)
    banco=int(banco.group(0))
    for bancos,codigos in lista_bancos.items():
        if codigos==banco:
            banco_final=bancos
            
    if banco_final=='':
        banco_final='Não foi possível identificar nenhum banco.'
    codigo_barra=codigo_barra.replace(' ','')
    codigo_barra=codigo_barra.replace('  ','')
    codigo_barra=codigo_barra.replace('.','')
    

    linha_digitavel=codigo_barra
    codigo_barra=[]
    codigo_barra.append(linha_digitavel[:4])
    codigo_barra.append(linha_digitavel[32:])
    codigo_barra.append(linha_digitavel[4:9])
    codigo_barra.append(linha_digitavel[10:16])
    codigo_barra.append(linha_digitavel[16:20])
    codigo_barra.append(linha_digitavel[21:31])
    codigo_barra=str(codigo_barra)

    codigo_barra=codigo_barra.replace(' ','')
    codigo_barra=codigo_barra.replace('  ','')
    codigo_barra=codigo_barra.replace(',','')
    codigo_barra=codigo_barra.replace("'",'')
    codigo_barra=codigo_barra.replace('[','')
    codigo_barra=codigo_barra.replace(']','')
    codigo_barra_final=codigo_barra
    
    
    lista.append(codigo_barra_final)
    lista.append(linha_digitavel)
    lista.append(banco_final)

def valor_datas():
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

    if Valor:
        valor_final=Valor[0]
        
    else:
        valor_final='Nenhum valor monetário encontrado.'
    lista.append(valor_final)

    padrao_data = r'\d{2}/\d{2}/\d{4}'
    datas_encontradas = re.findall(padrao_data, subtexto)

    datas_convertidas = [datetime.strptime(data, '%d/%m/%Y') for data in datas_encontradas]

    if datas_convertidas:
        data_mais_recente = max(datas_convertidas)
        vencimento_final=data_mais_recente.strftime('%d/%m/%Y')
    else:
        vencimento_final='Nenhuma data encontrada.'
    
    
    if datas_convertidas:
        data_mais_recente = min(datas_convertidas)
        emissao_final=data_mais_recente.strftime('%d/%m/%Y')
    else:
        emissao_final='Nenhuma data encontrada.'
   
    
    lista.append(vencimento_final)
    lista.append(emissao_final)
    
        
def beneficiario():
    padrao_beneficiario=re.compile(r'[bB][eE][nN][eE][fF][iI][cC][iI][aáAÁ][rR][iI][oO]')
    beneficiario=re.search(padrao_beneficiario,texto)

    benef_txt=(texto[beneficiario.end():])

    padrao_beneficiario=re.compile(r'[A-ZÇÃÁÚ/ ]+')
    beneficiario=re.findall(padrao_beneficiario,benef_txt)

    beneficiario2=[]

    for i,escrita in enumerate(beneficiario):
        if len(beneficiario[i])>4 and 'CPF' not in beneficiario[i]:
            beneficiario2.append(beneficiario[i])
        

    if len(beneficiario2[0])>len(beneficiario2[1]):
        beneficiario_final=beneficiario2[0]
    if len(beneficiario2[1])>len(beneficiario2[0]):
        beneficiario_final=beneficiario2[1]
    beneficiario_final=beneficiario_final
    
    lista.append(beneficiario_final)
lista2=[]
i=1
caminho_arquivo=sorted(glob(r'C:/Users/bruno/Documents/pdf/*.pdf'))
for item in caminho_arquivo:
    with open(item, "rb") as pdf:
        leitor_pdf = PyPDF2.PdfReader(pdf)
        texto = ""
        for pagina in leitor_pdf.pages:
            texto += pagina.extract_text()
    banco_codigo_barra()
    valor_datas()
    beneficiario()
    lista2.insert(i,lista)
    i+=1
    lista=[]
for item in caminho_arquivo:
    print(item)
    i=caminho_arquivo.index(item)
    print(lista2[i])
# lista[x][0]= Código de Barra
# lista[x][1]= Linha Digitável
# lista[x][2]= Banco
# lista[x][3]= Valor
# lista[x][4]= Vencimento
# lista[x][5]= Emissão
# lista[x][6]= Beneficiário

def codigo_barra_f(boleto):
    codigo_barra=lista2[boleto][0]
    return codigo_barra
def linha_digitavel_f(boleto):
    linha_digitavel=lista2[boleto][1]
    return linha_digitavel
def banco_f(boleto):
    banco=lista2[boleto][2]
    return banco
def valor_f(boleto):
    valor=lista2[boleto][3]
    return valor
def vencimento_f(boleto):
    vencimento=lista2[boleto][4]
    return vencimento
def emissao_f(boleto):
    emissao=lista2[boleto][5]
    return emissao
def beneficiario_f(boleto):
    beneficiario=lista2[boleto][6]
    return beneficiario
