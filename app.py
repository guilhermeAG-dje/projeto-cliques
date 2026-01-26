from flask import Flask, render_template, request, jsonify, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

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
    data = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM cliques WHERE data = ? AND botao = ?", (data, botao))
    contador = c.fetchone()[0] + 1
    c.execute("INSERT INTO cliques (botao, contador, data, hora) VALUES (?, ?, ?, ?)",
              (botao, contador, data, hora))
    conn.commit()
    conn.close()
    return jsonify({'contador': contador, 'data': data, 'hora': hora})

@app.route('/logs')
def view_logs():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM cliques ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    html = """...""" # (Omitido aqui por brevidade, veja na página /code)
    return render_template_string(html, logs=logs)

@app.route('/code')
def view_code():
    # Rota que serve o código fonte completo
    # ...
    return render_template_string(code_html, ...)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
