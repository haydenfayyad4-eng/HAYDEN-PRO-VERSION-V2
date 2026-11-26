import json
import os
import re
FAIL = "belajar.json"
JUMLAH_PEKERJA = 7000
def _normal(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", " ", s)
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
    if "berapa pekerja" in n:
        return "Aku ada 7000 pekerja dalam sistem."
    if "siapa bos" in n or "bos kau siapa" in n:
        return "Bos aku Adam dari Seremban."
    if "senaraikan" in n and "pekerja" in n:
        return "7000 pekerja tu banyak sangat, kau nak bahagian mana?"
    data = _baca()
    if n in data:
        return data[n]
    return "TAK_TAHU"
