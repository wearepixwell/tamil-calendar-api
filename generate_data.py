"""
Data Generation Script
Generates Panchangam data for all years and locations and saves to JSON files
"""

import json
import os
from datetime import datetime, timedelta
from panchangam import PanchangamCalculator
from config import LOCATIONS, YEARS
from tqdm import tqdm


def generate_all_data(output_dir="data"):
    """Generate Panchangam data for all years and locations"""

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    calculator = PanchangamCalculator()

    print("Starting data generation...")
    print(f"Years: {YEARS}")
    print(f"Locations: {len(LOCATIONS)}")

    total_days = 0
    for year in YEARS:
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        total_days += (end - start).days + 1

    total_operations = total_days * len(LOCATIONS)
    print(f"Total days to calculate: {total_days}")
    print(f"Total operations: {total_operations}\n")

    # Progress bar
    with tqdm(total=total_operations, desc="Generating Panchangam data") as pbar:
        for year in YEARS:
            year_dir = os.path.join(output_dir, str(year))
            os.makedirs(year_dir, exist_ok=True)

            # Generate for each location
            for loc_key, loc_data in LOCATIONS.items():
                location_dir = os.path.join(year_dir, loc_key)
                os.makedirs(location_dir, exist_ok=True)

                # Generate for each day of the year
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31)
                current_date = start_date

                year_data = []

                while current_date <= end_date:
                    # Calculate Panchangam
                    panchangam = calculator.calculate_panchangam(
                        current_date,
                        loc_data["lat"],
                        loc_data["lon"],
                        loc_data["timezone"]
                    )

                    # Add location info
                    panchangam["location_info"] = {
                        "key": loc_key,
                        "name": loc_data["name"],
                        "country": loc_data["country"]
                    }

                    year_data.append(panchangam)

                    # Also save individual day file
                    day_filename = f"{current_date.strftime('%Y-%m-%d')}.json"
                    day_filepath = os.path.join(location_dir, day_filename)

                    with open(day_filepath, 'w', encoding='utf-8') as f:
                        json.dump(panchangam, f, ensure_ascii=False, indent=2)

                    current_date += timedelta(days=1)
                    pbar.update(1)

                # Save full year file
                year_filename = f"{year}_{loc_key}_full.json"
                year_filepath = os.path.join(year_dir, year_filename)

                with open(year_filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        "year": year,
                        "location": loc_key,
                        "count": len(year_data),
                        "data": year_data
                    }, f, ensure_ascii=False, indent=2)

    print(f"\nData generation complete!")
    print(f"Data saved to: {os.path.abspath(output_dir)}")


def generate_location_year(year, location_key, output_dir="data"):
    """Generate data for a specific year and location"""

    if location_key not in LOCATIONS:
        print(f"Error: Location '{location_key}' not found")
        return

    if year not in YEARS:
        print(f"Warning: Year {year} not in configured years list")

    calculator = PanchangamCalculator()
    loc_data = LOCATIONS[location_key]

    # Create directories
    year_dir = os.path.join(output_dir, str(year))
    location_dir = os.path.join(year_dir, location_key)
    os.makedirs(location_dir, exist_ok=True)

    print(f"Generating data for {loc_data['name']} - {year}")

    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current_date = start_date

    year_data = []
    total_days = (end_date - start_date).days + 1

    with tqdm(total=total_days, desc=f"{location_key} {year}") as pbar:
        while current_date <= end_date:
            # Calculate Panchangam
            panchangam = calculator.calculate_panchangam(
                current_date,
                loc_data["lat"],
                loc_data["lon"],
                loc_data["timezone"]
            )

            # Add location info
            panchangam["location_info"] = {
                "key": location_key,
                "name": loc_data["name"],
                "country": loc_data["country"]
            }

            year_data.append(panchangam)

            # Save individual day file
            day_filename = f"{current_date.strftime('%Y-%m-%d')}.json"
            day_filepath = os.path.join(location_dir, day_filename)

            with open(day_filepath, 'w', encoding='utf-8') as f:
                json.dump(panchangam, f, ensure_ascii=False, indent=2)

            current_date += timedelta(days=1)
            pbar.update(1)

    # Save full year file
    year_filename = f"{year}_{location_key}_full.json"
    year_filepath = os.path.join(year_dir, year_filename)

    with open(year_filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "year": year,
            "location": location_key,
            "count": len(year_data),
            "data": year_data
        }, f, ensure_ascii=False, indent=2)

    print(f"Data saved to: {os.path.abspath(location_dir)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        # Generate all data
        generate_all_data()
    elif len(sys.argv) == 3:
        # Generate specific year and location
        year = int(sys.argv[1])
        location = sys.argv[2]
        generate_location_year(year, location)
    else:
        print("Usage:")
        print("  python generate_data.py                    # Generate all data")
        print("  python generate_data.py <year> <location>  # Generate specific data")
        print(f"\nSupported locations: {', '.join(LOCATIONS.keys())}")
        print(f"Supported years: {', '.join(map(str, YEARS))}")
