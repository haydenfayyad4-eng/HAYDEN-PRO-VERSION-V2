import json
import os
import hashlib

FILE_BELAJAR = "belajar.json"
JUMLAH_PEKERJA = 7000

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

def pekerja_security(tanya):
    t = tanya.lower()
    if "password" in t or "kata laluan" in t:
        return "PEKERJA SECURITY - Password Kuat: Buat password 12 huruf ke atas, campur huruf besar, huruf kecil, nombor dan simbol. Contoh: Seremban2026Adam. Jangan guna password sama untuk semua akaun. On kan 2FA."
    if "phishing" in t or "scam" in t or "link tipu" in t or "kena hack" in t or "kena scam" in t:
        return "PEKERJA SECURITY - Jangan Kena Scam: Jangan klik link dari nombor tak kenal. Jangan bagi nombor OTP 6 digit kat sesiapa."
    if "bocor" in t or "leak" in t:
        return "PEKERJA SECURITY - Check Akaun Bocor: Pergi kat Google, taip have i been pwned, masukkan email kau."
    return "TAK_TAHU"

def bos_hayden(tanya):
    t = tanya.lower().strip()
    belajar = load_belajar()
    if t in belajar:
        return belajar[t]
    if t in ["hi", "hello", "assalamualaikum", "salam"]:
        return "Waalaikumsalam Bos Adam. HAYDEN dah ready. Sekarang aku ada 7000 pekerja."
    if "berapa pekerja" in t:
        return f"Aku ada {JUMLAH_PEKERJA} pekerja Bos."
    if "siapa bos" in t or "siapa nama bos" in t:
        return "Bos aku Adam dari Seremban. Bos paling power."
    if "siapa kau" in t or "nama kau" in t:
        return "Aku HAYDEN-PRO-VERSION V2. Aku ada 7000 pekerja."
    if "apa khabar" in t:
        return "Aku sihat Bos, 7000 pekerja tengah kerja untuk Bos ni."
    j = pekerja_security(tanya)
    if j != "TAK_TAHU":
        return j
    return "TAK_TAHU"
