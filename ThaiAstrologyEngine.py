import swisseph as swe

class ThaiAstrologyEngine:
    def __init__(self):
        self.planet_elements = {
            "อาทิตย์ (๑)": "ไฟ", "จันทร์ (๒)": "ดิน", "อังคาร (๓)": "ลม",
            "พุธ (๔)": "น้ำ", "พฤหัสบดี (๕)": "ดิน", "ศุกร์ (๖)": "น้ำ",
            "เสาร์ (๗)": "ไฟ", "ราหู (๘)": "ลม", "มฤตยู (๐)": "อากาศธาตุ"
        }
        self.planet_types = {
            "อาทิตย์ (๑)": "บาปเคราะห์", "จันทร์ (๒)": "ศุภเคราะห์", "อังคาร (๓)": "บาปเคราะห์",
            "พุธ (๔)": "ศุภเคราะห์", "พฤหัสบดี (๕)": "ศุภเคราะห์", "ศุกร์ (๖)": "ศุภเคราะห์",
            "เสาร์ (๗)": "บาปเคราะห์", "ราหู (๘)": "บาปเคราะห์", "มฤตยู (๐)": "บาปเคราะห์"
        }
        self.dignities = {
            "อาทิตย์ (๑)": {"เกษตร": ["สิงห์"], "อุจจ์": ["เมษ"], "นิจ": ["ตุลย์"], "ประ": ["กุมภ์"]},
            "จันทร์ (๒)": {"เกษตร": ["กรกฎ"], "อุจจ์": ["พฤษภ"], "นิจ": ["พิจิก"], "ประ": ["มังกร"]},
            "อังคาร (๓)": {"เกษตร": ["เมษ", "พิจิก"], "อุจจ์": ["มังกร"], "นิจ": ["กรกฎ"], "ประ": ["พฤษภ", "ตุลย์"]},
            "พุธ (๔)": {"เกษตร": ["มิถุน", "กันย์"], "อุจจ์": ["กันย์"], "นิจ": ["มีน"], "ประ": ["ธนู", "มีน"]},
            "พฤหัสบดี (๕)": {"เกษตร": ["ธนู", "มีน"], "อุจจ์": ["กรกฎ"], "นิจ": ["มังกร"], "ประ": ["มิถุน", "กันย์"]},
            "ศุกร์ (๖)": {"เกษตร": ["พฤษภ", "ตุลย์"], "อุจจ์": ["มีน"], "นิจ": ["กันย์"], "ประ": ["เมษ", "พิจิก"]},
            "เสาร์ (๗)": {"เกษตร": ["มังกร"], "อุจจ์": ["ตุลย์"], "นิจ": ["เมษ"], "ประ": ["กรกฎ"]},
            "ราหู (๘)": {"เกษตร": ["กุมภ์"], "อุจจ์": ["พิจิก"], "นิจ": ["พฤษภ"], "ประ": ["สิงห์"]},
            "มฤตยู (๐)": {"เกษตร": [], "อุจจ์": [], "นิจ": [], "ประ": []}
        }
        self.zodiac_signs = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์", "ตุลย์", "พิจิก", "ธนู", "มังกร", "กุมภ์", "มีน"]
        self.house_names = ["ตนุ", "กดุมภะ", "สหัชชะ", "พันธุ", "ปุตตะ", "อริ", "ปัตนิ", "มรณะ", "ศุภะ", "กัมมะ", "ลาภะ", "วินาศ"]

    def calculate_positions(self, dt, lat, lon, ref_lagna_index=None):
        swe.set_ephe_path()
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', flags)
        ascendant_degree = ascmc[0]
        lagna_sign_index = int(ascendant_degree / 30)
        lagna_sign = self.zodiac_signs[lagna_sign_index]

        use_lagna_index = lagna_sign_index if ref_lagna_index is None else ref_lagna_index

        planets_to_calculate = {
            "อาทิตย์ (๑)": swe.SUN, "จันทร์ (๒)": swe.MOON, "อังคาร (๓)": swe.MARS,
            "พุธ (๔)": swe.MERCURY, "พฤหัสบดี (๕)": swe.JUPITER, "ศุกร์ (๖)": swe.VENUS,
            "เสาร์ (๗)": swe.SATURN, "ราหู (๘)": swe.MEAN_NODE, "มฤตยู (๐)": swe.URANUS
        }

        results = {
            "lagna": lagna_sign,
            "lagna_index": lagna_sign_index,
            "planets": {}
        }

        for name, planet_id in planets_to_calculate.items():
            res = swe.calc_ut(jd, planet_id, flags)
            longitude = res[0][0]
            speed = res[0][3]

            sign_index = int(longitude / 30)
            sign_name = self.zodiac_signs[sign_index]
            house_index = (sign_index - use_lagna_index) % 12
            
            found_dignities = []
            for dig, signs in self.dignities.get(name, {}).items():
                if sign_name in signs:
                    found_dignities.append(dig)
            dignity_str = "/".join(found_dignities) if found_dignities else "มาตรฐานปกติ"
            
            results["planets"][name] = {
                "longitude": longitude,
                "sign": sign_name,
                "house": self.house_names[house_index],
                "element": self.planet_elements.get(name, "ไม่ระบุ"),
                "type": self.planet_types.get(name, "ไม่ระบุ"),
                "dignity": dignity_str,
                "is_walking_slowly": speed < 0 or (speed < (0.5 * self._get_avg_speed(planet_id)))
            }
        return results

    def _get_avg_speed(self, planet_id):
        avg_speeds = { swe.SUN: 0.98, swe.MOON: 13.17, swe.MARS: 0.52, swe.MERCURY: 1.38, swe.JUPITER: 0.08, swe.VENUS: 1.2, swe.SATURN: 0.03, swe.MEAN_NODE: 0.05, swe.URANUS: 0.01 }
        return avg_speeds.get(planet_id, 1.0)
