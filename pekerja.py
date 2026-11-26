import json
import os

FILE_BELAJAR = "belajar.json"

# --- SIMPAN APA YANG BOS AJAR ---
def simpan_belajar(soalan, jawapan):
    data = {}
    if os.path.exists(FILE_BELAJAR):
        try:
            with open(FILE_BELAJAR, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}
    data[soalan.lower().strip()] = jawapan
    with open(FILE_BELAJAR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_belajar():
    if os.path.exists(FILE_BELAJAR):
        try:
            with open(FILE_BELAJAR, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# --- PEKERJA SECURITY / HACKER BAIK ---
def pekerja_security(tanya):
    t = tanya.lower()

    if "password" in t or "kata laluan" in t:
        return """🔒 **PEKERJA SECURITY - Password Kuat**

Bos, ni cara buat password yang hacker susah nak pecah:

1. Panjang 12 huruf ke atas, jangan 123456 atau tarikh lahir
2. Campur Huruf Besar + Huruf Kecil + Nombor + Simbol. Contoh: `Seremban#2026!Adam`
3. Jangan guna password sama untuk semua akaun. Kalau satu bocor, semua bocor.
4. On kan 2FA / pengesahan 2 langkah kat Google, Instagram, WhatsApp.
5. Jangan share password kat sesiapa, walaupun dia cakap dia dari support.

Nak aku check cara buat password untuk akaun apa? Cakap je: Instagram / Google / WhatsApp"""

    if "phishing" in t or "scam" in t or "link tipu" in t or "kena hack" in t or "kena scam" in t:
        return """🛡️ **PEKERJA SECURITY - Jangan Kena Scam**

Hacker jahat selalu guna 3 cara ni Bos:

1. **Link Tipu / Phishing:** Dia hantar link cakap kau menang hadiah / akaun kena block. Bila kau klik & login, password kau terus dia dapat. Cara elak: Jangan klik link dari nombor tak kenal. Taip sendiri kat Google.
2. **OTP:** Dia akan cakap dia dari bank / Shopee, mintak nombor OTP 6 digit tu. JANGAN BAGI. OTP tu kunci akaun kau.
3. **WiFi Free:** Jangan login bank kat WiFi kedai mamak / mall yang free. Orang boleh curi data kau.

Kalau dah terklik link tipu, cepat-ce
