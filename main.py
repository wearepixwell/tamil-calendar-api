"""
Tamil Calendar API
FastAPI application for serving Panchangam data
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, List
import pytz
import json
import os
from functools import lru_cache

from panchangam import PanchangamCalculator
from muhurtam import MuhurtamCalculator
from config import LOCATIONS, YEARS

# Initialize FastAPI app
app = FastAPI(
    title="Tamil Calendar API",
    description="API for Tamil Panchangam (Hindu Calendar) data across multiple locations and years",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize calculators
calculator = PanchangamCalculator()
muhurtam_calculator = MuhurtamCalculator()

# Cache directory for pre-calculated Muhurtam data
CACHE_DIR = "muhurtam_cache"
os.makedirs(CACHE_DIR, exist_ok=True)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Tamil Calendar API",
        "version": "1.0.0",
        "endpoints": {
            "/panchangam": "Get Panchangam for a specific date and location",
            "/panchangam/range": "Get Panchangam for a date range",
            "/panchangam/month": "Get Panchangam for an entire month",
            "/panchangam/year": "Get Panchangam for an entire year",
            "/muhurtam": "Get auspicious Muhurtam dates for a specific type, year, and location",
            "/muhurtam/all": "Get all Muhurtam types for a specific year and location",
            "/locations": "Get list of supported locations",
            "/health": "Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/locations")
async def get_locations():
    """Get list of all supported locations"""
    locations_list = []
    for key, loc in LOCATIONS.items():
        locations_list.append({
            "key": key,
            "name": loc["name"],
            "country": loc["country"],
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "timezone": loc["timezone"]
        })

    return {
        "count": len(locations_list),
        "locations": locations_list
    }


@app.get("/panchangam")
async def get_panchangam(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    location: str = Query(..., description="Location key (e.g., 'hyderabad', 'newyork')")
):
    """
    Get Panchangam for a specific date and location

    Args:
        date: Date in YYYY-MM-DD format
        location: Location key from the supported locations list

    Returns:
        Complete Panchangam data for the specified date and location
    """
    # Validate location
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    # Parse and validate date
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    # Get location details
    loc = LOCATIONS[location]

    # Calculate Panchangam
    try:
        panchangam = calculator.calculate_panchangam(
            dt,
            loc["lat"],
            loc["lon"],
            loc["timezone"]
        )

        # Add location info
        panchangam["location_info"] = {
            "key": location,
            "name": loc["name"],
            "country": loc["country"]
        }

        return panchangam

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Panchangam: {str(e)}"
        )


@app.get("/panchangam/range")
async def get_panchangam_range(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    location: str = Query(..., description="Location key")
):
    """
    Get Panchangam for a date range

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        location: Location key

    Returns:
        List of Panchangam data for each date in the range
    """
    # Validate location
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    # Parse dates
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    # Validate range
    if end_dt < start_dt:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    # Limit range to avoid excessive computation
    days_diff = (end_dt - start_dt).days
    if days_diff > 366:
        raise HTTPException(
            status_code=400,
            detail="Date range too large. Maximum 366 days allowed."
        )

    # Get location details
    loc = LOCATIONS[location]

    # Calculate Panchangam for each date
    try:
        panchangam_list = []
        current_dt = start_dt

        while current_dt <= end_dt:
            panchangam = calculator.calculate_panchangam(
                current_dt,
                loc["lat"],
                loc["lon"],
                loc["timezone"]
            )

            panchangam["location_info"] = {
                "key": location,
                "name": loc["name"],
                "country": loc["country"]
            }

            panchangam_list.append(panchangam)
            current_dt += timedelta(days=1)

        return {
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "count": len(panchangam_list),
            "data": panchangam_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Panchangam: {str(e)}"
        )


@app.get("/panchangam/month")
async def get_panchangam_month(
    year: int = Query(..., description="Year (e.g., 2026)"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    location: str = Query(..., description="Location key")
):
    """
    Get Panchangam for an entire month

    Args:
        year: Year
        month: Month (1-12)
        location: Location key

    Returns:
        Panchangam data for all days in the specified month
    """
    # Validate location
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    # Create start and end dates for the month
    try:
        start_dt = datetime(year, month, 1)

        # Get last day of month
        if month == 12:
            end_dt = datetime(year, 12, 31)
        else:
            next_month = datetime(year, month + 1, 1)
            end_dt = next_month - timedelta(days=1)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid year or month"
        )

    # Get location details
    loc = LOCATIONS[location]

    # Calculate Panchangam for each day
    try:
        panchangam_list = []
        current_dt = start_dt

        while current_dt <= end_dt:
            panchangam = calculator.calculate_panchangam(
                current_dt,
                loc["lat"],
                loc["lon"],
                loc["timezone"]
            )

            panchangam["location_info"] = {
                "key": location,
                "name": loc["name"],
                "country": loc["country"]
            }

            panchangam_list.append(panchangam)
            current_dt += timedelta(days=1)

        return {
            "year": year,
            "month": month,
            "location": location,
            "count": len(panchangam_list),
            "data": panchangam_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Panchangam: {str(e)}"
        )


@app.get("/panchangam/year")
async def get_panchangam_year(
    year: int = Query(..., description="Year (e.g., 2026)"),
    location: str = Query(..., description="Location key")
):
    """
    Get Panchangam for an entire year

    Args:
        year: Year
        location: Location key

    Returns:
        Panchangam data for all days in the specified year
    """
    # Validate location
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    # Validate year
    if year not in YEARS:
        raise HTTPException(
            status_code=400,
            detail=f"Year not supported. Supported years: {', '.join(map(str, YEARS))}"
        )

    # Create start and end dates
    start_dt = datetime(year, 1, 1)
    end_dt = datetime(year, 12, 31)

    # Get location details
    loc = LOCATIONS[location]

    # Calculate Panchangam for each day
    try:
        panchangam_list = []
        current_dt = start_dt

        while current_dt <= end_dt:
            panchangam = calculator.calculate_panchangam(
                current_dt,
                loc["lat"],
                loc["lon"],
                loc["timezone"]
            )

            panchangam["location_info"] = {
                "key": location,
                "name": loc["name"],
                "country": loc["country"]
            }

            panchangam_list.append(panchangam)
            current_dt += timedelta(days=1)

        return {
            "year": year,
            "location": location,
            "count": len(panchangam_list),
            "data": panchangam_list
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Panchangam: {str(e)}"
        )


@app.get("/muhurtam")
async def get_muhurtam(
    year: int = Query(..., description="Year (e.g., 2026)"),
    muhurtam_type: str = Query(..., description="Type: marriage, grihapravesam, vehicle, naamkaranam, annaprasanam, upanayanam"),
    location: str = Query(..., description="Location key")
):
    """
    Get auspicious Muhurtam dates for a specific year, type, and location
    Uses caching for faster response times

    Args:
        year: Year (2025, 2026, or 2027)
        muhurtam_type: Type of muhurtam
        location: Location key

    Returns:
        List of auspicious dates for the specified muhurtam type
    """
    # Validate inputs
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    if year not in YEARS:
        raise HTTPException(
            status_code=400,
            detail=f"Year not supported. Supported years: {', '.join(map(str, YEARS))}"
        )

    valid_types = ['marriage', 'grihapravesam', 'vehicle', 'naamkaranam', 'annaprasanam', 'upanayanam']
    if muhurtam_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid muhurtam type. Supported types: {', '.join(valid_types)}"
        )

    # Check cache first
    cache_file = os.path.join(CACHE_DIR, f"{muhurtam_type}_{year}_{location}.json")

    if os.path.exists(cache_file):
        # Return cached data
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
            return cached_data

    # Calculate if not in cache
    try:
        loc = LOCATIONS[location]
        muhurtam_dates = muhurtam_calculator.calculate_muhurtam_dates(
            year=year,
            muhurtam_type=muhurtam_type,
            lat=loc["lat"],
            lon=loc["lon"],
            tz=loc["timezone"]
        )

        result = {
            "year": year,
            "muhurtam_type": muhurtam_type,
            "location": {
                "key": location,
                "name": loc["name"],
                "country": loc["country"]
            },
            "count": len(muhurtam_dates),
            "dates": muhurtam_dates
        }

        # Cache the result
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Muhurtam: {str(e)}"
        )


@app.get("/muhurtam/all")
async def get_all_muhurtam(
    year: int = Query(..., description="Year (e.g., 2026)"),
    location: str = Query(..., description="Location key")
):
    """
    Get all Muhurtam types for a specific year and location
    Returns pre-calculated data for all 6 muhurtam types

    Args:
        year: Year
        location: Location key

    Returns:
        Dictionary with all muhurtam types and their dates
    """
    # Validate inputs
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid location. Supported locations: {', '.join(LOCATIONS.keys())}"
        )

    if year not in YEARS:
        raise HTTPException(
            status_code=400,
            detail=f"Year not supported. Supported years: {', '.join(map(str, YEARS))}"
        )

    muhurtam_types = ['marriage', 'grihapravesam', 'vehicle', 'naamkaranam', 'annaprasanam', 'upanayanam']
    all_muhurtam = {}

    try:
        loc = LOCATIONS[location]

        for muhurtam_type in muhurtam_types:
            cache_file = os.path.join(CACHE_DIR, f"{muhurtam_type}_{year}_{location}.json")

            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    all_muhurtam[muhurtam_type] = cached_data['dates']
            else:
                # Calculate if not cached
                muhurtam_dates = muhurtam_calculator.calculate_muhurtam_dates(
                    year=year,
                    muhurtam_type=muhurtam_type,
                    lat=loc["lat"],
                    lon=loc["lon"],
                    tz=loc["timezone"]
                )

                all_muhurtam[muhurtam_type] = muhurtam_dates

                # Cache it
                result = {
                    "year": year,
                    "muhurtam_type": muhurtam_type,
                    "location": {
                        "key": location,
                        "name": loc["name"],
                        "country": loc["country"]
                    },
                    "count": len(muhurtam_dates),
                    "dates": muhurtam_dates
                }

                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        return {
            "year": year,
            "location": {
                "key": location,
                "name": loc["name"],
                "country": loc["country"]
            },
            "muhurtam_data": all_muhurtam
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating Muhurtam: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
