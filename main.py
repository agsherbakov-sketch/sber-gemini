from fastapi import FastAPI, Request
from google import genai
import os

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
            model="gemini-2.5-flash",
            contents=user_message
        )
        answer_text = response.text
    except Exception as e:
        answer_text = f"Ошибка генерации: {str(e)}"

    return {
        "response": {
            "text": answer_text,
            "tts": answer_text,
            "items": [
                {
                    "bubble": {
                        "text": answer_text
                    }
                }
            ]
        },
        "session": req_data.get("session", {}),
        "version": req_data.get("version", "1.0")
    }
