# Marketing AI Agent

App de marketing inteligente con agentes IA para SEO, Analytics y Google Ads automation.

## 🎯 Características

- **SEO Agent**: Auditoría técnica + análisis IA con datos de Google Search Console
- **Analytics Agent**: Métricas de Google Ads en tiempo real
- **Search Console Agent**: Consultas de búsqueda y datos de rendimiento
- **Coordinator Agent**: Reporte integrado SEO + Analytics
- **Automation**: Workflow de creación de campañas en Google Ads

## 🚀 Deployment en Render

### Requisitos
- Cuenta en [Render.com](https://render.com)
- Credenciales de Google (Ads, Search Console, Gemini)

### Paso 1: Preparar repositorio

```bash
# 1. Sube tu código a GitHub
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Paso 2: Crear servicio en Render

1. Ve a [render.com/dashboard](https://render.com/dashboard)
2. Click en **"New +"** → **"Web Service"**
3. Selecciona tu repositorio
4. Configura:
   - **Name**: `marketing-ai`
   - **Region**: Elige la más cercana
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: Free

### Paso 3: Variables de entorno

En la sección **Environment Variables**, añade:

```
DEBUG=False
APP_NAME=Marketing AI
DB_HOST=localhost
DB_PORT=5432
DB_NAME=marketing_ai
DB_USER=marketing_user
DB_PASSWORD=(genera una contraseña segura)

DEEPSEEK_API_KEY=(opcional)
GOOGLE_ADS_DEVELOPER_TOKEN=
GOOGLE_ADS_CLIENT_ID=
GOOGLE_ADS_CLIENT_SECRET=
GOOGLE_ADS_REFRESH_TOKEN=
GOOGLE_ADS_LOGIN_CUSTOMER_ID=
GOOGLE_ADS_CUSTOMER_ID=

GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=
GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=
GOOGLE_SEARCH_CONSOLE_SITE_URL=sc-domain:tudominio.com

GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.6-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

### Paso 4: Crear base de datos PostgreSQL

1. Click en **"New +"** → **"PostgreSQL"**
2. Configura:
   - **Name**: `marketing-ai-db`
   - **Plan**: Free
3. Click **Create Database**
4. Copia la **Internal Database URL** y actualiza en el Web Service:
   - Variable: `DATABASE_URL`
   - Valor: La URL que copiaste

### Paso 5: Deploy

1. Click **"Deploy"** en el Web Service
2. Espera 2-3 minutos
3. Verifica en `https://marketing-ai.onrender.com/health`

---

## 🔧 Desarrollo Local

### Setup

```bash
# 1. Clonar repo
git clone <tu-repo>
cd marketing-agent

# 2. Crear venv
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Edita .env con tus credenciales
```

### Ejecutar

```bash
# Backend debe estar corriendo en localhost:5432 (PostgreSQL)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints principales

- `GET /health` - Estado general
- `GET /health/db` - Conexión a BD
- `GET /health/integrations` - Estado de integraciones
- `POST /api/v1/seo/ai-audit` - Auditoría SEO con IA + Search Console
- `POST /api/v1/search-console/queries` - Datos de Search Console
- `POST /api/v1/analytics/campaign` - Métricas de Google Ads
- `POST /api/v1/coordinator/report` - Reporte integrado

Documentación interactiva: `http://localhost:8000/docs`

---

## 🔐 Credenciales necesarias

### Google Ads
1. Ve a [Google Ads API](https://developers.google.com/google-ads/api/docs/start)
2. Crea credenciales OAuth 2.0
3. Autoriza la app y obtén el refresh token

### Google Search Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita "Google Search Console API"
3. Descarga credenciales OAuth
4. Ejecuta `generate_access_token.py` en local
5. Copia tokens a `.env`

### Gemini API
1. Ve a [Google AI Studio](https://aistudio.google.com/apikey)
2. Crea una API Key
3. Cópiala a `GEMINI_API_KEY`

---

## 📊 Arquitectura

```
backend/
├── app/
│   ├── ai/                 # Agentes IA
│   ├── api/routes/         # Endpoints
│   ├── core/               # Config
│   ├── infrastructure/      # Integraciones externas
│   ├── schemas/            # Modelos Pydantic
│   └── main.py
├── migrations/             # Alembic
└── requirements.txt
```

---

## 📝 Notas

- Los tokens de Google expiran cada ~1 hora. Render ejecuta automáticamente renovación.
- La BD PostgreSQL gratuita en Render tiene límites. Para producción, considera un upgrade.
- Si necesitas frontend, considera Vercel o Netlify.

---

## 🆘 Troubleshooting

**Error 401 en Search Console**
→ Token expirado. Regenera en local y actualiza `.env`

**Error de conexión a BD**
→ Verifica que `DATABASE_URL` está configurada en Render

**Memoria insuficiente**
→ Upgrade a plan pago o optimiza queries

---

## 📧 Soporte

Contacta al desarrollador o abre un issue en el repositorio.
