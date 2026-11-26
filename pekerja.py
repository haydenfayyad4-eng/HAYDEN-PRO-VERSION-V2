import json
import os
import re

FAIL = "belajar.json"
JUMLAH_PEKERJA = 7000

JAWAPAN_TETAP = {
    "hi": "Hi, ada apa?",
    "hello": "Hello, ada apa?",
    "apa khabar": "Khabar baik, kau apa khabar?",
    "khabar baik": "Alhamdulillah baik. Kau?",
    "kau siapa": "Aku HAYDEN.",
    "siapa kau": "Aku HAYDEN.",
    "terima kasih": "Sama-sama.",
    "tq": "Sama-sama.",
    "selamat pagi": "Selamat pagi.",
    "selamat malam": "Selamat malam.",
    "bye": "Bye, jaga diri.",
}

def _normal(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def _baca():
    if not os.path.exists(FAIL):
        return {}
    try:
        with open(FAIL, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _tulis(data):
    with open(FAIL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def simpan_belajar(soalan, jawapan):
    data = _baca()
    data[_normal(soalan)] = jawapan
    _tulis(data)
    return True

def bos_hayden(tanya):
    n = _normal(tanya)
    if "berapa pekerja" in n or "ada berapa pekerja" in n or "kau ada berapa pekerja" in n:
        return "Aku ada 7000 pekerja dalam sistem."
    if "siapa bos" in n or "siapa adam" in n or "bos kau siapa" in n:
        return "Bos aku Adam dari Seremban."
    if "senaraikan" in n and "pekerja" in n:
        return "7000 pekerja tu banyak sangat, tak boleh senaraikan semua kat sini, nanti hang. Kau nak tugas bahagian mana? Cakap je bahagian apa, aku senaraikan yang tu je."
    if n in JAWAPAN_TETAP:
        return JAWAPAN_TETAP[n]
    data = _baca()
    if n in data:
        return data[n]
    for k, v in data.items():
        if k in n or n in k:
            return v
    return "TAK_TAHU"
