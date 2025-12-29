# Tamil Calendar API

A comprehensive REST API for Tamil Panchangam (Hindu Calendar) data across multiple locations worldwide and multiple years.

## Features

- **Accurate Astronomical Calculations**: Uses Swiss Ephemeris for precise calculations
- **Multiple Locations**: Supports 18 locations across India, USA, Canada, UK, Australia, New Zealand, South Africa, UAE, Saudi Arabia, Singapore, and Malaysia
- **Multiple Years**: Pre-configured for 2025, 2026, and 2027
- **Complete Panchangam Data**: Includes all traditional elements:
  - Tithi (Lunar day)
  - Nakshatra (Lunar mansion)
  - Yoga
  - Karana
  - Masa (Month) and Paksha (Fortnight)
  - Samvatsara (60-year cycle year)
  - Ayana (Solstice period)
  - Ruthu (Season)
  - Rashi (Zodiac signs for Sun and Moon)
  - Sunrise, Sunset, Moonrise, Moonset
  - Inauspicious times (Rahukalam, Yamagandam, Varjyam, Durmuhurtham)
  - Auspicious times (Abhijit Muhurtham, Amruthakalam)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
cd tamil-calendar-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API Server

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Generating Data Files

Generate pre-calculated Panchangam data for all years and locations:

```bash
python generate_data.py
```

This will create JSON files in the `data/` directory organized by year and location.

To generate data for a specific year and location:

```bash
python generate_data.py 2026 hyderabad
```

## API Endpoints

### 1. Get Panchangam for a Single Date

```
GET /panchangam?date=2026-01-01&location=hyderabad
```

**Parameters:**
- `date` (required): Date in YYYY-MM-DD format
- `location` (required): Location key

**Example Response:**
```json
{
  "date": "2026-01-01",
  "location": {
    "latitude": 17.385,
    "longitude": 78.4867
  },
  "timezone": "Asia/Kolkata",
  "sunrise": "06:45",
  "sunset": "18:03",
  "moonrise": "07:30",
  "moonset": "19:15",
  "tithi_name": {
    "en": "Pratipada",
    "ta": "பிரதமை"
  },
  "tithi_end": "08:25",
  "nakshatra_name": {
    "en": "Ashwini",
    "ta": "அஸ்வினி"
  },
  "nakshatra_end": "10:42",
  "yoga_name": {
    "en": "Vishkambha",
    "ta": "விஷ்கம்பா"
  },
  "yoga_end": "09:15",
  "karana_json": "[{\"name\":{\"en\":\"Bava\",\"ta\":\"பவ\"},\"end\":\"20:30\"}]",
  "masa": {
    "en": "Pushya",
    "ta": "புஷ்ய"
  },
  "paksha": {
    "en": "Shukla Paksha",
    "ta": "சுக்ல பக்ஷம்"
  },
  "samvatsaram": {
    "en": "Prabhava",
    "ta": "Prabhava"
  },
  "ayana": {
    "en": "Uttarayana",
    "ta": "உத்தராயண"
  },
  "ruthu": {
    "en": "Hemanta",
    "ta": "ஹேமந்த"
  },
  "suryarashi": {
    "en": "Sagittarius",
    "ta": "தனுசு"
  },
  "chandrarashi": {
    "en": "Aries",
    "ta": "மேஷம்"
  },
  "rahukalam": {
    "start": "15:20",
    "end": "16:52"
  },
  "yamagandam": {
    "start": "12:15",
    "end": "13:47"
  },
  "varjyam": {
    "start": "11:23",
    "end": "12:11"
  },
  "durmuhurtham_json": "[{\"period\":\"Morning\",\"start\":\"08:30\",\"end\":\"09:18\"},{\"period\":\"Evening\",\"start\":\"17:15\",\"end\":\"18:03\"}]",
  "abhijit_muhurtham": {
    "start": "12:00",
    "end": "12:48"
  },
  "amruthakalam": {
    "start": "08:15",
    "end": "09:03"
  },
  "location_info": {
    "key": "hyderabad",
    "name": "Hyderabad, Telangana",
    "country": "India"
  }
}
```

### 2. Get Panchangam for a Date Range

```
GET /panchangam/range?start_date=2026-01-01&end_date=2026-01-07&location=hyderabad
```

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format (max 366 days from start)
- `location` (required): Location key

### 3. Get Panchangam for a Month

```
GET /panchangam/month?year=2026&month=1&location=hyderabad
```

**Parameters:**
- `year` (required): Year (e.g., 2026)
- `month` (required): Month (1-12)
- `location` (required): Location key

### 4. Get Panchangam for a Year

```
GET /panchangam/year?year=2026&location=hyderabad
```

**Parameters:**
- `year` (required): Year (must be in supported years: 2025, 2026, 2027)
- `location` (required): Location key

### 5. Get Supported Locations

```
GET /locations
```

Returns a list of all supported locations with their coordinates and timezones.

### 6. Health Check

```
GET /health
```

Returns API health status.

## Supported Locations

| Key | Location | Country | Timezone |
|-----|----------|---------|----------|
| amaravati | Amaravati, Andhra Pradesh | India | Asia/Kolkata |
| hyderabad | Hyderabad, Telangana | India | Asia/Kolkata |
| atlanta | Atlanta | USA | America/New_York |
| chicago | Chicago | USA | America/Chicago |
| newark | Newark, New Jersey | USA | America/New_York |
| newyork | New York City | USA | America/New_York |
| phoenix | Phoenix | USA | America/Phoenix |
| sanfrancisco | San Francisco | USA | America/Los_Angeles |
| losangeles | Los Angeles | USA | America/Los_Angeles |
| toronto | Toronto | Canada | America/Toronto |
| london | London | United Kingdom | Europe/London |
| auckland | Auckland | New Zealand | Pacific/Auckland |
| sydney | Sydney | Australia | Australia/Sydney |
| capetown | Cape Town | South Africa | Africa/Johannesburg |
| riyadh | Riyadh | Saudi Arabia | Asia/Riyadh |
| dubai | Dubai | UAE | Asia/Dubai |
| singapore | Singapore | Singapore | Asia/Singapore |
| kualalumpur | Kuala Lumpur | Malaysia | Asia/Kuala_Lumpur |

## Data Structure

The API returns comprehensive Panchangam data with the following structure:

```typescript
interface PanchangamData {
  // Basic Info
  date: string;                    // YYYY-MM-DD format
  location: {
    latitude: number;
    longitude: number;
  };
  timezone: string;

  // Sun and Moon
  sunrise: string;                 // HH:MM format
  sunset: string;
  moonrise: string | null;
  moonset: string | null;

  // Panchangam Elements (bilingual)
  tithi_name: {
    en: string;
    ta: string;                    // Tamil script
  };
  tithi_end: string;               // HH:MM format

  nakshatra_name: {
    en: string;
    ta: string;
  };
  nakshatra_end: string;

  yoga_name: {
    en: string;
    ta: string;
  };
  yoga_end: string;

  karana_json: string;             // JSON array of karanas

  masa: {
    en: string;
    ta: string;
  };

  paksha: {
    en: string;
    ta: string;
  };

  samvatsaram: {
    en: string;
    ta: string;
  };

  ayana: {
    en: string;
    ta: string;
  };

  ruthu: {
    en: string;
    ta: string;
  };

  suryarashi: {
    en: string;
    ta: string;
  };

  chandrarashi: {
    en: string;
    ta: string;
  };

  // Inauspicious Times
  rahukalam: {
    start: string;
    end: string;
  };

  yamagandam: {
    start: string;
    end: string;
  };

  varjyam: {
    start: string;
    end: string;
  };

  durmuhurtham_json: string;       // JSON array with morning/evening periods

  // Auspicious Times
  abhijit_muhurtham: {
    start: string;
    end: string;
  };

  amruthakalam: {
    start: string;
    end: string;
  };

  // Location Info
  location_info: {
    key: string;
    name: string;
    country: string;
  };
}
```

## CORS Configuration

The API is configured to accept requests from any origin. For production use, update the `allow_origins` in `main.py` to specify your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

### Running Tests

```bash
pytest
```

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t tamil-calendar-api .
docker run -p 8000:8000 tamil-calendar-api
```

### Environment Variables

You can configure the API using environment variables:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Performance Considerations

- The API uses Swiss Ephemeris for real-time calculations
- For better performance, pre-generate data using `generate_data.py`
- Consider implementing caching for frequently accessed dates
- Use database storage for large-scale deployments

## Technical Details

### Astronomical Calculations

The API uses Swiss Ephemeris (PySwisseph) for precise astronomical calculations:

- **Tithi**: Based on the elongation between Moon and Sun (12° per tithi)
- **Nakshatra**: Based on Moon's sidereal longitude (13°20' per nakshatra)
- **Yoga**: Based on sum of Sun and Moon longitudes
- **Karana**: Half-tithi periods
- **Sunrise/Sunset**: Calculated for exact location coordinates
- **Inauspicious times**: Calculated based on traditional formulas and day segments

### Timezone Handling

All times are calculated and returned in the local timezone of the specified location. The API properly handles:
- Daylight Saving Time (DST) transitions
- Timezone offsets
- International Date Line

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Credits

- **Swiss Ephemeris**: Used for astronomical calculations
- **FastAPI**: Modern web framework for building APIs
- **PyTZ**: Timezone handling

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Email: support@tamilcalendar.io

## Changelog

### Version 1.0.0 (2025)
- Initial release
- Support for 18 locations worldwide
- Years 2025-2027
- Complete Panchangam calculations
- REST API with multiple endpoints
- Data generation script

---

**Tamil Calendar API** - Bringing ancient wisdom to modern applications
