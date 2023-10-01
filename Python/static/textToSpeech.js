const textarea = document.querySelector("textarea"),
    voiceList = document.querySelector("select"),
    speechBtn = document.querySelector(".btnconvert");

let synth = window.speechSynthesis,
    isSpeaking = true;

let utterance = new SpeechSynthesisUtterance();

function voices() {
    synth.addEventListener("voiceschanged", () => {
        voiceList.innerHTML = "";
        for (let voice of synth.getVoices()) {
            let selected = voice.name === "Google US English" ? "selected" : "";
            let option = `<option value="${voice.name}" ${selected}>${voice.name} (${voice.lang})</option>`;
            voiceList.insertAdjacentHTML("beforeend", option);
        }
    });
}

voices();

function textToSpeech(text) {
    utterance.text = text;
    for (let voice of synth.getVoices()) {
        if (voice.name === voiceList.value) {
            utterance.voice = voice;
        }
    }
    synth.speak(utterance);

}

speechBtn.addEventListener("click", e => {
    e.preventDefault();
    if (textarea.value !== "") {
        if (!synth.speaking) {
            textToSpeech(textarea.value);
        }
        if (textarea.value.length > 80) {
            setInterval(() => {
                if (!synth.speaking && !isSpeaking) {
                    isSpeaking = true;
                    speechBtn.innerText = "Convert To Speech";
                } else {
                }
            }, 500);
            if (isSpeaking) {
                synth.resume();
                isSpeaking = false;
                speechBtn.innerText = "Pause Speech";
            } else {
                synth.pause();
                isSpeaking = true;
                speechBtn.innerText = "Resume Speech";
            }
        } else {
            speechBtn.innerText = "Convert To Speech";
        }
    }
});

const error = document.getElementById("error")

textarea.addEventListener("input", function (event) {
    if (event.target.value !== "") {
        error.style.display = 'none';
    }
    else {
        error.style.display = 'flex'
    }
    /*const typedText = event.target.value;
    console.log("Typed text:", typedText);*/
});

function displayIns() {
    const instruct = document.getElementById("instruct");
    const readBtn = document.querySelector("#readBtn");

    if (instruct.style.display === "block") {
        instruct.style.display = "none";
        readBtn.textContent = "Read Instructions";
    } else {
        instruct.style.display = "block";
        readBtn.textContent = "❌";
    }
}