from fastapi import FastAPI, Request
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "ваш"))

@app.post("/")
async def handle_salute_request(request: Request):
    req_data = await request.json()
    user_message = ""
    try:
        user_message = req_data.get("payload", {}).get("message", {}).get("normalized_text", "")
    except Exception:
        pass
    
    if not user_message:
        user_message = "Привет! Чем могу помочь?"

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_message,
        )
        ai_text = response.text
    except Exception as e:
        ai_text = f"Ошибка: {str(e)}"

    return {
        "suppress_speech": False,
        "payload": {
            "pronounce_text": ai_text,
            "text": ai_text
        },
        "session": req_data.get("session", {}),
        "version": req_data.get("version", "2.0")
    }