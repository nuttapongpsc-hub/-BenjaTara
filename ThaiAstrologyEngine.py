import swisseph as swe

class ThaiAstrologyEngine:
    def __init__(self):
        # กำหนดธาตุประจำดาวตามหลักโหราศาสตร์ไทย
        self.planet_elements = {
            "อาทิตย์ (๑)": "ไฟ",
            "จันทร์ (๒)": "ดิน",
            "อังคาร (๓)": "ลม",
            "พุธ (๔)": "น้ำ",
            "พฤหัสบดี (๕)": "ดิน",
            "ศุกร์ (๖)": "น้ำ",
            "เสาร์ (๗)": "ไฟ",
            "ราหู (๘)": "ลม",
            "เกตุ (๙)": "วิญญาณธาตุ",
            "มฤตยู (๐)": "อากาศธาตุ"
        }

    def calculate_positions(self, dt, lat, lon):
        """คำนวณตำแหน่งดาวและคืนค่าพร้อมระบุธาตุและสถานะการเดิน"""
        swe.set_ephe_path() # ใช้ตำแหน่งไฟล์ดาวพื้นฐาน
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
        
        # รายชื่อดาวที่ต้องการคำนวณ
        planets_to_calculate = {
            "อาทิตย์ (๑)": swe.SUN,
            "จันทร์ (๒)": swe.MOON,
            "อังคาร (๓)": swe.MARS,
            "พุธ (๔)": swe.MERCURY,
            "พฤหัสบดี (๕)": swe.JUPITER,
            "ศุกร์ (๖)": swe.VENUS,
            "เสาร์ (๗)": swe.SATURN,
            "ราหู (๘)": swe.MEAN_NODE,
            "มฤตยู (๐)": swe.URANUS
        }
        
        results = {}
        for name, planet_id in planets_to_calculate.items():
            res = swe.calc_ut(jd, planet_id)
            longitude = res[0][0]
            speed = res[0][3] # ความเร็วในการโคจร
            
            results[name] = {
                "longitude": longitude,
                "element": self.planet_elements.get(name, "ไม่ระบุ"), # เพิ่มส่วนนี้เพื่อแก้ Error
                "is_walking_slowly": speed < 0 or (speed < (0.5 * self._get_avg_speed(planet_id)))
            }
        return results

    def _get_avg_speed(self, planet_id):
        """คืนค่าความเร็วเฉลี่ยโดยประมาณของดาวแต่ละดวง"""
        avg_speeds = {
            swe.SUN: 0.98, swe.MOON: 13.17, swe.MARS: 0.52,
            swe.MERCURY: 1.38, swe.JUPITER: 0.08, swe.VENUS: 1.2,
            swe.SATURN: 0.03, swe.MEAN_NODE: 0.05, swe.URANUS: 0.01
        }
        return avg_speeds.get(planet_id, 1.0)
