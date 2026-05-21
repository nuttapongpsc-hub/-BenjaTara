import random

class TarotEngine:
    def __init__(self):
        self.cards = {
            "The Fool": {
                "meaning": "การเริ่มต้นใหม่, อิสระ, การเดินทางที่คาดไม่ถึง, การกล้าเสี่ยง",
                "image": "https://upload.wikimedia.org/wikipedia/en/9/90/RWS_Tarot_00_Fool.jpg"
            },
            "The Magician": {
                "meaning": "ความสามารถรอบด้าน, การสร้างปาฏิหาริย์ด้วยตัวเอง, พลังสร้างสรรค์, การสื่อสาร",
                "image": "https://upload.wikimedia.org/wikipedia/en/d/de/RWS_Tarot_01_Magician.jpg"
            },
            "The High Priestess": {
                "meaning": "สัญชาตญาณ, ความลึกลับ, การใช้ความรู้สึกนำทาง, พลังหยิน",
                "image": "https://upload.wikimedia.org/wikipedia/en/8/88/RWS_Tarot_02_High_Priestess.jpg"
            },
            "The Emperor": {
                "meaning": "อำนาจ, ความเป็นผู้นำ, ความมั่นคงในหน้าที่การงาน, กฎระเบียบ",
                "image": "https://upload.wikimedia.org/wikipedia/en/c/c3/RWS_Tarot_04_Emperor.jpg"
            },
            "The Lovers": {
                "meaning": "การตัดสินใจครั้งสำคัญ, ความสัมพันธ์, ความสามัคคี, เสน่ห์ดึงดูด",
                "image": "https://upload.wikimedia.org/wikipedia/en/d/db/RWS_Tarot_06_Lovers.jpg"
            },
            "The Chariot": {
                "meaning": "ความมุ่งมั่น, การควบคุมสถานการณ์, ชัยชนะที่ต้องแลกมาด้วยความพยายาม, การเดินทาง",
                "image": "https://upload.wikimedia.org/wikipedia/en/9/9b/RWS_Tarot_07_Chariot.jpg"
            },
            "Death": {
                "meaning": "การจบสิ้นเพื่อเริ่มต้นใหม่, การเปลี่ยนแปลงข้ามผ่านสภาวะเดิม, การปล่อยวาง",
                "image": "https://upload.wikimedia.org/wikipedia/en/d/d7/RWS_Tarot_13_Death.jpg"
            },
            "The Star": {
                "meaning": "ความหวัง, แรงบันดาลใจ, การฟื้นฟูเยียวยา, โชคชะตาที่สดใส",
                "image": "https://upload.wikimedia.org/wikipedia/en/c/cd/RWS_Tarot_17_Star.jpg"
            },
            "Ace of Wands": {
                "meaning": "โอกาสใหม่ในเรื่องงาน, แรงบันดาลใจที่พุ่งพล่าน, พลังแห่งการริเริ่ม",
                "image": "https://upload.wikimedia.org/wikipedia/en/1/11/Wands01.jpg"
            },
            "Ace of Pentacles": {
                "meaning": "โชคลาภทางการเงิน, ข่าวดีเรื่องรายได้, ความมั่นคงทางวัตถุ, การเริ่มต้นธุรกิจ",
                "image": "https://upload.wikimedia.org/wikipedia/en/f/fd/Pents01.jpg"
            },
            "Ace of Swords": {
                "meaning": "ความชัดเจน, การตัดสินใจที่เด็ดขาด, การเอาชนะอุปสรรคด้วยสติปัญญา",
                "image": "https://upload.wikimedia.org/wikipedia/en/1/1a/Swords01.jpg"
            },
            "Ace of Cups": {
                "meaning": "ความสุขทางใจ, ความรักครั้งใหม่, ความอิ่มเอมใจ, อารมณ์ที่ลึกซึ้ง",
                "image": "https://upload.wikimedia.org/wikipedia/en/3/36/Cups01.jpg"
            }
        }

    def get_all_card_names(self):
        """คืนค่ารายชื่อไพ่ทั้งหมดเพื่อให้ผู้ใช้เลือกใน Dropdown"""
        return list(self.cards.keys())

    def get_card_info(self, card_name):
        """คืนค่าข้อมูลของไพ่ที่ระบุ (ความหมาย และ รูปภาพ)"""
        return self.cards.get(card_name, {"meaning": "ไม่พบข้อมูล", "image": ""})

    def draw_card(self):
        """ฟังก์ชันสุ่มไพ่ 1 ใบ (สำหรับปุ่มเสี่ยงทายด้านล่าง)"""
        card_name = random.choice(list(self.cards.keys()))
        card_data = self.cards[card_name]
        return card_name, card_data["meaning"], card_data["image"]