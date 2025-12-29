"""
Panchangam calculation module using Swiss Ephemeris
Calculates all Panchangam elements for a given date and location
"""

import swisseph as swe
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple
import json

from config import NAKSHATRAS, TITHIS, YOGAS, KARANAS, MASAS, RASHIS, RUTHUS, AYANAS


class PanchangamCalculator:
    """Calculate Panchangam elements using Swiss Ephemeris"""

    def __init__(self):
        # Set Swiss Ephemeris path (uses built-in data)
        swe.set_ephe_path('')

        # Set Lahiri Ayanamsa (Chitrapaksha) - Standard for Indian Panchangam
        # This is crucial for accurate Vedic/Hindu calendar calculations
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    def calculate_panchangam(self, date: datetime, lat: float, lon: float, tz: str) -> Dict:
        """
        Calculate complete Panchangam for a given date and location

        Args:
            date: Date to calculate for
            lat: Latitude of location
            lon: Longitude of location
            tz: Timezone string (e.g., 'Asia/Kolkata')

        Returns:
            Dictionary containing all Panchangam elements
        """
        timezone = pytz.timezone(tz)
        local_date = timezone.localize(datetime(date.year, date.month, date.day, 0, 0, 0))

        # Calculate Julian Day for midnight
        jd_midnight = self._get_julian_day(local_date, timezone)

        # Calculate sunrise/sunset first
        sun_times = self._calculate_sun_times(jd_midnight, lat, lon, timezone)

        # Get sunrise time for this date and convert to JD
        # Traditional Panchangam uses Tithi/Nakshatra at sunrise, not midnight
        geopos = (lon, lat, 0)
        sunrise_jd = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_RISE, geopos)[1][0]

        # Calculate all elements
        panchangam = {
            "date": date.strftime("%Y-%m-%d"),
            "location": {"latitude": lat, "longitude": lon},
            "timezone": tz,

            # Sunrise and Sunset
            **sun_times,

            # Tithi (at sunrise)
            **self._calculate_tithi(sunrise_jd, timezone),

            # Nakshatra (at sunrise)
            **self._calculate_nakshatra(sunrise_jd, timezone),

            # Yoga (at sunrise)
            **self._calculate_yoga(sunrise_jd, timezone),

            # Karana (at sunrise)
            **self._calculate_karana(sunrise_jd, timezone),

            # Masa and Paksha (at sunrise)
            **self._calculate_masa_paksha(sunrise_jd),

            # Samvatsara (at sunrise)
            **self._calculate_samvatsara(sunrise_jd),

            # Ayana and Ruthu (at sunrise)
            **self._calculate_ayana_ruthu(sunrise_jd),

            # Rashi (Zodiac signs - at sunrise)
            **self._calculate_rashis(sunrise_jd),

            # Inauspicious times (calculated from midnight for full day)
            **self._calculate_inauspicious_times(jd_midnight, lat, lon, timezone),

            # Auspicious times (calculated from midnight for full day)
            **self._calculate_auspicious_times(jd_midnight, lat, lon, timezone)
        }

        return panchangam

    def _get_julian_day(self, dt: datetime, timezone) -> float:
        """Convert datetime to Julian Day"""
        utc_dt = dt.astimezone(pytz.UTC)
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                       utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
        return jd

    def _calculate_sun_times(self, jd: float, lat: float, lon: float, timezone) -> Dict:
        """Calculate sunrise, sunset, moonrise, moonset"""
        # Geographic position: (longitude, latitude, altitude)
        geopos = (lon, lat, 0)

        # Get sunrise and sunset
        sunrise_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_RISE, geopos)[1][0]
        sunset_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_SET, geopos)[1][0]

        # Get moonrise and moonset
        moonrise_result = swe.rise_trans(jd, swe.MOON, swe.CALC_RISE, geopos)
        moonset_result = swe.rise_trans(jd, swe.MOON, swe.CALC_SET, geopos)

        sunrise = self._jd_to_time_str(sunrise_jd, timezone)
        sunset = self._jd_to_time_str(sunset_jd, timezone)

        moonrise = self._jd_to_time_str(moonrise_result[1][0], timezone) if moonrise_result[0] == 0 else None
        moonset = self._jd_to_time_str(moonset_result[1][0], timezone) if moonset_result[0] == 0 else None

        return {
            "sunrise": sunrise,
            "sunset": sunset,
            "moonrise": moonrise,
            "moonset": moonset
        }

    def _calculate_tithi(self, jd: float, timezone) -> Dict:
        """Calculate Tithi (lunar day)"""
        # Use sidereal (Lahiri) positions for accurate Panchangam
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        # Tithi is based on elongation of Moon from Sun
        elongation = (moon_pos - sun_pos) % 360
        tithi_num = int(elongation / 12)  # Each tithi is 12 degrees

        # Find tithi end time
        target_elongation = ((tithi_num + 1) * 12) % 360
        tithi_end_jd = self._find_transition(jd, jd + 1, swe.SUN, swe.MOON, target_elongation)

        paksha = "Shukla Paksha" if tithi_num < 15 else "Krishna Paksha"

        return {
            "tithi_name": TITHIS[tithi_num],
            "tithi_end": self._jd_to_time_str(tithi_end_jd, timezone) if tithi_end_jd else None,
            "paksha": {"en": paksha, "ta": "சுக்ல பக்ஷம்" if tithi_num < 15 else "கிருஷ்ண பக்ஷம்"}
        }

    def _calculate_nakshatra(self, jd: float, timezone) -> Dict:
        """Calculate Nakshatra (lunar mansion)"""
        # Use sidereal (Lahiri) position for Moon
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        # Each nakshatra is 13°20' (13.333...)
        nakshatra_num = int(moon_pos / (360/27))

        # Find nakshatra end time
        target_pos = ((nakshatra_num + 1) * 360/27) % 360
        nakshatra_end_jd = self._find_moon_transition(jd, jd + 1, target_pos)

        return {
            "nakshatra_name": NAKSHATRAS[nakshatra_num],
            "nakshatra_end": self._jd_to_time_str(nakshatra_end_jd, timezone) if nakshatra_end_jd else None
        }

    def _calculate_yoga(self, jd: float, timezone) -> Dict:
        """Calculate Yoga"""
        # Use sidereal (Lahiri) positions
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        # Yoga is based on sum of Sun and Moon longitudes
        yoga_sum = (sun_pos + moon_pos) % 360
        yoga_num = int(yoga_sum / (360/27))

        # Find yoga end time
        target_sum = ((yoga_num + 1) * 360/27) % 360
        yoga_end_jd = self._find_yoga_transition(jd, jd + 1, target_sum)

        return {
            "yoga_name": YOGAS[yoga_num],
            "yoga_end": self._jd_to_time_str(yoga_end_jd, timezone) if yoga_end_jd else None
        }

    def _calculate_karana(self, jd: float, timezone) -> Dict:
        """Calculate Karana (half-tithi)"""
        # Use sidereal (Lahiri) positions
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        elongation = (moon_pos - sun_pos) % 360
        karana_num = int(elongation / 6) % 60  # Each karana is 6 degrees

        # Map to the 11 karanas (first 4 are fixed, rest repeat)
        if karana_num < 57:
            karana_index = karana_num % 7
        else:
            karana_index = 7 + (karana_num - 57)

        karana_list = []
        for i in range(2):  # Usually 2 karanas per day
            k_num = (karana_num + i) % 60
            if k_num < 57:
                k_idx = k_num % 7
            else:
                k_idx = 7 + (k_num - 57)

            end_jd = self._find_karana_end(jd, jd + 1, (karana_num + i + 1) * 6)
            karana_list.append({
                "name": KARANAS[min(k_idx, 10)],
                "end": self._jd_to_time_str(end_jd, timezone) if end_jd else None
            })

        return {
            "karana_json": json.dumps(karana_list)
        }

    def _calculate_masa_paksha(self, jd: float) -> Dict:
        """Calculate Masa (month) and Paksha"""
        # Use sidereal (Lahiri) positions
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        # Masa is based on Sun's position in zodiac
        masa_num = int(sun_pos / 30)

        # Paksha based on tithi
        elongation = (moon_pos - sun_pos) % 360
        tithi_num = int(elongation / 12)
        paksha = "Shukla Paksha" if tithi_num < 15 else "Krishna Paksha"

        return {
            "masa": MASAS[masa_num % 12],
            "paksha": {"en": paksha, "ta": "சுக்ல பக்ஷம்" if tithi_num < 15 else "கிருஷ்ண பக்ஷம்"}
        }

    def _calculate_samvatsara(self, jd: float) -> Dict:
        """Calculate Samvatsara (60-year cycle)"""
        # Simplified calculation - actual calculation is complex
        gregorian_year = swe.revjul(jd)[0]

        # Tamil Samvatsara names (60-year cycle)
        samvatsaras = [
            "Prabhava", "Vibhava", "Shukla", "Pramoda", "Prajapati",
            "Angirasa", "Shrimukha", "Bhava", "Yuva", "Dhatri",
            "Ishvara", "Bahudhanya", "Pramadhi", "Vikrama", "Vrisha",
            "Chitrabhanu", "Svabhanu", "Tarana", "Parthiva", "Vyaya",
            "Sarvajit", "Sarvadharin", "Virodhi", "Vikrita", "Khara",
            "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukha",
            "Hevilambi", "Vilambi", "Vikari", "Sharvari", "Plava",
            "Shubhakrit", "Shobhana", "Krodhi", "Vishvavasu", "Parabhava",
            "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrit",
            "Paridhavin", "Pramadicha", "Ananda", "Rakshasa", "Nala",
            "Pingala", "Kalayukta", "Siddharthi", "Raudra", "Durmathi",
            "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Akshaya"
        ]

        # Calculate year in 60-year cycle
        year_offset = (gregorian_year - 1987) % 60  # 1987 was Prabhava year
        samvatsara_name = samvatsaras[year_offset]

        return {
            "samvatsaram": {"en": samvatsara_name, "ta": samvatsara_name}
        }

    def _calculate_ayana_ruthu(self, jd: float) -> Dict:
        """Calculate Ayana (solstice period) and Ruthu (season)"""
        # Use sidereal (Lahiri) position for Sun
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]

        # Ayana: Uttarayana (winter solstice to summer) vs Dakshinayana
        ayana = AYANAS[0] if 270 <= sun_pos or sun_pos < 90 else AYANAS[1]

        # Ruthu: 6 seasons, each roughly 2 months
        ruthu_num = int((sun_pos % 360) / 60)
        ruthu = RUTHUS[ruthu_num]

        return {
            "ayana": ayana,
            "ruthu": ruthu
        }

    def _calculate_rashis(self, jd: float) -> Dict:
        """Calculate Sun and Moon Rashi (zodiac signs)"""
        # Use sidereal (Lahiri) positions
        sun_pos = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

        sun_rashi_num = int(sun_pos / 30)
        moon_rashi_num = int(moon_pos / 30)

        return {
            "suryarashi": RASHIS[sun_rashi_num],
            "chandrarashi": RASHIS[moon_rashi_num]
        }

    def _calculate_inauspicious_times(self, jd: float, lat: float, lon: float, timezone) -> Dict:
        """Calculate inauspicious times: Rahukalam, Yamagandam, Varjyam, Durmuhurtham"""
        # Geographic position: (longitude, latitude, altitude)
        geopos = (lon, lat, 0)

        # Get sunrise and sunset times
        sunrise_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_RISE, geopos)[1][0]
        sunset_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_SET, geopos)[1][0]

        day_duration = (sunset_jd - sunrise_jd) * 24  # in hours
        segment = day_duration / 8  # Divide day into 8 segments

        # Get weekday (0=Monday, 6=Sunday)
        weekday = int((jd + 1.5) % 7)

        # Rahukalam timings (different for each day)
        rahu_periods = [7, 1, 6, 4, 5, 3, 2]  # Monday to Sunday
        rahu_start_jd = sunrise_jd + (rahu_periods[weekday] * segment / 24)
        rahu_end_jd = rahu_start_jd + (segment / 24)

        # Yamagandam timings
        yama_periods = [4, 3, 2, 1, 7, 6, 5]  # Monday to Sunday
        yama_start_jd = sunrise_jd + (yama_periods[weekday] * segment / 24)
        yama_end_jd = yama_start_jd + (segment / 24)

        # Durmuhurtham (morning and evening)
        durmu_morning_start = sunrise_jd + (6 * 60 / (24 * 60))  # ~6 ghatikas after sunrise
        durmu_morning_end = durmu_morning_start + (48 / (24 * 60))  # 48 minutes

        durmu_evening_start = sunset_jd - (48 / (24 * 60))
        durmu_evening_end = sunset_jd

        # Varjyam (simplified calculation)
        varjyam_start_jd = sunrise_jd + (day_duration * 0.4 / 24)
        varjyam_end_jd = varjyam_start_jd + (48 / (24 * 60))

        return {
            "rahukalam": {
                "start": self._jd_to_time_str(rahu_start_jd, timezone),
                "end": self._jd_to_time_str(rahu_end_jd, timezone)
            },
            "yamagandam": {
                "start": self._jd_to_time_str(yama_start_jd, timezone),
                "end": self._jd_to_time_str(yama_end_jd, timezone)
            },
            "varjyam": {
                "start": self._jd_to_time_str(varjyam_start_jd, timezone),
                "end": self._jd_to_time_str(varjyam_end_jd, timezone)
            },
            "durmuhurtham_json": json.dumps([
                {
                    "period": "Morning",
                    "start": self._jd_to_time_str(durmu_morning_start, timezone),
                    "end": self._jd_to_time_str(durmu_morning_end, timezone)
                },
                {
                    "period": "Evening",
                    "start": self._jd_to_time_str(durmu_evening_start, timezone),
                    "end": self._jd_to_time_str(durmu_evening_end, timezone)
                }
            ])
        }

    def _calculate_auspicious_times(self, jd: float, lat: float, lon: float, timezone) -> Dict:
        """Calculate auspicious times: Abhijit Muhurtham, Amruthakalam"""
        # Geographic position: (longitude, latitude, altitude)
        geopos = (lon, lat, 0)

        # Get sunrise and sunset
        sunrise_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_RISE, geopos)[1][0]
        sunset_jd = swe.rise_trans(jd, swe.SUN, swe.CALC_SET, geopos)[1][0]

        day_duration = (sunset_jd - sunrise_jd) * 24

        # Abhijit Muhurtham: 8th muhurta from sunrise (middle of the day)
        muhurta_duration = day_duration / 15  # Day divided into 15 muhurtas
        abhijit_start_jd = sunrise_jd + (7 * muhurta_duration / 24)
        abhijit_end_jd = abhijit_start_jd + (muhurta_duration / 24)

        # Amruthakalam (simplified)
        amrutha_start_jd = sunrise_jd + (2 * muhurta_duration / 24)
        amrutha_end_jd = amrutha_start_jd + (muhurta_duration / 24)

        return {
            "abhijit_muhurtham": {
                "start": self._jd_to_time_str(abhijit_start_jd, timezone),
                "end": self._jd_to_time_str(abhijit_end_jd, timezone)
            },
            "amruthakalam": {
                "start": self._jd_to_time_str(amrutha_start_jd, timezone),
                "end": self._jd_to_time_str(amrutha_end_jd, timezone)
            }
        }

    def _find_transition(self, jd_start: float, jd_end: float, body1: int, body2: int, target: float) -> float:
        """Find when elongation reaches target value"""
        # Binary search for transition time
        precision = 1 / (24 * 60)  # 1 minute precision

        while (jd_end - jd_start) > precision:
            jd_mid = (jd_start + jd_end) / 2
            # Use sidereal positions
            pos1 = swe.calc_ut(jd_mid, body1, swe.FLG_SIDEREAL)[0][0]
            pos2 = swe.calc_ut(jd_mid, body2, swe.FLG_SIDEREAL)[0][0]
            current = (pos2 - pos1) % 360

            if abs(current - target) < 0.1:
                return jd_mid
            elif current < target:
                jd_start = jd_mid
            else:
                jd_end = jd_mid

        return (jd_start + jd_end) / 2

    def _find_moon_transition(self, jd_start: float, jd_end: float, target: float) -> float:
        """Find when Moon reaches target longitude"""
        precision = 1 / (24 * 60)

        while (jd_end - jd_start) > precision:
            jd_mid = (jd_start + jd_end) / 2
            # Use sidereal position
            current = swe.calc_ut(jd_mid, swe.MOON, swe.FLG_SIDEREAL)[0][0]

            if abs(current - target) < 0.01:
                return jd_mid
            elif current < target:
                jd_start = jd_mid
            else:
                jd_end = jd_mid

        return (jd_start + jd_end) / 2

    def _find_yoga_transition(self, jd_start: float, jd_end: float, target: float) -> float:
        """Find when Yoga (Sun + Moon) reaches target"""
        precision = 1 / (24 * 60)

        while (jd_end - jd_start) > precision:
            jd_mid = (jd_start + jd_end) / 2
            # Use sidereal positions
            sun_pos = swe.calc_ut(jd_mid, swe.SUN, swe.FLG_SIDEREAL)[0][0]
            moon_pos = swe.calc_ut(jd_mid, swe.MOON, swe.FLG_SIDEREAL)[0][0]
            current = (sun_pos + moon_pos) % 360

            if abs(current - target) < 0.1:
                return jd_mid
            elif current < target:
                jd_start = jd_mid
            else:
                jd_end = jd_mid

        return (jd_start + jd_end) / 2

    def _find_karana_end(self, jd_start: float, jd_end: float, target_elongation: float) -> float:
        """Find when Karana ends"""
        return self._find_transition(jd_start, jd_end, swe.SUN, swe.MOON, target_elongation % 360)

    def _jd_to_time_str(self, jd: float, timezone) -> str:
        """Convert Julian Day to time string in local timezone"""
        year, month, day, hour = swe.revjul(jd)

        # Create UTC datetime - convert to integers
        dt_utc = datetime(int(year), int(month), int(day)) + timedelta(hours=hour)
        dt_utc = pytz.UTC.localize(dt_utc)

        # Convert to local timezone
        dt_local = dt_utc.astimezone(timezone)

        return dt_local.strftime("%H:%M")
