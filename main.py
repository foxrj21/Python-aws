# Importa a biblioteca yfinance, que permite acessar dados financeiros do Yahoo Finance.
import yfinance as yf

# Importa o módulo time, usado para pausar a execução entre atualizações.
import time

# Define uma função chamada pegar_preco_yahoo, que recebe o nome da ação como parâmetro (ex: 'PETR4.SA').
def pegar_preco_yahoo(ticker):
    """
    Usa a biblioteca yfinance para buscar a cotação atual da ação.
    :param ticker: Código do ativo (ex: PETR4.SA)
    :return: Preço mais recente da ação
    """
    try:
        # Cria um objeto da ação usando o ticker informado (ex: 'PETR4.SA')
        acao = yf.Ticker(ticker)

        # Busca o histórico de preços da ação com:
        # - period='1d' => últimos 1 dia
        # - interval='1m' => com intervalo de 1 minuto
        dados = acao.history(period='1d', interval='1m')

        # Verifica se o DataFrame não está vazio (ou seja, tem dados)
        if not dados.empty:
            # Retorna o último preço de fechamento (última linha da coluna 'Close')
            return dados['Close'].iloc[-1]
        else:
            # Se não tiver dados, retorna None
            return None

    # Captura qualquer erro que acontecer durante a execução da função
    except Exception as e:
        # Imprime o erro ocorrido
        print(f"Erro ao buscar {ticker}: {e}")
        # Retorna None indicando falha
        return None

# Bloco principal do programa, que só roda se o script for executado diretamente
if __name__ == '__main__':
    # Início de um loop infinito para atualização contínua
    while True:
        # Busca o preço atual da ação PETR4
        preco_petr4 = pegar_preco_yahoo('PETR4.SA')

        # Busca o preço atual da ação PETR3
        preco_petr3 = pegar_preco_yahoo('PETR3.SA')

        # Exibe os preços formatados com duas casas decimais
        print(f"PETR4: {preco_petr4:.2f} | PETR3: {preco_petr3:.2f}")

        # Aguarda 10 segundos antes de repetir o processo
        time.sleep(10)
