import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine

# ตั้งค่าหน้าเว็บให้กว้างขึ้น
st.set_page_config(page_title="BenjaTara - เบญจทารา", page_icon="🔮", layout="wide")

st.title("🔮 เบญจทารา (BenjaTara)")
st.subheader("ระบบพยากรณ์ความสอดคล้องของธาตุและดวงดาว (ฉบับสมบูรณ์)")

with st.form("astrology_form"):
    st.write("กรุณากรอกข้อมูลวันเกิดของคุณเพื่อผูกดวงกำเนิด")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("ชื่อของคุณ", "ผู้ใช้งาน")
        birth_date = st.date_input("วัน/เดือน/ปีเกิด (สากล)")
        
    with col2:
        birth_time = st.time_input("เวลาเกิด (ชม:นาที)")
        lat = st.number_input("ละติจูด (Latitude)", value=13.7563, format="%.4f")
        lon = st.number_input("ลองจิจูด (Longitude)", value=100.5018, format="%.4f")
        
    submit_button = st.form_submit_button(label="✨ วิเคราะห์ดวงชะตาและพลังงานวันนี้")

if submit_button:
    with st.spinner("กำลังประมวลผลข้อมูลระดับลึก..."):
        try:
            # ==========================================
            # แกนประมวลผลหลัก
            # ==========================================
            bazi = BaziAnalyzer()
            bazi_chart = bazi.get_bazi_chart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
            day_master, scores = bazi.calculate_strength(bazi_chart)
            bazi_result = bazi.find_useful_god(day_master, scores)
            
            birth_dt = datetime.combine(birth_date, birth_time)
            thai = ThaiAstrologyEngine()
            thai_result = thai.calculate_positions(birth_dt, lat, lon)
            
            hybrid = HybridSynthesisEngine()
            report_natal = hybrid.verify_and_predict(bazi_result, thai_result) # ดวงกำเนิด
            
            # --- คำนวณดวงจร (Transit) สำหรับวันนี้ ---
            today_dt = datetime.now()
            today_thai_result = thai.calculate_positions(today_dt, lat, lon)
            report_transit = hybrid.verify_and_predict(bazi_result, today_thai_result) # ดวงจรวันนี้

            # ==========================================
            # ส่วนแสดงผลบนหน้าเว็บ (UI)
            # ==========================================
            st.success("✅ ประมวลผลเสร็จสมบูรณ์!")
            st.markdown("---")
            st.header(f"ดวงชะตาของ: คุณ{name}")
            
            # แบ่งหน้าจอเป็น 2 ฝั่ง: ซ้าย=ข้อมูลปาจือ/กราฟ, ขวา=คำทำนาย
            col_left, col_right = st.columns([1, 1.2])
            
            with col_left:
                st.subheader("☯️ สัดส่วนพลังงานธาตุ (Bazi)")
                c1, c2 = st.columns(2)
                c1.metric("ดิถี (ธาตุประจำตัว)", bazi_result['day_master'])
                c2.metric("รูปแบบดวง", bazi_result['chart_type'])
                st.info(f"**ธาตุให้คุณ:** {', '.join(bazi_result['useful_gods'])}")
                
                # --- วาดกราฟ Radar Chart 5 ธาตุ ---
                elements = ['ไม้', 'ไฟ', 'ดิน', 'ทอง', 'น้ำ']
                # เรียงคะแนนตาม elements
                val_scores = [bazi_result['scores'].get(el, 0) for el in elements]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=val_scores + [val_scores[0]], # ปิดวงกราฟ
                    theta=elements + [elements[0]],
                    fill='toself',
                    line_color='#636EFA',
                    name='พลังงานธาตุ'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(val_scores)+10])),
                    showlegend=False,
                    margin=dict(l=40, r=40, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                # ดวงกำเนิด
                st.subheader("🌟 โครงสร้างดวงกำเนิด (Natal Chart)")
                st.write(f"**สรุปพื้นดวง:** {report_natal['prediction']}")
                
                with st.expander("ดูรายละเอียดคำแนะนำพื้นดวง", expanded=False):
                    for insight in report_natal['actionable_insights']:
                        st.success(insight)
                    for warning in report_natal['warnings']:
                        st.warning(warning)
                        
                st.markdown("---")
                
                # ดวงจร (สถานการณ์ปัจจุบัน)
                st.subheader(f"⏳ พลังงานดวงดาวจร ณ ปัจจุบัน")
                st.caption(f"อัปเดตข้อมูล ณ วันที่: {today_dt.strftime('%d/%m/%Y')}")
                
                st.write(f"**แนวโน้มสถานการณ์ช่วงนี้:** {report_transit['prediction']}")
                
                st.write("**คำแนะนำสำหรับการใช้ชีวิตในช่วงเวลานี้:**")
                if not report_transit['actionable_insights'] and not report_transit['warnings']:
                    st.write("- พลังงานดวงดาวอยู่ในสภาวะเป็นกลาง ดำเนินชีวิตได้ตามปกติ")
                else:
                    for insight in report_transit['actionable_insights']:
                        st.success(f"**โอกาส:** {insight}")
                    for warning in report_transit['warnings']:
                        st.warning(f"**ระวัง:** {warning}")
                    
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการคำนวณ: {e}")