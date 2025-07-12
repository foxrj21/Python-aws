nome = input("Digite o nome do aluno: ")
nota1 = input("Digite a primeira nota: ")
nota2 = input("Digite a segunda nota: ")
nota3 = input("Digite a terceira nota: ")

media = (nota1 + nota2 + nota3) / 3

print("Aluno:", nome)
print("Média:", media)

if media >= 7:
    print("Situação: Aprovado")
else:
    print("Situação: Reprovado")
