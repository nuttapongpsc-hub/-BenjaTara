import random

class TarotEngine:
    def __init__(self):
        # ฐานข้อมูลไพ่ยิปซี 78 ใบ (ดึงภาพจากหน้าแรก Root Directory ของ GitHub โดยตรง)
        self.cards = {
            # ================= MAJOR ARCANA (22 ใบ) =================
            "The Fool": {"meaning": "การเริ่มต้นใหม่, อิสระ, การเดินทางที่คาดไม่ถึง, การกล้าเสี่ยง, การทำตามใจเรียกร้อง", "image": "the fool.jpg"},
            "The Magician": {"meaning": "ความสามารถรอบด้าน, การสร้างปาฏิหาริย์ด้วยตัวเอง, พลังสร้างสรรค์, การสื่อสารที่โน้มน้าวใจ", "image": "the magician.jpg"},
            "The High Priestess": {"meaning": "สัญชาตญาณ, ความลึกลับ, การใช้ความรู้สึกนำทาง, พลังหยิน, เซนส์ที่แม่นยำ", "image": "the high priestess.jpg"},
            "The Empress": {"meaning": "ความอุดมสมบูรณ์, ความเป็นแม่, ความรักที่อบอุ่น, ความงดงาม, การเจริญเติบโต", "image": "the empress.jpg"},
            "The Emperor": {"meaning": "อำนาจ, ความเป็นผู้นำ, ความมั่นคงในหน้าที่การงาน, กฎระเบียบ, ผู้ชายที่มีอิทธิพล", "image": "the emperor.jpg"},
            "The Hierophant": {"meaning": "ประเพณี, ความเชื่อ, ครูบาอาจารย์, การขอคำปรึกษา, สิ่งศักดิ์สิทธิ์คุ้มครอง", "image": "the hierophant.jpg"},
            "The Lovers": {"meaning": "การตัดสินใจครั้งสำคัญ, ความสัมพันธ์, ความสามัคคี, เสน่ห์ดึงดูด, ความรักที่ต้องเลือก", "image": "the lovers.jpg"},
            "The Chariot": {"meaning": "ความมุ่งมั่น, การควบคุมสถานการณ์, ชัยชนะที่ต้องแลกมาด้วยความพยายาม, การเดินทางไกล", "image": "the chariot.jpg"},
            "Strength": {"meaning": "ความกล้าหาญ, พลังใจที่เข้มแข็ง, การเอาชนะอุปสรรคด้วยความอ่อนโยน, การควบคุมสติ", "image": "strength.jpg"},
            "The Hermit": {"meaning": "การปลีกวิเวก, การค้นหาคำตอบในใจ, ความสงบ, การใช้สติปัญญาไตร่ตรอง, ความสันโดษ", "image": "the hermit.jpg"},
            "Wheel of Fortune": {"meaning": "โชคชะตา, การเปลี่ยนแปลงกะทันหัน, กงล้อแห่งกรรม, โอกาสใหม่ๆ, จุดเปลี่ยนของชีวิต", "image": "wheel of fortune.jpg"},
            "Justice": {"meaning": "ความยุติธรรม, ความสมดุล, กฎหมาย, คดีความ, การตัดสินใจด้วยเหตุและผล", "image": "justice.jpg"},
            "The Hanged Man": {"meaning": "การเสียสละ, การรอคอย, การมองมุมกลับ, ภาวะหยุดชะงักเพื่อทบทวนตัวเอง", "image": "the hanged man.jpg"},
            "Death": {"meaning": "การจบสิ้นเพื่อเริ่มต้นใหม่, การเปลี่ยนแปลงข้ามผ่านสภาวะเดิม, การปล่อยวางอดีต", "image": "death.jpg"},
            "Temperance": {"meaning": "การปรับตัว, การโยกย้าย, ความสมดุล, การผสมผสานสิ่งใหม่ๆ, การเดินทางต่างถิ่น", "image": "temperance.jpg"},
            "The Devil": {"meaning": "กิเลส, พันธนาการ, ความลุ่มหลง, การยึดติดกับวัตถุ, เสน่ห์ที่อันตราย", "image": "the devil.jpg"},
            "The Tower": {"meaning": "การพังทลาย, เหตุการณ์ไม่คาดฝัน, การตื่นรู้, การรื้อโครงสร้างเก่าเพื่อสร้างใหม่", "image": "the tower.jpg"},
            "The Star": {"meaning": "ความหวัง, แรงบันดาลใจ, การฟื้นฟูเยียวยา, โชคชะตาที่สดใส, ชื่อเสียงที่โดดเด่น", "image": "the star.jpg"},
            "The Moon": {"meaning": "ความกังวล, ความสับสน, อารมณ์ที่ซ่อนเร้น, ภาพลวงตา, สัญชาตญาณที่คลุมเครือ", "image": "the moon.jpg"},
            "The Sun": {"meaning": "ความสำเร็จ, ความสุขสมหวัง, พลังงานบวก, การเฉลิมฉลอง, ชัยชนะที่ชัดเจน", "image": "the sun.jpg"},
            "Judgement": {"meaning": "การตื่นรู้, ผลของการกระทำ, การประเมินผล, การปลดแอก, การได้รับโอกาสครั้งที่สอง", "image": "judgement.jpg"},
            "The World": {"meaning": "ความสมบูรณ์แบบ, การจบรอบวัฏจักรอย่างสวยงาม, ความสำเร็จระดับสูง, การเดินทางต่างประเทศ", "image": "the world.jpg"},

            # ================= MINOR ARCANA: WANDS (ไม้เท้า - การงาน/พลังงาน) =================
            "Ace of Wands": {"meaning": "โอกาสใหม่ในเรื่องงาน, แรงบันดาลใจที่พุ่งพล่าน, พลังแห่งการริเริ่มโปรเจกต์ใหม่", "image": "ace of wands.jpg"},
            "Two of Wands": {"meaning": "การวางแผนอนาคต, วิสัยทัศน์ที่กว้างไกล, การรอคอยผลลัพธ์, หุ้นส่วนทางธุรกิจ", "image": "two of wands.jpg"},
            "Three of Wands": {"meaning": "การขยายกิจการ, การเติบโต, โอกาสจากต่างประเทศ, ความสำเร็จในขั้นต้น", "image": "three of wands.jpg"},
            "Four of Wands": {"meaning": "ความมั่นคง, การเฉลิมฉลองความสำเร็จ, รากฐานที่แข็งแรง, งานแต่งงานหรือขึ้นบ้านใหม่", "image": "four of wands.jpg"},
            "Five of Wands": {"meaning": "การแข่งขัน, ความขัดแย้งเล็กๆ น้อยๆ, การถกเถียงเพื่อหาข้อสรุป, อุปสรรคที่ต้องฟันฝ่า", "image": "five of wands.jpg"},
            "Six of Wands": {"meaning": "ชัยชนะ, การได้รับการยกย่อง, ข่าวดี, ความก้าวหน้าที่ได้รับการยอมรับจากคนรอบข้าง", "image": "six of wands.jpg"},
            "Seven of Wands": {"meaning": "การต่อสู้เพื่อรักษาสิ่งที่มีอยู่, ความกล้าหาญ, การยืนหยัดต่ออุปสรรคเพียงลำพัง", "image": "seven of wands.jpg"},
            "Eight of Wands": {"meaning": "ความรวดเร็ว, ข่าวสาร, การเดินทาง, เหตุการณ์ที่กำลังพุ่งเข้ามาอย่างฉับไวและราบรื่น", "image": "eight of wands.jpg"},
            "Nine of Wands": {"meaning": "ความระแวดระวัง, การตั้งรับ, ประสบการณ์จากบาดแผลในอดีต, ความอดทนในโค้งสุดท้าย", "image": "nine of wands.jpg"},
            "Ten of Wands": {"meaning": "ภาระที่หนักอึ้ง, ความรับผิดชอบล้นมือ, การทำงานหนักจนเกินไป, ความเหนื่อยล้า", "image": "ten of wands.jpg"},
            "Page of Wands": {"meaning": "ข่าวดีเรื่องงานหรือการเรียน, ความกระตือรือร้น, การเริ่มต้นไอเดียใหม่ๆ", "image": "page of wands.jpg"},
            "Knight of Wands": {"meaning": "ความใจร้อน, พลังงานที่พุ่งทะยาน, การเดินทางกะทันหัน, ความมุ่งมั่นที่จะลุย", "image": "knight of wands.jpg"},
            "Queen of Wands": {"meaning": "ผู้หญิงเก่ง, ความมั่นใจในตัวเอง, มีเสน่ห์ดึงดูด, การบริหารจัดการที่ยอดเยี่ยม", "image": "queen of wands.jpg"},
            "King of Wands": {"meaning": "ผู้นำที่มีวิสัยทัศน์, เจ้าของกิจการ, ผู้ชายวัยกลางคนที่มีความมุ่งมั่นและประสบความสำเร็จ", "image": "king of wands.jpg"},

            # ================= MINOR ARCANA: CUPS (ถ้วย - ความรัก/อารมณ์) =================
            "Ace of Cups": {"meaning": "ความสุขทางใจ, ความรักครั้งใหม่, ความอิ่มเอมใจ, อารมณ์ที่ลึกซึ้งและบริสุทธิ์", "image": "ace of cups.jpg"},
            "Two of Cups": {"meaning": "ความรักที่สมหวัง, ความเข้าใจซึ่งกันและกัน, การแต่งงาน, หุ้นส่วนที่เข้ากันได้ดี", "image": "two of cups.jpg"},
            "Three of Cups": {"meaning": "การเฉลิมฉลอง, มิตรภาพ, งานเลี้ยง, ความสุขที่ได้แบ่งปันกับเพื่อนฝูง", "image": "three of cups.jpg"},
            "Four of Cups": {"meaning": "ความเบื่อหน่าย, ความไม่พอใจในสิ่งที่มี, การมองข้ามโอกาสใหม่ๆ ที่หยิบยื่นให้", "image": "four of cups.jpg"},
            "Five of Cups": {"meaning": "ความเศร้าโศก, การสูญเสีย, การยึดติดกับอดีตที่ผิดหวัง (โดยลืมมองสิ่งที่ยังเหลืออยู่)", "image": "five of cups.jpg"},
            "Six of Cups": {"meaning": "ความคิดถึง, ถ่านไฟเก่า, การหวนคืนของอดีต, ความทรงจำที่งดงามในวัยเด็ก", "image": "six of cups.jpg"},
            "Seven of Cups": {"meaning": "ทางเลือกที่หลากหลาย, ภาพลวงตา, ความเพ้อฝัน, การตัดสินใจที่ยากลำบากเพราะมีตัวเลือกมาก", "image": "seven of cups.jpg"},
            "Eight of Cups": {"meaning": "การเดินจากไป, การละทิ้งสิ่งที่เคยสร้างมาเพื่อค้นหาสิ่งที่ดีกว่า, ความผิดหวังลึกๆ", "image": "eight of cups.jpg"},
            "Nine of Cups": {"meaning": "ความพึงพอใจในตัวเอง, ความสมบูรณ์พูนสุข, ไพ่แห่งความสมหวัง (Wish Card), การตามใจตัวเอง", "image": "nine of cups.jpg"},
            "Ten of Cups": {"meaning": "ครอบครัวที่อบอุ่น, ความสุขสมบูรณ์ถึงขีดสุด, ความปรองดอง, ตอนจบที่แฮปปี้เอนดิ้ง", "image": "ten of cups.jpg"},
            "Page of Cups": {"meaning": "ข่าวดีเรื่องความรัก, อารมณ์อ่อนไหว, เด็กหนุ่มสาวที่โรแมนติก, การเริ่มต้นของความรู้สึกดีๆ", "image": "page of cups.jpg"},
            "Knight of Cups": {"meaning": "ชายหนุ่มโรแมนติก, ข้อเสนอเรื่องความรัก, การตามหาความฝัน, ศิลปินผู้มีอารมณ์ศิลป์", "image": "knight of cups.jpg"},
            "Queen of Cups": {"meaning": "ผู้หญิงที่มีความเมตตา, อบอุ่น, อ่อนโยน, มีสัญชาตญาณความเป็นแม่สูง, ชอบช่วยเหลือผู้อื่น", "image": "queen of cups.jpg"},
            "King of Cups": {"meaning": "ผู้ชายที่ควบคุมอารมณ์ได้ดี, มีความเมตตา, ที่ปรึกษาที่ดี, ผู้ใหญ่ที่อบอุ่นและใจเย็น", "image": "king of cups.jpg"},

            # ================= MINOR ARCANA: SWORDS (ดาบ - ความคิด/ปัญหา) =================
            "Ace of Swords": {"meaning": "ความชัดเจน, การตัดสินใจที่เด็ดขาด, การเอาชนะอุปสรรคด้วยสติปัญญา, จุดเริ่มต้นของความคิดใหม่", "image": "ace of swords.jpg"},
            "Two of Swords": {"meaning": "ความลังเลใจ, การปิดกั้นตัวเอง, การอยู่ตรงกลางระหว่างความขัดแย้ง, การประนีประนอม", "image": "two of swords.jpg"},
            "Three of Swords": {"meaning": "ความเสียใจ, ความเจ็บปวด, รักสามเส้า, การถูกหักหลัง, ความขัดแย้งที่สร้างบาดแผล", "image": "three of swords.jpg"},
            "Four of Swords": {"meaning": "การพักผ่อน, การฟื้นฟูร่างกายและจิตใจ, การหยุดนิ่งเพื่อรอเวลา, การหลีกหนีปัญหาชั่วคราว", "image": "four of swords.jpg"},
            "Five of Swords": {"meaning": "ความขัดแย้ง, ชัยชนะที่ได้ไม่คุ้มเสีย, การทะเลาะเบาะแว้ง, ทิฐิที่นำมาซึ่งความสูญเสีย", "image": "five of swords.jpg"},
            "Six of Swords": {"meaning": "การข้ามพ้นอุปสรรค, การเดินทางเพื่อหนีปัญหา, สถานการณ์ค่อยๆ ดีขึ้นอย่างช้าๆ", "image": "six of swords.jpg"},
            "Seven of Swords": {"meaning": "การเล่ห์เหลี่ยม, การทำอะไรอย่างลับๆ, การขโมย, การแก้ปัญหาด้วยวิธีพลิกแพลง", "image": "seven of swords.jpg"},
            "Eight of Swords": {"meaning": "ความรู้สึกมืดมน, การถูกจำกัดสิทธิ์, สภาวะที่หาทางออกไม่ได้ (แต่มักเป็นเพราะความคิดตัวเอง)", "image": "eight of swords.jpg"},
            "Nine of Swords": {"meaning": "ความเครียด, ฝันร้าย, ความวิตกกังวลอย่างหนัก, อาการนอนไม่หลับ, ปัญหาที่รุมเร้า", "image": "nine of swords.jpg"},
            "Ten of Swords": {"meaning": "จุดต่ำสุดของชีวิต, ความเจ็บปวดแสนสาหัส, การถูกหักหลัง, จุดจบของปัญหา", "image": "ten of swords.jpg"},
            "Page of Swords": {"meaning": "ความอยากรู้อยากเห็น, ข่าวกรอง, การเฝ้าระวัง, เด็กที่ฉลาดแต่ดื้อรั้น", "image": "page of swords.jpg"},
            "Knight of Swords": {"meaning": "ความใจร้อน, การพุ่งเข้าชนปัญหา, ความก้าวร้าว, เหตุการณ์ที่เกิดขึ้นอย่างฉับพลันและรุนแรง", "image": "knight of swords.jpg"},
            "Queen of Swords": {"meaning": "ผู้หญิงเด็ดขาด, ความตรงไปตรงมา, การใช้เหตุผลมากกว่าอารมณ์, หญิงเก่งที่พึ่งพาตัวเอง", "image": "queen of swords.jpg"},
            "King of Swords": {"meaning": "ผู้ชายที่มีอำนาจตัดสินใจ, กฎหมาย, ความยุติธรรม, การใช้เหตุผลขั้นเด็ดขาด, คนในเครื่องแบบ", "image": "king of swords.jpg"},

            # ================= MINOR ARCANA: PENTACLES (เหรียญ - การเงิน/วัตถุ) =================
            "Ace of Pentacles": {"meaning": "โชคลาภทางการเงิน, ข่าวดีเรื่องรายได้, ความมั่นคงทางวัตถุ, การเริ่มต้นธุรกิจที่จับต้องได้", "image": "ace of pentacles.jpg"},
            "Two of Pentacles": {"meaning": "การหมุนเงิน, การประคับประคองหลายสิ่งพร้อมกัน, ความยืดหยุ่นทางการเงิน, การรักษาสมดุล", "image": "two of pentacles.jpg"},
            "Three of Pentacles": {"meaning": "การทำงานเป็นทีม, การเรียนรู้, การพัฒนาทักษะวิชาชีพ, ความร่วมมือที่ก่อให้เกิดรายได้", "image": "three of pentacles.jpg"},
            "Four of Pentacles": {"meaning": "ความตระหนี่, การหวงแหนทรัพย์สิน, ความไม่ยอมเปลี่ยนแปลง, การยึดติดกับสิ่งที่ตัวเองมี", "image": "four of pentacles.jpg"},
            "Five of Pentacles": {"meaning": "ความขัดสน, ปัญหาทางการเงิน, ความรู้สึกโดดเดี่ยว, การถูกทอดทิ้ง, การสูญเสียทรัพย์", "image": "five of pentacles.jpg"},
            "Six of Pentacles": {"meaning": "การให้และการรับ, ความใจบุญ, การบริจาค, การกู้ยืมเงิน, ความสมดุลทางผลประโยชน์", "image": "six of pentacles.jpg"},
            "Seven of Pentacles": {"meaning": "การรอคอยผลกำไร, การประเมินผลงาน, ความอดทนเพื่อผลลัพธ์ในระยะยาว, การลงทุน", "image": "seven of pentacles.jpg"},
            "Eight of Pentacles": {"meaning": "ความอุตสาหะ, การทำงานหนัก, ความเชี่ยวชาญเฉพาะด้าน, การใส่ใจในรายละเอียด", "image": "eight of pentacles.jpg"},
            "Nine of Pentacles": {"meaning": "ความมั่งคั่งด้วยตัวเอง, ความสำเร็จส่วนตัว, อิสระทางการเงิน, ความหรูหราสุขสบาย", "image": "nine of pentacles.jpg"},
            "Ten of Pentacles": {"meaning": "ความมั่งคั่งของครอบครัว, มรดก, ความสำเร็จที่ส่งต่อถึงลูกหลาน, ความมั่นคงระยะยาว", "image": "ten of pentacles.jpg"},
            "Page of Pentacles": {"meaning": "ข่าวดีเรื่องเงิน, เด็กที่ตั้งใจเรียนรู้, การเริ่มต้นโปรเจกต์ที่สร้างรายได้", "image": "page of pentacles.jpg"},
            "Knight of Pentacles": {"meaning": "ความค่อยเป็นค่อยไป, ความขยันขันแข็ง, การทำงานที่น่าเบื่อแต่มั่นคง, คนที่ไว้ใจได้", "image": "knight of pentacles.jpg"},
            "Queen of Pentacles": {"meaning": "ผู้หญิงที่มั่งคั่ง, มีความสุขกับความสมบูรณ์ทางวัตถุ, นักธุรกิจหญิง, ความใจดีมีเมตตา", "image": "queen of pentacles.jpg"},
            "King of Pentacles": {"meaning": "ผู้ชายที่ร่ำรวย, ประสบความสำเร็จในธุรกิจ, เจ้าของกิจการ, ผู้ที่มั่นคงและพึ่งพาได้", "image": "king of pentacles.jpg"}
        }

    def get_all_card_names(self):
        return list(self.cards.keys())

    def get_card_info(self, card_name):
        return self.cards.get(card_name, {"meaning": "ไม่พบข้อมูล", "image": ""})

    def draw_card(self):
        card_name = random.choice(list(self.cards.keys()))
        card_data = self.cards[card_name]
        return card_name, card_data["meaning"], card_data["image"]
