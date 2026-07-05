import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")

genai.configure(api_key=api_key)

# ใช้โมเดล gemini-2.5-flash ตามที่คุณเลือกไว้ได้เลย
model = genai.GenerativeModel("gemini-2.5-flash")

# ปรับให้รับทั้งข้อความจาก PDF และคำถามจากผู้ใช้
def ask_gemini(pdf_text, question):
    # รวมข้อความและคำถามเข้าด้วยกันเป็น Prompt เดียว
    full_prompt = f"อ้างอิงข้อมูลจาก Datasheet ต่อไปนี้:\n{pdf_text}\n\nคำถามจากผู้ใช้งาน: {question}"
    
    response = model.generate_content(full_prompt)
    return response.text