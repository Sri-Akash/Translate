
//Code for populate the Languages

const voiceList = document.querySelector("#languageDropdown");

function populateLanguageDropdown() {
    fetch('/get_languages')  // Fetch the list of languages from Flask
        .then(response => response.json())
        .then(data => {
            const languages = data.languages;

            for (const lang of languages) {
                const option = document.createElement("option");
                option.textContent = lang;
                option.value = lang;
                voiceList.appendChild(option);
            }
        })
        .catch(error => {
            console.error('Error fetching languages:', error);
        });
}

// Call the function to populate the list initially
populateLanguageDropdown();


//Code for Copying text

document.addEventListener("DOMContentLoaded", function () {
    const copyButton = document.getElementById("copy-button");
    const textToCopy = document.getElementsByClassName("text")[1].textContent;

    copyButton.addEventListener("click", function () {
        navigator.clipboard.writeText(textToCopy).then(function () {
            alert("Text copied to clipboard!");
        }).catch(function (err) {
            console.error("Unable to copy text: ", err);
        });
    });
});


//Speak the Converted Text

const speechBtns = document.getElementsByClassName("speechBtn");

// Loop through each element and add an event listener
for (const speechBtn of speechBtns) {
    speechBtn.addEventListener("click", e => {
        e.preventDefault();
        const text = document.querySelector(".translated_text").textContent;
        console.log(text);
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    });
}


/*const micBtn = document.getElementsByClassName("gradient-border");
micBtn.addEventListener("click", e=>{
    e.preventDefault();
    msg = "Recognizing.....";
});*/
function displayMsg() {
    let recog = document.getElementById("recog");
    recog.innerText = "I'm Recognizing your voice ......";
}

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