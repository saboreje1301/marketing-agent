#!/usr/bin/env python3
"""Script para renovar el access token usando el refresh token"""

import json
from pathlib import Path
import httpx
from app.core.config import settings


async def refresh_access_token():
    """Obtiene un nuevo access token usando el refresh token"""
    
    if not settings.GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN:
        raise ValueError("GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN no configurado en .env")
    
    client_secret_file = Path(__file__).parent / "client_secret.json"
    if not client_secret_file.exists():
        raise ValueError(f"No encontrado: {client_secret_file}")
    
    with open(client_secret_file) as f:
        client_data = json.load(f)["installed"]
    
    print("🔄 Renovando access token...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_data["client_id"],
                "client_secret": client_data["client_secret"],
                "refresh_token": settings.GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN,
                "grant_type": "refresh_token",
            }
        )
        response.raise_for_status()
        data = response.json()
        
        new_access_token = data.get("access_token")
        print(f"\n✅ Access token renovado")
        print(f"🔑 Nuevo token: {new_access_token[:20]}...")
        print(f"⏰ Válido por: {data.get('expires_in')} segundos")
        print(f"\n📝 Actualiza en backend/.env:")
        print(f"GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN={new_access_token}")
        
        return new_access_token


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(refresh_access_token())
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
