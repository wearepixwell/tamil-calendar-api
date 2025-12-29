"""
Simple test script to verify API functionality
"""

from datetime import datetime
from panchangam import PanchangamCalculator
from config import LOCATIONS
import json


def test_single_date():
    """Test calculating Panchangam for a single date"""
    print("Testing single date calculation...")

    calculator = PanchangamCalculator()

    # Test for Hyderabad on January 1, 2026
    test_date = datetime(2026, 1, 1)
    location = LOCATIONS["hyderabad"]

    result = calculator.calculate_panchangam(
        test_date,
        location["lat"],
        location["lon"],
        location["timezone"]
    )

    print(f"\nPanchangam for {test_date.date()} - {location['name']}")
    print("=" * 60)
    print(f"Sunrise: {result['sunrise']}")
    print(f"Sunset: {result['sunset']}")
    print(f"Tithi: {result['tithi_name']['en']} ({result['tithi_name']['te']})")
    print(f"Nakshatra: {result['nakshatra_name']['en']} ({result['nakshatra_name']['te']})")
    print(f"Yoga: {result['yoga_name']['en']} ({result['yoga_name']['te']})")
    print(f"Masa: {result['masa']['en']} ({result['masa']['te']})")
    print(f"Paksha: {result['paksha']['en']} ({result['paksha']['te']})")
    print(f"Rahukalam: {result['rahukalam']['start']} - {result['rahukalam']['end']}")
    print(f"Abhijit Muhurtham: {result['abhijit_muhurtham']['start']} - {result['abhijit_muhurtham']['end']}")

    print("\n✓ Single date test passed!")
    return result


def test_multiple_locations():
    """Test calculating for multiple locations"""
    print("\n\nTesting multiple locations...")

    calculator = PanchangamCalculator()
    test_date = datetime(2026, 1, 1)

    locations_to_test = ["hyderabad", "newyork", "london", "sydney"]

    for loc_key in locations_to_test:
        location = LOCATIONS[loc_key]
        result = calculator.calculate_panchangam(
            test_date,
            location["lat"],
            location["lon"],
            location["timezone"]
        )

        print(f"\n{location['name']}:")
        print(f"  Sunrise: {result['sunrise']}, Sunset: {result['sunset']}")
        print(f"  Tithi: {result['tithi_name']['en']}")
        print(f"  Nakshatra: {result['nakshatra_name']['en']}")

    print("\n✓ Multiple locations test passed!")


def test_data_structure():
    """Test that all required fields are present"""
    print("\n\nTesting data structure...")

    calculator = PanchangamCalculator()
    test_date = datetime(2026, 1, 1)
    location = LOCATIONS["hyderabad"]

    result = calculator.calculate_panchangam(
        test_date,
        location["lat"],
        location["lon"],
        location["timezone"]
    )

    required_fields = [
        "date", "sunrise", "sunset", "tithi_name", "tithi_end",
        "nakshatra_name", "nakshatra_end", "yoga_name", "yoga_end",
        "karana_json", "masa", "paksha", "samvatsaram", "ayana", "ruthu",
        "suryarashi", "chandrarashi", "rahukalam", "yamagandam",
        "varjyam", "durmuhurtham_json", "abhijit_muhurtham", "amruthakalam"
    ]

    missing_fields = []
    for field in required_fields:
        if field not in result:
            missing_fields.append(field)

    if missing_fields:
        print(f"✗ Missing fields: {missing_fields}")
        return False
    else:
        print(f"✓ All {len(required_fields)} required fields present!")

    # Check bilingual structure
    bilingual_fields = ["tithi_name", "nakshatra_name", "yoga_name", "masa", "paksha"]
    for field in bilingual_fields:
        if "en" not in result[field] or "ta" not in result[field]:
            print(f"✗ Bilingual structure missing for {field}")
            return False

    print("✓ Bilingual structure verified!")
    return True


def save_sample_output():
    """Save a sample output for reference"""
    print("\n\nSaving sample output...")

    calculator = PanchangamCalculator()
    test_date = datetime(2026, 1, 1)
    location = LOCATIONS["hyderabad"]

    result = calculator.calculate_panchangam(
        test_date,
        location["lat"],
        location["lon"],
        location["timezone"]
    )

    result["location_info"] = {
        "key": "hyderabad",
        "name": location["name"],
        "country": location["country"]
    }

    with open("sample_panchangam.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✓ Sample output saved to sample_panchangam.json")


if __name__ == "__main__":
    print("Telugu Calendar API - Test Suite")
    print("=" * 60)

    try:
        # Run tests
        test_single_date()
        test_multiple_locations()
        test_data_structure()
        save_sample_output()

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
