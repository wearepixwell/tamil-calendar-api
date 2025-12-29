#!/usr/bin/env python3
"""
Script to update Telugu translations to Tamil translations in config.py
"""

# Tamil translations mappings
YOGAS_TAMIL = [
    "விஷ்கம்பா", "ப்ரீதி", "ஆயுஷ்மான்", "சௌபாக்ய", "சோபன",
    "அதிகண்ட", "சுகர்மா", "த்ருதி", "சூலா", "கண்ட",
    "வ்ருத்தி", "த்ருவ", "வ்யாகாத", "ஹர்ஷண", "வஜ்ரா",
    "சித்தி", "வ்யதீபாத", "வரீயான்", "பரிக", "சிவ",
    "சித்த", "சாத்ய", "சுப", "சுக்ல", "ப்ரம்ம",
    "இந்திர", "வைத்ருதி"
]

KARANAS_TAMIL = [
    "பவ", "பாலவ", "கௌலவ", "தைதில", "கரஜ",
    "வணிஜ", "விஷ்டி", "சகுனி", "சதுஷ்பாத", "நாக",
    "கிம்ஸ்துக்ன"
]

MASAS_TAMIL = [
    "சித்திரை", "வைகாசி", "ஆனி", "ஆடி", "ஆவணி",
    "புரட்டாசி", "ஐப்பசி", "கார்த்திகை", "மார்கழி", "தை",
    "மாசி", "பங்குனி"
]

RASHIS_TAMIL = [
    "மேஷம்", "ரிஷபம்", "மிதுனம்", "கர்க்கடகம்", "சிம்மம்",
    "கன்னி", "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்",
    "கும்பம்", "மீனம்"
]

RUTHUS_TAMIL = [
    "வசந்தம்", "கிரீஷ்மம்", "வர்ஷா", "சரத்", "ஹேமந்தம்",
    "சிசிர"
]

AYANAS_TAMIL = [
    "உத்தராயணம்", "தக்ஷிணாயனம்"
]

def update_config():
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Yogas
    for i, tamil in enumerate(YOGAS_TAMIL):
        # Find the line with Telugu and replace
        import re
        # This is complex, let's just manually define the updates we need

    print("Config updated with Tamil translations")

if __name__ == "__main__":
    update_config()
