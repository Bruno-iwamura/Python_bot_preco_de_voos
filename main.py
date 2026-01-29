import requests
import pandas as pd
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime
from amadeus import Client, ResponseError
import os
from dotenv import load_dotenv


#----------> Configs

load_dotenv()

client_id = os.getenv('AMADEUS_ID')
client_secret = os.getenv('AMADEUS_SECRET')
email_password = os.getenv('EMAIL_PASSWORD')


EmailDestino = 'iw.bruno@live.com'
ArquivoLog = 'historico_de_precos.csv'

#---------> API configs

amadeus = Client(
    client_id=client_id,
    client_secret=client_secret
)

#Lista de dicionarios a serem pesquisados

WISHLIST = [
    {'origem': 'GRU', 'destino': 'CDG', 'data': '2026-05-15', 'alvo_brl': 3500},
    {'origem': 'GRU', 'destino': 'JFK', 'data': '2026-06-10', 'alvo_brl': 2800},
    {'origem': 'GRU', 'destino': 'LIS', 'data': '2026-09-20', 'alvo_brl': 3200}
]

DICIONARIO_PAISES = {
    'GRU': 'Brazil',
    'CDG': 'France',
    'JFK': 'United States',
    'LIS': 'Portugal',
    'EZE': 'Argentina',
    'MAD': 'Spain'
}

cache_localidades = {}

def obter_pais_por_codigo(codigo_iata):
    # 1. Tenta no nosso dicionário manual primeiro (mais rápido e garantido)
    if codigo_iata in DICIONARIO_PAISES:
        return DICIONARIO_PAISES[codigo_iata]
    
    # 2. Se não estiver lá, tenta no cache de buscas anteriores
    if codigo_iata in cache_localidades:
        return cache_localidades[codigo_iata]
    
    # 3. Por último, tenta a API
    try:
        # Mudamos de keyword para buscar especificamente por IATA
        response = amadeus.reference_data.location(codigo_iata).get()
        
        if response.data:
            nome_pais = response.data['address']['countryName']
            cache_localidades[codigo_iata] = nome_pais
            return nome_pais
    except Exception as e:
        print(f"⚠️ API não encontrou país para {codigo_iata}. Usando 'Desconhecido'.")
    
    return "Desconhecido"

def busca_precos(origem, destino, data_partida):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origem,
            destinationLocationCode=destino,
            departureDate=data_partida,
            adults=1,
            max=5 
        )
        
        if not response.data:
            return []

        # Traduzindo os códigos das companhias 

        companhias = response.result.get('dictionaries', {}).get('carriers', {})
        pais_origem = obter_pais_por_codigo(origem)
        pais_destino = obter_pais_por_codigo(destino)
        
        lista_ofertas = []
        for voo in response.data:
            codigo_cia = voo['itineraries'][0]['segments'][0]['carrierCode']
            lista_ofertas.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "origem": origem,
                "pais_origem": pais_origem,
                "destino": destino,
                "pais_destino": pais_destino,
                "data_voo": data_partida,
                "companhia": companhias.get(codigo_cia, codigo_cia),
                "preco_original": float(voo['price']['total']),
                "moeda": voo['price']['currency'],
                "assentos": voo.get('numberOfBookableSeats', 0)
            })
        return lista_ofertas

    except ResponseError as error:
        print(f"Erro API na rota {origem}->{destino}: {error}")
        return []
    
def salvar_log(lista_ofertas):
    if not lista_ofertas: return
    try:
        df = pd.DataFrame(lista_ofertas)
        colunas = ['timestamp', 'origem','pais_origem', 'destino','pais_destino', 'data_voo', 'companhia', 'preco_original', 'moeda', 'preco_brl', 'assentos']
        file_exists = os.path.isfile(ArquivoLog)
        df.to_csv(ArquivoLog, mode='a', index=False, header=not file_exists, columns=colunas)
        
    except PermissionError:
        print(f"⚠️ ERRO DE PERMISSÃO: O arquivo '{ArquivoLog}' está aberto no Excel ou outro programa.")
        print("Feche o arquivo para que o bot possa salvar os dados no próximo ciclo.")
    except Exception as e:
        print(f"❌ Erro inesperado ao salvar: {e}")
def enviar_alerta(preco, moeda, destino, data):
    
    try:
        msg = EmailMessage()
        msg.set_content(f"ALERTA DE PREÇO! Passagem para {destino} encontrada por R$ {preco} em {data}")
        msg['Subject'] = f"Oportunidade de Viagem para {destino}!"
        msg['From'] = "bruno.s.iwamura@gmail.com"
        msg['To'] = EmailDestino

        # CONFIGURAÇÃO DE ENVIO (Descomente e use sua senha de app se quiser testar o envio real)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("bruno.s.iwamura@gmail.com", email_password)
            smtp.send_message(msg)
        
        print(f"Notificação lógica disparada: Preço {moeda} {preco} está abaixo do alvo!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def pegar_cotacao_euro():
    # Busca a cotação atual do Euro para conversão
    try:
        url = "https://economia.awesomeapi.com.br/last/EUR-BRL"
        response = requests.get(url).json()
        return float(response['EURBRL']['bid'])
        
    except:
        print("Erro ao buscar câmbio, usando o valor padrão 5.50")
        return 5.50

print(f"🚀 Bot iniciado! Monitorando voos para {EmailDestino}...")

while True:
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Buscando as 5 melhores ofertas...")
    
    cotacao_atual = pegar_cotacao_euro()

    print(f"Cotação atual: R$ {cotacao_atual}")

    for rota in WISHLIST:
        print(f"🔍 Verificando: {rota['origem']} -> {rota['destino']} para {rota['data']}...")
        ofertas = busca_precos(rota['origem'], rota['destino'], rota['data'])

        if ofertas:
            for o in ofertas:
                o['preco_brl'] = round(o['preco_original'] * cotacao_atual, 2)

            salvar_log(ofertas)
            melhor_preco = ofertas[0]['preco_brl']
            print(f"   ✅ Melhor preço encontrado: R$ {melhor_preco}")

        # Lógica de alerta baseada no MELHOR preço encontrado
            if melhor_preco <= rota['alvo_brl']:
                print(f"   🔔 ALERTA: Preço alvo atingido para {rota['destino']}!")
                enviar_alerta(melhor_preco, "BRL",rota['destino'],rota['data'])

        time.sleep(2)
    
    print("Aguardando 1 hora...")
    time.sleep(3600)