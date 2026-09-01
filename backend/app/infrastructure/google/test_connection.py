#!/usr/bin/env python3
"""Script para probar la conexión a Google Search Console"""

import asyncio
from datetime import date, timedelta
from app.core.config import settings
from app.infrastructure.google.search_console import query_search_console


async def test_connection():
    """Prueba la conexión a Google Search Console"""
    try:
        print("🔍 Probando conexión a Google Search Console...")
        print(f"📍 Sitio: {settings.GOOGLE_SEARCH_CONSOLE_SITE_URL}")
        print(f"🔑 Access Token: {settings.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN[:20]}...")
        
        # Obtener datos de los últimos 7 días
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
        
        # Probar primero con la URL configurada
        site_url = settings.GOOGLE_SEARCH_CONSOLE_SITE_URL
        print(f"\n📌 Intentando con: {site_url}")
        
        try:
            result = await query_search_console(
                site_url=site_url,
                start_date=start_date,
                end_date=end_date,
                row_limit=10
            )
        except Exception as e:
            # Si falla, probar con formato de dominio
            if "403" in str(e):
                domain_format = f"sc-domain:{site_url.replace('https://', '').replace('http://', '').replace('www.', '')}"
                print(f"\n⚠️  Primer intento falló. Intentando con: {domain_format}")
                result = await query_search_console(
                    site_url=domain_format,
                    start_date=start_date,
                    end_date=end_date,
                    row_limit=10
                )
            else:
                raise
        
        print("\n✅ ¡Conexión exitosa!")
        print(f"\n📊 Datos del período {start_date} a {end_date}:")
        print(f"Total de búsquedas: {len(result['rows'])}")
        
        if result['rows']:
            print("\n🔝 Top búsquedas:")
            for i, row in enumerate(result['rows'], 1):
                print(f"  {i}. {row['query']}")
                print(f"     Clics: {row['clicks']} | Impresiones: {row['impressions']}")
                print(f"     CTR: {row['ctr']:.2%} | Posición: {row['position']:.1f}")
        else:
            print("No hay datos disponibles para este período")
            
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
