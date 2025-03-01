import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from cryptography.fernet import Fernet
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set API keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not OPENAI_API_KEY or not API_KEY:
    raise ValueError("Missing API keys in environment variables")
openai.api_key = OPENAI_API_KEY

# Retrieve encryption key or generate one if missing
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
cipher = Fernet(ENCRYPTION_KEY.encode())

# Initialize FastAPI app
app = FastAPI()

# Configure Logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("FastAPI app started successfully.")

# Mount static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../static")), name="static")

# Language Mapping: ISO code -> Language Name
LANGUAGE_MAPPING = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "zh": "Chinese", "ar": "Arabic", "hi": "Hindi", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "ja": "Japanese", "ko": "Korean",
    "tr": "Turkish"
}

# Reverse mapping: Language Name (lowercase) -> ISO code
LANGUAGE_NAME_TO_CODE = {v.lower(): k for k, v in LANGUAGE_MAPPING.items()}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204) 

# API Key verification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# File cleanup helper function
def cleanup_file(path: str):
    try:
        os.remove(path)
        logging.info(f"Cleaned up temporary file: {path}")
    except Exception as e:
        logging.error(f"Error cleaning up file {path}: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Translation App!"}

@app.post("/transcribe/", dependencies=[Depends(verify_api_key)])
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        logging.info(f"Audio file saved at: {temp_audio_path}")

        with open(temp_audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)

        os.remove(temp_audio_path)
        return {"transcript": response.get("text", "")}
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logging.error(f"General Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

async def translate_text_gpt(text: str, input_lang: str, output_lang: str) -> str:
    try:
        system_prompt = (
            f"You are a professional translator with expertise in medical terms. "
            f"Translate the following text from {LANGUAGE_MAPPING.get(input_lang, input_lang)} "
            f"to {LANGUAGE_MAPPING.get(output_lang, output_lang)} with high accuracy."
        )
        logging.info(f"Calling OpenAI API for translation: {system_prompt}")
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        logging.info(f"OpenAI API response: {response}")

        translated_text = response["choices"][0]["message"]["content"].strip()
        return translated_text
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="OpenAI API translation failed")
    except Exception as e:
        logging.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail="Translation process failed")

@app.post("/translate/", dependencies=[Depends(verify_api_key)])
async def translate_and_speak(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    input_lang_code: str = Form(...),
    output_lang_code: str = Form(...),
):
    try:
        logging.info(f"Received translation request for text: {text}")
        translated_text = await translate_text_gpt(text, input_lang_code, output_lang_code)
        logging.info(f"Translation successful: {translated_text}")

        # Convert provided output language to a valid ISO code if needed
        if output_lang_code not in LANGUAGE_MAPPING:
            mapped_code = LANGUAGE_NAME_TO_CODE.get(output_lang_code.lower())
            if mapped_code:
                output_lang_code = mapped_code
            else:
                logging.warning(f"Language code for '{output_lang_code}' not found. Falling back to English.")
                output_lang_code = "en"

        try:
            tts = gTTS(translated_text, lang=output_lang_code)
        except ValueError as e:
            logging.error(f"Error in TTS generation with lang '{output_lang_code}': {e}")
            tts = gTTS(translated_text, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            temp_file_path = temp_audio.name

        # Encrypt the audio file for secure transport
        with open(temp_file_path, "rb") as file:
            encrypted_data = cipher.encrypt(file.read())
        with open(temp_file_path, "wb") as file:
            file.write(encrypted_data)

        # NOTE: Removed immediate cleanup here to ensure the file remains available
        logging.info(f"Returning audio file path: {temp_file_path}")
        return {"original_text": text, "translated_text": translated_text, "audio_file": os.path.basename(temp_file_path)}

    except Exception as e:
        logging.error(f"Translation or TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation/TTS process failed: {str(e)}")

@app.get("/audio/{filename}", dependencies=[Depends(verify_api_key)])
async def serve_audio(filename: str, background_tasks: BackgroundTasks):
    try:
        file_path = os.path.join(tempfile.gettempdir(), filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        decrypted_file_path = file_path + "_decrypted.mp3"
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        with open(decrypted_file_path, "wb") as file:
            file.write(decrypted_data)

        # Schedule cleanup for both decrypted and encrypted files after serving
        background_tasks.add_task(cleanup_file, decrypted_file_path)
        background_tasks.add_task(cleanup_file, file_path)
        return FileResponse(decrypted_file_path, media_type="audio/mp3")
    except Exception as e:
        logging.error(f"Audio decryption error: {e}")
        raise HTTPException(status_code=500, detail="Audio decryption failed")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
