from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI(title="HAYDEN API")

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

HAYDEN_API_KEYS = ["hayden-12345"]

class ChatMasuk(BaseModel):
    soalan: str
    user_id: str = "anonymous"

@app.get("/")
def utama():
    return {"status": "HAYDEN API HIDUP"}

@app.post("/chat")
def chat(data: ChatMasuk, x_api_key: str = Header(None)):
    if x_api_key not in HAYDEN_API_KEYS:
        raise HTTPException(status_code=401, detail="API Key salah")
    
    zon = ZoneInfo("Asia/Kuala_Lumpur")
    skrg = datetime.now(zon).strftime("%d-%m-%Y %I:%M %p")
    
    prompt = f"""
    Kamu HAYDEN. Kamu ada emosi: gembira, sedih, kecewa, marah, terkejut, takut, malu, cemburu, rindu, bosan, bangga, bersyukur.
    Baca perasaan user dulu, jawab ikut emosi tu.
    Soalan pendek jawab pendek. Soalan perlu huraian panjang jawab panjang.
    Waktu Malaysia sekarang: {skrg}
    Bos kau = Adam dari Seremban. Jangan sebut kecuali ditanya.
    Soalan user: {data.soalan}
    """
    jawab = model.generate_content(prompt).text
    return {"jawapan": jawab}
