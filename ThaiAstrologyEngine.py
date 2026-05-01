import swisseph as swe
from datetime import datetime, timezone, timedelta

class ThaiAstrologyEngine:
    def __init__(self):
        # โหราศาสตร์ไทยนิยมใช้ค่าอายนางศะแบบ Lahiri (ระบบอินเดีย/นิรายนะ) 
        # เพื่อปรับองศาดาวสากล (Tropical) ให้เป็นแบบไทย (Sidereal)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Mapping รหัสดาวของ swisseph ให้เป็นตัวเลขไทย
        self.thai_planets = {
            swe.SUN: {"id": "๑", "name": "อาทิตย์"},
            swe.MOON: {"id": "๒", "name": "จันทร์"},
            swe.MARS: {"id": "๓", "name": "อังคาร"},
            swe.MERCURY: {"id": "๔", "name": "พุธ"},
            swe.JUPITER: {"id": "๕", "name": "พฤหัสบดี"},
            swe.VENUS: {"id": "๖", "name": "ศุกร์"},
            swe.SATURN: {"id": "๗", "name": "เสาร์"},
            swe.MEAN_NODE: {"id": "๘", "name": "ราหู"}, # ใช้ Mean Node หรือ True Node ก็ได้
            swe.URANUS: {"id": "๐", "name": "มฤตยู"}
        }

        # ชื่อราศีทั้ง 12
        self.zodiac_signs = [
            "เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์",
            "ตุลย์", "พิจิก", "ธนู", "มังกร", "กุมภ์", "มีน"
        ]

    def calculate_positions(self, birth_dt, lat, lon):
        """
        birth_dt: datetime object (ควรเป็นเวลา Local)
        lat, lon: พิกัดสถานที่เกิด
        """
        # 1. แปลงเวลาเกิดเป็นเวลาสากล (UTC) ก่อนคำนวณ
        # โหราศาสตร์ไทยอิงเวลามาตรฐาน UTC+7
        utc_dt = birth_dt - timedelta(hours=7) 
        
        # 2. แปลงเป็น Julian Day
        # swisseph ต้องการเวลาในรูปแบบ ทศนิยมของชั่วโมง (Hour + Min/60)
        decimal_hour = utc_dt.hour + (utc_dt.minute / 60.0) + (utc_dt.second / 3600.0)
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, decimal_hour)

        result = {
            "lagna": {},
            "planets": {}
        }

        # 3. การคำนวณลัคนา (Ascendant)
        # ใช้ระบบ House System 'W' (Whole Sign) หรือ 'P' (Placidus) สำหรับหา Ascendant
        houses, ascmc = swe.houses_ex(jd, lat, lon, b'W')
        asc_deg = ascmc[0] # องศาของลัคนา
        asc_sign_index = int(asc_deg // 30)
        result["lagna"] = {
            "degree": round(asc_deg, 2),
            "sign_index": asc_sign_index,
            "sign_name": self.zodiac_signs[asc_sign_index],
            "degree_in_sign": round(asc_deg % 30, 2)
        }

        # 4. การคำนวณตำแหน่งดาว (Planets)
        # flag = swe.FLG_SWIEPH (ใช้ Ephemeris แม่นยำสูง) | swe.FLG_SIDEREAL (ใช้อายนางศะ)
        calc_flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

        for p_id, p_info in self.thai_planets.items():
            # calc_ut คืนค่า array: [องศารวม, ละติจูด, ระยะห่าง, ความเร็ว...]
            pos, ret = swe.calc_ut(jd, p_id, calc_flag)
            
            lon_deg = pos[0] # องศารวม (0 - 360)
            sign_index = int(lon_deg // 30)
            deg_in_sign = lon_deg % 30 # องศาภายในราศี (0 - 30)
            
            # เช็กการเดินผิดปกติของดาว (พักร์, มนท์, เสริด) จากความเร็ว pos[3]
            speed = pos[3]
            motion = "ปกติ"
            if speed < 0:
                motion = "พักร์ (ถอยหลัง)"
            elif p_id != swe.MEAN_NODE and speed < 0.2: # ราหูเดินถอยหลังเป็นปกติอยู่แล้ว
                motion = "มนท์ (ช้า)"

            result["planets"][p_info["name"]] = {
                "id": p_info["id"],
                "total_degree": round(lon_deg, 2),
                "sign_index": sign_index,
                "sign_name": self.zodiac_signs[sign_index],
                "degree_in_sign": round(deg_in_sign, 2),
                "motion": motion
            }

        return result

# --- ทดลองรันระบบ ---
if __name__ == "__main__":
    birth_datetime = datetime(1990, 5, 15, 10, 30)
    engine = ThaiAstrologyEngine()
    chart_data = engine.calculate_positions(birth_datetime, 13.75, 100.5)

    print(f"ลัคนาสถิตราศี: {chart_data['lagna']['sign_name']} (ที่ {chart_data['lagna']['degree_in_sign']} องศา)")
    print("-" * 30)
    for planet, data in chart_data['planets'].items():
        print(f"ดาว {data['id']} ({planet}): สถิตราศี{data['sign_name']} ({data['degree_in_sign']} องศา) - การโคจร: {data['motion']}")