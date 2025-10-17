# Deployment Guide - Railway

## Quick Deploy to Railway

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway to access your repositories

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `glodinasflexwork/kayablue-backend`
4. Railway will automatically detect the configuration

### Step 3: Configure Deployment
Railway will automatically:
- ✅ Detect Python project
- ✅ Install Ghostscript (via nixpacks.toml)
- ✅ Install Python dependencies
- ✅ Set up the start command
- ✅ Assign a public URL

### Step 4: Get Your API URL
1. Go to your project settings
2. Click on "Deployments"
3. Find your public URL (e.g., `https://kayablue-backend-production.up.railway.app`)
4. Copy this URL - you'll need it for the frontend

### Step 5: Test Your API
```bash
# Replace with your Railway URL
API_URL="https://kayablue-backend-production.up.railway.app"

# Health check
curl $API_URL/health

# Test PDF compression
curl -X POST $API_URL/api/compress-pdf \
  -F "file=@test.pdf" \
  -F "quality=medium" \
  --output compressed.pdf
```

## Environment Variables

No environment variables are required! Railway automatically sets:
- `PORT` - The port your app should listen on

## Monitoring

### View Logs
1. Go to your Railway project
2. Click on "Deployments"
3. Click on the latest deployment
4. View real-time logs

### Check Health
Visit: `https://your-app.up.railway.app/health`

Should return:
```json
{
  "status": "healthy",
  "ghostscript_available": true,
  "endpoints": {
    "compress_pdf": "/api/compress-pdf",
    "health": "/health"
  }
}
```

## Updating the Backend

### Automatic Deployments
Railway automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update API"
git push origin master

# Railway will automatically deploy!
```

### Manual Deployment
1. Go to Railway dashboard
2. Click "Deploy"
3. Select the commit you want to deploy

## Troubleshooting

### Deployment Failed
1. Check Railway logs for errors
2. Verify nixpacks.toml includes Ghostscript
3. Ensure requirements.txt is valid

### Ghostscript Not Found
- Check nixpacks.toml has `ghostscript` in nixPkgs
- Verify deployment logs show Ghostscript installation
- Test with `/health` endpoint

### CORS Errors
- Add your frontend URL to CORS origins in main.py
- Redeploy after updating CORS settings

## Cost Estimate

### Railway Pricing
- **Free Tier**: $5 credit/month (good for testing)
- **Hobby Plan**: $5/month (500 hours)
- **Pro Plan**: $20/month (unlimited)

### Typical Usage
- Small projects: Free tier sufficient
- Production: Hobby plan ($5/month)

## Alternative: Render

If you prefer Render over Railway:

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repo
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Add Apt Package**: `ghostscript`

## Next Steps

After deployment:
1. ✅ Copy your API URL
2. ✅ Update frontend to use this URL
3. ✅ Test PDF compression from frontend
4. ✅ Monitor logs for any issues

## Support

For Railway support:
- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)

For this backend:
- Open an issue on GitHub
- Check the README.md

