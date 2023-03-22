var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var recognition = new SpeechRecognition();

recognition.continuous = true;
recognition.interimResults = true;

function initializeAudioProcessing(stream) {
  if (typeof AudioContext !== 'undefined') {
    var audioContext = new AudioContext();
    var analyser = audioContext.createAnalyser();
    var microphone = audioContext.createMediaStreamSource(stream);
    var processor = audioContext.createScriptProcessor(1024, 1, 1);

    analyser.smoothingTimeConstant = 0.8;
    analyser.fftSize = 1024;

    microphone.connect(analyser);
    analyser.connect(processor);
    processor.connect(audioContext.destination);
    processor.onaudioprocess = function () {
      var array = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(array);
      var values = 0;
      var length = array.length;
      for (var i = 0; i < length; i++) {
        values += array[i];
      }

      var average = values / length;
      if (average > 60) {
        recognition.stop();
        recognition.start();
      }
    };
  }
}



// // Add the audio processing code here
// navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
//   if (typeof AudioContext !== 'undefined') {
//     var audioContext = new AudioContext();
//     var analyser = audioContext.createAnalyser();
//     var microphone = audioContext.createMediaStreamSource(stream);
//     var processor = audioContext.createScriptProcessor(1024, 1, 1);

//     analyser.smoothingTimeConstant = 0.8;
//     analyser.fftSize = 1024;

//     microphone.connect(analyser);
//     analyser.connect(processor);
//     processor.connect(audioContext.destination);
//     processor.onaudioprocess = function () {
//       var array = new Uint8Array(analyser.frequencyBinCount);
//       analyser.getByteFrequencyData(array);
//       var values = 0;
//       var length = array.length;
//       for (var i = 0; i < length; i++) {
//         values += array[i];
//       }

//       var average = values / length;
//       if (average > 60) {
//         recognition.stop();
//         recognition.start();
//       }
//     };
//   }
// }).catch(function (err) {
//   console.error('Error getting audio stream:', err);
// });

function updateRecognitionLanguage() {
  recognition.lang = document.getElementById("input-language-select").value;
}

updateRecognitionLanguage();

var recognizing = false;
var conversationHistory = [];


function translateText(text) {
  var input_language = document.getElementById("input-language-select").value;
  var target_language = document.getElementById("translate-language-select").value;

  // Get the API key input value
  var apiKey = document.getElementById("apikey").value;

  fetch("/translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: text,
      input_language: input_language,
      target_language: target_language,
      api_key: apiKey, // Include the API key in the request body
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      var translatedText = response.translated_text;
      // Add line breaks after each bullet point in the translated text
      translatedText = translatedText.replace(/- /g, "\n- ");

      document.getElementById("translated-text").innerHTML = translatedText;

      // Add line breaks after each bullet point in the translated text
      translatedText = translatedText.replace(/\n/g, "<br>");

      document.getElementById("conversation-history").innerHTML +=
        "<p><strong>Original Text:</strong><br>" + text + "</p>";
      document.getElementById("conversation-history").innerHTML +=
        "<p><strong>Translated Text:</strong><br>" + translatedText + "</p>";
      conversationHistory.push([text, translatedText]);
    });
}


  

recognition.onresult = function (event) {
  var text = "";
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal) {
      text += event.results[i][0].transcript;
    }
  }
  if (text.trim() !== "") {
    document.getElementById("original-text").innerHTML = text;
    translateText(text);
  }
};

// function startRecognition() {
//   if (!recognizing) {
//     recognition.start();
//     recognizing = true;
//     document.getElementById("start-recognition-btn").disabled = true;
//     document.getElementById("stop-recognition-btn").disabled = false;
//   }
// }
async function startRecognition() {
  if (!recognizing) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error('navigator.mediaDevices or getUserMedia() not supported');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      initializeAudioProcessing(stream);
    } catch (err) {
      console.error('Error getting audio stream:', err);
      return;
    }
    recognition.start();
    recognizing = true;
    document.getElementById("start-recognition-btn").disabled = true;
    document.getElementById("stop-recognition-btn").disabled = false;
  }
}





function stopRecognition() {
  if (recognizing) {
    recognition.stop();
    recognizing = false;
    document.getElementById("start-recognition-btn").disabled = false;
    document.getElementById("stop-recognition-btn").disabled = true;
  }
}

function saveConversation() {
  if (conversationHistory.length > 0) {
    var conversationText = "";
    for (var i = 0; i < conversationHistory.length; i++) {
      conversationText +=
        "Original Text: " +
        conversationHistory[i][0] +
        "\n" +
        "Translated Text: " +
        conversationHistory[i][1] +
        "\n\n";
    }
    fetch("/save-conversation", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ conversation_history: conversationHistory }),
    })
      .then((response) => response.json())
      .then((response) => {
        var filename = response.filename;
        window.alert("Conversation saved as " + filename);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    conversationHistory = [];
  }
}



function summarizeConversation() {
  var target_language = document.getElementById("translate-language-select").value;

  // Get the API key input value
  var apiKey = document.getElementById("apikey").value;

  fetch("/summarize-conversation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      target_language: target_language,
      conversation: JSON.stringify(conversationHistory).replace(/- /g, "\n- "),
      api_key: apiKey, // Include the API key in the request body
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      var summary_original = response.summary.original.replace(/\n/g, "<br>");
      var summary_translated = response.summary.translated.replace(/\n/g, "<br>");

      // Display the summaries in the summary history
      const summaryHistory = document.getElementById("summary-history");
      const summaryItem = document.createElement("div");
      summaryItem.classList.add("summary-item");

      const originalSummary = document.createElement("div");
      originalSummary.classList.add("original-summary");
      originalSummary.innerHTML = "<strong>Original:</strong><br>" + summary_original;

      const translatedSummary = document.createElement("div");
      translatedSummary.classList.add("translated-summary");
      translatedSummary.innerHTML = "<strong>Translated:</strong><br>" + summary_translated;

      summaryItem.appendChild(originalSummary);
      summaryItem.appendChild(translatedSummary);
      summaryHistory.appendChild(summaryItem);
    });
}









document
  .getElementById("input-language-select")
  .addEventListener("change", updateRecognitionLanguage);
document
  .getElementById("start-recognition-btn")
  .addEventListener("click", startRecognition);
document
  .getElementById("stop-recognition-btn")
  .addEventListener("click", stopRecognition);
document
  .getElementById("save-conversation-btn")
  .addEventListener("click", saveConversation);
document
  .getElementById("summarize-conversation-btn")
  .addEventListener("click", summarizeConversation);
document
  .getElementById("input-language-select")
  .addEventListener("change", function () {
    var originalText = document.getElementById("original-text").innerHTML;
    if (originalText) {
      translateText(originalText);
    }
  });
