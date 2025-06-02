
from flask import Flask, render_template, request, send_file
import json, random
from collections import defaultdict
import tempfile

app = Flask(__name__)

def carregar_receitas():
    with open('receitas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def selecionar_receitas_inteligente(receitas, dieta, refeicoes, dias):
    cardapio = {dia: {} for dia in range(1, dias+1)}
    usadas = {tipo: [] for tipo in refeicoes}

    for tipo in refeicoes:
        disponiveis = [r for r in receitas if tipo in r['tipo'] and (dieta in r['restricoes'] or 'comum' in r['restricoes'])]
        if not disponiveis:
            continue
        for dia in cardapio:
            opcoes = [r for r in disponiveis if r['nome'] not in [u['nome'] for u in usadas[tipo]]]
            if not opcoes:
                usadas[tipo] = []
                opcoes = disponiveis[:]
            receita_escolhida = random.choice(opcoes)
            cardapio[dia][tipo] = receita_escolhida
            usadas[tipo].append(receita_escolhida)
    return cardapio

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_cardapio():
    dieta = request.form.get('dieta')
    pessoas = int(request.form.get('pessoas'))
    refeicoes = request.form.getlist('refeicoes')
    dias = 7

    receitas = carregar_receitas()
    cardapio = selecionar_receitas_inteligente(receitas, dieta, refeicoes, dias)

    return render_template('resultado.html', cardapio=cardapio, pessoas=pessoas)

@app.route('/lista_compras', methods=['POST'])
def lista_compras():
    cardapio = json.loads(request.form['cardapio'])
    pessoas = int(request.form['pessoas'])

    ingredientes = defaultdict(int)
    for refeicoes in cardapio.values():
        for receita in refeicoes.values():
            for ingrediente in receita['ingredientes']:
                ingredientes[ingrediente] += pessoas

    conteudo = '🛒 Lista de Compras da Semana\n\n'
    for item, quantidade in sorted(ingredientes.items()):
        conteudo += f"- {item} (x{quantidade})\n"

    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt', encoding='utf-8') as f:
        f.write(conteudo)
        temp_path = f.name

    return send_file(temp_path, as_attachment=True, download_name="lista_compras.txt")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
