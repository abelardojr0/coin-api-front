# import requests


# API_KEY = "0f6ea8d2-d6cf-4b08-a080-38dd22451b3c"



# BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


# headers = {
#     "Accepts": "application/json",
#     "X-CMC_PRO_API_KEY": API_KEY,
# }

# def get_crypto_data():
#     resposta = requests.get(BASE_URL, headers=headers, params={"limit": 10})
    
#     if resposta.status_code == 200:
#         data = resposta.json()
#         cryptos = [
#             {"name": crypto["name"], "symbol": crypto["symbol"], "price": crypto["quote"]["USD"]["price"]}
#             for crypto in data["data"]
#         ]
#         return cryptos
#     else:
#         print("Erro ao acessar API:", resposta.status_code)
#         return []


# while True:
#     cryptos = get_crypto_data()
    
#     if not cryptos:
#         break
    
#     print("\nEscolha uma criptomoeda para ver o preço atual (ou digite 0 para sair):")
#     for i, crypto in enumerate(cryptos, 1):
#         print(f"{i}. {crypto['name']} ({crypto['symbol']})")
#     print("0. Sair")
    
#     escolha = input("\nDigite o número da moeda desejada: ")
    
#     try:
#         escolha = int(escolha)
#         if escolha == 0:
#             print("Saindo... Até mais! 👋")
#             break
#         elif 1 <= escolha <= len(cryptos):
#             selecionada = cryptos[escolha - 1]
#             print(f"\n🪙 {selecionada['name']} ({selecionada['symbol']}) está valendo ${selecionada['price']:.2f}\n")
#         else:
#             print("Número inválido. Tente novamente.")
#     except ValueError:
#         print("Entrada inválida. Digite um número.")






import requests

# APIs das exchanges
EXCHANGE_APIS = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol={}",
    "OKX": "https://www.okx.com/api/v5/market/ticker?instId={}",
    "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={}",
    "Mexc": "https://www.mexc.com/open/api/v2/market/ticker?symbol={}"
}

# Formato correto dos símbolos para cada exchange
SYMBOL_CONVERSION = {
    "Binance": "{}USDT",
    "OKX": "{}-USDT",
    "KuCoin": "{}-USDT",
    "Mexc": "{}_USDT"
}

# Lista de criptomoedas disponíveis
MOEDAS_DISPONIVEIS = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "Binance Coin": "BNB",
    "Cardano": "ADA",
    "XRP": "XRP"
}

def get_price_from_exchange(exchange, symbol):
    """Consulta o preço da criptomoeda em uma exchange específica."""
    url = EXCHANGE_APIS[exchange].format(SYMBOL_CONVERSION[exchange].format(symbol))

    try:
        response = requests.get(url)
        
        # Verifica se a resposta está vazia ou com erro
        if response.status_code != 200 or not response.text:
            print(f"❌ Erro ao buscar preço na {exchange}: Resposta vazia ou erro HTTP {response.status_code}")
            return None
        
        data = response.json()

        if exchange == "Binance":
            return float(data["price"])

        elif exchange == "OKX":
            if "data" in data and data["data"]:
                return float(data["data"][0]["last"])

        elif exchange == "KuCoin":
            if "data" in data and "price" in data["data"]:
                return float(data["data"]["price"])

        elif exchange == "Mexc":
            if "data" in data and data["data"]:
                return float(data["data"][0]["last"])

    except Exception as e:
        print(f"❌ Erro ao buscar preço na {exchange}: {e}")
    
    return None  # Retorna None caso não consiga pegar o preço

def get_crypto_prices(symbol):
    """Busca os preços da criptomoeda nas exchanges e retorna uma lista ordenada da mais barata para a mais cara."""
    prices = {}
    for exchange in EXCHANGE_APIS.keys():
        price = get_price_from_exchange(exchange, symbol)
        if price:
            prices[exchange] = price

    return sorted(prices.items(), key=lambda x: x[1])  # Ordena do mais barato para o mais caro


def menu():
    """Menu interativo para escolher criptomoeda e ver preços nas exchanges."""
    while True:
        print("\nEscolha uma criptomoeda para ver os preços nas exchanges (ou digite 0 para sair):")

        moedas_nomes = list(MOEDAS_DISPONIVEIS.keys())
        for i, moeda in enumerate(moedas_nomes, 1):
            print(f"{i}. {moeda}")

        print("0. Sair")

        escolha = input("\nDigite o número da moeda desejada: ")

        try:
            escolha = int(escolha)
            if escolha == 0:
                print("Saindo... Até mais! 👋")
                break
            elif 1 <= escolha <= len(moedas_nomes):
                moeda_selecionada = moedas_nomes[escolha - 1]
                symbol = MOEDAS_DISPONIVEIS[moeda_selecionada]
                print(f"\n🔍 Buscando preços para {moeda_selecionada} ({symbol})...")

                exchanges = get_crypto_prices(symbol)

                if exchanges:
                    print("\n💰 Preços nas Exchanges (da mais barata para a mais cara):")
                    for exchange, price in exchanges:
                        print(f" - {exchange}: ${price:.2f}")

                    print(f"\n✅ Mais barata: {exchanges[0][0]} (${exchanges[0][1]:.2f})")
                    print(f"❌ Mais cara: {exchanges[-1][0]} (${exchanges[-1][1]:.2f})")

            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

if __name__ == "__main__":
    menu()
