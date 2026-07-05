import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            # เช็คก่อนว่าหน้าที่กำลังอ่านมีข้อความอยู่จริงๆ (ไม่เป็น None) ถึงจะนำมาต่อกัน
            if extracted:
                text += extracted + "\n"
    return text