from flask import Flask, render_template, request, jsonify, render_template_string, send_file
import sqlite3
import io
from datetime import datetime

app = Flask(__name__)

# Inicialização da Base de Dados
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cliques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        botao TEXT,
        contador INTEGER,
        data TEXT,
        hora TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS config (
        chave TEXT PRIMARY KEY, valor TEXT
    )''')
    botoes_iniciais = [('btn1', 'Botão 1'), ('btn2', 'Botão 2'), ('btn3', 'Botão 3'), ('btn4', 'Botão 4')]
    for chave, valor in botoes_iniciais:
        c.execute("INSERT OR IGNORE INTO config (chave, valor) VALUES (?, ?)", (chave, valor))
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html', names=get_button_names())

@app.route('/click', methods=['POST'])
def click():
    botao_id = request.json['botao']
    botao_nome = get_button_names().get(botao_id, botao_id)
    agora = datetime.now()
    data = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM cliques WHERE data = ? AND botao = ?", (data, botao_nome))
    contador = c.fetchone()[0] + 1
    c.execute("INSERT INTO cliques (botao, contador, data, hora) VALUES (?, ?, ?, ?)", (botao_nome, contador, data, hora))
    conn.commit()
    conn.close()
    return jsonify({'contador': contador, 'data': data, 'hora': hora, 'nome_exibicao': botao_nome})

@app.route('/api/logs')
def api_logs():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM cliques ORDER BY id DESC")
    logs = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(logs)
