# Configuration for Tamil Calendar API

# Location data with coordinates and timezones
LOCATIONS = {
    "chennai": {
        "name": "Chennai, Tamil Nadu",
        "country": "India",
        "lat": 13.0827,
        "lon": 80.2707,
        "timezone": "Asia/Kolkata"
    },
    "madurai": {
        "name": "Madurai, Tamil Nadu",
        "country": "India",
        "lat": 9.9252,
        "lon": 78.1198,
        "timezone": "Asia/Kolkata"
    },
    "coimbatore": {
        "name": "Coimbatore, Tamil Nadu",
        "country": "India",
        "lat": 11.0168,
        "lon": 76.9558,
        "timezone": "Asia/Kolkata"
    },
    "amaravati": {
        "name": "Amaravati, Andhra Pradesh",
        "country": "India",
        "lat": 16.541,
        "lon": 80.515,
        "timezone": "Asia/Kolkata"
    },
    "hyderabad": {
        "name": "Hyderabad, Telangana",
        "country": "India",
        "lat": 17.3850,
        "lon": 78.4867,
        "timezone": "Asia/Kolkata"
    },
    "atlanta": {
        "name": "Atlanta",
        "country": "USA",
        "lat": 33.7490,
        "lon": -84.3880,
        "timezone": "America/New_York"
    },
    "chicago": {
        "name": "Chicago",
        "country": "USA",
        "lat": 41.8781,
        "lon": -87.6298,
        "timezone": "America/Chicago"
    },
    "newark": {
        "name": "Newark, New Jersey",
        "country": "USA",
        "lat": 40.7357,
        "lon": -74.1724,
        "timezone": "America/New_York"
    },
    "newyork": {
        "name": "New York City",
        "country": "USA",
        "lat": 40.7128,
        "lon": -74.0060,
        "timezone": "America/New_York"
    },
    "phoenix": {
        "name": "Phoenix",
        "country": "USA",
        "lat": 33.4484,
        "lon": -112.0740,
        "timezone": "America/Phoenix"
    },
    "sanfrancisco": {
        "name": "San Francisco",
        "country": "USA",
        "lat": 37.7749,
        "lon": -122.4194,
        "timezone": "America/Los_Angeles"
    },
    "losangeles": {
        "name": "Los Angeles",
        "country": "USA",
        "lat": 34.0522,
        "lon": -118.2437,
        "timezone": "America/Los_Angeles"
    },
    "toronto": {
        "name": "Toronto",
        "country": "Canada",
        "lat": 43.6532,
        "lon": -79.3832,
        "timezone": "America/Toronto"
    },
    "london": {
        "name": "London",
        "country": "United Kingdom",
        "lat": 51.5074,
        "lon": -0.1278,
        "timezone": "Europe/London"
    },
    "auckland": {
        "name": "Auckland",
        "country": "New Zealand",
        "lat": -36.8485,
        "lon": 174.7633,
        "timezone": "Pacific/Auckland"
    },
    "sydney": {
        "name": "Sydney",
        "country": "Australia",
        "lat": -33.8688,
        "lon": 151.2093,
        "timezone": "Australia/Sydney"
    },
    "capetown": {
        "name": "Cape Town",
        "country": "South Africa",
        "lat": -33.9249,
        "lon": 18.4241,
        "timezone": "Africa/Johannesburg"
    },
    "riyadh": {
        "name": "Riyadh",
        "country": "Saudi Arabia",
        "lat": 24.7136,
        "lon": 46.6753,
        "timezone": "Asia/Riyadh"
    },
    "dubai": {
        "name": "Dubai",
        "country": "UAE",
        "lat": 25.2048,
        "lon": 55.2708,
        "timezone": "Asia/Dubai"
    },
    "singapore": {
        "name": "Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lon": 103.8198,
        "timezone": "Asia/Singapore"
    },
    "kualalumpur": {
        "name": "Kuala Lumpur",
        "country": "Malaysia",
        "lat": 3.1390,
        "lon": 101.6869,
        "timezone": "Asia/Kuala_Lumpur"
    }
}

# Years to generate data for
YEARS = [2025, 2026, 2027]

# Nakshatra names (27 nakshatras)
NAKSHATRAS = [
    {"en": "Ashwini", "ta": "அஸ்வினி"},
    {"en": "Bharani", "ta": "பரணி"},
    {"en": "Krittika", "ta": "கார்த்திகை"},
    {"en": "Rohini", "ta": "ரோகிணி"},
    {"en": "Mrigashira", "ta": "மிருகசீரிடம்"},
    {"en": "Ardra", "ta": "திருவாதிரை"},
    {"en": "Punarvasu", "ta": "புனர்பூசம்"},
    {"en": "Pushya", "ta": "பூசம்"},
    {"en": "Ashlesha", "ta": "ஆயில்யம்"},
    {"en": "Magha", "ta": "மகம்"},
    {"en": "Purva Phalguni", "ta": "பூரம்"},
    {"en": "Uttara Phalguni", "ta": "உத்திரம்"},
    {"en": "Hasta", "ta": "ஹஸ்தம்"},
    {"en": "Chitra", "ta": "சித்திரை"},
    {"en": "Swati", "ta": "சுவாதி"},
    {"en": "Vishakha", "ta": "விசாகம்"},
    {"en": "Anuradha", "ta": "அனுஷம்"},
    {"en": "Jyeshtha", "ta": "கேட்டை"},
    {"en": "Mula", "ta": "மூலம்"},
    {"en": "Purva Ashadha", "ta": "பூராடம்"},
    {"en": "Uttara Ashadha", "ta": "உத்திராடம்"},
    {"en": "Shravana", "ta": "திருவோணம்"},
    {"en": "Dhanishtha", "ta": "அவிட்டம்"},
    {"en": "Shatabhisha", "ta": "சதயம்"},
    {"en": "Purva Bhadrapada", "ta": "பூரட்டாதி"},
    {"en": "Uttara Bhadrapada", "ta": "உத்திரட்டாதி"},
    {"en": "Revati", "ta": "ரேவதி"}
]

# Tithi names (30 tithis)
TITHIS = [
    {"en": "Pratipada", "ta": "பிரதமை"},
    {"en": "Dwitiya", "ta": "துவிதியை"},
    {"en": "Tritiya", "ta": "திருதியை"},
    {"en": "Chaturthi", "ta": "சதுர்த்தி"},
    {"en": "Panchami", "ta": "பஞ்சமி"},
    {"en": "Shashthi", "ta": "சஷ்டி"},
    {"en": "Saptami", "ta": "சப்தமி"},
    {"en": "Ashtami", "ta": "அஷ்டமி"},
    {"en": "Navami", "ta": "நவமி"},
    {"en": "Dashami", "ta": "தசமி"},
    {"en": "Ekadashi", "ta": "ஏகாதசி"},
    {"en": "Dwadashi", "ta": "துவாதசி"},
    {"en": "Trayodashi", "ta": "திரயோதசி"},
    {"en": "Chaturdashi", "ta": "சதுர்த்தசி"},
    {"en": "Purnima", "ta": "பௌர்ணமி"},
    {"en": "Pratipada", "ta": "பிரதமை"},
    {"en": "Dwitiya", "ta": "துவிதியை"},
    {"en": "Tritiya", "ta": "திருதியை"},
    {"en": "Chaturthi", "ta": "சதுர்த்தி"},
    {"en": "Panchami", "ta": "பஞ்சமி"},
    {"en": "Shashthi", "ta": "சஷ்டி"},
    {"en": "Saptami", "ta": "சப்தமி"},
    {"en": "Ashtami", "ta": "அஷ்டமி"},
    {"en": "Navami", "ta": "நவமி"},
    {"en": "Dashami", "ta": "தசமி"},
    {"en": "Ekadashi", "ta": "ஏகாதசி"},
    {"en": "Dwadashi", "ta": "துவாதசி"},
    {"en": "Trayodashi", "ta": "திரயோதசி"},
    {"en": "Chaturdashi", "ta": "சதுர்த்தசி"},
    {"en": "Amavasya", "ta": "அமாவாசை"}
]

# Yoga names (27 yogas)
YOGAS = [
    {"en": "Vishkambha", "ta": "விஷ்கம்பா"},
    {"en": "Priti", "ta": "ப்ரீதி"},
    {"en": "Ayushman", "ta": "ஆயுஷ்மான்"},
    {"en": "Saubhagya", "ta": "சௌபாக்ய"},
    {"en": "Shobhana", "ta": "சோபன"},
    {"en": "Atiganda", "ta": "அதிகண்ட"},
    {"en": "Sukarma", "ta": "சுகர்மா"},
    {"en": "Dhriti", "ta": "த்ருதி"},
    {"en": "Shoola", "ta": "சூலா"},
    {"en": "Ganda", "ta": "கண்ட"},
    {"en": "Vriddhi", "ta": "வ்ருத்தி"},
    {"en": "Dhruva", "ta": "த்ருவ"},
    {"en": "Vyaghata", "ta": "வ்யாகாத"},
    {"en": "Harshana", "ta": "ஹர்ஷண"},
    {"en": "Vajra", "ta": "வஜ்ரா"},
    {"en": "Siddhi", "ta": "சித்தி"},
    {"en": "Vyatipata", "ta": "வ்யதீபாத"},
    {"en": "Variyana", "ta": "வரீயான்"},
    {"en": "Parigha", "ta": "பரிக"},
    {"en": "Shiva", "ta": "சிவ"},
    {"en": "Siddha", "ta": "சித்த"},
    {"en": "Sadhya", "ta": "சாத்ய"},
    {"en": "Shubha", "ta": "சுப"},
    {"en": "Shukla", "ta": "சுக்ல"},
    {"en": "Brahma", "ta": "ப்ரம்ம"},
    {"en": "Indra", "ta": "இந்திர"},
    {"en": "Vaidhriti", "ta": "வைத்ருதி"}
]

# Karana names (11 karanas)
KARANAS = [
    {"en": "Bava", "ta": "பவ"},
    {"en": "Balava", "ta": "பாலவ"},
    {"en": "Kaulava", "ta": "கௌலவ"},
    {"en": "Taitila", "ta": "தைதில"},
    {"en": "Garaja", "ta": "கரஜ"},
    {"en": "Vanija", "ta": "வணிஜ"},
    {"en": "Vishti", "ta": "விஷ்டி"},
    {"en": "Shakuni", "ta": "சகுனி"},
    {"en": "Chatushpada", "ta": "சதுஷ்பாத"},
    {"en": "Naga", "ta": "நாக"},
    {"en": "Kimstughna", "ta": "கிம்ஸ்துக்ன"}
]

# Masa names (12 months)
# Tamil Solar Months (Saura Masam) - Based on Sun's transit through zodiac signs
# Month starts when Sun enters the corresponding Rashi (zodiac sign)
MASAS = [
    {"en": "Chithirai", "ta": "சித்திரை", "rashi": "Mesha", "rashi_num": 0},      # Aries (Apr 14 - May 14)
    {"en": "Vaikasi", "ta": "வைகாசி", "rashi": "Vrishabha", "rashi_num": 1},       # Taurus (May 15 - Jun 14)
    {"en": "Aani", "ta": "ஆனி", "rashi": "Mithuna", "rashi_num": 2},                # Gemini (Jun 15 - Jul 16)
    {"en": "Aadi", "ta": "ஆடி", "rashi": "Kataka", "rashi_num": 3},                 # Cancer (Jul 17 - Aug 16)
    {"en": "Aavani", "ta": "ஆவணி", "rashi": "Simha", "rashi_num": 4},               # Leo (Aug 17 - Sep 16)
    {"en": "Purattasi", "ta": "புரட்டாசி", "rashi": "Kanya", "rashi_num": 5},      # Virgo (Sep 17 - Oct 17)
    {"en": "Aippasi", "ta": "ஐப்பசி", "rashi": "Tula", "rashi_num": 6},            # Libra (Oct 18 - Nov 16)
    {"en": "Karthigai", "ta": "கார்த்திகை", "rashi": "Vrischika", "rashi_num": 7}, # Scorpio (Nov 17 - Dec 16)
    {"en": "Margazhi", "ta": "மார்கழி", "rashi": "Dhanus", "rashi_num": 8},        # Sagittarius (Dec 17 - Jan 14)
    {"en": "Thai", "ta": "தை", "rashi": "Makara", "rashi_num": 9},                  # Capricorn (Jan 15 - Feb 13)
    {"en": "Maasi", "ta": "மாசி", "rashi": "Kumbha", "rashi_num": 10},              # Aquarius (Feb 14 - Mar 14)
    {"en": "Panguni", "ta": "பங்குனி", "rashi": "Meena", "rashi_num": 11}          # Pisces (Mar 15 - Apr 13)
]

# Rashi (zodiac) names
RASHIS = [
    {"en": "Aries", "ta": "மேஷம்"},
    {"en": "Taurus", "ta": "ரிஷபம்"},
    {"en": "Gemini", "ta": "மிதுனம்"},
    {"en": "Cancer", "ta": "கர்க்கடகம்"},
    {"en": "Leo", "ta": "சிம்மம்"},
    {"en": "Virgo", "ta": "கன்னி"},
    {"en": "Libra", "ta": "துலாம்"},
    {"en": "Scorpio", "ta": "விருச்சிகம்"},
    {"en": "Sagittarius", "ta": "தனுசு"},
    {"en": "Capricorn", "ta": "மகரம்"},
    {"en": "Aquarius", "ta": "கும்பம்"},
    {"en": "Pisces", "ta": "மீனம்"}
]

# Ruthu (seasons)
RUTHUS = [
    {"en": "Vasanta", "ta": "வசந்தம்"},
    {"en": "Grishma", "ta": "கிரீஷ்மம்"},
    {"en": "Varsha", "ta": "வர்ஷா"},
    {"en": "Sharad", "ta": "சரத்"},
    {"en": "Hemanta", "ta": "ஹேமந்தம்"},
    {"en": "Shishira", "ta": "சிசிர"}
]

# Ayana
AYANAS = [
    {"en": "Uttarayana", "ta": "உத்தராயணம்"},
    {"en": "Dakshinayana", "ta": "தக்ஷிணாயனம்"}
]
