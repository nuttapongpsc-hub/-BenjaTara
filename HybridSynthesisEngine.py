class HybridSynthesisEngine:
    def __init__(self):
        self.element_wisdom_detailed = {
            "ไม้": {"work": "พลังงานธาตุไม้เปรียบเสมือนต้นไม้ที่กำลังแตกกิ่งก้านสาขา ช่วงเวลานี้ดวงชะตาส่งเสริมให้เกิดการเริ่มต้นสิ่งใหม่ๆ", "money": "รายได้จะมาจากผลงานและรากฐานที่คุณเคยสร้างไว้ในอดีต", "love": "ความรักจะค่อยๆ งอกงามและพัฒนาไปอย่างมั่นคงแข็งแรง"},
            "ไฟ": {"work": "ดวงชะตาได้รับพลังงานธาตุไฟที่โชติช่วง ช่วงเวลานี้เหมาะสำหรับการแสดงศักยภาพ การเป็นผู้นำโปรเจกต์", "money": "กระแสการเงินหมุนเวียนอย่างรวดเร็ว มีโอกาสได้จับเงินก้อน", "love": "ความรักมีความตื่นเต้น เร่าร้อน และมีเสน่ห์ดึงดูดใจอย่างมาก"},
            "ดิน": {"work": "พลังงานธาตุดินส่งเสริมให้คุณมีความหนักแน่นและมั่นคงเป็นพิเศษ เหมาะกับงานที่ต้องใช้ความอดทน", "money": "รากฐานทางการเงินของคุณกำลังถูกสร้างให้แข็งแกร่งขึ้น โชคลาภมาจากทรัพย์สินชิ้นใหญ่", "love": "ความสัมพันธ์เน้นความหนักแน่น จริงใจ และการสร้างครอบครัว"},
            "ทอง": {"work": "พลังงานธาตุทองมอบความเฉียบคมและความเด็ดขาด คุณมีความสามารถในการมองทะลุถึงปัญหา", "money": "คุณมีเซนส์ในการประเมินมูลค่าและโอกาสทางการเงิน รายได้เกิดจากการกล้าตัดสินใจ", "love": "ดวงความรักต้องการความชัดเจน ตรงไปตรงมา และการรักษาสัจจะ"},
            "น้ำ": {"work": "พลังงานธาตุน้ำส่งเสริมให้คุณมีความพลิกแพลง ปรับตัวเข้ากับทุกสถานการณ์ได้ดี", "money": "กระแสเงินสดมีความคล่องตัวสูงมาก โอกาสมักจะมาจากช่องทางที่หลากหลาย", "love": "คุณจะมีความอ่อนโยน ลึกซึ้ง และมีสัมผัสที่ไวต่อความรู้สึกของคนรัก"}
        }

    def _generate_dynamic_details(self, primary_element, score, is_smooth):
        wisdom = self.element_wisdom_detailed.get(primary_element, self.element_wisdom_detailed["ดิน"])
        details = {
            "work": wisdom['work'],
            "money": wisdom['money'],
            "love": wisdom['love']
        }
        return details

    def verify_and_predict(self, bazi_result, thai_result):
        useful_gods = bazi_result['useful_gods']
        scores = bazi_result.get('scores', {})
        found_gods = []
        warnings = []
        actionable_insights = []
        
        planets_data = thai_result['planets']
        lagna_attr = thai_result.get('lagna_attributes', {})

        for planet, status in planets_data.items():
            if status['element'] in useful_gods:
                tarot_card = status.get('zodiac_attributes', {}).get('tarot_major', '')
                tarot_msg = f"<br>🎴 <i>[ไพ่: <b>{tarot_card}</b>]</i>"
                
                if status['house'] in ["อริ", "มรณะ", "วินาศ"]:
                    warnings.append(f"**ดาว{planet}** ตกภพเสีย: ต้องใช้ความอดทนและระมัดระวังเป็นพิเศษ{tarot_msg}")
                else:
                    actionable_insights.append(f"**พลังดาว{planet}** เข้าภพ'{status['house']}': ส่งเสริมด้าน{status['house']}{tarot_msg}")

        base_score = 50
        final_score = max(min(base_score + (len(found_gods) * 15) - (len(warnings) * 8), 100), 0)
        primary_el = useful_gods[0] if useful_gods else "ดิน"
        
        return {
            "score": final_score,
            "prediction": "ดวงชะตาอยู่ในเกณฑ์ที่ปรับเปลี่ยนได้ตามความพยายาม",
            "details": self._generate_dynamic_details(primary_el, scores.get(primary_el, 20), len(warnings) < 2),
            "actionable_insights": actionable_insights,
            "warnings": warnings,
            "lagna": thai_result['lagna'],
            "tarot_card": lagna_attr.get('tarot_major', '')
        }

    def generate_final_summary(self, report, selected_cards_meanings):
        tarot_summary = " ".join(selected_cards_meanings)
        advice = "ให้ใช้ความมีสติและความรอบคอบเป็นที่ตั้งในการตัดสินใจเรื่องสำคัญช่วงนี้ครับ"
        if report['score'] >= 70: advice = "จังหวะนี้เป็นนาทีทอง ขอให้มั่นใจและเดินหน้าเต็มกำลัง!"
        
        return f"### 🔮 บทสรุปพยากรณ์รวม\n**แนวโน้ม:** {report['prediction']}\n\n**ภาพรวมไพ่สะท้อน:** {tarot_summary}\n\n**คำแนะนำ:** {advice}"
