import React, { useState } from "react";
import axios from "axios";

// Use the environment variable for the API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL; // e.g., http://127.0.0.1:8000

export default function App() {
  const [transcript, setTranscript] = useState("");
  const [translation, setTranslation] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [inputLang, setInputLang] = useState("en");
  const [outputLang, setOutputLang] = useState("es");

  // Supported languages
  const languages = {
    en: "English",
    es: "Spanish",
    fr: "French",
    de: "German",
    zh: "Chinese",
    ar: "Arabic",
    hi: "Hindi",
  };

  // Handle speech recognition
  const handleSpeechRecognition = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = inputLang;
    recognition.start();
    setLoading(true);

    recognition.onresult = (event) => {
      setTranscript(event.results[0][0].transcript);
      setLoading(false);
    };

    recognition.onerror = (event) => {
      setError("Speech recognition failed.");
      setLoading(false);
    };
  };

  // Handle audio file upload and transcription
  const handleAudioUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    setTranscript("");
    setTranslation("");
    setAudioUrl(null);
    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_BASE_URL}/transcribe/`, formData, {
        headers: { "x-api-key": process.env.REACT_APP_API_KEY },
      });
      console.log("Transcription Response:", response.data);
      setTranscript(response.data.transcript);
    } catch (err) {
      console.error("Transcription error:", err.response || err);
      setError("Failed to transcribe audio.");
    } finally {
      setLoading(false);
    }
  };

  // Handle translation (using FormData because the backend expects form data)
  const handleTranslation = async () => {
    if (!transcript) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("text", transcript);
      formData.append("input_lang_code", inputLang);
      formData.append("output_lang_code", outputLang);

      const response = await axios.post(`${API_BASE_URL}/translate/`, formData, {
        headers: {
          "x-api-key": process.env.REACT_APP_API_KEY,
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Translation response:", response.data);
      setTranslation(response.data.translated_text);
    } catch (err) {
      console.error("Translation error:", err.response || err);
      setError("Translation failed.");
    } finally {
      setLoading(false);
    }
  };

  // Handle text-to-speech (also using FormData)
  const handleTextToSpeech = async () => {
    if (!translation) return;
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("text", translation);
      formData.append("input_lang_code", inputLang);
      formData.append("output_lang_code", outputLang);

      const response = await axios.post(`${API_BASE_URL}/translate/`, formData, {
        headers: {
          "x-api-key": process.env.REACT_APP_API_KEY,
          "Content-Type": "multipart/form-data",
        },
      });

      const audioFileName = response.data.audio_file;
      const audioResponse = await axios.get(`${API_BASE_URL}/audio/${audioFileName}`, {
        headers: { "x-api-key": process.env.REACT_APP_API_KEY },
        responseType: "arraybuffer",
      });
      const audioBlob = new Blob([audioResponse.data], { type: "audio/mp3" });
      setAudioUrl(URL.createObjectURL(audioBlob));
    } catch (err) {
      console.error("Text-to-speech error:", err.response || err);
      setError("Text-to-speech conversion failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center p-10 w-full max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-5">Healthcare Translation App</h1>

      <div className="flex gap-2 mb-3">
        <select onChange={(e) => setInputLang(e.target.value)} value={inputLang} className="border p-2">
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
        <select onChange={(e) => setOutputLang(e.target.value)} value={outputLang} className="border p-2">
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>

      <button onClick={handleSpeechRecognition} className="bg-blue-500 text-white px-4 py-2 rounded mb-3">
        Start Speech
      </button>
      <input type="file" accept="audio/*" onChange={handleAudioUpload} className="mb-3" />

      {loading && <p className="text-blue-500">Processing...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {transcript && <p className="mb-3">Transcript: {transcript}</p>}
      <button
        onClick={handleTranslation}
        className="bg-green-500 text-white px-4 py-2 rounded mb-3 disabled:opacity-50"
        disabled={!transcript || loading}
      >
        Translate
      </button>
      {translation && <p className="mb-3">Translation: {translation}</p>}

      <button
        onClick={handleTextToSpeech}
        className="bg-purple-500 text-white px-4 py-2 rounded mb-3 disabled:opacity-50"
        disabled={!translation || loading}
      >
        Play Audio
      </button>
      {audioUrl && <audio controls src={audioUrl} className="mt-3" />}
    </div>
  );
}
