"""
Muhurtam calculation module
Calculates auspicious dates for various life events based on Panchangam principles
"""

import swisseph as swe
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple
import json

from config import NAKSHATRAS, TITHIS


class MuhurtamCalculator:
    """Calculate auspicious Muhurtam dates for various purposes"""

    def __init__(self):
        # Set Swiss Ephemeris path
        swe.set_ephe_path('')
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Auspicious Tithis for different Muhurtams
        self.auspicious_tithis = {
            'marriage': [2, 3, 5, 7, 10, 11, 12, 13],  # Indices: Dvitiya, Tritiya, Panchami, Saptami, Dasami, Ekadasi, Dvadasi, Trayodasi
            'grihapravesam': [2, 3, 5, 7, 10, 11, 12, 13],
            'vehicle': [2, 3, 5, 6, 7, 10, 11, 12, 13],
            'naamkaranam': [5, 6, 10, 11, 12],
            'annaprasanam': [5, 6, 10, 11, 12],
            'upanayanam': [2, 3, 5, 7, 10, 11, 12, 13]
        }

        # Auspicious Nakshatras for different Muhurtams
        self.auspicious_nakshatras = {
            'marriage': [0, 2, 3, 4, 6, 7, 9, 10, 12, 13, 14, 16, 19, 22, 25, 26],  # Ashwini, Rohini, Mrigashirsha, Punarvasu, Pushya, Ashlesha, Magha, UPhalguni, Hasta, Swati, Anuradha, UAshadha, Shravana, Dhanishta, Revati
            'grihapravesam': [0, 2, 3, 4, 6, 9, 10, 12, 13, 16, 19, 22, 25, 26],
            'vehicle': [0, 2, 3, 4, 6, 9, 10, 12, 13, 16, 19, 22, 25, 26],
            'naamkaranam': [0, 2, 3, 4, 6, 9, 10, 12, 13, 16, 22, 25, 26],
            'annaprasanam': [0, 2, 3, 4, 6, 9, 10, 12, 13, 16, 22, 25, 26],
            'upanayanam': [0, 2, 3, 4, 6, 9, 10, 12, 13, 16, 22, 25, 26]
        }

        # Inauspicious weekdays for marriage (Tuesday, Saturday)
        self.marriage_avoid_weekdays = [1, 5]  # Monday=0, Tuesday=1, ..., Sunday=6

    def calculate_muhurtam_dates(
        self,
        year: int,
        muhurtam_type: str,
        lat: float,
        lon: float,
        tz: str
    ) -> List[Dict]:
        """
        Calculate auspicious Muhurtam dates for a given year and type

        Args:
            year: Year to calculate for
            muhurtam_type: Type of muhurtam (marriage, grihapravesam, vehicle, etc.)
            lat: Latitude
            lon: Longitude
            tz: Timezone

        Returns:
            List of auspicious dates with details
        """
        if muhurtam_type not in self.auspicious_tithis:
            raise ValueError(f"Unknown muhurtam type: {muhurtam_type}")

        auspicious_dates = []
        timezone = pytz.timezone(tz)

        # Start from Jan 1st
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        current_date = start_date

        auspicious_tithi_indices = self.auspicious_tithis[muhurtam_type]
        auspicious_nakshatra_indices = self.auspicious_nakshatras[muhurtam_type]

        while current_date <= end_date:
            # Skip certain weekdays for marriage
            if muhurtam_type == 'marriage' and current_date.weekday() in self.marriage_avoid_weekdays:
                current_date += timedelta(days=1)
                continue

            # Get Panchangam data for this date
            local_date = timezone.localize(datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0))
            jd_midnight = self._get_julian_day(local_date, timezone)

            # Get sunrise JD
            geopos = (lon, lat, 0)
            try:
                sunrise_jd = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_RISE, geopos)[1][0]
            except:
                current_date += timedelta(days=1)
                continue

            # Calculate Tithi and Nakshatra at sunrise
            tithi_info = self._calculate_tithi(sunrise_jd, timezone)
            nakshatra_info = self._calculate_nakshatra(sunrise_jd, timezone)
            masa_paksha = self._calculate_masa_paksha(sunrise_jd)

            tithi_index = tithi_info['tithi_number'] - 1  # Convert to 0-indexed
            nakshatra_index = nakshatra_info['nakshatra_number'] - 1  # Convert to 0-indexed

            # Check if Tithi and Nakshatra are auspicious
            if (tithi_index in auspicious_tithi_indices and
                nakshatra_index in auspicious_nakshatra_indices):

                # Skip certain months for marriage (Ashada and Bhadrapada Krishna Paksha)
                if muhurtam_type == 'marriage':
                    masa_name = masa_paksha['masa']['en']
                    paksha_name = masa_paksha['paksha']['en']

                    # Skip during inauspicious periods
                    if (masa_name in ['Ashadha', 'Bhadrapada'] and 'Krishna' in paksha_name):
                        current_date += timedelta(days=1)
                        continue

                auspicious_dates.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day': current_date.strftime('%A'),
                    'tithi': tithi_info['tithi_name']['en'],
                    'tithi_end': tithi_info.get('tithi_end', ''),
                    'nakshatra': nakshatra_info['nakshatra_name']['en'],
                    'nakshatra_end': nakshatra_info.get('nakshatra_end', ''),
                    'masa': masa_paksha['masa']['en'],
                    'paksha': masa_paksha['paksha']['en']
                })

            current_date += timedelta(days=1)

        return auspicious_dates

    def _get_julian_day(self, dt: datetime, timezone) -> float:
        """Convert datetime to Julian Day"""
        utc_dt = dt.astimezone(pytz.UTC)
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                       utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
        return jd

    def _calculate_tithi(self, jd: float, timezone) -> Dict:
        """Calculate Tithi at given Julian Day"""
        # Calculate Moon and Sun positions
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]

        # Tithi is the angular distance between Moon and Sun divided by 12 degrees
        tithi_angle = (moon_pos - sun_pos) % 360
        tithi_num = int(tithi_angle / 12) + 1

        # Calculate when tithi ends (when moon-sun angle reaches next multiple of 12)
        next_tithi_angle = (int(tithi_angle / 12) + 1) * 12

        # Find approximate end time by iterating
        jd_temp = jd
        tithi_end_time = None

        for _ in range(48):  # Check every 30 minutes for next 24 hours
            jd_temp += (30.0 / (24.0 * 60.0))  # Add 30 minutes
            moon_pos_temp = swe.calc_ut(jd_temp, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]
            sun_pos_temp = swe.calc_ut(jd_temp, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]
            angle_temp = (moon_pos_temp - sun_pos_temp) % 360

            if angle_temp >= next_tithi_angle or (angle_temp < 12 and next_tithi_angle >= 348):
                # Convert JD back to local time
                year, month, day, hour = swe.revjul(jd_temp)
                dt_utc = datetime(year, month, day, int(hour), int((hour % 1) * 60))
                dt_utc = pytz.UTC.localize(dt_utc)
                dt_local = dt_utc.astimezone(timezone)
                tithi_end_time = dt_local.strftime("%H:%M")
                break

        # Determine Paksha (Shukla or Krishna)
        if tithi_num <= 15:
            paksha = "Shukla"
        else:
            paksha = "Krishna"
            tithi_num = tithi_num - 15

        return {
            'tithi_number': tithi_num,
            'tithi_name': {'en': TITHIS[tithi_num - 1]['en'], 'ta': TITHIS[tithi_num - 1]['ta']},
            'tithi_end': tithi_end_time if tithi_end_time else "23:59",
            'paksha': {'en': f"{paksha} Paksha", 'ta': f"{paksha} பக்ஷம்"}
        }

    def _calculate_nakshatra(self, jd: float, timezone) -> Dict:
        """Calculate Nakshatra at given Julian Day"""
        # Calculate Moon position
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]

        # Each Nakshatra spans 13°20' (13.333... degrees)
        nakshatra_span = 360.0 / 27.0
        nakshatra_num = int(moon_pos / nakshatra_span) + 1

        # Calculate when nakshatra ends
        next_nakshatra_angle = nakshatra_num * nakshatra_span

        jd_temp = jd
        nakshatra_end_time = None

        for _ in range(48):
            jd_temp += (30.0 / (24.0 * 60.0))
            moon_pos_temp = swe.calc_ut(jd_temp, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]

            if moon_pos_temp >= next_nakshatra_angle or (moon_pos_temp < nakshatra_span and next_nakshatra_angle >= 360 - nakshatra_span):
                year, month, day, hour = swe.revjul(jd_temp)
                dt_utc = datetime(year, month, day, int(hour), int((hour % 1) * 60))
                dt_utc = pytz.UTC.localize(dt_utc)
                dt_local = dt_utc.astimezone(timezone)
                nakshatra_end_time = dt_local.strftime("%H:%M")
                break

        return {
            'nakshatra_number': nakshatra_num,
            'nakshatra_name': {'en': NAKSHATRAS[nakshatra_num - 1]['en'], 'ta': NAKSHATRAS[nakshatra_num - 1]['ta']},
            'nakshatra_end': nakshatra_end_time if nakshatra_end_time else "23:59"
        }

    def _calculate_masa_paksha(self, jd: float) -> Dict:
        """Calculate Masa and Paksha"""
        # Calculate Moon and Sun positions
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]

        # Tithi calculation for paksha
        tithi_angle = (moon_pos - sun_pos) % 360
        tithi_num = int(tithi_angle / 12) + 1

        if tithi_num <= 15:
            paksha = "Shukla"
        else:
            paksha = "Krishna"

        # Masa is determined by the zodiac sign the Sun is in
        from config import MASAS
        rashi_num = int(sun_pos / 30) + 1

        # Tamil Solar Month: Sun's Rashi directly maps to Tamil month
        # Rashi 1 (Mesha/Aries) = Chithirai (index 0)
        # So rashi_num - 1 = masa_index
        masa_index = (rashi_num - 1) % 12

        return {
            'masa': {'en': MASAS[masa_index]['en'], 'ta': MASAS[masa_index]['ta']},
            'paksha': {'en': f"{paksha} Paksha", 'ta': f"{paksha} பக்ஷம்"}
        }
