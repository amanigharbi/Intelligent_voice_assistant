
var SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
var recognition = new SpeechRecognition();
var language = "";
var charDuration=null;
var idIndex=1;
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
            mess1 = "Salut. je suis Sam. comment puis-je vous aider?";
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
  
    // switch (language) {
    //     case "anglais":
    //         recognition.lang = "en-US";
    //         break;
    //     case "français":
    //         recognition.lang = "fr-FR";
    //         break;
    //     case "arabe":
    //         recognition.lang = "ar-AE";
    //         break;
    //     default:
    //         break;
    // }
    // console.log("aaaa " + recognition.lang);
    let device = navigator.mediaDevices.getUserMedia({ audio: true });
    let chunks = [];
    let recorder;
    device.then(stream => {
        recorder = new MediaRecorder(stream);

        recorder.ondataavailable = e => {
          chunks.push(e.data);
          console.log("data "+chunks)
            if (recorder.state == 'inactive') {
                let blob = new Blob(chunks, { type: 'audio/webm' });
                let audio = {name: "audio",message:URL.createObjectURL(blob)};
                messages.push(audio);
                updateChatText(chatbox);
            }
        }

        recorder.start(1000);
    });

    setTimeout(() => {
        recorder.stop()
    }, 2000);
     recognition.onresult = function (e) {
  
         let textField = e.results[0][0].transcript;
        // if (textField === "") {
        //     return;
        // }

         let msg1 = { name: "User", message: textField };
        messages.push(msg1);
       
        
 
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

function readOutLoud(message,id) {
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

    // if(charDuration&&id){
    //     progress = 0;
    //     const progressbar = document.getElementById(id);
    //     const changeProgress = (progress) => {
    //       progressbar.style.width = `${progress}%`;
    //     };
        
    //     step=120/speech.text.length;
    //     console.log(step,charDuration)
    //     speech.onstart = function (event) {
    //            interval= setInterval(function(){
    //               progress+=step;
    //             changeProgress(progress);
    //           }, charDuration);
    //     };

    //     speech.onend = function (event) {
    //         changeProgress(0);
    //         clearInterval(interval);
    //         console.log(event.elapsedTime);
    //     };
    // }

    // if(charDuration==null){
    //     speech.onend = function (event) {
    //         charDuration=event.elapsedTime/speech.text.length;
    //     };
    // }

    window.speechSynthesis.speak(speech);
}


function updateChatText(chatbox) {
    var html = "";
    messages
        .slice()
        .reverse()
        .forEach(function (item, index) {
         
        
            // if (item.name === "langue") {
            //     html +=
            //         `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('anglais')">` +
            //         "anglais" +
            //         `</div>` +
            //         `<div class="messages__item messages__item--visitor"  onClick="modifyLanguage('français')">` +
            //         "français" +
            //         `</div>` +
            //         `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('arabe')">` +
            //         "arabe" +
            //         `</div>`+
            //         // `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
            //         //  +
            //         `<div class="messages__item messages__item--visitor">
            //          <div class="progress-container" >
            //         <div class="progress fa fa-play" id="prog-`+idIndex+`" onClick="readOutLoud('` + item.message + `','prog-`+idIndex+`')"></div> 
            //         </div> </div>`;
            //         idIndex++;
            // }
            // if (item.name === "welcome_Sam") {
            //     // html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
            //    html+=`<div class="messages__item messages__item--visitor">
            //          <div class="progress-container" >
            //         <div class="progress fa fa-play" id="prog-`+idIndex+`" onClick="readOutLoud('` + item.message + `','prog-`+idIndex+`')"></div> 
            //         </div> </div>`;
            //         idIndex++;

            //   }
            // if (item.name === "Sam") {
            //     // html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
            //     html += `<div class="messages__item messages__item--visitor">
            //     <div class="progress-container" >
            //     <div class="progress fa fa-play"  id="prog-`+idIndex+`" onClick="readOutLoud('` + item.message + `','prog-`+idIndex+`')"></div> 
            //           </div> </div>`;
            //           idIndex++;
            //   }
            // if (item.name === "User") {
            //     //  html += `<div class="messages__item messages__item--operator" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
            //     html += `<div class="messages__item messages__item--operator">
            //     <div class="progress-container" >
            //     <div class="progress fa fa-play" id="prog-`+idIndex+`" onClick="readOutLoud('` + item.message + `','prog-`+idIndex+`')"></div> 
            //           </div> </div>`;
            //           idIndex++;
            //   }
              switch (item.name) {
                  case "langue":
                      html += `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('anglais')">` +
                      "anglais" +
                      `</div>` +
                      `<div class="messages__item messages__item--visitor"  onClick="modifyLanguage('français')">` +
                      "français" +
                      `</div>` +
                      `<div class="messages__item messages__item--visitor" onClick="modifyLanguage('arabe')">` +
                      "arabe" +
                      `</div>`+
                      `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                      break;
                    case "welcome_Sam":
                        html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                    break;

                    case "Sam":
                        html += `<div class="messages__item messages__item--visitor" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                    break;
                    case "User" && "audio":
          console.log(item.message)
                        // html += `<div class="messages__item messages__item--operator" onClick="readOutLoud('` + item.message + `')">` + item.message + `</div>`;
                        html += `<div class="messages__item messages__item--operator">
                        <audio class="audio" id="audio" controls>
                      
                         <source src=" `+item.message + `" type="video/webm" />
                        </audio>
                        </div>`
                        break;

                  default:
                      
                      break;
              }
        });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
}
