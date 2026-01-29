# ✈️ Advanced Flight Price Monitor & Pipeline

Este projeto é um pipeline de Engenharia de Dados em Python que automatiza o monitoramento de passagens aéreas para múltiplas rotas internacionais. O bot integra dados de voos, câmbio em tempo real e enriquecimento geográfico para gerar insights prontos para Business Intelligence (Power BI/Tableau).


## 🌟 Diferenciais Técnicos

- **Multi-Route Tracking**: Monitora uma `WISHLIST` de destinos simultaneamente em um único ciclo de execução.
- **Data Enrichment**: 
    - Converte preços dinamicamente de EUR/USD para **BRL** via AwesomeAPI.
    - Traduz códigos aeroportuários (IATA) para nomes de **Países** usando Reference Data.
- **Robustez e Segurança**:
    - Gestão de credenciais via variáveis de ambiente (`.env`).
    - Tratamento de erros de permissão (ex: arquivo aberto no Excel).
    - Sistema de Cache local para otimizar chamadas de API.
- **Tidy Data Architecture**: Logs salvos em formato longo, ideal para análise de séries temporais e dashboards.

## 🛠️ Stack Tecnológica

* **Linguagem**: Python 3.13
* **Libs Principais**: Pandas, Amadeus SDK, Requests, Python-Dotenv
* **Protocolos**: REST APIs, SMTP (TLS/SSL)

## 📋 Pré-requisitos

1.  Obtenha suas chaves de API em [Amadeus for Developers](https://developers.amadeus.com/).
2.  Crie uma **Senha de App** no seu Gmail para o envio de alertas.
3.  Instale as dependências:
    ```bash
    pip install pandas amadeus requests python-dotenv
    ```

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:
   ```text
   AMADEUS_ID=seu_client_id
   AMADEUS_SECRET=seu_client_secret
   EMAIL_PASSWORD=sua_senha_de_app_gmail
