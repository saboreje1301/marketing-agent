# ✅ Checklist de Deployment en Render

## 1️⃣ Preparación local (hoy)

- [ ] Verificar que la app funciona en local:
  ```bash
  cd backend
  uvicorn app.main:app --reload
  # Prueba http://localhost:8000/docs
  ```

- [ ] Verificar credenciales en `.env` local (solo para tests)

- [ ] Revisar `.gitignore` (debe excluir `.env` y `client_secret.json`)
  ```bash
  cat .gitignore | grep -E "\.env|client_secret"
  ```

---

## 2️⃣ GitHub (5 minutos)

- [ ] Crear repositorio en GitHub
  
- [ ] Inicializar git local:
  ```bash
  cd /home/saboreje/web/marketing-agent
  git init
  git add .
  git commit -m "Initial commit - Marketing AI Agent"
  git branch -M main
  git remote add origin https://github.com/TU_USER/marketing-agent.git
  git push -u origin main
  ```

- [ ] Verificar en GitHub que NO subió:
  - `.env`
  - `client_secret.json`
  - Archivos de credentials

---

## 3️⃣ Render (10 minutos)

### 3a. Crear PostgreSQL
- [ ] Ir a https://render.com/dashboard
- [ ] **New +** → **PostgreSQL**
- [ ] Configurar:
  - Name: `marketing-ai-db`
  - Database: `marketing_ai`
  - User: `marketing_user`
  - Plan: **Free**
- [ ] **Create Database**
- [ ] **Copiar Internal Database URL** (guardar en un documento)

### 3b. Crear Web Service
- [ ] **New +** → **Web Service**
- [ ] Seleccionar repo: `marketing-agent`
- [ ] Configurar:
  - Name: `marketing-ai`
  - Region: Misma que BD
  - Branch: `main`
  - Runtime: `Docker`
  - Plan: **Free**

### 3c. Environment Variables y Secrets (⚠️ IMPORTANTE)

Render tiene dos sistemas - **Secrets es más seguro**:

**Opción A: Subir archivo .env (recomendado - más seguro)**

1. En Settings → Environment
2. Click **"Load from file"**
3. Sube `backend/.env` local
4. Render automáticamente:
   - Clasifica tokens/keys como **Secrets** (encriptados)
   - Clasifica config pública como **Environment Variables**
5. ✅ No se exponen en logs

**Opción B: Manual (si prefieres)**

- [ ] En el Web Service, sección **Environment**
- [ ] **Environment Variables** (públicas):
  ```
  DEBUG=False
  APP_NAME=Marketing AI
  GEMINI_MODEL=gemini-3.6-flash
  GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
  GOOGLE_SEARCH_CONSOLE_SITE_URL=sc-domain:parteluzarquitectura.com
  ```

- [ ] **Secrets** (encriptadas):
  ```
  DATABASE_URL=postgresql://marketing_user:PASSWORD@dpg-xxx.internal:5432/marketing_ai
  GEMINI_API_KEY=sk-...
  GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN=ya29.a0AdMD6...
  GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN=1//0f5IVsnqNYJ3OCgYI...
  GOOGLE_ADS_DEVELOPER_TOKEN=...
  GOOGLE_ADS_CLIENT_ID=...
  GOOGLE_ADS_CLIENT_SECRET=...
  GOOGLE_ADS_REFRESH_TOKEN=...
  GOOGLE_ADS_LOGIN_CUSTOMER_ID=...
  GOOGLE_ADS_CUSTOMER_ID=...
  ```

📖 Ver [RENDER_SECRETS.md](RENDER_SECRETS.md) para más detalles sobre seguridad

- [ ] **Create Web Service**
- [ ] **Esperar deploy** (3-5 minutos)

---

## 4️⃣ Verificación

- [ ] Cuando termine el deploy, click en el URL generado
- [ ] Prueba:
  ```bash
  curl https://marketing-ai-XXXX.onrender.com/health
  # Debe devolver: {"status":"ok","app":"Marketing AI","debug":false}
  
  curl https://marketing-ai-XXXX.onrender.com/health/db
  # Debe devolver: {"database":"connected"}
  
  curl https://marketing-ai-XXXX.onrender.com/health/integrations
  # Muestra estado de Gemini, Search Console, etc.
  ```

- [ ] Accede a documentación: `https://marketing-ai-XXXX.onrender.com/docs`

---

## 5️⃣ Uso posterior

- [ ] Cada `git push` a `main` = redeploy automático
- [ ] Si necesitas actualizar credenciales:
  - Regenera token en local
  - Actualiza en Render → Environment
  - El servicio redeploya automáticamente

- [ ] Para ver logs:
  - Render dashboard → Web Service → **Logs**

---

## 🚨 Posibles problemas y soluciones

| Problema | Solución |
|----------|----------|
| Error "database connection refused" | Verifica `DATABASE_URL` en Environment vars |
| Error 500 en endpoint | Ve a Logs en Render dashboard |
| Servicio se pausa constantemente | Es normal en Free tier (se pausa después de 15 min inactividad) |
| Token de Google expirado (401) | Regenera en local y actualiza en Render |

---

## 📊 Resultado final

```
✅ API en: https://marketing-ai.onrender.com
✅ Base de datos: PostgreSQL en Render
✅ Documentación: https://marketing-ai.onrender.com/docs
✅ Código en GitHub (sin credenciales)
✅ Deploy automático en cada git push
```

---

**¡Listo para deployar! 🚀**

Si algo falla, revisa [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.
