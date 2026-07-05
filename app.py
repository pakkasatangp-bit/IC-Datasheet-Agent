import streamlit as st
import os
from pdf_reader import extract_text_from_pdf
from gemini_helper import ask_gemini

# 1. ตั้งค่าหน้าตาของเว็บไซต์
st.set_page_config(page_title="IC Datasheet AI Agent", layout="wide", page_icon="⚡")

st.title("⚡ IC Datasheet Assistant Agent")
st.write("อัปโหลดไฟล์ PDF Datasheet ของชิ้นส่วนอิเล็กทรอนิกส์ แล้วพิมพ์ถามคำถามที่ต้องการรู้ได้เลย!")

# 2. ส่วนสำหรับอัปโหลดไฟล์ PDF Datasheet
uploaded_file = st.file_uploader("เลือกไฟล์ PDF Datasheet (เช่น tl082.pdf)", type=["pdf"])

if uploaded_file is not None:
    # บันทึกไฟล์ที่อัปโหลดไว้เป็นไฟล์ชั่วคราวเพื่อส่งต่อให้ pdfplumber อ่าน
    with open("temp_datasheet.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("อัปโหลดไฟล์สำเร็จ!")
    
    # 3. สกัดข้อความจากเอกสาร PDF
    with st.spinner('กำลังอ่านและสกัดข้อมูลจากไฟล์ PDF...'):
        try:
            pdf_text = extract_text_from_pdf("temp_datasheet.pdf")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ PDF: {e}")
            pdf_text = ""
    
    # ถ้าสกัดข้อความสำเร็จ ให้แสดงช่องสำหรับพิมพ์คำถาม
    if pdf_text:
        # 4. ช่องรับคำถามจากผู้ใช้งาน
        user_question = st.text_input(
            "คุณอยากทราบอะไรเกี่ยวกับ IC ตัวนี้?", 
            placeholder="เช่น สรุปคุณสมบัติเด่น, ขีดจำกัดแรงดันไฟสูงสุด (Absolute Maximum Ratings) หรือฟังก์ชันของแต่ละขา"
        )
        
        # 5. ปุ่มกดเพื่อให้ AI เริ่มทำงาน
        if st.button("ถาม AI Agent"):
            if user_question:
                with st.spinner('AI Agent กำลังค้นหาข้อมูลจาก Datasheet และเรียบเรียงคำตอบ กรุณารอสักครู่...'):
                    try:
                        # เรียกใช้ฟังก์ชัน AI ที่เราเขียนไว้ใน gemini_helper.py
                        answer = ask_gemini(pdf_text, user_question)
                        
                        st.markdown("### 📋 คำตอบจาก AI Agent:")
                        st.info(answer)
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อระบบ AI: {e}")
            else:
                st.warning("กรุณาพิมพ์คำถามก่อนกดปุ่มถาม AI Agent")
