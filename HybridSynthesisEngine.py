class HybridSynthesisEngine:
    def __init__(self):
        self.element_wisdom = {
            "ไม้": {"nature": "การเติบโต", "strategy": "วางแผนระยะยาว", "vibe": "มีความคิดสร้างสรรค์"},
            "ไฟ": {"nature": "ความโชติช่วง", "strategy": "สร้างชื่อเสียง", "vibe": "กระตือรือร้น"},
            "ดิน": {"nature": "ความมั่นคง", "strategy": "จัดระบบที่จับต้องได้", "vibe": "หนักแน่น"},
            "ทอง": {"nature": "ความเฉียบคม", "strategy": "ตัดสินใจเด็ดขาด", "vibe": "ยึดมั่นหลักการ"},
            "น้ำ": {"nature": "การปรับตัว", "strategy": "ใช้ไหวพริบเจรจา", "vibe": "ลึกซึ้ง"}
        }

    def _generate_dynamic_details(self, primary_element, score, is_smooth):
        wisdom = self.element_wisdom.get(primary_element, self.element_wisdom["ดิน"])
        intensity = f"ด้วยพลังธาตุ{primary_element}ที่โดดเด่น " if score > 40 else f"ด้วยสมดุลธาตุ{primary_element} "
        flow_msg = "ส่งผลให้ชีวิตมีความคล่องตัวสูง" if is_smooth else "แต่ควรระวังความล่าช้าในบางจังหวะ"
        return {
            "work": f"{intensity} เน้น{wisdom['strategy']} {flow_msg}",
            "money": f"การเงินเน้น{wisdom['nature']} มีโอกาสจากธาตุ{primary_element}",
            "love": f"ลักษณะความรักคือ{wisdom['vibe']}"
        }

    def verify_and_predict(self, bazi_result, thai_result):
        useful_gods = bazi_result['useful_gods']
        scores = bazi_result.get('scores', {})
        found_gods = []
        warnings = []
        actionable_insights = []
        
        # ดึงข้อมูลดาวจรที่เทียบกับลัคนาเกิดแล้ว
        planets_data = thai_result['planets']

        for planet, status in planets_data.items():
            if status['element'] in useful_gods:
                # 1. เช็กภพเสีย (อริ, มรณะ, วินาศ)
                if status['house'] in ["อริ", "มรณะ", "วินาศ"]:
                    warnings.append(f"ดาว{planet} ({status['type']}) เป็นธาตุให้คุณ แต่ตกภพ{status['house']} อาจมีอุปสรรคแฝงมากับโอกาส")
                elif status['is_walking_slowly']:
                    warnings.append(f"ดาว{planet} ({status['type']}) ให้คุณ แต่กำลังเดินมนท์ (ช้า) เป้าหมายอาจคลาดเคลื่อน")
                else:
                    found_gods.append(status['element'])
                    # 2. แปลความหมายภพดี
                    house_meaning = ""
                    if status['house'] == "กัมมะ": house_meaning = "ส่งเสริมด้านการงานเต็มที่"
                    elif status['house'] == "กดุมภะ": house_meaning = "ดึงดูดทรัพย์สินและรายได้"
                    elif status['house'] == "ปัตนิ": house_meaning = "ดีต่อเรื่องคู่ครอง/หุ้นส่วน"
                    elif status['house'] == "ลาภะ": house_meaning = "นำมาซึ่งโชคลาภความสำเร็จ"
                    else: house_meaning = f"เกื้อหนุนในเรื่อง{status['house']}"

                    actionable_insights.append(f"พลังดาว{planet} ({status['type']}) โคจรเข้าภพ{status['house']} {house_meaning}")

        base_score = 50
        final_score = max(min(base_score + (len(found_gods) * 15) - (len(warnings) * 10), 100), 0)
        primary_el = useful_gods[0] if useful_gods else "ดิน"
        
        dynamic_details = self._generate_dynamic_details(primary_el, scores.get(primary_el, 20), len(warnings) < 2)

        summary = "จังหวะชีวิตเป็นใจให้ลงมือทำเรื่องสำคัญ" if final_score >= 70 else "สถานการณ์อยู่ในระดับปานกลาง ควบคุมได้" if final_score >= 50 else "ควรเน้นตั้งรับและวางแผนอย่างรอบคอบ"

        return {
            "score": final_score,
            "prediction": summary,
            "details": dynamic_details,
            "actionable_insights": actionable_insights,
            "warnings": warnings,
            "lagna": thai_result['lagna'] # ส่งชื่อลัคนาไปแสดงผล
        }
