from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Criar BD e tabela

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
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    botao = request.json['botao']
    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    hora = agora.strftime('%H:%M')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM cliques WHERE data = ?", (data,))
    contador = c.fetchone()[0] + 1

    c.execute("INSERT INTO cliques (botao, contador, data, hora) VALUES (?, ?, ?, ?)",
              (botao, contador, data, hora))

    conn.commit()
    conn.close()

    return jsonify({
        'contador': contador,
        'data': data,
        'hora': hora
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)