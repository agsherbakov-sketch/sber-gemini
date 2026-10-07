from fastapi import FastAPI, Request
from google import genai
import os

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/")
async def handle_salute_request(request: Request):
    req_data = await request.json()
    print("=== Входящий запрос ===")
    print(req_data)

    # --- Извлекаем текст пользователя ---
    user_message = ""
    try:
        user_message = (
            req_data.get("payload", {})
            .get("message", {})
            .get("original_text")
            or req_data.get("payload", {})
            .get("message", {})
            .get("normalized_text")
            or ""
        )
    except Exception:
        pass

    if not user_message:
        user_message = "Привет"

    print(f"Текст пользователя: {user_message}")

    # --- Запрос к Gemini ---
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message
        )
        answer_text = response.text or "Не удалось получить ответ"
        print(f"Ответ Gemini: {answer_text}")
    except Exception as e:
        answer_text = f"Произошла ошибка: {str(e)}"
        print(f"Ошибка Gemini: {answer_text}")

    result = {
        "messageName": "ANSWER_TO_USER",
        "sessionId": req_data.get("sessionId"),
        "messageId": req_data.get("messageId", 0),
        "uuid": req_data.get("uuid", {}),
        "payload": {
            "pronounceText": answer_text,
            "pronounceTextType": "application/text",
            "items": [
                {
                    "bubble": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    print("=== Отправляем ответ ===")
    print(result)
    return result
