# Railway Deployment Checklist

## ✅ Pre-Deployment Checklist

### Files Ready
- [x] `requirements.txt` - All dependencies included
- [x] `Procfile` - Gunicorn configured
- [x] `railway.json` - Railway configuration
- [x] `runtime.txt` - Python version specified
- [x] `.gitignore` - Sensitive files excluded
- [x] `settings.py` - Configured for Railway (PostgreSQL, WhiteNoise, environment variables)

### Settings Configuration
- [x] Environment variables support (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [x] PostgreSQL database configuration (auto-detects DATABASE_URL)
- [x] WhiteNoise for static files
- [x] SQLite fallback for local development

## 🚀 Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets DATABASE_URL

5. **Set Environment Variables**
   In Railway project → Settings → Variables:
   
   - **SECRET_KEY**: Generate with:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   
   - **DEBUG**: Set to `False` (for production)
   
   - **ALLOWED_HOSTS**: Your Railway domain (e.g., `your-app.up.railway.app`)
     Or leave as `*` (Railway handles it)

6. **Deploy**
   - Railway will automatically detect Django
   - It will install dependencies
   - It will build and deploy

7. **Run Migrations** (First Time)
   - In Railway dashboard → Your service → Settings → Deploy
   - Add one-off command: `python manage.py migrate`
   - Or use Railway CLI: `railway run python manage.py migrate`

8. **Create Superuser**
   - Use Railway CLI:
     ```bash
     railway run python manage.py createsuperuser
     ```
   - Or add one-off command in Railway dashboard

9. **Collect Static Files** (if needed)
   - Railway should handle this automatically
   - If not: `railway run python manage.py collectstatic --noinput`

## 🔍 Post-Deployment Verification

- [ ] Website loads correctly
- [ ] Static files (CSS, images) load
- [ ] Database connection works
- [ ] Admin panel accessible
- [ ] All pages render correctly
- [ ] Contact form works
- [ ] No errors in Railway logs

## 📝 Notes

- Railway automatically provides HTTPS
- Static files are served via WhiteNoise
- Database is PostgreSQL (auto-configured)
- Media files are stored locally (consider cloud storage for production)
- Railway provides $5 free credit monthly

## 🆘 Troubleshooting

If something doesn't work:
1. Check Railway logs (Service → Logs)
2. Verify environment variables are set
3. Ensure migrations have run
4. Check that all dependencies are in requirements.txt
5. Verify static files were collected

See `RAILWAY_DEPLOYMENT.md` for detailed instructions.

