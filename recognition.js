const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';
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
        voiceStatus.textContent = '🔊 Listening...';
    recognition.start();
}

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const voiceStatus = document.getElementById('voiceStatus');
                                     voiceStatus.textContent = `You said: ${transcript}`;
    // Sends the transcript to Streamlit using postMessage
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        args: {
            key: 'voice_input_hidden',
            value: transcript
        }
    }, '*');

    // Reloads the page after recognition to process the new input
    setTimeout(() => {
        window.parent.location.reload();
    }, 100);
};

recognition.onend = () => {
    isRecognizing = false;
    const voiceButton = document.getElementById('voiceButton');
    const voiceStatus = document.getElementById('voiceStatus');
    voiceButton.classList.remove('active');
        voiceStatus.textContent = 'Recognition finished.';
    // Does not reload here, as it is already done in onresult
    // setTimeout(() => { voiceStatus.textContent = ''; }, 2000);
};

recognition.onerror = (event) => {
    isRecognizing = false;
    const voiceStatus = document.getElementById('voiceStatus');
        voiceStatus.textContent = `Recognition error: ${event.error}`;
    console.error('Speech recognition error', event.error);
    const voiceButton = document.getElementById('voiceButton');
    voiceButton.classList.remove('active');
};

// Informs Streamlit that the component is ready (if necessary, depending on the integration)
// window.addEventListener('load', () => {
//     if (window.parent.Streamlit) {
//         window.parent.Streamlit.setComponentReady();
//     } else {
//         console.error('Streamlit is not defined in parent window on load.');
//     }
// });

document.getElementById('voiceButton').onclick = startRecognition;
