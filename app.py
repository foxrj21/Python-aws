from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        nome = request.form["nome"]
        try:
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            nota3 = float(request.form["nota3"])
            media = (nota1 + nota2 + nota3) /3
            situacao = "Aprovado" if media >= 7 else "Reprovado"
           
            resultado = {
                "nome": nome,
                "media": round(media, 2),
                "situacao": situacao
            }
        except ValueError :
            resultado = {"erro": "Por favor, insira notas válidas(números)."}

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
