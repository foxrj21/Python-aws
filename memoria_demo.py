# Script: memoria_demo.py
# Mostra diferença entre "memória volátil" (variável) e "não volátil" (arquivo)

def salvar_em_arquivo(texto, arquivo):
    with open(arquivo, "w") as f:
        f.write(texto)
    print(f"Texto salvo em '{arquivo}' (não volátil).")

def ler_do_arquivo(arquivo):
    try:
        with open(arquivo, "r") as f:
            conteudo = f.read()
        print(f"Conteúdo lido de '{arquivo}': {conteudo}")
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado (nada salvo ainda).")

def main():
    print("=== Simulação de memória ===")

    # Parte 1: memória volátil
    texto_volatil = input("Digite um texto para guardar na variável (volátil): ")
    print(f"Guardado na variável (volátil): {texto_volatil}")

    # Parte 2: memória não volátil
    escolha = input("Deseja salvar em arquivo (não volátil)? (s/n): ").lower()
    if escolha == 's':
        salvar_em_arquivo(texto_volatil, "memoria.txt")
    
    print("\n== Simulando encerramento e reinício do programa ==")
    ler_do_arquivo("memoria.txt")

if __name__ == "__main__":
    main()
