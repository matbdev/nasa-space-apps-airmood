
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'pt-BR';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

let isRecognizing = false;

function startRecognition() {
    const voiceButton = document.getElementById('voiceButton');
    const voiceStatus = document.getElementById('voiceStatus');

    if (isRecognizing) {
        recognition.stop();
        isRecognizing = false;
        voiceButton.classList.remove('active');
        voiceStatus.textContent = '';
        return;
    }

    isRecognizing = true;
    voiceButton.classList.add('active');
    voiceStatus.textContent = '🔊 Ouvindo...';
    recognition.start();
}

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const voiceStatus = document.getElementById('voiceStatus');
    voiceStatus.textContent = `Você disse: ${transcript}`;

    // Envia a transcrição para o Streamlit usando postMessage
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        args: {
            key: 'voice_input_hidden',
            value: transcript
        }
    }, '*');

    // Recarrega a página após o reconhecimento para processar a nova entrada
    setTimeout(() => {
        window.parent.location.reload();
    }, 100);
};

recognition.onend = () => {
    isRecognizing = false;
    const voiceButton = document.getElementById('voiceButton');
    const voiceStatus = document.getElementById('voiceStatus');
    voiceButton.classList.remove('active');
    voiceStatus.textContent = 'Reconhecimento finalizado.';
    // Não recarrega aqui, pois já é feito no onresult
    // setTimeout(() => { voiceStatus.textContent = ''; }, 2000);
};

recognition.onerror = (event) => {
    isRecognizing = false;
    const voiceStatus = document.getElementById('voiceStatus');
    voiceStatus.textContent = `Erro de reconhecimento: ${event.error}`;
    console.error('Speech recognition error', event.error);
    const voiceButton = document.getElementById('voiceButton');
    voiceButton.classList.remove('active');
};

// Informa ao Streamlit que o componente está pronto (se necessário, dependendo da integração)
// window.addEventListener('load', () => {
//     if (window.parent.Streamlit) {
//         window.parent.Streamlit.setComponentReady();
//     } else {
//         console.error('Streamlit is not defined in parent window on load.');
//     }
// });

document.getElementById('voiceButton').onclick = startRecognition;

