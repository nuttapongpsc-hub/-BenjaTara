from lunar_python import Solar

class BaziAnalyzer:
    def __init__(self):
        self.stem_elements = {
            "กะ": "ไม้", "อิก": "ไม้", "เปิ่ง": "ไฟ", "เต็ง": "ไฟ", "บู๊": "ดิน", "กี๋": "ดิน",
            "แก": "ทอง", "ซิง": "ทอง", "ยิ้ม": "น้ำ", "กุ่ย": "น้ำ"
        }
        self.branch_elements = {
            "ขาล": "ไม้", "เถาะ": "ไม้", "มะเส็ง": "ไฟ", "มะเมีย": "ไฟ",
            "มะโรง": "ดิน", "มะแม": "ดิน", "จอ": "ดิน", "ฉลู": "ดิน",
            "วอก": "ทอง", "ระกา": "ทอง", "กุน": "น้ำ", "ชวด": "น้ำ"
        }
        self.cycle = {
            "ไม้": {"produces": "ไฟ", "produced_by": "น้ำ", "controlled_by": "ทอง", "controls": "ดิน"},
            "ไฟ": {"produces": "ดิน", "produced_by": "ไม้", "controlled_by": "น้ำ", "controls": "ทอง"},
            "ดิน": {"produces": "ทอง", "produced_by": "ไฟ", "controlled_by": "ไม้", "controls": "น้ำ"},
            "ทอง": {"produces": "น้ำ", "produced_by": "ดิน", "controlled_by": "ไฟ", "controls": "ไม้"},
            "น้ำ": {"produces": "ไม้", "produced_by": "ทอง", "controlled_by": "ดิน", "controls": "ไฟ"}
        }
        
        # Mapping อักษรจีน -> ไทย
        self.cn_to_th_stem = {
            "甲": "กะ", "乙": "อิก", "丙": "เปิ่ง", "丁": "เต็ง",
            "戊": "บู๊", "己": "กี๋", "庚": "แก", "辛": "ซิง",
            "壬": "ยิ้ม", "癸": "กุ่ย"
        }
        self.cn_to_th_branch = {
            "子": "ชวด", "丑": "ฉลู", "寅": "ขาล", "卯": "เถาะ",
            "辰": "มะโรง", "巳": "มะเส็ง", "午": "มะเมีย", "未": "มะแม",
            "申": "วอก", "酉": "ระกา", "戌": "จอ", "亥": "กุน"
        }

    def get_bazi_chart(self, year, month, day, hour, minute):
        """แปลงวันเกิดสากลเป็น 4 เสา (กะจื้อ)"""
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
        baZi = lunar.getEightChar()

        chart = {
            "year": {
                "stem": self.cn_to_th_stem.get(baZi.getYearGan(), ""),
                "branch": self.cn_to_th_branch.get(baZi.getYearZhi(), "")
            },
            "month": {
                "stem": self.cn_to_th_stem.get(baZi.getMonthGan(), ""),
                "branch": self.cn_to_th_branch.get(baZi.getMonthZhi(), "")
            },
            "day": {
                "stem": self.cn_to_th_stem.get(baZi.getDayGan(), ""),
                "branch": self.cn_to_th_branch.get(baZi.getDayZhi(), "")
            },
            "hour": {
                "stem": self.cn_to_th_stem.get(baZi.getTimeGan(), ""),
                "branch": self.cn_to_th_branch.get(baZi.getTimeZhi(), "")
            }
        }
        return chart

    def calculate_strength(self, bazi_chart):
        day_master_stem = bazi_chart["day"]["stem"]
        day_master_element = self.stem_elements[day_master_stem]

        scores = {"ไม้": 0, "ไฟ": 0, "ดิน": 0, "ทอง": 0, "น้ำ": 0}
        weights = {
            "year_stem": 10, "year_branch": 10,
            "month_stem": 12, "month_branch": 35, 
            "day_stem": 0, "day_branch": 15,
            "hour_stem": 10, "hour_branch": 8
        }

        for pillar, data in bazi_chart.items():
            if pillar != "day" or data["stem"] != day_master_stem:
                stem_el = self.stem_elements.get(data["stem"])
                if stem_el: scores[stem_el] += weights[f"{pillar}_stem"]
            
            branch_el = self.branch_elements.get(data["branch"])
            if branch_el: scores[branch_el] += weights[f"{pillar}_branch"]

        return day_master_element, scores

    def find_useful_god(self, day_master_element, scores):
        support_element = self.cycle[day_master_element]["produced_by"]
        support_score = scores[day_master_element] + scores[support_element]
        weaken_score = sum(v for k, v in scores.items() if k not in [day_master_element, support_element])

        is_strong = support_score > weaken_score
        
        useful_gods = []
        if is_strong:
            chart_type = "ดิถีแข็งแรง"
            useful_gods.extend([self.cycle[day_master_element]["produces"], self.cycle[day_master_element]["controls"]])
        else:
            chart_type = "ดิถีอ่อนแอ"
            useful_gods.extend([support_element, day_master_element])

        return {
            "day_master": day_master_element,
            "chart_type": chart_type,
            "useful_gods": useful_gods,
            "scores": scores # ส่งคะแนนกลับไปเผื่อใช้แสดงผล
        }