# 🔐 Configuración de credenciales para Render.com

## ⚠️ IMPORTANTE: NO SUBAS CREDENCIALES A GITHUB

Los siguientes archivos contienen credenciales y NO deben subirse:

```
client_secret.json
.env (archivo local)
credentials.json
token.json
```

Estos ya están en `.gitignore`, así que `git push` no los sube. ✅

---

## 📋 Cómo obtener cada credencial

### 1️⃣ Google Search Console

```bash
# En local, genera el token
cd backend/app/infrastructure/google
python generate_access_token.py
# Se abre navegador → autoriza → genera tokens
```

Copias los tokens al `.env` local:
```
GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=ya29.a0AdMD6EgJ9zsa9...
GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=1//0f5IVsnqNYJ3OCgYI...
```

Luego creas una variable de entorno en Render con el **access token actual**:
- En el dashboard de Render → Web Service → Environment
- Añade: `GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=` (el token actual)
- Añade: `GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=` (el refresh token)

---

### 2️⃣ Gemini API Key

```
1. Ve a https://aistudio.google.com/apikey
2. Click "Get API Key"
3. Copia la key
4. En Render → Environment: GEMINI_API_KEY=sk-...
```

---

### 3️⃣ Google Ads (si lo quieres usar)

```
1. Ve a https://developers.google.com/google-ads/api/docs/start
2. Sigue los pasos para crear OAuth 2.0
3. Obtén: CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
4. En Render → Environment, añade los tres
```

---

## 🔄 Renovación automática de tokens

Los tokens de Google expiran cada ~1 hora. En Render:

1. Cuando vencen, la app rechaza con 401
2. Tú vuelves a generar el token en local:
   ```bash
   cd backend/app/infrastructure/google
   python -c "
   import asyncio
   from app.infrastructure.google.refresh_access_token import refresh_access_token
   asyncio.run(refresh_access_token())
   "
   ```
3. Copias el nuevo token
4. Actualizas en Render → Environment variables
5. El servicio redeploya automáticamente

---

## ✅ Checklist antes de subir a GitHub

```bash
# Verifica que NO estás subiendo credenciales
git status

# Debe mostrar "nothing to commit" o solo archivos que querés
# Si ves client_secret.json o .env, HAZ:
git rm --cached client_secret.json
git rm --cached .env
git commit -m "Remove credentials from git"
```

---

## 🚀 Una vez en Render

- Las credenciales viven en las **Environment Variables**
- GitHub solo tiene el código
- Las credenciales nunca se exponen públicamente ✅

---

## ⚠️ Si algo sale mal

Si accidentalmente subiste credenciales:

```bash
# 1. Elimina el token inmediatamente en Google Cloud Console
# 2. En GitHub repo → Settings → Secrets & variables
# 3. Regenera nuevas credenciales
# 4. Actualiza en Render
```

---

¡Listo! Puedes deployar sin preocupaciones. 🎉
