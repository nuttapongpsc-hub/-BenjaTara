class HybridSynthesisEngine:
    def __init__(self):
        # 1. สร้างสะพานเชื่อม (The Bridge) ระหว่างธาตุจีน กับ ดาวไทย
        self.element_to_planet = {
            "ไฟ": ["๑", "๓"],    # อาทิตย์, อังคาร
            "ดิน": ["๒", "๕"],   # จันทร์, พฤหัสบดี
            "ทอง": ["๔", "๖"],   # พุธ, ศุกร์
            "น้ำ": ["๘", "๐"],    # ราหู, มฤตยู
            "ไม้": ["๓", "๕"]    # อังคาร(พลังขับเคลื่อน), พฤหัส(การเติบโต)
        }

    def verify_and_predict(self, bazi_data, thai_data):
        """
        นำ JSON ของทั้ง 2 ศาสตร์มาเปรียบเทียบกัน
        """
        useful_gods = bazi_data.get("useful_gods", [])
        thai_planets = thai_data.get("planets", {})
        
        confidence_score = 50 # คะแนนเริ่มต้น
        insights = []
        warnings = []

        # 2. Logic การตรวจจับ "จุดส่งเสริม" (Synergy Check)
        for element in useful_gods:
            matched_planets = self.element_to_planet.get(element, [])
            
            for planet_name, planet_data in thai_planets.items():
                if planet_data["id"] in matched_planets:
                    
                    # เช็กสถานะของดาวบนท้องฟ้า (โคจรปกติ = ดี, พักร์/ถอยหลัง = มีอุปสรรค)
                    if planet_data["motion"] == "ปกติ":
                        confidence_score += 15
                        insights.append(
                            f"✅ พลังงานธาตุ{element}ให้คุณ และดาว{planet_name}({planet_data['id']}) โคจรเป็นปกติ "
                            f"ส่งผลดีอย่างมากให้ลงมือทำเรื่องสำคัญได้เลย"
                        )
                    elif planet_data["motion"] in ["พักร์ (ถอยหลัง)", "มนท์ (ช้า)"]:
                        confidence_score -= 5
                        warnings.append(
                            f"⚠️ แม้ธาตุ{element}จะให้คุณ แต่ดาว{planet_name}({planet_data['id']}) กำลังเดิน{planet_data['motion']} "
                            f"โอกาสมีอยู่แต่จะเกิดความล่าช้าหรือต้องรอคอย"
                        )

        # 3. Logic วิเคราะห์ภาพรวมและเลือกคำทำนาย
        confidence_score = min(max(confidence_score, 0), 100) # กำหนดให้อยู่ในกรอบ 0-100%
        
        final_prediction = ""
        if confidence_score >= 80:
            final_prediction = "วันนี้ดวงดาวและพลังงานธาตุสอดประสานกันอย่างสมบูรณ์แบบ เป็นจังหวะทองคำที่คุณควรเร่งเจรจาหรือเริ่มโปรเจกต์ใหม่"
        elif 50 <= confidence_score < 80:
            final_prediction = "สถานการณ์ภาพรวมอยู่ในเกณฑ์บวก ราบรื่น แต่อาจมีเรื่องจุกจิกเล็กน้อย ให้ใช้ความรอบคอบในการตัดสินใจ"
        else:
            final_prediction = "พลังงานและดวงดาวขัดแย้งกัน ควรหลีกเลี่ยงการทำธุรกรรมสำคัญ เน้นจัดการงานเอกสารหรืองานเบื้องหลังจะปลอดภัยที่สุด"

        return {
            "score": confidence_score,
            "prediction": final_prediction,
            "actionable_insights": insights,
            "warnings": warnings
        }

# --- จำลองการทำงาน (Mock Data) ---
# สมมติว่านี่คือ Output ที่ประมวลผลเสร็จแล้วจากฐานข้อมูล
mock_bazi_output = {
    "chart_type": "ดิถีอ่อนแอ",
    "useful_gods": ["ทอง", "ดิน"] # ต้องการธาตุทองและดินมาเสริม
}

mock_thai_output = {
    "planets": {
        "พฤหัสบดี": {"id": "๕", "motion": "ปกติ", "sign_name": "ธนู"}, # ธาตุดิน เดินปกติ
        "ศุกร์": {"id": "๖", "motion": "พักร์ (ถอยหลัง)", "sign_name": "พิจิก"}, # ธาตุทอง เดินถอยหลัง
        "อาทิตย์": {"id": "๑", "motion": "ปกติ", "sign_name": "พฤษภ"} 
    }
}

# รันระบบประมวลผล
engine = HybridSynthesisEngine()
result = engine.verify_and_predict(mock_bazi_output, mock_thai_output)

# แสดงผลลัพธ์
print("🎯 [ ผลการวิเคราะห์ดวงชะตารายวัน ] 🎯")
print(f"ความมั่นใจของคำทำนาย (Confidence Score): {result['score']}%")
print(f"คำทำนายหลัก: {result['prediction']}")
print("\n[ รายละเอียดเชิงลึก ]")
for insight in result['actionable_insights']:
    print(insight)
for warning in result['warnings']:
    print(warning)