import yfinance as yf
import time

def pegar_preco_yahoo(ticker):
    """
    Usa a biblioteca yfinance para buscar a cotação atual da ação.
    """
    try:
        acao = yf.Ticker(ticker)
        dados = acao.history(period='1d', interval='1m')
        if not dados.empty:
            return dados['Close'].iloc[-1]
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        return None

if __name__ == '__main__':
    while True:
        preco_petr4 = pegar_preco_yahoo('PETR4.SA')
        preco_petr3 = pegar_preco_yahoo('PETR3.SA')

        print(f"PETR4: {preco_petr4:.2f} | PETR3: {preco_petr3:.2f}")

        time.sleep(10)  # Atualiza a cada 10 segundos
