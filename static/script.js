function toggleTutorial() {
    const tutorial = document.getElementById('tutorial-section');
    tutorial.classList.toggle('hidden');
}

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
        // Feedback visual
        const resultDiv = document.getElementById('resultado');
        resultDiv.classList.remove('fade-in');
        void resultDiv.offsetWidth;
        resultDiv.classList.add('fade-in');
    });
}
