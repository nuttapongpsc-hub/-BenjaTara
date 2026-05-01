import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine

st.set_page_config(page_title="BenjaTara - เบญจทารา", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .prediction-card {background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #636EFA; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 เบญจทารา (BenjaTara)")
st.subheader("ระบบพยากรณ์และสังเคราะห์พลังงานธาตุผสมผสานโหราศาสตร์ไทย")
st.markdown("---")

with st.sidebar:
    st.header("📍 ข้อมูลเจ้าชะตา")
    with st.form("user_data_form"):
        name = st.text_input("ชื่อ-นามสกุล", "คุณผู้ใช้งาน")
        
        # --- แก้ไขปฏิทินให้ครอบคลุมถึงปีปัจจุบัน ---
        min_date = datetime(1900, 1, 1)
        max_date = datetime.now() 
        birth_date = st.date_input("วันเกิด (ค.ศ.)", value=datetime(1990, 1, 1), min_value=min_date, max_value=max_date)
        # -------------------------------------
        
        birth_time = st.time_input("เวลาเกิด", value=datetime.strptime("12:00", "%H:%M").time())
        st.write("---")
        st.caption("พิกัดสถานที่เกิด (Default: กรุงเทพฯ)")
        lat = st.number_input("Latitude", value=13.7563, format="%.4f")
        lon = st.number_input("Longitude", value=100.5018, format="%.4f")
        submit_btn = st.form_submit_button("✨ วิเคราะห์ดวงชะตาขั้นสูง")

if submit_btn:
    with st.spinner("🧠 ระบบกำลังคำนวณลัคนาและสังเคราะห์ข้อมูล 12 ภพ..."):
        try:
            bazi = BaziAnalyzer()
            thai = ThaiAstrologyEngine()
            hybrid = HybridSynthesisEngine()
            
            # 1. วิเคราะห์ปาจือ
            bazi_chart = bazi.get_bazi_chart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
            day_master, scores = bazi.calculate_strength(bazi_chart)
            bazi_result = bazi.find_useful_god(day_master, scores)
            
            # 2. ผูกดวงกำเนิดโหราศาสตร์ไทย (หาลัคนา)
            birth_dt = datetime.combine(birth_date, birth_time)
            thai_natal = thai.calculate_positions(birth_dt, lat, lon)
            
            # 3. วิเคราะห์ดวงจร (Transit) โดยเทียบกับลัคนาเกิด
            now = datetime.now()
            thai_transit = thai.calculate_positions(now, lat, lon, ref_lagna_index=thai_natal['lagna_index'])
            
            # 4. สังเคราะห์คำทำนาย
            report = hybrid.verify_and_predict(bazi_result, thai_transit)
            
            st.header(f"📊 ผลการวิเคราะห์ดวงชะตา: คุณ{name}")
            col_graph, col_summary = st.columns([1, 1.2])
            
            with col_graph:
                st.subheader("☯️ สมดุลพลังงาน 5 ธาตุ")
                elements = ['ไม้', 'ไฟ', 'ดิน', 'ทอง', 'น้ำ']
                val_scores = [scores.get(el, 0) for el in elements]
                fig = go.Figure(data=go.Scatterpolar(r=val_scores + [val_scores[0]], theta=elements + [elements[0]], fill='toself', line=dict(color='#636EFA', width=2)))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(val_scores)+15])), showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col_summary:
                st.subheader("💡 อัตลักษณ์ทางพลังงาน")
                c1, c2, c3 = st.columns(3)
                c1.metric("ดิถี (ธาตุ)", day_master)
                c2.metric("สถานะดิถี", bazi_result['chart_type'])
                # แสดงผลลัคนาไทยที่เพิ่งคำนวณได้
                c3.metric("ลัคนาราศี (ไทย)", report['lagna'])
                
                st.markdown(f"""
                <div class="prediction-card">
                    <h4>🌟 ธาตุที่ส่งเสริมดวงชะตา (Useful Gods)</h4>
                    <p style="font-size: 1.2rem; color: #2E7D32;"><b>{', '.join(bazi_result['useful_gods'])}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("คะแนนความราบรื่นปัจจุบัน", f"{report['score']}%")

            st.markdown("---")
            st.header("🔮 คำทำนายและการพยากรณ์สถานการณ์ปัจจุบัน")
            st.write(f"**ภาพรวม:** {report['prediction']}")
            
            tab1, tab2, tab3 = st.tabs(["💼 การงาน", "💰 การเงิน", "❤️ ความรัก"])
            with tab1: st.info(report['details'].get('work', ''))
            with tab2: st.success(report['details'].get('money', ''))
            with tab3: st.warning(report['details'].get('love', ''))

            st.markdown("---")
            col_inc, col_war = st.columns(2)
            with col_inc:
                st.subheader("✅ โอกาสที่เข้ามา (ดวงจรเข้าภพ)")
                if report['actionable_insights']:
                    for item in report['actionable_insights']: st.write(f"🟢 {item}")
                else: st.write("พลังงานเป็นกลาง รักษาระดับเดิมไว้")

            with col_war:
                st.subheader("⚠️ อุปสรรค/ภพเสียที่ต้องระวัง")
                if report['warnings']:
                    for item in report['warnings']: st.write(f"🟠 {item}")
                else: st.write("ไม่พบเกณฑ์อันตรายที่รุนแรง")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

st.markdown("---")
st.caption("© 2026 BenjaTara Project - ผสานปฏิทินโหราศาสตร์และ 12 ภพ")
