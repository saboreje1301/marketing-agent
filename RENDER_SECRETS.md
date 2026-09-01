# 🔐 Secrets en Render.com (Recomendado)

Render tiene dos tipos de variables:

| Tipo | Visibilidad | Uso | Seguridad |
|------|-------------|-----|----------|
| **Environment Variables** | Visible en logs | Config pública | ⚠️ Baja |
| **Secrets** | Oculta | Credenciales API | ✅ Alta (encriptados) |

---

## 📋 Variables públicas (Environment)

Usa **Environment Variables** para:
```
DEBUG=False
APP_NAME=Marketing AI
GEMINI_MODEL=gemini-3.6-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GOOGLE_SEARCH_CONSOLE_SITE_URL=sc-domain:parteluzarquitectura.com
```

---

## 🔑 Credenciales sensibles (Secrets)

**⚠️ IMPORTANTE: Usa valores REALES de tus credenciales, NO estos ejemplos**

Usa **Secrets** (encriptados) para:

```
DATABASE_URL=postgresql://marketing_user:TU_PASSWORD@dpg-xxxxx.internal:5432/marketing_ai
GOOGLE_ADS_DEVELOPER_TOKEN=TU_DEVELOPER_TOKEN_AQUI
GOOGLE_ADS_CLIENT_ID=TU_CLIENT_ID_GOOGLE.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-TU_CLIENT_SECRET_AQUI
GOOGLE_ADS_REFRESH_TOKEN=1//0fTU_REFRESH_TOKEN_AQUI...
GOOGLE_ADS_LOGIN_CUSTOMER_ID=TU_LOGIN_CUSTOMER_ID
GOOGLE_ADS_CUSTOMER_ID=TU_CUSTOMER_ID
GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=ya29.aTU_ACCESS_TOKEN_AQUI...
GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=1//0fTU_SC_REFRESH_TOKEN_AQUI...
GEMINI_API_KEY=TU_GEMINI_API_KEY_AQUI
```

---

## ⚙️ Cómo configurar en Render

### Opción 1: Dashboard manual

1. Ve a tu Web Service en Render
2. Click en **Settings** → **Environment**
3. Sección **Environment Variables** (públicas):
   ```
   DEBUG=False
   APP_NAME=Marketing AI
   ```

4. Sección **Secrets** (encriptadas, no aparecen en logs):
   ```
   DATABASE_URL=postgresql://...
   GEMINI_API_KEY=sk-...
   GOOGLE_ADS_DEVELOPER_TOKEN=...
   etc.
   ```

### Opción 2: File upload (recomendado)

Render permite subir un archivo `.env`:

1. En Settings → Environment
2. Click en **"Load from file"**
3. Sube `backend/.env`
4. Render automáticamente:
   - Detecta variables sensibles
   - Las pone como Secrets
   - Las públicas como Environment Variables

---

## 🛡️ Buenas prácticas

✅ **Hacer**
- Usar Secrets para cualquier API key o token
- Cambiar contraseña de BD después de crear la BD
- Rotar tokens mensualmente
- Usar `render.yaml` para reproducibilidad

❌ **NO hacer**
- Subir `.env` a GitHub
- Compartir Secrets en Slack/email
- Hardcodear tokens en el código
- Usar `DEBUG=True` en producción

---

## 🔄 Actualizar Secrets

Si necesitas renovar un token:

1. Regenera el token en Google Cloud
2. En Render → Settings → Environment → Secrets
3. Actualiza el valor
4. Render redeploya automáticamente

---

## 📊 Render inyecta automáticamente

Si usas base de datos de Render, la app recibe:

```
DATABASE_URL=postgresql://user:pass@host:5432/db
```

Automáticamente (no la configures manualmente).

---

## ✅ Checklist de seguridad

- [ ] `DATABASE_URL` está en Secrets (no visible en logs)
- [ ] Todos los `*_TOKEN` y `*_KEY` están en Secrets
- [ ] `DEBUG=False` en producción
- [ ] `.env` local NO está en GitHub (verificar `.gitignore`)
- [ ] No compartir URLs/credenciales de Render en chat o email
- [ ] Cambiar contraseña de BD si se expuso

---

## 🚨 Si expusiste credenciales accidentalmente

1. **Inmediatamente**:
   - Ir a Google Cloud Console
   - Revocar el API key/token
   - Generar uno nuevo

2. **En Render**:
   - Actualizar el Secret con el nuevo valor
   - El servicio redeploya automáticamente

3. **En el repo**:
   - Verificar que `.env` NO está en Git
   - Si está: `git rm --cached .env && git commit`

---

¡Ahora tus credenciales están seguras! 🎉
