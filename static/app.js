messages = [];
var button =document.getElementById("button")
var SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition ;
var recognition = new SpeechRecognition()
recognition.lang = 'en-US';


   button.addEventListener("click",start=>{
   recognition.start()
   });
   inputText=document.getElementById("id")
   inputText2=document.getElementById("id2")
   recognition.onresult=function(e){
   console.log(e)
   let transcript= e.results[0][0].transcript

    //console.log(transcript)
    inputText.value=transcript;
    inputText.innerHTML +="| "+ inputText.value;

fetch('http://127.0.0.1:5050/predict', {
method: 'POST',
body: JSON.stringify({ message: transcript }),
mode: 'cors',
headers: {
    'Content-Type': 'application/json'
},

}).then(response => response.json())
.then(data => {
readOutLoud(data);
inputText2.innerHTML += "| "+data;
}).catch(console.error);


function readOutLoud(message) {
	var speech = new SpeechSynthesisUtterance();

  // Set the text and voice attributes.
	speech.text = message;
	speech.volume = 1;
	speech.rate = 1;
	speech.pitch = 1;

	window.speechSynthesis.speak(speech);
}


   }



