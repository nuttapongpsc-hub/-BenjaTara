class HybridSynthesisEngine:
    def __init__(self):
        # ส่วนประกอบของคำทำนาย (Phrase Bank) เพื่อนำมาประกอบกันแบบจิ๊กซอว์
        self.element_wisdom = {
            "ไม้": {
                "nature": "การเติบโตและการขยายตัว",
                "strategy": "เน้นการวางแผนระยะยาวและการเรียนรู้",
                "vibe": "มีความคิดสร้างสรรค์และเปี่ยมด้วยเมตตา"
            },
            "ไฟ": {
                "nature": "โชติช่วงและการแสดงออก",
                "strategy": "เน้นความรวดเร็วและการสร้างชื่อเสียง",
                "vibe": "มีความกระตือรือร้นและส่งต่อพลังงานให้ผู้อื่น"
            },
            "ดิน": {
                "nature": "ความมั่นคงและการสะสม",
                "strategy": "เน้นความรอบคอบและการสร้างระบบที่จับต้องได้",
                "vibe": "มีความหนักแน่นและเป็นที่พึ่งพาได้"
            },
            "ทอง": {
                "nature": "ความเฉียบคมและการตัดสินใจ",
                "strategy": "เน้นความเด็ดขาดและการบริหารจัดการคน",
                "vibe": "มีความยุติธรรมและยึดมั่นในหลักการ"
            },
            "น้ำ": {
                "nature": "การไหลลื่นและการปรับตัว",
                "strategy": "เน้นการเจรจาและใช้ไหวพริบพลิกแพลง",
                "vibe": "มีความลึกซึ้งและเข้าใจสถานการณ์ได้ดี"
            }
        }

    def _generate_dynamic_details(self, primary_element, score, is_smooth):
        """สังเคราะห์ประโยคคำทำนายใหม่ตามระดับคะแนนและสถานะดวงดาว"""
        wisdom = self.element_wisdom.get(primary_element, self.element_wisdom["ดิน"])
        
        # ปรับความหมายตามพลังงานธาตุ (Intensity Analysis)
        if score > 40:
            intensity = f"ด้วยพลังธาตุ{primary_element}ที่โดดเด่นมากในดวงชะตา "
        elif score < 15:
            intensity = f"แม้ธาตุ{primary_element}จะมีปริมาณน้อยแต่เป็นธาตุให้คุณ "
        else:
            intensity = f"ด้วยความสมดุลของธาตุ{primary_element}ที่พอดี "

        # ปรับความหมายตามสถานะดาว (Flow Analysis)
        if is_smooth:
            flow_msg = "ส่งผลให้จังหวะชีวิตมีความคล่องตัวสูง มีโอกาสเข้ามาให้หยิบจับแบบไม่ทันตั้งตัว"
        else:
            flow_msg = "แต่ต้องระวังจังหวะที่ล่าช้าลงเล็กน้อย แนะนำให้รอคอยจังหวะที่เหมาะสมและอย่ารีบร้อน"

        # สร้างรายละเอียด 3 ด้าน
        details = {
            "work": f"{intensity} {wisdom['strategy']} {flow_msg}",
            "money": f"การเงินเน้น{wisdom['nature']} มีเกณฑ์ได้ลาภจากช่องทางที่เกี่ยวข้องกับธาตุ{primary_element}โดยตรง",
            "love": f"ลักษณะความรักในช่วงนี้คือ{wisdom['vibe']} ความเข้าใจกันจะนำมาซึ่งความสุข"
        }
        return details

    def verify_and_predict(self, bazi_result, thai_result):
        useful_gods = bazi_result['useful_gods']
        scores = bazi_result.get('scores', {})
        found_gods = []
        warnings = []
        actionable_insights = []
        
        # 1. วิเคราะห์ดาวจรเปรียบเทียบกับธาตุให้คุณ
        for planet, status in thai_result.items():
            if status['element'] in useful_gods:
                if status['is_walking_slowly']:
                    warnings.append(f"ดาว{planet} (ธาตุ{status['element']}) ให้คุณ แต่กำลังเดินช้าลง อาจทำให้เป้าหมายคลาดเคลื่อนไปบ้าง")
                else:
                    found_gods.append(status['element'])
                    actionable_insights.append(f"พลังดาว{planet} ส่งเสริมธาตุ{status['element']} ของคุณได้อย่างยอดเยี่ยมในตอนนี้")

        # 2. คำนวณ Confidence Score แบบถ่วงน้ำหนัก
        base_score = 60
        bonus = len(found_gods) * 10
        penalty = len(warnings) * 5
        final_score = max(min(base_score + bonus - penalty, 100), 0)

        # 3. สังเคราะห์คำทำนาย
        primary_el = useful_gods[0] if useful_gods else "ดิน"
        el_score = scores.get(primary_el, 20)
        is_smooth = len(warnings) < 2
        
        # เรียกใช้ฟังก์ชันสังเคราะห์ประโยค
        dynamic_details = self._generate_dynamic_details(primary_el, el_score, is_smooth)

        # สรุปภาพรวม
        if final_score >= 75:
            summary = f"ช่วงเวลานี้พลังงานธาตุ{primary_el}กำลังรุ่งโรจน์ จังหวะชีวิตเป็นใจให้ลงมือทำเรื่องสำคัญ"
        elif final_score >= 50:
            summary = f"สถานการณ์อยู่ในระดับที่ควบคุมได้ มีความราบรื่นสลับกับความล่าช้าในบางจังหวะ"
        else:
            summary = "ควรเน้นการตั้งรับและวางแผนอย่างรอบคอบ พลังงานดาวจรยังไม่ส่งเสริมเต็มที่"

        return {
            "score": final_score,
            "prediction": summary,
            "details": dynamic_details,
            "actionable_insights": actionable_insights,
            "warnings": warnings
        }
