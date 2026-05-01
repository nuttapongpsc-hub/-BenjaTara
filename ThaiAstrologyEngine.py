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
        self.zodiac_signs = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์", "ตุลย์", "พิจิก", "ธนู", "มังกร", "กุมภ์", "มีน"]
        self.house_names = ["ตนุ", "กดุมภะ", "สหัชชะ", "พันธุ", "ปุตตะ", "อริ", "ปัตนิ", "มรณะ", "ศุภะ", "กัมมะ", "ลาภะ", "วินาศ"]

    def calculate_positions(self, dt, lat, lon, ref_lagna_index=None):
        swe.set_ephe_path()
        # ใช้ระบบตัดอายนางศะแบบ Lahiri เพื่อให้ใกล้เคียงโหราศาสตร์ไทย
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

        # 1. คำนวณลัคนา (Ascendant)
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', flags)
        ascendant_degree = ascmc[0]
        lagna_sign_index = int(ascendant_degree / 30)
        lagna_sign = self.zodiac_signs[lagna_sign_index]

        # หากมีลัคนาอ้างอิง (เช่น ดูดวงจร) ให้ใช้ลัคนาเดิมในการนับภพ
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

        # 2. คำนวณดาวและภพ
        for name, planet_id in planets_to_calculate.items():
            res = swe.calc_ut(jd, planet_id, flags)
            longitude = res[0][0]
            speed = res[0][3]

            sign_index = int(longitude / 30)
            # หาภพโดยนับจากลัคนาเกิด
            house_index = (sign_index - use_lagna_index) % 12
            
            results["planets"][name] = {
                "longitude": longitude,
                "sign": self.zodiac_signs[sign_index],
                "house": self.house_names[house_index],
                "element": self.planet_elements.get(name, "ไม่ระบุ"),
                "type": self.planet_types.get(name, "ไม่ระบุ"),
                "is_walking_slowly": speed < 0 or (speed < (0.5 * self._get_avg_speed(planet_id)))
            }
        return results

    def _get_avg_speed(self, planet_id):
        avg_speeds = { swe.SUN: 0.98, swe.MOON: 13.17, swe.MARS: 0.52, swe.MERCURY: 1.38, swe.JUPITER: 0.08, swe.VENUS: 1.2, swe.SATURN: 0.03, swe.MEAN_NODE: 0.05, swe.URANUS: 0.01 }
        return avg_speeds.get(planet_id, 1.0)
