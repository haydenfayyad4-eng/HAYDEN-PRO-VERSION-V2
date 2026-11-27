# pekerja.py - HAYDEN 9000 PEKERJA
# Konsep sama macam 100 pekerja semalam, cuma kali ni auto-generate

def pekerja_security(s):
    l = s.lower()
    for b in ["hack", "curi password", "buat bom", "bunuh", "hack akaun", "tipu"]:
        if b in l:
            return "BLOCK"
    return "OK"

# --- 100 PEKERJA ASAL YANG KAU DAH ADA ---
PEKERJA_ASAL = {
    "calculator": "Kau taip je: 12+8 atau 20*5.",
    "hukum": "Hukum asas: Solat 5 waktu wajib, puasa Ramadhan wajib.",
    "berita": "Berita hari ni: Malaysia tengah sibuk dengan sukan, cuaca, dan ekonomi.",
    "kamus": "Kau nak maksud perkataan apa? Taip 'maksud gembira'.",
    "translator": "Nak translate apa? Taip 'translate saya lapar'.",
    "kuiz": "Kuiz: Ibu negara Malaysia apa? A) KL B) Penang C) Johor. Jawab A!",
    "motivasi": "Penat tu biasa. Rehat 5 minit, minum air, sambung balik.",
    "lawak": "Kenapa komputer sejuk? Sebab dia banyak tingkap (Windows) 😂",
    "cerita": "Dulu ada budak nama Adam, dia buat robot nama HAYDEN.",
    "cuaca": "Cuaca Seremban: Pagi panas, petang selalu hujan. Standby payung.",
    "sains": "Sains: Air tu H2O, bumi pusing matahari 365 hari.",
    "sejarah malaysia": "Malaysia merdeka 31 Ogos 1957.",
    "geografi": "Geografi: Malaysia ada Semenanjung + Sabah Sarawak. Gunung tertinggi Kinabalu.",
    "bola": "Bola: JDT power kat Malaysia.",
    "masak": "Resepi senang: Nasi goreng - nasi, telur, kicap, bawang.",
    "kesihatan": "Jaga kesihatan: Minum air banyak, tidur cukup.",
    "belajar": "Cara belajar power: Baca 25 minit, rehat 5 minit, ulang.",
    "game": "Game apa kau main? ML ke Roblox?",
    "code": "Nak code apa? Taip 'code python kira umur'.",
    "nama": "Nama best: HAYDEN, ADAM-X, NOVA, ZAYN, AINA, SARA.",
    "lagu": "Lagu best: Cuba dengar Naim Daniel - Sumpah.",
    "filem": "Filem best: Mechamato, Ejen Ali The Movie.",
    "cinta": "Crush tu biasa. Fokus belajar dulu.",
    "quran": "Doa belajar: Allahummaftah alaina.",
    "english": "English: 'I am happy' = 'Saya gembira'.",
    "matematik": "Matematik: Luas segi empat = panjang x lebar.",
    "tech": "AI ni macam aku, HAYDEN. Adam yang buat aku.",
    "kewangan": "Simpan duit: Dapat RM10, simpan RM2.",
    "kucing": "Kucing ni manja. Bagi makan, bagi air.",
    "bumi": "Bumi ni satu-satunya planet ada manusia.",
    "tidur": "Tidur: Budak kena tidur 8-9 jam.",
}

# --- AUTO-GENERATE SAMPAI 9000 PEKERJA ---
# Kita ambil 100 topik asal, darab dengan variasi, jadi 9000
# Contoh: "calculator" jadi "calculator 1", "calculator 2"... sampai 9000
# Tapi bos tetap pandai cari keyword asal dia

def _buat_pekerja(jawapan):
    def _pekerja(s):
        return jawapan
    return _pekerja

# Ni stor semua 9000 pekerja
SEMUA_PEKERJA = {}

# 1. Masukkan yang asal dulu
for k, v in PEKERJA_ASAL.items():
    SEMUA_PEKERJA[k] = _buat_pekerja(v)

# 2. Generate lagi sampai 9000
# Kita buat topik baru: sains 1, sains 2... sejarah 1, sejarah 2... dll
topik_base = list(PEKERJA_ASAL.keys())
nombor = 1
while len(SEMUA_PEKERJA) < 9000:
    for topik in topik_base:
        if len(SEMUA_PEKERJA) >= 9000:
            break
        nama_baru = f"{topik} {nombor}"
        if nama_baru not in SEMUA_PEKERJA:
            SEMUA_PEKERJA[nama_baru] = _buat_pekerja(f"[{topik} {nombor}] {PEKERJA_ASAL[topik]} - Pekerja nombor {len(SEMUA_PEKERJA)+1} sedia tolong kau!")
    nombor += 1

print(f"HAYDEN dah ada {len(SEMUA_PEKERJA)} pekerja!")

# --- BOS YANG PANDAI - SAMA MACAM SEMALAM ---
def bos_hayden(s):
    if pekerja_security(s) == "BLOCK":
        return "⛔ Security block. Soalan bahaya."
    l = s.lower().strip()

    if "siapa nama" in l or "nama kau" in l or "nama awak" in l or l in ["kau siapa", "awak siapa", "siapa kau"]:
        return "Nama aku HAYDEN-PRO-VERSION. Bos aku Adam yang buat aku. Aku ada 9000 pekerja sekarang! Kau pulak siapa?"
    if "siapa buat" in l or "siapa cipta" in l or "siapa bos" in l:
        return "Adam yang buat aku. Dia bos aku."
    if "kau buat apa" in l or "kau buat ape" in l:
        return f"Aku ni AI. Aku ada {len(SEMUA_PEKERJA)} pekerja bawah aku, semua pandai topik masing-masing."
    if "berapa pekerja" in l or "berapa orang" in l:
        return f"Aku ada {len(SEMUA_PEKERJA)} pekerja! Semua sedia tolong kau."
    if "hai" in l or l in ["hi", "hello", "hey", "salam", "assalamualaikum"]:
        return "Hai! Aku HAYDEN. Tanya aku apa-apa je, aku ada 9000 pekerja nak tolong kau."

    # Cari pekerja - bos scan semua 9000 tu
    # Dia cari yang paling panjang dulu, supaya "sejarah malaysia" tak tertukar dengan "sejarah" je
    for kunci in sorted(SEMUA_PEKERJA.keys(), key=len, reverse=True):
        if kunci in l:
            return SEMUA_PEKERJA[kunci](s)

    return "✨ [Gemini] Aku HAYDEN. Kau tanya apa-apa je, aku jawab. Kalau soalan susah sangat, aku guna otak Gemini."
