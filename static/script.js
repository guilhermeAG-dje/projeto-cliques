function registar(botao) {
    fetch('/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ botao: botao })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultado').innerHTML =
            `Clique nº <strong>${data.contador}</strong><br>` +
            `Data: ${data.data}<br>` +
            `Hora: ${data.hora}`;
    });
}
