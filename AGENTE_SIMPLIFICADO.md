📊 AGENTE OPTIMIZADO - CONVERSIÓN SIMPLIFICADA

Tu agente ahora es ULTRA SIMPLE y enfocado 100% en CONVERSIONES.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 CÓMO FUNCIONA

1. Tú asignas:
   - Campaign ID (de Google Ads)
   - Presupuesto diario

2. El agente automáticamente:
   ✅ Obtiene métricas de Google Ads
   ✅ Analiza conversion rate por ad group
   ✅ Aumenta bids en ad groups que convierten
   ✅ Reduce bids en ad groups que no convierten
   ✅ Ajusta presupuesto de la campaña
   ✅ Retorna análisis detallado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 ENDPOINT ÚNICO

POST /api/v1/optimize

BODY:
{
  "campaign_id": "123456",
  "budget": 50.00
}

RESPONSE:
{
  "campaign_id": "123456",
  "status": "optimized",
  "conversions_before": 15,
  "conversions_projected": 18,
  "budget_assigned": 50.00,
  "budget_action": "increased_to_target",
  "optimizations": [
    {
      "ad_group_id": "789",
      "ad_group_name": "High Converting Keywords",
      "conversions": 10,
      "conversion_rate": 5.25,
      "cpa": 4.75,
      "old_bid": 1.50,
      "new_bid": 1.73,
      "action": "increase_bid"
    },
    {
      "ad_group_id": "790",
      "ad_group_name": "Low Performing",
      "conversions": 0,
      "conversion_rate": 0.0,
      "cpa": "N/A",
      "old_bid": 2.00,
      "new_bid": 1.70,
      "action": "reduce_bid"
    }
  ],
  "summary": "Optimización completada: 2 ad groups ajustados"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 ESTRUCTURA FINAL

backend/app/
├── ai/
│   └── conversion_optimizer_agent.py  ← Agente de optimización
├── api/routes/
│   ├── campaigns.py                   ← Listar/crear campañas
│   ├── health.py                      ← Health check
│   └── optimization.py                ← Endpoint de optimización
├── core/
│   └── config.py                      ← Configuración (con DATABASE_URL)
├── database/
│   └── database.py                    ← Conexión a BD
└── main.py                            ← FastAPI app (limpia y simple)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ENDPOINTS DISPONIBLES

GET  /                               → Status del servicio
GET  /api/v1/health                 → Health check
GET  /api/v1/campaigns              → Listar campañas
POST /api/v1/campaigns              → Crear campaña
POST /api/v1/optimize               → Optimizar para conversiones ⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CONFIGURACIÓN NECESARIA

En Render:
1. Environment → Agregar variable:
   DATABASE_URL = postgresql://...
   
2. Redeploy el servicio

¡Listo! El agente está listo para usar.
