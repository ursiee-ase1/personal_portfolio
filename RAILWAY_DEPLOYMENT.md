# Deploying Django Portfolio to Railway

Railway is an excellent platform for deploying Django applications. It provides PostgreSQL databases, automatic deployments, and easy configuration.

## 🚀 Quick Start Guide

### Step 1: Create a Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended) or email
3. Create a new project

### Step 2: Connect Your Repository

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your portfolio repository
4. Railway will automatically detect Django

### Step 3: Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

### Step 4: Set Environment Variables

In your Railway project settings, add these environment variables:

1. **SECRET_KEY** (Required)
   - Generate one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Or use: `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

2. **DEBUG** (Optional, defaults to False)
   - Set to `False` for production
   - Set to `True` only for debugging

3. **ALLOWED_HOSTS** (Optional)
   - Your Railway domain: `your-app.up.railway.app`
   - Or leave as `*` (Railway will handle it)

4. **DATABASE_URL** (Automatic)
   - Railway sets this automatically when you add PostgreSQL
   - No need to set manually

### Step 5: Deploy

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run migrations (if configured)
- Collect static files
- Start your Django app with Gunicorn

### Step 6: Run Migrations (First Time)

After the first deployment:

1. Go to your Railway project
2. Click on your service
3. Go to "Settings" → "Deploy"
4. Add a one-off command: `python manage.py migrate`
5. Or use Railway CLI:
   ```bash
   railway run python manage.py migrate
   ```

### Step 7: Create Superuser

To access Django admin:

1. Use Railway CLI:
   ```bash
   railway run python manage.py createsuperuser
   ```
2. Or add a one-off command in Railway dashboard

## 📁 Files Created for Railway

- **`Procfile`**: Defines how to run your app
- **`railway.json`**: Railway-specific configuration
- **`requirements.txt`**: Python dependencies (updated with Railway packages)
- **`runtime.txt`**: Python version specification

## 🔧 Configuration Details

### Database
- Railway automatically provides PostgreSQL
- `DATABASE_URL` is set automatically
- Settings.py is configured to use PostgreSQL on Railway, SQLite locally

### Static Files
- WhiteNoise middleware handles static files
- Static files are collected during deployment
- No additional configuration needed

### Media Files
- Media files are stored locally on Railway
- For production, consider using cloud storage (AWS S3, Cloudinary)
- See "Media File Storage" section below

## 🛠️ Railway CLI (Optional)

Install Railway CLI for easier management:

```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell
```

## 📦 Media File Storage (Optional)

For production, use cloud storage instead of local files:

### Option 1: AWS S3
1. Install: `pip install django-storages boto3`
2. Add to `INSTALLED_APPS`: `'storages'`
3. Configure in settings.py:
   ```python
   AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   ```

### Option 2: Cloudinary
1. Install: `pip install django-cloudinary-storage`
2. Add to `INSTALLED_APPS`: `'cloudinary_storage'`, `'cloudinary'`
3. Configure in settings.py:
   ```python
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
       'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
       'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
   }
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

## 🔒 Security Checklist

Before going live:

- [ ] Set `DEBUG=False` in production
- [ ] Use a strong `SECRET_KEY` (not the default)
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use HTTPS (Railway provides this automatically)
- [ ] Review Django security settings
- [ ] Set up proper media file storage (cloud storage)

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL service is running in Railway
- Check that `DATABASE_URL` is set automatically
- Verify migrations have run

### Static Files Not Loading
- Check that `collectstatic` ran during deployment
- Verify WhiteNoise is in `MIDDLEWARE`
- Check `STATIC_ROOT` is set correctly

### App Not Starting
- Check Railway logs: Click on your service → "Logs"
- Verify all environment variables are set
- Check that `requirements.txt` has all dependencies

### Migrations Not Running
- Run manually: `railway run python manage.py migrate`
- Or add to Procfile before collectstatic

## 📊 Monitoring

Railway provides:
- Real-time logs
- Metrics (CPU, Memory, Network)
- Deployment history
- Automatic HTTPS

## 💰 Pricing

- **Free Tier**: $5 credit/month
- **Hobby Plan**: $5/month (after free credit)
- **Pro Plan**: $20/month

Check [railway.app/pricing](https://railway.app/pricing) for current pricing.

## 🎉 Next Steps

After deployment:

1. Set up a custom domain (optional)
2. Configure media file storage (cloud storage)
3. Set up monitoring/analytics
4. Configure backups for your database
5. Set up CI/CD for automatic deployments

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)

