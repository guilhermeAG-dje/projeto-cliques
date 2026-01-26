function toggleTutorial() {
    const tutorial = document.getElementById('tutorial-section');
    tutorial.classList.toggle('hidden');
}

function startTutorial() {
    introJs().setOptions({
        nextLabel: 'Próximo',
        prevLabel: 'Anterior',
        doneLabel: 'Entendido!',
        hidePrev: true
    }).start();
}

// Inicia o guia interativo se for a primeira vez
window.addEventListener('load', function() {
    if (!localStorage.getItem('tutorial_concluido')) {
        startTutorial();
        localStorage.setItem('tutorial_concluido', 'true');
    }
});

window.addEventListener('keydown', function(e) {
    // Atalho Ctrl + Q para o tutorial
    if (e.ctrlKey && e.key.toLowerCase() === 'q') {
        e.preventDefault();
        startTutorial();
    }
    
    if (e.ctrlKey && e.key === '9') {
        e.preventDefault();
        const password = prompt("Introduza a palavra-passe de administrador:");
        if (password === '123') {
            window.open('/admin', '_blank');
        } else if (password !== null) {
            alert("Palavra-passe incorreta!");
        }
    }
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

document.addEventListener('DOMContentLoaded', initTheme);

function downloadLogs() {
    const password = '123'; // No contexto do admin após login
    fetch('/admin-export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password })
    })
    .then(response => {
        if (response.ok) return response.blob();
        throw new Error('Erro ao exportar');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'relatorio_cliques.txt';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(err => alert(err.message));
}

function copyCode(elementId) {
    const codeElement = document.getElementById(elementId);
    if (!codeElement) return;
    
    const text = codeElement.innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("Código copiado para a área de transferência!");
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        alert("Erro ao copiar o código.");
    });
}

function registar(botao) {
    const container = document.getElementById('resultado-container');
    
    fetch('/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ botao: botao })
    })
    .then(response => response.json())
    .then(data => {
        // Atualiza os valores
        document.getElementById('stat-label-contador').textContent = `Cliques (${botao})`;
        document.getElementById('stat-contador').textContent = data.contador;
        document.getElementById('stat-data').textContent = data.data;
        document.getElementById('stat-hora').textContent = data.hora;

        // Mostra o container se estiver escondido
        if (container.classList.contains('hidden')) {
            container.classList.remove('hidden');
        }

        // Adiciona efeito de feedback visual
        const resultDiv = document.getElementById('resultado');
        resultDiv.classList.remove('fade-in');
        void resultDiv.offsetWidth; // Trigger reflow
        resultDiv.classList.add('fade-in');
    })
    .catch(error => {
        console.error('Erro ao registar clique:', error);
    });
}
