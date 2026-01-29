# ✈️ Flight Price Monitor & Alert Bot

Este é um projeto de automação de dados desenvolvido em Python que monitora preços de passagens aéreas em tempo real, realiza conversão de moeda e notifica o usuário via e-mail sobre oportunidades de viagem.



## 🚀 Funcionalidades

- **Data Ingestion**: Consumo de dados reais de mais de 400 companhias aéreas através da API **Amadeus**.
- **Data Enrichment**: Integração com a **AwesomeAPI** para conversão automática de câmbio (EUR/USD para BRL).
- **Storage (Logs)**: Armazenamento estruturado de cada consulta em um arquivo `.csv` usando **Pandas**, criando um histórico de volatilidade.
- **Automated Alerting**: Sistema de notificação via **SMTP (Gmail)** que dispara alertas quando o preço atinge um valor alvo.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas**: Manipulação e estruturação de dados.
* **Amadeus Python SDK**: Conexão com a API de viagens.
* **Requests**: Consumo da API de câmbio.
* **Smtplib & Email.Message**: Automação de envios de e-mail.

## 📋 Pré-requisitos

Antes de rodar o script, você precisará:

1.  Uma conta no [Amadeus for Developers](https://developers.amadeus.com/) para obter seu `API Key` e `API Secret`.
2.  Uma **Senha de App** do Google (caso use Gmail) para o envio de e-mails via SMTP.
3.  Instalar as dependências:
    ```bash
    pip install pandas amadeus requests
    ```

## 🔧 Configuração e Uso

1.  Clone o repositório.
2.  No arquivo principal, insira suas credenciais da Amadeus:
    ```python
    amadeus = Client(client_id='SUA_CHAVE', client_secret='SEU_SEGREDO')
    ```
3.  Configure o `PrecoAlvo` e o `EmailDestino`.
4.  Execute o script:
    ```bash
    python monitor_voos.py
    ```

## 📊 Estrutura do Arquivo de Log

O bot gera um arquivo chamado `historico_de_precos.csv` com a seguinte estrutura, ideal para análises no **Power BI**:

| timestamp | companhia | origem | destino | preco | moeda | preco_brl |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-05-15 10:00:01 | Air France | GRU | CDG | 450.00 | EUR | 2745.00 |



## 📈 Próximos Passos

- [ ] Implementar suporte a múltiplos destinos simultâneos.
- [ ] Criar um Dashboard no Power BI para visualização da média móvel de preços.
- [ ] Adicionar tratamento de erros para diferentes moedas de origem.

## ✒️ Autor

* **Bruno Iwamura** - [Seu LinkedIn](https://linkedin.com/in/seu-perfil)