from flask import Flask, render_template, request, jsonify, render_template_string
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
    data = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Contador individual por botão e dia
    c.execute("SELECT COUNT(*) FROM cliques WHERE data = ? AND botao = ?", (data, botao))
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

@app.route('/logs')
def view_logs():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM cliques ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Logs da Base de Dados</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #121212; color: #fff; }
            table { width: 100%; border-collapse: collapse; background: #1e1e1e; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.5); border: 1px solid #333; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
            th { background: #d4af37; color: #000; }
            tr:hover { background: #2a2a2a; }
            .back { margin-bottom: 20px; display: inline-block; color: #d4af37; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <a href="/" class="back">← Voltar</a>
        <h1>Registos de Cliques</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Botão</th>
                    <th>Seq. (Dia)</th>
                    <th>Data</th>
                    <th>Hora</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs %}
                <tr>
                    <td>{{ log['id'] }}</td>
                    <td>{{ log['botao'] }}</td>
                    <td>{{ log['contador'] }}</td>
                    <td>{{ log['data'] }}</td>
                    <td>{{ log['hora'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html, logs=logs)

@app.route('/code')
def view_code():
    with open('app.py', 'r') as f: app_code = f.read()
    with open('static/script.js', 'r') as f: script_code = f.read()
    with open('templates/index.html', 'r') as f: html_code = f.read()
    with open('static/style.css', 'r') as f: css_code = f.read()
    code_html = """...""" # Estrutura de visualização de código
    return render_template_string(code_html, app_code=app_code, script_code=script_code, html_code=html_code, css_code=css_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
