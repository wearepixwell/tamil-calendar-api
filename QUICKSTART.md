# Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd telugu-calendar-api
pip install -r requirements.txt
```

### Step 2: Test the Installation

Run the test script to verify everything works:

```bash
python test_api.py
```

You should see output like:
```
Telugu Calendar API - Test Suite
============================================================
Testing single date calculation...

Panchangam for 2026-01-01 - Hyderabad, Telangana
============================================================
Sunrise: 06:45
Sunset: 18:03
Tithi: Pratipada (పాడ్యమి)
Nakshatra: Ashwini (అశ్విని)
...
✓ All tests passed successfully!
```

### Step 3: Start the API Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Step 4: Test the API

Open your browser and visit:
- API Documentation: http://localhost:8000/docs
- Try an API call: http://localhost:8000/panchangam?date=2026-01-01&location=hyderabad

## Quick API Examples

### Example 1: Get Today's Panchangam

```bash
curl "http://localhost:8000/panchangam?date=2026-01-01&location=hyderabad"
```

### Example 2: Get Week's Panchangam

```bash
curl "http://localhost:8000/panchangam/range?start_date=2026-01-01&end_date=2026-01-07&location=hyderabad"
```

### Example 3: Get January 2026 Panchangam

```bash
curl "http://localhost:8000/panchangam/month?year=2026&month=1&location=hyderabad"
```

### Example 4: List All Locations

```bash
curl "http://localhost:8000/locations"
```

## Frontend Integration

### JavaScript/React Example

```javascript
async function getPanchangam(date, location) {
  const response = await fetch(
    `http://localhost:8000/panchangam?date=${date}&location=${location}`
  );
  const data = await response.json();
  return data;
}

// Usage
getPanchangam('2026-01-01', 'hyderabad')
  .then(data => {
    console.log('Tithi:', data.tithi_name.en);
    console.log('Sunrise:', data.sunrise);
    console.log('Rahukalam:', data.rahukalam);
  });
```

### Python Example

```python
import requests

def get_panchangam(date, location):
    url = f"http://localhost:8000/panchangam"
    params = {"date": date, "location": location}
    response = requests.get(url, params=params)
    return response.json()

# Usage
data = get_panchangam('2026-01-01', 'hyderabad')
print(f"Tithi: {data['tithi_name']['en']}")
print(f"Sunrise: {data['sunrise']}")
```

## Pre-generating Data (Optional)

For better performance, pre-generate all data:

```bash
# Generate all data (takes ~30 minutes)
python generate_data.py

# Or generate specific year/location
python generate_data.py 2026 hyderabad
```

This creates JSON files in the `data/` directory that can be served statically.

## Common Use Cases

### 1. Daily Panchangam Website

Fetch today's panchangam on page load:

```javascript
const today = new Date().toISOString().split('T')[0];
const panchangam = await getPanchangam(today, 'hyderabad');
```

### 2. Calendar Application

Fetch entire month and display in calendar:

```javascript
async function getMonthData(year, month, location) {
  const response = await fetch(
    `http://localhost:8000/panchangam/month?year=${year}&month=${month}&location=${location}`
  );
  return await response.json();
}
```

### 3. Multi-Location Dashboard

Show panchangam for multiple cities:

```javascript
const locations = ['hyderabad', 'newyork', 'london', 'sydney'];
const promises = locations.map(loc => getPanchangam('2026-01-01', loc));
const results = await Promise.all(promises);
```

## Available Locations

| Key | Location |
|-----|----------|
| `hyderabad` | Hyderabad, India |
| `amaravati` | Amaravati, India |
| `newyork` | New York, USA |
| `chicago` | Chicago, USA |
| `sanfrancisco` | San Francisco, USA |
| `london` | London, UK |
| `sydney` | Sydney, Australia |
| `dubai` | Dubai, UAE |
| `singapore` | Singapore |
| ... and 9 more! |

See full list: `GET /locations`

## Data Fields Explained

### Time Fields
- `sunrise`, `sunset`: Sun rising and setting times
- `moonrise`, `moonset`: Moon rising and setting times
- All times in HH:MM format, local timezone

### Panchangam Elements
- `tithi_name`: Lunar day (30 tithis in a month)
- `nakshatra_name`: Lunar mansion (27 nakshatras)
- `yoga_name`: Yoga (27 yogas)
- `karana_json`: Half-tithis (JSON array)
- `masa`: Hindu month
- `paksha`: Fortnight (Shukla/Krishna)

### Auspicious/Inauspicious Times
- `rahukalam`: Inauspicious period based on weekday
- `yamagandam`: Another inauspicious period
- `durmuhurtham_json`: Morning and evening bad periods
- `abhijit_muhurtham`: Most auspicious midday period
- `amruthakalam`: Auspicious period

## Troubleshooting

### Error: "Module swisseph not found"

```bash
pip install pyswisseph
```

### Error: "Invalid location"

Check supported locations:
```bash
curl http://localhost:8000/locations
```

### Port 8000 already in use

Change port in `main.py` or:
```bash
PORT=8080 python main.py
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the interactive API docs at http://localhost:8000/docs
3. Generate pre-calculated data for better performance
4. Integrate with your frontend application

## Support

For issues or questions:
- Check the README.md
- Review API documentation at /docs
- Create an issue on GitHub

---

**Happy Coding!** 🎉
