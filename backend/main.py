# main.py
import traceback
import io
from PIL import Image
import pytesseract
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# CRITICAL FIX: Direct import for Uvicorn
from utils import translate_text, get_pronunciation_audio

# --- CONFIGURATION SECTION ---

# 1. Tesseract Path (CRITICAL FOR WINDOWS)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 2. OCR Language
FRENCH_LANG_CODE = 'fra' 

# --- FASTAPI SETUP ---

app = FastAPI()

# 3. CORS MIDDLEWARE 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINT ---

@app.post("/ocr_process")
async def ocr_process_endpoint(image: UploadFile = File(...)):
    
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        # 4. Read and Open Image
        file_content = await image.read()
        pil_image = Image.open(io.BytesIO(file_content))
        
        # 5. Perform OCR
        extracted_text = pytesseract.image_to_string(pil_image, lang=FRENCH_LANG_CODE)
        clean_text = extracted_text.strip()
        
        if not clean_text:
            return JSONResponse(content={
                "status": "success",
                "extracted_text": "No text found",
                "translated_meaning": "No meaning available",
                "pronunciation_audio": "" 
            })
            
        # 6. Perform Translation
        translated_meaning = translate_text(clean_text) 
        
        # 7. Perform Pronunciation Generation (Enabled)
        pronunciation_audio = get_pronunciation_audio(clean_text) 
        
        # 8. Return Success
        return JSONResponse(content={
            "status": "success",
            "extracted_text": clean_text,
            "translated_meaning": translated_meaning,
            "pronunciation_audio": pronunciation_audio # Sending the base64 string
        })

    except pytesseract.TesseractNotFoundError:
        error_message = "Tesseract executable not found. Check path in main.py."
        print(f"FATAL ERROR: {error_message}")
        raise HTTPException(status_code=500, detail=error_message)
        
    except Exception as e:
        traceback.print_exc() 
        print(f"--- UNHANDLED CRASH DETECTED: {str(e)} ---")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")



