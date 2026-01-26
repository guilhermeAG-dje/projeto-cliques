function toggleTutorial() {
    const tutorial = document.getElementById('tutorial-section');
    tutorial.classList.toggle('hidden');
}

// Inicia o guia automático para novos usuários
window.addEventListener('load', function() {
    if (!localStorage.getItem('tutorial_concluido')) {
        introJs().setOptions({
            nextLabel: 'Próximo',
            doneLabel: 'Entendido!',
            hidePrev: true
        }).start();
        localStorage.setItem('tutorial_concluido', 'true');
    }
});

function registar(botao) {
    fetch('/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ botao: botao })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('stat-label-contador').textContent = `Cliques (${botao})`;
        document.getElementById('stat-contador').textContent = data.contador;
        document.getElementById('stat-data').textContent = data.data;
        document.getElementById('stat-hora').textContent = data.hora;
        // ... feedback visual ...
    });
}function registar(botao) {
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
        // Atualiza os valores na interface
        document.getElementById('stat-label-contador').textContent = `Cliques (${botao})`;
        document.getElementById('stat-contador').textContent = data.contador;
        document.getElementById('stat-data').textContent = data.data;
        document.getElementById('stat-hora').textContent = data.hora;

        // Mostra o container se estiver escondido
        if (container.classList.contains('hidden')) {
            container.classList.remove('hidden');
        }

        // Adiciona efeito de feedback visual (animação)
        const resultDiv = document.getElementById('resultado');
        resultDiv.classList.remove('fade-in');
        void resultDiv.offsetWidth; // Trigger reflow para reiniciar animação
        resultDiv.classList.add('fade-in');
    })
    .catch(error => {
        console.error('Erro ao registar clique:', error);
    });
}
