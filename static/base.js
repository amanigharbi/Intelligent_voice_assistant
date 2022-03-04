
var SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
var recognition = new SpeechRecognition();
var language = "";
audioChunks = [];
var button = document.getElementById("button");
button.addEventListener("click", (start) => {
    recognition.start();
});

args = {
    openButton: document.querySelector(".chatbox__button"),
    chatBox: document.querySelector(".chatbox__support"),
    sendButton: document.querySelector(".send__button"),
};
messages = new Array();
state = false;

const { openButton, chatBox, sendButton } = args;

openButton.addEventListener("click", () => toggleState(chatBox));

sendButton.addEventListener("click", () => onSendButton(chatBox));

function modifyLanguage(lang) {
    language = lang;
    console.log("language " + language);
    switch (language) {
        case "anglais":
            mess0 = "Hi. My name is Sam. How can I help you?";
            let msg01 = { name: "welcome_Sam", message: mess0 };
            messages.push(msg01);
            updateChatText(chatBox);
            readOutLoud(mess0);
            break;
        case "français":
            mess1 = "Salut. je m'appelle Sam. comment puis-je vous aider?";
            let msg02 = { name: "welcome_Sam", message: mess1 };
            messages.push(msg02);
            updateChatText(chatBox);
            readOutLoud(mess1);
            break;
        case "arabe":
            mess2 = "مرحبا. اسمي سام كيف يمكنني مساعدتك؟";
            let msg03 = { name: "welcome_Sam", message: mess2 };
            messages.push(msg03);
            updateChatText(chatBox);
            readOutLoud(mess2);
            break;
        default:
            readOutLoud("choisir une langue");
    }
}
function toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
        chatbox.classList.add("chatbox--active");

        msg = "Choisir une langue";
        let msg0 = { name: "langue", message: msg };
        messages.push(msg0);
        updateChatText(chatbox);
        readOutLoud(msg);
    } else {
        chatbox.classList.remove("chatbox--active");
        for (let index = 0; index < messages.length; index++) {
            messages = [];
            language = "";
        }
    }
}
function onSendButton(chatbox) {
  
    switch (language) {
        case "anglais":
            recognition.lang = "en-US";
            break;
        case "français":
            recognition.lang = "fr-FR";
            break;
        case "arabe":
            recognition.lang = "ar-AE";
            break;
        default:
            break;
    }
    console.log("aaaa " + recognition.lang);
    recognition.onresult = function (e) {
        let textField = e.results[0][0].transcript;
        if (textField === "") {
            return;
        }
        let msg1 = { name: "User", message: textField };
        messages.push(msg1);
        updateChatText(chatbox);

        fetch("http://127.0.0.1:5050/predict", {
            method: "POST",
            body: JSON.stringify({ message: textField }),
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                readOutLoud(data);
                let msg2 = { name: "Sam", message: data };
                messages.push(msg2);
                updateChatText(chatbox);
                textField.value = "";
            })
            .catch(console.error);
    };
}
function readOutLoud(message) {
    var speech = new SpeechSynthesisUtterance();

    // Set the text and voice attributes.
    speech.text = message;
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    switch (language) {
        case "anglais":
            speech.lang = "en-US";
            break;
        case "français":
            speech.lang = "fr-FR";
            break;
        case "arabe":
            speech.lang = "ar-AE";
            break;
        default:
            speech.lang = "fr-FR";
    }
    // audioEnd = false;
    // progress = 10;
    // const progressbar = document.querySelector(".progress");
    // const changeProgress = (progress) => {
    //   progressbar.style.width = `${progress}%`;
    // };


    // speech.onstart = function (event) {
    //     console.log("Utterance has finished being spoken after " + event.elapsedTime + " seconds.");
    //     while (!audioEnd && progress < 80) {
    //       progress=progress+0.001;
    //       setTimeout(() => changeProgress(progress), 500);
          
    //   }
    // };

    // speech.onend = function (event) {
    //     console.log("Utterance has finished being spoken after " + event.elapsedTime + " seconds.");
    //     audioEnd = true;
    //     changeProgress(100);
    // };

    window.speechSynthesis.speak(speech);
    
  

    
}


function updateChatText(chatbox) {
    var html = "";
    messages
        .slice()
        .reverse()
        .forEach(function (item, index) {
            if (item.name === "langue") {
                html +=
              
                    `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('anglais')">` +
                    "anglais" +
                    `</div>` +
                    `<div class="messages__item messages__item--visitor"  onClick="modifyLanguage('français')">` +
                    "français" +
                    `</div>` +
                    `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('arabe')">` +
                    "arabe" +
                    `</div>`+
                    `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                    //  +
                    // `<div class="messages__item messages__item--visitor">
                    //  <div class="progress-container" >
                    // <div class="progress fa fa-play"  onClick="readOutLoud('` + item.message + `')"></div> 
                    // </div> </div>`
            }
            if (item.name === "welcome_Sam") {
                html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                // html += `<div class="messages__item messages__item--visitor">
                // <div class="progress-container" >
                // <div class="progress fa fa-play"  onClick="readOutLoud('` + item.message + `')"></div> 
                //       </div> </div>`;

              }
            if (item.name === "Sam") {
                html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                // html += `<div class="messages__item messages__item--visitor">
                // <div class="progress-container" >
                // <div class="progress fa fa-play"  onClick="readOutLoud('` + item.message + `')"></div> 
                //       </div> </div>`;
              }
            if (item.name === "User") {
                 html += `<div class="messages__item messages__item--operator" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                // html += `<div class="messages__item messages__item--operator">
                // <div class="progress-container" >
                // <div class="progress fa fa-play"  onClick="readOutLoud('` + item.message + `')"></div> 
                //       </div> </div>`;
              }
        });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
}
