import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import random
import os

from BaziAnalyzer import BaziAnalyzer
from ThaiAstrologyEngine import ThaiAstrologyEngine
from HybridSynthesisEngine import HybridSynthesisEngine
from TarotEngine import TarotEngine

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="BenjaTara", layout="wide")
tarot_engine = TarotEngine()

if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False

with st.sidebar:
    st.header("📍 ข้อมูลเจ้าชะตา")
    with st.form("data"):
        name = st.text_input("ชื่อ", "คุณผู้ใช้งาน")
        date = st.date_input("วันเกิด")
        time = st.time_input("เวลาเกิด")
        lat = st.number_input("Lat", value=13.7563)
        lon = st.number_input("Lon", value=100.5018)
        all_cards = tarot_engine.get_all_card_names()
        selected_positions = st.multiselect("เลือกไพ่ 3 ใบ (คว่ำหน้า)", [f"ไพ่ตำแหน่งที่ {i}" for i in range(1, len(all_cards)+1)], max_selections=3)
        submit = st.form_submit_button("วิเคราะห์ดวง")

if submit:
    # 1. คำนวณ (ใช้คลาสต่างๆ ที่คุณมี)
    bazi = BaziAnalyzer()
    thai = ThaiAstrologyEngine()
    hybrid = HybridSynthesisEngine()
    
    # 2. สับไพ่และเลือก
    shuffled = all_cards.copy()
    random.shuffle(shuffled)
    selected_indices = [int(p.split()[-1])-1 for p in selected_positions]
    st.session_state.selected_cards = [shuffled[i] for i in selected_indices]
    
    # 3. วิเคราะห์ดวง (จำลอง)
    # [เติมโค้ดคำนวณเหมือนเดิมที่คุณมี]
    st.session_state.analysis_done = True
    st.session_state.name = name
    st.session_state.report = hybrid.verify_and_predict({'useful_gods':[], 'scores':{}}, {'planets':{}})

if st.session_state.analysis_done:
    st.header(f"ผลการวิเคราะห์: {st.session_state.name}")
    
    # แสดงไพ่ที่เลือก
    cols = st.columns(3)
    for idx, card in enumerate(st.session_state.selected_cards):
        info = tarot_engine.get_card_info(card)
        with cols[idx]:
            if os.path.exists(info['image']): st.image(info['image'])
            st.write(f"**{card}**")
            st.write(info['meaning'])

    # แสดงบทสรุปปิดท้าย
    meanings = [tarot_engine.get_card_info(c)['meaning'] for c in st.session_state.selected_cards]
    summary = HybridSynthesisEngine().generate_final_summary(st.session_state.report, meanings)
    st.markdown(f"--- \n {summary}")
