# Tamil Calendar API - Railway Deployment Guide

## Overview

This is the Tamil Calendar API, adapted from the Telugu Calendar API with Tamil-specific translations and locations.

## Key Differences from Telugu Calendar

### Calendar System
Both Tamil and Telugu calendars use the **same astronomical calculations**:
- Swiss Ephemeris for precise planetary positions
- Lahiri Ayanamsa (Chitrapaksha) for sidereal calculations
- Identical Panchangam element calculations (Tithi, Nakshatra, Yoga, Karana, etc.)

### What's Different
1. **Language**: All translations changed from Telugu (te) to Tamil (ta)
2. **Locations**: Added Tamil Nadu cities (Chennai, Madurai, Coimbatore)
3. **Month Names**: Uses Tamil month names (Chitt

irai, Vaikasi, Aani, etc.)
4. **Branding**: Changed from Telugu Calendar to Tamil Calendar

## Railway Deployment Steps

### 1. Create New Railway Project

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account if not already connected
5. Select the Tamil Calendar API repository

### 2. Configure Railway

Railway will automatically detect the Python project. The following files are configured for Railway:

- **Procfile**: Defines the web process
  ```
  web: uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

- **runtime.txt**: Specifies Python version
  ```
  python-3.11
  ```

- **requirements.txt**: Lists all Python dependencies

- **nixpacks.toml**: Build configuration for Railway

### 3. Environment Variables

Railway will automatically set the `PORT` variable. No additional environment variables are required.

### 4. Deploy

Railway will automatically:
1. Detect the Python project
2. Install dependencies from requirements.txt
3. Build the application
4. Deploy to a public URL

### 5. Access Your API

Once deployed, Railway will provide a public URL like:
```
https://tamil-calendar-api-production.up.railway.app
```

You can access:
- API Root: `https://your-url.railway.app/`
- Interactive Docs: `https://your-url.railway.app/docs`
- ReDoc: `https://your-url.railway.app/redoc`

## API Endpoints

### Main Endpoints

1. **Get Panchangam for Single Date**
   ```
   GET /panchangam?date=2026-01-01&location=chennai
   ```

2. **Get Panchangam for Date Range**
   ```
   GET /panchangam/range?start_date=2026-01-01&end_date=2026-01-07&location=chennai
   ```

3. **Get Panchangam for Month**
   ```
   GET /panchangam/month?year=2026&month=1&location=chennai
   ```

4. **Get Panchangam for Year**
   ```
   GET /panchangam/year?year=2026&location=chennai
   ```

5. **Get Muhurtam Dates**
   ```
   GET /muhurtam?year=2026&type=marriage&location=chennai
   ```

6. **Get All Muhurtam Types**
   ```
   GET /muhurtam/all?year=2026&location=chennai
   ```

7. **Get Supported Locations**
   ```
   GET /locations
   ```

## Supported Locations

### Tamil Nadu Cities (Primary)
- `chennai` - Chennai, Tamil Nadu
- `madurai` - Madurai, Tamil Nadu
- `coimbatore` - Coimbatore, Tamil Nadu

### Other Indian Cities
- `amaravati` - Amaravati, Andhra Pradesh
- `hyderabad` - Hyderabad, Telangana

### International Cities
- USA: `atlanta`, `chicago`, `newark`, `newyork`, `phoenix`, `sanfrancisco`, `losangeles`
- Canada: `toronto`
- UK: `london`
- Australia: `sydney`
- New Zealand: `auckland`
- South Africa: `capetown`
- Middle East: `riyadh`, `dubai`
- Asia: `singapore`, `kualalumpur`

## Supported Years

- 2025
- 2026
- 2027

## Frontend Integration

### Update Frontend API Configuration

In your Tamil Calendar frontend (`Tamil-Calendar-2026` directory), update the API endpoint in `js/api-config.js`:

```javascript
const API_CONFIG = {
    baseURL: 'https://your-railway-url.railway.app',
    // or use environment variable
    // baseURL: process.env.API_URL || 'https://your-railway-url.railway.app'
};
```

## Performance Optimization

### Optional: Pre-generate Muhurtam Cache

For better performance, you can pre-generate the Muhurtam cache:

```bash
python generate_muhurtam_cache.py
```

This creates 324 JSON files (3 years × 6 types × 18 locations) in the `muhurtam_cache` directory.

**Note**: Railway has file system limitations, so this step is optional. The API will calculate on-the-fly if cache doesn't exist.

## Monitoring

### Railway Dashboard

Monitor your API through the Railway dashboard:
- View logs in real-time
- Check resource usage (CPU, Memory, Network)
- View deployment history
- Set up custom domains

### Health Check

Test if your API is running:
```bash
curl https://your-railway-url.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Tamil Calendar API"
}
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies in requirements.txt are available
   - Verify Python version compatibility

2. **Runtime Errors**
   - Check Railway logs for error messages
   - Verify environment variables are set correctly

3. **Performance Issues**
   - Consider upgrading Railway plan for more resources
   - Implement caching if not already done

## CORS Configuration

The API is configured to accept requests from any origin. For production, update `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-tamil-calendar-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Cost Optimization

Railway provides:
- **Free Tier**: $5 worth of usage per month
- **Pro Plan**: $20/month with increased limits

### Tips to Stay Within Free Tier
1. Use efficient queries (specific date ranges)
2. Implement client-side caching
3. Monitor usage through Railway dashboard
4. Consider pre-generating data files

## Next Steps

1. Push code to GitHub repository
2. Deploy to Railway using the steps above
3. Update frontend with Railway API URL
4. Test all endpoints
5. Monitor performance and optimize as needed

## Support

For issues or questions:
- Check Railway documentation: https://docs.railway.app
- API issues: Create GitHub issue
- Email: support@tamilcalendar.io

---

**Tamil Calendar API** - Bringing ancient Tamil wisdom to modern applications
