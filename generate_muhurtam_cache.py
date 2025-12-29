"""
Pre-generate Muhurtam cache for all years, types, and locations
This script calculates all Muhurtam combinations and stores them in cache files
Run this script once to generate all cache files for faster API responses
"""

import json
import os
from muhurtam import MuhurtamCalculator
from config import LOCATIONS, YEARS

def generate_all_muhurtam_cache():
    """Generate cache files for all combinations"""
    calculator = MuhurtamCalculator()

    muhurtam_types = ['marriage', 'grihapravesam', 'vehicle', 'naamkaranam', 'annaprasanam', 'upanayanam']

    cache_dir = "muhurtam_cache"
    os.makedirs(cache_dir, exist_ok=True)

    total_combinations = len(YEARS) * len(muhurtam_types) * len(LOCATIONS)
    current = 0

    print(f"Generating {total_combinations} cache files...")
    print(f"Years: {YEARS}")
    print(f"Muhurtam Types: {muhurtam_types}")
    print(f"Locations: {len(LOCATIONS)}\n")

    for year in YEARS:
        print(f"\n{'='*60}")
        print(f"Processing Year: {year}")
        print(f"{'='*60}")

        for muhurtam_type in muhurtam_types:
            print(f"\n  Muhurtam Type: {muhurtam_type.upper()}")

            for location_key, loc in LOCATIONS.items():
                current += 1
                cache_file = os.path.join(cache_dir, f"{muhurtam_type}_{year}_{location_key}.json")

                # Skip if already exists
                if os.path.exists(cache_file):
                    print(f"    [{current}/{total_combinations}] {location_key:15s} - CACHED (skipped)")
                    continue

                try:
                    # Calculate Muhurtam dates
                    muhurtam_dates = calculator.calculate_muhurtam_dates(
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
                            "key": location_key,
                            "name": loc["name"],
                            "country": loc["country"]
                        },
                        "count": len(muhurtam_dates),
                        "dates": muhurtam_dates
                    }

                    # Save to cache
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)

                    print(f"    [{current}/{total_combinations}] {location_key:15s} - DONE ({len(muhurtam_dates)} dates)")

                except Exception as e:
                    print(f"    [{current}/{total_combinations}] {location_key:15s} - ERROR: {str(e)}")

    print(f"\n{'='*60}")
    print(f"Cache generation complete!")
    print(f"Total files generated: {current}")
    print(f"Cache directory: {os.path.abspath(cache_dir)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    generate_all_muhurtam_cache()
