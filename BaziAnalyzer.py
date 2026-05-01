from lunar_python import Solar

class BaziAnalyzer:
    def __init__(self):
        # ข้อมูลราศีบน (Heavenly Stems) พร้อมธาตุและขั้ว (+/-)
        self.stems = {
            "甲": {"element": "ไม้", "polarity": "+"}, "乙": {"element": "ไม้", "polarity": "-"},
            "丙": {"element": "ไฟ", "polarity": "+"}, "丁": {"element": "ไฟ", "polarity": "-"},
            "戊": {"element": "ดิน", "polarity": "+"}, "己": {"element": "ดิน", "polarity": "-"},
            "庚": {"element": "ทอง", "polarity": "+"}, "辛": {"element": "ทอง", "polarity": "-"},
            "壬": {"element": "น้ำ", "polarity": "+"}, "癸": {"element": "น้ำ", "polarity": "-"}
        }
        # ข้อมูลราศีล่าง (Earthly Branches - นักษัตร)
        self.branches = {
            "子": {"element": "น้ำ", "polarity": "-"}, "丑": {"element": "ดิน", "polarity": "-"},
            "寅": {"element": "ไม้", "polarity": "+"}, "卯": {"element": "ไม้", "polarity": "-"},
            "辰": {"element": "ดิน", "polarity": "+"}, "巳": {"element": "ไฟ", "polarity": "+"},
            "午": {"element": "ไฟ", "polarity": "-"}, "未": {"element": "ดิน", "polarity": "-"},
            "申": {"element": "ทอง", "polarity": "+"}, "酉": {"element": "ทอง", "polarity": "-"},
            "戌": {"element": "ดิน", "polarity": "+"}, "亥": {"element": "น้ำ", "polarity": "+"}
        }
        
        # วงจร 5 ธาตุ (ก่อกำเนิด และ พิฆาตทำลาย)
        self.generate = {"ไม้": "ไฟ", "ไฟ": "ดิน", "ดิน": "ทอง", "ทอง": "น้ำ", "น้ำ": "ไม้"}
        self.control = {"ไม้": "ดิน", "ดิน": "น้ำ", "น้ำ": "ไฟ", "ไฟ": "ทอง", "ทอง": "ไม้"}

    def _get_ten_god(self, dm_element, dm_polarity, target_element, target_polarity):
        """คำนวณระบบ 10 เทพ (Ten Gods / 十神)"""
        if target_element == dm_element:
            return "ปี่เกียง (เพื่อน)" if dm_polarity == target_polarity else "เกียบไช้ (คู่แข่ง)"
        elif self.generate[dm_element] == target_element:
            return "เจียะซิ้ง (ผลงาน)" if dm_polarity == target_polarity else "ซังกัว (แสดงออก)"
        elif self.control[dm_element] == target_element:
            return "เพี้ยงไช้ (ลาภลอย)" if dm_polarity == target_polarity else "เจี้ยไช้ (การเงิน)"
        elif self.control[target_element] == dm_element:
            return "ชิกสัวะ (อำนาจ)" if dm_polarity == target_polarity else "เจี้ยกัว (ตำแหน่ง)"
        elif self.generate[target_element] == dm_element:
            return "เพี้ยงอิ่ง (อุปถัมภ์รอง)" if dm_polarity == target_polarity else "เจี้ยอิ่ง (อุปถัมภ์หลัก)"
        return "ไม่ทราบ"

    def get_bazi_chart(self, year, month, day, hour, minute):
        """ผูกดวง 4 เสาชะตา (8 ตัวอักษร)"""
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        chart = {
            "year_stem": bazi.getYearGan(), "year_branch": bazi.getYearZhi(),
            "month_stem": bazi.getMonthGan(), "month_branch": bazi.getMonthZhi(),
            "day_stem": bazi.getDayGan(), "day_branch": bazi.getDayZhi(),
            "hour_stem": bazi.getTimeGan(), "hour_branch": bazi.getTimeZhi()
        }
        return chart

    def calculate_strength(self, chart):
        scores = {"ไม้": 0, "ไฟ": 0, "ดิน": 0, "ทอง": 0, "น้ำ": 0}
        
        dm_char = chart["day_stem"]
        day_master_element = self.stems[dm_char]["element"]
        dm_polarity = self.stems[dm_char]["polarity"]

        # น้ำหนักของแต่ละเสา (เดือนเกิดมีผลต่ออุณหภูมิดวงมากที่สุด)
        weights = {
            "year_stem": 10, "year_branch": 10,
            "month_stem": 15, "month_branch": 30,
            "day_stem": 0, "day_branch": 15,
            "hour_stem": 10, "hour_branch": 10
        }
        
        # คำนวณคะแนนธาตุ
        scores[self.stems[chart["year_stem"]]["element"]] += weights["year_stem"]
        scores[self.branches[chart["year_branch"]]["element"]] += weights["year_branch"]
        scores[self.stems[chart["month_stem"]]["element"]] += weights["month_stem"]
        scores[self.branches[chart["month_branch"]]["element"]] += weights["month_branch"]
        scores[self.branches[chart["day_branch"]]["element"]] += weights["day_branch"]
        scores[self.stems[chart["hour_stem"]]["element"]] += weights["hour_stem"]
        scores[self.branches[chart["hour_branch"]]["element"]] += weights["hour_branch"]

        # ประมวลผล 10 เทพ ประจำแต่ละเสา
        ten_gods = {}
        for pos, char in chart.items():
            if pos == "day_stem":
                ten_gods[pos] = "ดิถี (ตัวตน)"
                continue
            is_stem = "stem" in pos
            source = self.stems if is_stem else self.branches
            t_elem = source[char]["element"]
            t_pol = source[char]["polarity"]
            ten_gods[pos] = self._get_ten_god(day_master_element, dm_polarity, t_elem, t_pol)

        self.current_chart = chart
        self.ten_gods = ten_gods

        return day_master_element, scores

    def find_useful_god(self, day_master, scores):
        same = scores[day_master]
        resource = scores[next(k for k, v in self.generate.items() if v == day_master)]
        self_strength = same + resource
        
        chart_type = "ดิถีแข็งแรง" if self_strength > 45 else "ดิถีอ่อนแอ"
        
        useful_gods = []
        if chart_type == "ดิถีแข็งแรง":
            useful_gods.append(self.generate[day_master]) # ถ่ายเท
            useful_gods.append(self.control[day_master])  # โชคลาภ
        else:
            useful_gods.append(day_master) # ช่วยเหลือ
            useful_gods.append(next(k for k, v in self.generate.items() if v == day_master)) # อุปถัมภ์
            
        return {
            "day_master": day_master,
            "scores": scores,
            "chart_type": chart_type,
            "useful_gods": useful_gods,
            "four_pillars": self.current_chart, 
            "ten_gods": self.ten_gods 
        }
