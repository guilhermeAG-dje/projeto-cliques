function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const newTheme = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    const icon = document.querySelector('.theme-icon');
    if(icon) icon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
}

function openLogsModal() {
    const body = document.getElementById('logs-modal-body');
    body.innerHTML = '<tr><td colspan="4">A carregar...</td></tr>';
    document.getElementById('logs-modal').classList.add('active');
    fetch('/api/logs').then(res => res.json()).then(data => {
        body.innerHTML = data.map(log => `
            <tr><td>${log.botao}</td><td>${log.contador}</td><td>${log.data}</td><td>${log.hora}</td></tr>
        `).join('');
    });
}

function closeLogsModal() { document.getElementById('logs-modal').classList.remove('active'); }
function showModalHelp() { document.getElementById('modal-help-content').classList.toggle('hidden'); }

function registar(botaoId) {
    fetch('/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ botao: botaoId })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('stat-contador').textContent = data.contador;
        document.getElementById('stat-data').textContent = data.data;
        document.getElementById('stat-hora').textContent = data.hora;
        document.getElementById('resultado-container').classList.remove('hidden');
    });
}

// Atalhos e Inicialização
window.addEventListener('keydown', e => {
    if(e.ctrlKey && e.key === 'q') startTutorial();
    if(e.ctrlKey && e.key === '9') showAdminLogin();
});

document.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
});
