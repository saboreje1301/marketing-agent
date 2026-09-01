import json
import re

import httpx

from app.core.config import settings


async def generate_seo_strategy(context: dict) -> dict:
    api_key = settings.GEMINI_API_KEY.strip()
    if not api_key:
        raise ValueError("Falta configurar GEMINI_API_KEY en backend/.env")

    prompt = """Analiza esta auditoría SEO de una página orientada a Google.
Devuelve únicamente JSON válido con estas claves:
summary (string), recommendations (array de strings), suggested_title (string),
suggested_meta_description (string), suggested_keywords (array de strings).

Reglas: el título debe tener entre 30 y 60 caracteres, la meta descripción entre
120 y 160 caracteres, las recomendaciones deben ser concretas y no inventes datos
que no aparezcan en la auditoría.

Auditoría:
""" + json.dumps(context, ensure_ascii=False)

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            f"{settings.GEMINI_BASE_URL.rstrip('/')}/models/"
            f"{settings.GEMINI_MODEL}:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "systemInstruction": {
                    "parts": [{"text": "Eres un especialista técnico en SEO para Google."}]
                },
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "responseMimeType": "application/json",
                },
            },
        )
        response.raise_for_status()

    try:
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("Gemini no devolvió contenido") from error

    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
    try:
        result = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("Gemini no devolvió un JSON válido") from error

    required = {
        "summary",
        "recommendations",
        "suggested_title",
        "suggested_meta_description",
        "suggested_keywords",
    }
    if not required.issubset(result):
        raise ValueError("La respuesta de Gemini no contiene todos los campos SEO")
    return result