# 🚀 Guía de Deployment en Render.com

## Paso 1️⃣: Preparar repositorio GitHub

```bash
cd /home/saboreje/web/marketing-agent

# Inicializar git (si no lo has hecho)
git init
git add .
git commit -m "Initial commit - Marketing AI"

# Crear repositorio en GitHub y subir
git branch -M main
git remote add origin https://github.com/TU_USUARIO/marketing-agent.git
git push -u origin main
```

---

## Paso 2️⃣: Crear cuenta en Render.com

1. Ve a https://render.com
2. Haz signup con GitHub (más fácil)
3. Autoriza Render a acceder a tus repos

---

## Paso 3️⃣: Crear PostgreSQL en Render

1. En dashboard → **New +** → **PostgreSQL**
2. Configura:
   - **Name**: `marketing-ai-db`
   - **Database**: `marketing_ai`
   - **User**: `marketing_user`
   - **Region**: Elige la más cercana (ej: Frankfurt)
   - **Plan**: Free (gratuito)
3. Click **Create Database**
4. **⚠️ IMPORTANTE**: Copia la **Internal Database URL** (la que empieza con `postgresql://`)
   - Ejemplo: `postgresql://marketing_user:PASSWORD@dpg-xxx.internal:5432/marketing_ai`

---

## Paso 4️⃣: Crear Web Service en Render

1. Dashboard → **New +** → **Web Service**
2. Selecciona tu repositorio `marketing-agent`
3. Configura:
   - **Name**: `marketing-ai`
   - **Region**: Igual que la BD
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Build Command**: (dejar vacío - usa Dockerfile)
   - **Start Command**: (dejar vacío - usa Dockerfile)
   - **Plan**: Free

---

## Paso 5️⃣: Configurar variables de entorno

En la sección **Environment Variables** del Web Service, añade:

### Variables básicas
```
DEBUG=False
APP_NAME=Marketing AI
```

### Database (⚠️ MUY IMPORTANTE)
```
DATABASE_URL=postgresql://marketing_user:PASSWORD@dpg-xxx.internal:5432/marketing_ai
```
(Pega la URL interna de PostgreSQL que copiaste)

### Google Ads (opcional, solo si quieres usar)
```
GOOGLE_ADS_DEVELOPER_TOKEN=
GOOGLE_ADS_CLIENT_ID=
GOOGLE_ADS_CLIENT_SECRET=
GOOGLE_ADS_REFRESH_TOKEN=
GOOGLE_ADS_LOGIN_CUSTOMER_ID=
GOOGLE_ADS_CUSTOMER_ID=
```

### Google Search Console (opcional)
```
GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=
GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=
GOOGLE_SEARCH_CONSOLE_SITE_URL=sc-domain:parteluzarquitectura.com
```

### Gemini API (opcional)
```
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.6-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

---

## Paso 6️⃣: Deploy

1. Click **Create Web Service**
2. Render inicia el build automáticamente
3. Espera 3-5 minutos
4. Verifica el estado en el dashboard

---

## Paso 7️⃣: Verificar que está funcionando

Cuando el deploy termine, haz clic en el URL (ej: `https://marketing-ai.onrender.com`)

Prueba estos endpoints:

```bash
# Health check
curl https://marketing-ai.onrender.com/health

# Base de datos
curl https://marketing-ai.onrender.com/health/db

# Integraciones
curl https://marketing-ai.onrender.com/health/integrations

# Documentación interactiva
https://marketing-ai.onrender.com/docs
```

---

## 📝 Notas importantes

⚠️ **El plan Free tiene limitaciones:**
- Servicio se pausa después de 15 min de inactividad
- Tarda 30s en despertar cuando llamamos
- BD tiene 500 MB de almacenamiento
- Para producción seria, necesitas plan pago

✅ **Para pruebas personales, es perfecto**

---

## 🔄 Actualizaciones futuras

Cada vez que hagas `git push` a `main`, Render redeploya automáticamente.

---

## 🆘 Troubleshooting

**El servicio no inicia**
→ Ve a **Logs** en el dashboard y busca el error

**Error "database connection refused"**
→ Verifica que `DATABASE_URL` está correcta

**Error 404 en endpoints**
→ Esperá 30s (el servicio puede estar despertando)

---

## ✅ ¡Listo!

Tu app está en: `https://marketing-ai.onrender.com`

Puedes usarla desde cualquier lugar. 🎉
