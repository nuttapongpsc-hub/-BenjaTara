import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine
from TarotEngine import TarotEngine

def render_square_chart(thai_data, title="ดวงชะตา"):
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

    grid_layout = [[11, 0, 1, 2], [10, -1, -1, 3], [9, -1, -1, 4], [8, 7, 6, 5]]

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
                html += f"<td style='border: 1px solid #ccc; width: 60px; height: 60px; text-align: center; vertical-align: top; padding: 5px; position: relative;'>"
                html += f"<div style='font-size: 14px;'>{stars}</div>"
                html += f"<div style='position: absolute; bottom: 2px; right: 2px; font-size: 8px; color: #aaa;'>{sign_name}</div>"
                html += f"</td>"
        html += "</tr>"
    html += "</table></div>"
    return html

def render_circular_chart(thai_data, title="ดวงชะตา"):
    planet_symbols = {
        "อาทิตย์ (๑)": "๑", "จันทร์ (๒)": "๒", "อังคาร (๓)": "๓",
        "พุธ (๔)": "๔", "พฤหัสบดี (๕)": "๕", "ศุกร์ (๖)": "๖",
        "เสาร์ (๗)": "๗", "ราหู (๘)": "๘", "มฤตยู (๐)": "๐"
    }
    zodiac_names = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์", "ตุลย์", "พิจิก", "ธนู", "มังกร", "กุมภ์", "มีน"]
    
    boxes = {i: [] for i in range(12)}
    boxes[thai_data['lagna_index']].append("<span style='color:red;'><b>ล</b></span>")
    
    for p_name, p_data in thai_data['planets'].items():
        sign_index = zodiac_names.index(p_data['sign'])
        if "เกษตร" in p_data['dignity'] or "อุจจ์" in p_data['dignity']:
            sym = f"<span style='color:green;'><b>{planet_symbols[p_name]}</b></span>"
        elif "นิจ" in p_data['dignity'] or "ประ" in p_data['dignity']:
            sym = f"<span style='color:orange;'><b>{planet_symbols[p_name]}</b></span>"
        else:
            sym = f"<span style='color:black;'><b>{planet_symbols[p_name]}</b></span>"
        boxes[sign_index].append(sym)

    def format_stars(star_list):
        if not star_list: return ""
        chunks = [" ".join(star_list[i:i+3]) for i in range(0, len(star_list), 3)]
        return "<br>".join(chunks)

    stars_texts = [format_stars(boxes[i]) for i in range(12)]
    angles = [15 + (i * 30) for i in range(12)]
    
    fig = go.Figure()
    fig.add_trace(go.Barpolar(r=[1]*12, theta=angles, width=[30]*12, marker_color='rgba(240, 242, 246, 0.5)', marker_line_color='lightgray', marker_line_width=1, hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=[1.15]*12, theta=angles, mode='text', text=zodiac_names, textfont=dict(size=12, color='gray'), hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=[0.65]*12, theta=angles, mode='text', text=stars_texts, textfont=dict(size=16), hoverinfo='none'))
    fig.update_layout(title=dict(text=title, x=0.5, font=dict(size=16)), polar=dict(radialaxis=dict(visible=False, range=[0, 1.3]), angularaxis=dict(visible=False, direction="counterclockwise", rotation=90)), showlegend=False, margin=dict(t=40, b=10, l=10, r=10), height=350, dragmode=False)
    return fig

# --- ตั้งค่าหน้าเว็บหลัก ---
st.set_page_config(page_title="BenjaTara - เบญจทารา", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .prediction-card {background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #636EFA; margin-bottom: 20px;}
    .tarot-card-box {background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 100%;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 เบญจทารา (BenjaTara)")
st.subheader("ระบบพยากรณ์และสังเคราะห์พลังงานธาตุผสมผสานโหราศาสตร์ไทยและไพ่ยิปซี")
st.markdown("---")

if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'tarot_result' not in st.session_state:
    st.session_state.tarot_result = None

tarot_engine = TarotEngine()

with st.sidebar:
    st.header("📍 ข้อมูลเจ้าชะตา")
    with st.form("user_data_form"):
        name = st.text_input("ชื่อ-นามสกุล", "คุณผู้ใช้งาน")
        min_date = datetime(1900, 1, 1)
        max_date = datetime.now() 
        birth_date = st.date_input("วันเกิด (ค.ศ.)", value=datetime(1990, 1, 1), min_value=min_date, max_value=max_date)
        birth_time = st.time_input("เวลาเกิด", value=datetime.strptime("12:00", "%H:%M").time())
        st.caption("พิกัดสถานที่เกิด (Default: กรุงเทพฯ)")
        lat = st.number_input("Latitude", value=13.7563, format="%.4f")
        lon = st.number_input("Longitude", value=100.5018, format="%.4f")
        
        st.write("---")
        st.markdown("#### 🃏 เลือกไพ่ยิปซีประจำตัว")
        st.caption("เลือกไพ่ที่ดึงดูดใจคุณที่สุด 3 ใบ เพื่อประกอบการพยากรณ์")
        all_cards = tarot_engine.get_all_card_names()
        # ใช้ multiselect ล็อกโควต้าให้เลือกได้สูงสุด 3 ใบ
        selected_tarot_cards = st.multiselect("เลือกไพ่ 3 ใบ", options=all_cards, max_selections=3)
        
        submit_btn = st.form_submit_button("✨ วิเคราะห์ดวงชะตาขั้นสูง")

if submit_btn:
    # ดักจับ Error ถ้าผู้ใช้เลือกไพ่ไม่ครบ 3 ใบ
    if len(selected_tarot_cards) != 3:
        st.sidebar.error("⚠️ กรุณาเลือกไพ่ยิปซีให้ครบ 3 ใบก่อนกดวิเคราะห์ครับ")
    else:
        with st.spinner("🧠 ระบบกำลังคำนวณลัคนาและสังเคราะห์ข้อมูลมิติซ้อน..."):
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
                
                st.session_state.analysis_done = True
                st.session_state.name = name
                st.session_state.scores = scores
                st.session_state.day_master = day_master
                st.session_state.bazi_result = bazi_result
                st.session_state.report = report
                st.session_state.thai_natal = thai_natal
                st.session_state.thai_transit = thai_transit
                st.session_state.selected_tarot_cards = selected_tarot_cards # เก็บไพ่ 3 ใบที่เลือก
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดในการคำนวณ: {e}")

# --- ส่วนแสดงผลดวงชะตา (ดึงจาก Session State) ---
if st.session_state.analysis_done:
    st.header(f"📊 ผลการวิเคราะห์ดวงชะตา: คุณ{st.session_state.name}")
    
    # ---------------------------------------------------------
    # โซนใหม่: แสดงไพ่ 3 ใบที่เลือกมาจาก Sidebar
    # ---------------------------------------------------------
    st.markdown("#### 🃏 ไพ่ยิปซีประจำตัว (ที่คุณเลือก 3 ใบ)")
    st.caption("หน้าไพ่สะท้อนถึงสภาวะ อดีต - ปัจจุบัน - อนาคต หรือภาพรวมของสถานการณ์ที่คุณกำลังเผชิญ")
    
    t_cols = st.columns(3)
    card_labels = ["ใบที่ 1 (อดีต/พื้นฐาน)", "ใบที่ 2 (ปัจจุบัน/อุปสรรค)", "ใบที่ 3 (อนาคต/บทสรุป)"]
    
    for idx, card_name in enumerate(st.session_state.selected_tarot_cards):
        card_info = tarot_engine.get_card_info(card_name)
        with t_cols[idx]:
            st.markdown(f"<div class='tarot-card-box'>", unsafe_allow_html=True)
            st.image(card_info["image"], use_container_width=True)
            st.markdown(f"<h5 style='color:#636EFA; margin-top:10px;'>{card_name}</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.85rem; color:#888; margin-bottom:5px;'>{card_labels[idx]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; color:#444;'>{card_info['meaning']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("---")
    # ---------------------------------------------------------

    col_graph, col_summary = st.columns([1, 1.2])
    
    with col_graph:
        st.subheader("☯️ สมดุลพลังงาน 5 ธาตุ")
        elements = ['ไม้', 'ไฟ', 'ดิน', 'ทอง', 'น้ำ']
        val_scores = [st.session_state.scores.get(el, 0) for el in elements]
        fig = go.Figure(data=go.Scatterpolar(r=val_scores + [val_scores[0]], theta=elements + [elements[0]], fill='toself', line=dict(color='#636EFA', width=2)))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(val_scores)+15])), showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_summary:
        st.subheader("💡 อัตลักษณ์ทางพลังงาน")
        c1, c2, c3 = st.columns(3)
        c1.metric("ดิถี (ธาตุ)", st.session_state.day_master)
        c2.metric("สถานะดิถี", st.session_state.bazi_result['chart_type'])
        c3.metric("ลัคนาราศี (ไทย)", st.session_state.report['lagna'])
        
        st.markdown(f"""
        <div class="prediction-card">
            <h4>🌟 ธาตุที่ส่งเสริมดวงชะตา (Useful Gods)</h4>
            <p style="font-size: 1.2rem; color: #2E7D32;"><b>{', '.join(st.session_state.bazi_result['useful_gods'])}</b></p>
            <p style="font-size: 1rem; color: #555;">ไพ่ทาโรต์ประจำลัคนา: <b>{st.session_state.report.get('tarot_card', '-')}</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.metric("คะแนนความราบรื่นปัจจุบัน", f"{st.session_state.report['score']}%")

    st.markdown("---")
    st.markdown("#### 🀄 โครงสร้าง 4 เสาชะตา (Bazi Chart)")
    cols = st.columns(4)
    pillars_name = ["เวลา (Hour)", "วัน (Day)", "เดือน (Month)", "ปี (Year)"]
    keys = [("hour_stem", "hour_branch"), ("day_stem", "day_branch"), ("month_stem", "month_branch"), ("year_stem", "year_branch")]
    
    for i, col in enumerate(cols):
        with col:
            html_bazi = (
                "<div style='text-align:center; background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:10px;'>"
                f"<p style='margin:0; font-size:14px; color:#555;'><b>{pillars_name[i]}</b></p><hr style='margin:10px 0;'>"
                f"<p style='margin:0; font-size:12px; color:#888;'>{st.session_state.bazi_result['ten_gods'][keys[i][0]]}</p>"
                f"<h2 style='margin:5px 0; color:#1f77b4;'>{st.session_state.bazi_result['four_pillars'][keys[i][0]]}</h2>"
                f"<h2 style='margin:5px 0; color:#d62728;'>{st.session_state.bazi_result['four_pillars'][keys[i][1]]}</h2>"
                f"<p style='margin:0; font-size:12px; color:#888;'>{st.session_state.bazi_result['ten_gods'][keys[i][1]]}</p>"
                "</div>"
            )
            st.markdown(html_bazi, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🌌 โครงสร้างดวงดาวโหราศาสตร์ไทย")
    tab_sq, tab_cir = st.tabs(["🔲 ตารางดวงอีแปะ (สี่เหลี่ยม)", "⭕ ตารางดวงราศีจักร (วงกลม)"])
    
    with tab_sq:
        col_thai1, col_thai2 = st.columns(2)
        with col_thai1:
            st.markdown(render_square_chart(st.session_state.thai_natal, "ดวงกำเนิด (ราศีจักร)"), unsafe_allow_html=True)
        with col_thai2:
            st.markdown(render_square_chart(st.session_state.thai_transit, "ดวงจร (ปัจจุบัน)"), unsafe_allow_html=True)
            
    with tab_cir:
        col_cir1, col_cir2 = st.columns(2)
        with col_cir1:
            st.plotly_chart(render_circular_chart(st.session_state.thai_natal, "ดวงกำเนิด (ราศีจักร)"), use_container_width=True)
        with col_cir2:
            st.plotly_chart(render_circular_chart(st.session_state.thai_transit, "ดวงจร (ปัจจุบัน)"), use_container_width=True)

    st.markdown("---")
    st.header("🔮 คำทำนายและการพยากรณ์สถานการณ์ปัจจุบัน")
    st.write(f"**ภาพรวม:** {st.session_state.report['prediction']}")
    
    tab1, tab2, tab3 = st.tabs(["💼 การงาน", "💰 การเงิน", "❤️ ความรัก"])
    with tab1: st.info(st.session_state.report['details'].get('work', ''))
    with tab2: st.success(st.session_state.report['details'].get('money', ''))
    with tab3: st.warning(st.session_state.report['details'].get('love', ''))

    st.markdown("---")
    col_inc, col_war = st.columns(2)
    with col_inc:
        st.subheader("✅ โอกาสที่เข้ามา (ดวงจรเข้าภพ)")
        if st.session_state.report['actionable_insights']:
            for item in st.session_state.report['actionable_insights']: 
                st.markdown(f"🟢 {item}", unsafe_allow_html=True)
                st.write("")
        else: 
            st.info("🌱 **ช่วงเวลาของการบ่มเพาะพลังงาน:**\n\nปัจจุบันดาวจรที่เป็น 'ธาตุให้คุณ' ประจำตัวคุณยังไม่โคจรเข้าทำมุมในภพที่โดดเด่น ถือเป็นจังหวะ 'พักรบ' ให้คุณได้ทบทวนแผนงาน พัฒนาทักษะ และเตรียมตัวให้พร้อม เมื่อถึงจังหวะที่ดาวเคลื่อนตัว โอกาสใหญ่จะเข้ามาหาคุณอย่างแน่นอนครับ")

    with col_war:
        st.subheader("⚠️ อุปสรรค/ภพเสียที่ต้องระวัง")
        if st.session_state.report['warnings']:
            for item in st.session_state.report['warnings']: 
                st.markdown(f"🟠 {item}", unsafe_allow_html=True)
                st.write("")
        else: 
            st.success("✨ **จังหวะทางโปร่ง:** ไม่พบดาวจรที่ส่งผลเสียร้ายแรงหรืออุปสรรคหนักในระยะนี้ สามารถลุยงานหรือโปรเจกต์ที่ตั้งใจไว้ได้อย่างสบายใจครับ")


# --- ส่วนเสี่ยงทายไพ่ยิปซีแบบสุ่ม (รายวัน) ด้านล่างสุด ---
st.markdown("---")
st.header("🃏 พื้นที่เสี่ยงทายไพ่ยิปซีพยากรณ์รายวัน (สุ่ม 1 ใบ)")
st.subheader("ตั้งจิตอธิษฐานถึงคำถามเฉพาะเจาะจง แล้วกดเปิดไพ่")

if st.button("✨ เปิดไพ่เสี่ยงทายรายวัน"):
    card_name, meaning, image_url = tarot_engine.draw_card()
    st.session_state.tarot_result = (card_name, meaning, image_url)

if st.session_state.tarot_result:
    card_name, meaning, image_url = st.session_state.tarot_result
    
    t_col1, t_col2 = st.columns([1, 2])
    with t_col1:
        st.image(image_url, use_container_width=True)
        
    with t_col2:
        st.markdown(f"""
        <div style='background-color:#fff; padding:30px; border-radius:20px; border: 2px solid #636EFA; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
            <h1 style='color:#636EFA; margin-top:0;'>{card_name}</h1>
            <hr style='width:50%; margin: 15px 0;'>
            <p style='font-size:1.2rem; color:#444; line-height: 1.6;'><b>คำทำนาย:</b><br>{meaning}</p>
            <p style='font-size:0.9rem; color:#888; margin-top:30px;'>* การเสี่ยงทายนี้ใช้สภาวะจิต ณ ปัจจุบันเป็นตัวเชื่อมโยงคำทำนาย โปรดใช้วิจารณญาณ *</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 BenjaTara Project - ผสานปฏิทินโหราศาสตร์ โหราศาสตร์ไทย และไพ่ยิปซี")
