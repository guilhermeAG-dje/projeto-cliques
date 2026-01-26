from flask import Flask, render_template, request, jsonify, render_template_string, send_file
import sqlite3
import io
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
    
    html = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Logs da Base de Dados</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #f8fafc; }
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
            th { background: #4f46e5; color: white; }
            tr:hover { background: #f1f5f9; }
            .back { margin-bottom: 20px; display: inline-block; color: #4f46e5; text-decoration: none; font-weight: bold; }
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

@app.route('/admin')
def admin_page():
    # Carregar os códigos para exibir no admin.html
    try:
        with open('app.py', 'r') as f: app_code = f.read()
        with open('static/style.css', 'r') as f: css_code = f.read()
        with open('static/script.js', 'r') as f: js_code = f.read()
        with open('templates/index.html', 'r') as f: html_code = f.read()
    except:
        app_code = css_code = js_code = html_code = "Erro ao carregar ficheiro."

    return render_template('admin.html', 
                         app_code=app_code, 
                         css_code=css_code, 
                         js_code=js_code, 
                         html_code=html_code)

@app.route('/admin-export', methods=['POST'])
def admin_export():
    password = request.json.get('password')
    if password != '123':
        return jsonify({'error': 'Acesso negado'}), 403
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM cliques ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    
    output = io.StringIO()
    output.write("ID | Botão | Contador | Data | Hora\n")
    output.write("-" * 50 + "\n")
    for log in logs:
        output.write(f"{log['id']} | {log['botao']} | {log['contador']} | {log['data']} | {log['hora']}\n")
    
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        as_attachment=True,
        download_name='relatorio_cliques.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
