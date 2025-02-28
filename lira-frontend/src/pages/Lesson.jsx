import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import axios from "axios";

const words = ["bat", "cop", "bib", "pan", "rut", "fed"];

const Lesson = () => {
  const [index, setIndex] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [highlightedWord, setHighlightedWord] = useState(words[0]);
  const navigate = useNavigate();
  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  useEffect(() => {
    if (!listening && transcript) {
      checkPronunciation(transcript);
    }
  }, [transcript, listening]);

  const checkPronunciation = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setFeedback("⚠️ You need to be logged in.");
        return;
      }

      // Record audio
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("file", audioBlob, "audio.wav");
        formData.append("current_word", words[index]); // Send expected word

        console.log("🔹 Sending request with FormData:", formData);

        const response = await axios.post(
          "http://127.0.0.1:8000/lesson/speech",
          formData,
          {
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        console.log("✅ Response received:", response.data);

        if (response.data.correct) {
          setFeedback("✅ Correct! Moving to next word...");
          setTimeout(() => {
            if (index < words.length - 1) {
              setIndex((prev) => prev + 1);
              setHighlightedWord(words[index + 1]);
              resetTranscript();
              setFeedback("");
            } else {
              setFeedback("🎉 Lesson Complete!");
              setTimeout(() => navigate("/dashboard"), 2000);
            }
          }, 2000);
        } else {
          setFeedback("❌ Incorrect, try again!");
          setHighlightedWord(response.data.highlighted || words[index]);
        }
      };

      mediaRecorder.start();
      setTimeout(() => {
        mediaRecorder.stop();
      }, 3000); // Stop after 3 seconds

    } catch (error) {
      console.error("❌ Error checking pronunciation:", error);
      setFeedback("⚠️ Error processing speech. Try again.");
    }
  };

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <p>⚠️ Your browser does not support speech recognition.</p>;
  }

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Say the word:</h2>
      <h1 style={{ fontSize: "50px", color: "black" }}>
        <span dangerouslySetInnerHTML={{ __html: highlightedWord }} />
      </h1>

      <button 
        onClick={checkPronunciation} 
        disabled={listening}
      >
        🎤 Start Speaking
      </button>

      <p>🎙️ You said: {transcript}</p>
      <p>{feedback}</p>
    </div>
  );
};

export default Lesson;
