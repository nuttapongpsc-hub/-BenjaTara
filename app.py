import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine

def render_thai_astrology_chart(thai_data, title="ดวงชะตา"):
    """สร้างตารางดวงอีแปะ 12 ราศี (ตารางสี่เหลี่ยมแบบไทย)"""
    planet_symbols = {
        "อาทิตย์ (๑)": "๑", "จันทร์ (๒)": "๒", "อังคาร (๓)": "๓",
        "พุธ (๔)": "๔", "พฤหัสบดี (๕)": "๕", "ศุกร์ (๖)": "๖",
        "เสาร์ (๗)": "๗", "ราหู (๘)": "๘", "มฤตยู (๐)": "๐"
    }
    zodiac_names = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์", "ตุลย์", "พิจิก", "ธนู", "มังกร", "กุมภ์", "มีน"]
    
    boxes = {i: [] for i in range(12)}
    boxes[thai_data['lagna_index']].append("<span style='color:red; font-weight:bold;'>ล</span>")
    
    for p_name, p_data in thai_data['planets'].items():
        sign_index = zodiac_names.index(p_data['sign'])
        if "เกษตร" in p_data['dignity'] or "อุจจ์" in p_data['dignity']:
            sym = f"<span style='color:green; font-weight:bold;'>{planet_symbols[p_name]}</span>"
        elif "นิจ" in p_data['dignity'] or "ประ" in p_data['dignity']:
            sym = f"<span style='color:orange;'>{planet_symbols[p_name]}</span>"
        else:
            sym = f"<span style='color:black;'>{planet_symbols[p_name]}</span>"
        boxes[sign_index].append(sym)

    grid_layout = [
        [11, 0, 1, 2],
        [10, -1, -1, 3],
        [9, -1, -1, 4],
        [8, 7, 6, 5]
    ]

    html = f"<div style='text-align:center; margin-bottom: 20px;'><h4>{title}</h4>"
    html += "<table style='border-collapse: collapse; margin: 0 auto; background-color: white;'>"
    
    for row in grid_layout:
        html += "<tr>"
        for sign_idx in row:
            if sign_idx == -1:
                html += "<td style='border: none; width: 60px; height: 60px;'></td>"
            else:
                stars = " ".join(boxes[sign_idx])
                sign_name = zodiac_names[sign_idx]
                
                # เขียน HTML แบบต่อสตริงเพื่อป้องกัน Streamlit มองเป็น Code Block
                html += f"<td style='border: 1px solid #ccc; width: 60px; height: 60px; text-align: center; vertical-align: top; padding: 5px; position: relative;'>"
                html += f"<div style='font-size: 14px;'>{stars}</div>"
                html += f"<div style='position: absolute; bottom: 2px; right: 2px; font-size: 8px; color: #aaa;'>{sign_name}</div>"
                html += f"</td>"
                
        html += "</tr>"
    html += "</table></div>"
    return html

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
        
        min_date = datetime(1900, 1, 1)
        max_date = datetime.now() 
        birth_date = st.date_input("วันเกิด (ค.ศ.)", value=datetime(1990, 1, 1), min_value=min_date, max_value=max_date)
        
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
            
            bazi_chart = bazi.get_bazi_chart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
            day_master, scores = bazi.calculate_strength(bazi_chart)
            bazi_result = bazi.find_useful_god(day_master, scores)
            
            birth_dt = datetime.combine(birth_date, birth_time)
            thai_natal = thai.calculate_positions(birth_dt, lat, lon)
            
            now = datetime.now()
            thai_transit = thai.calculate_positions(now, lat, lon, ref_lagna_index=thai_natal['lagna_index'])
            
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
                c3.metric("ลัคนาราศี (ไทย)", report['lagna'])
                
                st.markdown(f"""
                <div class="prediction-card">
                    <h4>🌟 ธาตุที่ส่งเสริมดวงชะตา (Useful Gods)</h4>
                    <p style="font-size: 1.2rem; color: #2E7D32;"><b>{', '.join(bazi_result['useful_gods'])}</b></p>
                </div>
                """, unsafe_allow_html=True)
                st.metric("คะแนนความราบรื่นปัจจุบัน", f"{report['score']}%")

            st.markdown("---")
            st.markdown("#### 🀄 โครงสร้าง 4 เสาชะตา (Bazi Chart)")
            cols = st.columns(4)
            pillars_name = ["เวลา (Hour)", "วัน (Day)", "เดือน (Month)", "ปี (Year)"]
            keys = [("hour_stem", "hour_branch"), ("day_stem", "day_branch"), ("month_stem", "month_branch"), ("year_stem", "year_branch")]
            
            for i, col in enumerate(cols):
                with col:
                    # แก้ไขการต่อสตริง HTML ของ Bazi Chart ให้ปลอดภัยจากบั๊ก Markdown
                    html_bazi = (
                        "<div style='text-align:center; background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:10px;'>"
                        f"<p style='margin:0; font-size:14px; color:#555;'><b>{pillars_name[i]}</b></p>"
                        "<hr style='margin:10px 0;'>"
                        f"<p style='margin:0; font-size:12px; color:#888;'>{bazi_result['ten_gods'][keys[i][0]]}</p>"
                        f"<h2 style='margin:5px 0; color:#1f77b4;'>{bazi_result['four_pillars'][keys[i][0]]}</h2>"
                        f"<h2 style='margin:5px 0; color:#d62728;'>{bazi_result['four_pillars'][keys[i][1]]}</h2>"
                        f"<p style='margin:0; font-size:12px; color:#888;'>{bazi_result['ten_gods'][keys[i][1]]}</p>"
                        "</div>"
                    )
                    st.markdown(html_bazi, unsafe_allow_html=True)

            st.markdown("---")
            col_thai1, col_thai2 = st.columns(2)
            with col_thai1:
                thai_natal_html = render_thai_astrology_chart(thai_natal, "ดวงกำเนิด (ราศีจักร)")
                st.markdown(thai_natal_html, unsafe_allow_html=True)
            with col_thai2:
                thai_transit_html = render_thai_astrology_chart(thai_transit, "ดวงจร (ปัจจุบัน)")
                st.markdown(thai_transit_html, unsafe_allow_html=True)

            st.markdown("---")
            st.header("🔮 คำทำนายและการพยากรณ์สถานการณ์ปัจจุบัน")
            st.write(f"**ภาพรวม:** {report['prediction']}")
            
            tab1, tab2, tab3 = st.tabs(["💼 การงาน", "💰 การเงิน", "❤️ ความรัก"])
            with tab1: st.write(report['details'].get('work', ''))
            with tab2: st.write(report['details'].get('money', ''))
            with tab3: st.write(report['details'].get('love', ''))

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
st.caption("© 2026 BenjaTara Project - ผสานปฏิทินโหราศาสตร์และ 12 ภพขั้นสูง")
