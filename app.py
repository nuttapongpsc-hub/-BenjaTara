import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

# ดึง Engine ต่างๆ ของเรามาใช้งาน
from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine

# 1. ตั้งค่าหน้าเว็บให้ดูทันสมัยและกว้างขึ้น
st.set_page_config(
    page_title="BenjaTara - เบญจทารา", 
    page_icon="🔮", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ส่วนของ CSS เพื่อปรับแต่ง UI ให้สวยงามขึ้น
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .prediction-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #636EFA;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัวของโปรแกรม ---
st.title("🔮 เบญจทารา (BenjaTara)")
st.subheader("ระบบพยากรณ์และสังเคราะห์พลังงานธาตุผสมผสานโหราศาสตร์ไทย")
st.markdown("---")

# --- ส่วนรับข้อมูล (Sidebar หรือ Form) ---
with st.sidebar:
    st.header("📍 ข้อมูลเจ้าชะตา")
    with st.form("user_data_form"):
        name = st.text_input("ชื่อ-นามสกุล", "คุณผู้ใช้งาน")
        birth_date = st.date_input("วันเกิด (ค.ศ.)", value=datetime(1990, 1, 1))
        birth_time = st.time_input("เวลาเกิด", value=datetime.strptime("12:00", "%H:%M").time())
        
        st.write("---")
        st.caption("พิกัดสถานที่เกิด (Default: กรุงเทพฯ)")
        lat = st.number_input("Latitude", value=13.7563, format="%.4f")
        lon = st.number_input("Longitude", value=100.5018, format="%.4f")
        
        submit_btn = st.form_submit_button("✨ วิเคราะห์ดวงชะตาขั้นสูง")

# --- ส่วนการประมวลผลและแสดงผล ---
if submit_btn:
    with st.spinner("🧠 ระบบกำลังสังเคราะห์ความสัมพันธ์ของธาตุและดวงดาว..."):
        try:
            # 1. ประมวลผล Backend
            bazi = BaziAnalyzer()
            thai = ThaiAstrologyEngine()
            hybrid = HybridSynthesisEngine()
            
            # วิเคราะห์ปาจือ
            bazi_chart = bazi.get_bazi_chart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
            day_master, scores = bazi.calculate_strength(bazi_chart)
            bazi_result = bazi.find_useful_god(day_master, scores)
            
            # วิเคราะห์ดวงจร (Transit) ณ ปัจจุบัน
            now = datetime.now()
            thai_transit = thai.calculate_positions(now, lat, lon)
            
            # สังเคราะห์คำทำนาย (Hybrid)
            # เราส่งคะแนน (scores) เข้าไปด้วยเพื่อให้ HybridEngine วิเคราะห์ได้ยืดหยุ่นขึ้น
            report = hybrid.verify_and_predict(bazi_result, thai_transit)
            
            # --------------------------------------------------
            # แสดงผลส่วนที่ 1: ข้อมูลพื้นฐานและกราฟพลังงาน
            # --------------------------------------------------
            st.header(f"📊 ผลการวิเคราะห์ดวงชะตา: คุณ{name}")
            
            col_graph, col_summary = st.columns([1, 1])
            
            with col_graph:
                st.subheader("☯️ สมดุลพลังงาน 5 ธาตุ")
                elements = ['ไม้', 'ไฟ', 'ดิน', 'ทอง', 'น้ำ']
                val_scores = [scores.get(el, 0) for el in elements]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=val_scores + [val_scores[0]],
                    theta=elements + [elements[0]],
                    fill='toself',
                    fillcolor='rgba(99, 110, 250, 0.3)',
                    line=dict(color='#636EFA', width=2),
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(val_scores)+15])),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_summary:
                st.subheader("💡 อัตลักษณ์ทางพลังงาน")
                c1, c2 = st.columns(2)
                c1.metric("ธาตุประจำตัว (ดิถี)", day_master)
                c2.metric("สถานะดิถี", bazi_result['chart_type'])
                
                st.markdown(f"""
                <div class="prediction-card">
                    <h4>🌟 ธาตุที่ส่งเสริมดวงชะตา (Useful Gods)</h4>
                    <p style="font-size: 1.2rem; color: #2E7D32;"><b>{', '.join(bazi_result['useful_gods'])}</b></p>
                    <p>ระบบแนะนำให้เน้นการใช้สีสัน สถานที่ หรือกิจกรรมที่เกี่ยวข้องกับธาตุเหล่านี้เพื่อกระตุ้นโชคลาภ</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("คะแนนความราบรื่นปัจจุบัน", f"{report['score']}%")

            # --------------------------------------------------
            # แสดงผลส่วนที่ 2: คำทำนายเจาะลึกรายด้าน (Dynamic)
            # --------------------------------------------------
            st.markdown("---")
            st.header("🔮 คำทำนายและการพยากรณ์สถานการณ์ปัจจุบัน")
            st.write(f"**ภาพรวม:** {report['prediction']}")
            
            # แบ่งหมวดหมู่การวิเคราะห์
            tab1, tab2, tab3 = st.tabs(["💼 การงานและธุรกิจ", "💰 การเงินและโชคลาภ", "❤️ ความรักและความสัมพันธ์"])
            
            with tab1:
                st.info(report['details'].get('work', 'ข้อมูลอยู่ระหว่างการประมวลผล'))
            with tab2:
                st.success(report['details'].get('money', 'ข้อมูลอยู่ระหว่างการประมวลผล'))
            with tab3:
                st.warning(report['details'].get('love', 'ข้อมูลอยู่ระหว่างการประมวลผล'))

            # --------------------------------------------------
            # แสดงผลส่วนที่ 3: คำแนะนำและข้อควรระวัง
            # --------------------------------------------------
            st.markdown("---")
            col_inc, col_war = st.columns(2)
            
            with col_inc:
                st.subheader("✅ คำแนะนำเสริมดวง")
                if report['actionable_insights']:
                    for item in report['actionable_insights']:
                        st.write(f"🟢 {item}")
                else:
                    st.write("ช่วงนี้พลังงานเป็นกลาง แนะนำให้รักษามาตรฐานการทำงานเดิมไว้")

            with col_war:
                st.subheader("⚠️ ข้อควรระวัง")
                if report['warnings']:
                    for item in report['warnings']:
                        st.write(f"🟠 {item}")
                else:
                    st.write("ยังไม่พบเกณฑ์อันตรายหรืออุปสรรคที่รุนแรงในระยะนี้")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในระบบสังเคราะห์ข้อมูล: {e}")
            st.info("กรุณาตรวจสอบการตั้งค่าไฟล์ Engine ต่างๆ หรือลองรีเฟรชหน้าเว็บอีกครั้ง")

# ส่วนท้าย
st.markdown("---")
st.caption("© 2026 BenjaTara Project - พัฒนาโดยนักวิจัยอิสระเพื่อการศึกษาโหราศาสตร์ประยุกต์")
