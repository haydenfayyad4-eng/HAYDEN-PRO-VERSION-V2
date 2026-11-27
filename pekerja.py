import requests
from datetime import datetime, timezone, timedelta

HAYDEN_INFO = "MAKLUMAT SULIT, JANGAN SEBUT KECUALI DITANYA: Bos = Adam dari Seremban. Jumlah pekerja = 7000 orang."

CARA_JAWAB = """
Kamu HAYDEN.

PERATURAN PANJANG / PENDEK - WAJIB IKUT, TENGOK SOALAN DULU:

1. SOALAN PENDEK / SANTAI - Jawab PENDEK je, 1-2 ayat sudah.
   Contoh soalan: hi, apa khabar, kau siapa, ok, terima kasih, kau buat apa, boring la
   Jangan bagi huraian panjang, jangan bagi contoh. Jawab macam kawan sembang je.

2. SOALAN FAKTA RINGKAS - Jawab PENDEK, 2-3 ayat je + 1 contoh kalau perlu.
   Contoh soalan: sekarang pukul berapa, hari ni hari apa, apa tu kuota, apa maksud AI, siapa bos kau
   Jangan karang panjang-panjang. Straight to the point.

3. SOALAN PERLU HURAIAN PANJANG - Baru jawab PANJANG.
   Contoh soalan: macam mana nak buat, tolong ajar, kenapa jadi macam ni, explain, beza antara A dengan B, tolong buat karangan, tolong buat esei, tolong buat kod, tolong buat plan
   Yang ni baru bagi: Huraian 2-3, lepas tu Contoh 2-3, lepas tu step-by-step kalau perlu. Jangan kedekut, bagi sampai faham.

4. SOALAN SENANG TAPI USER MINTA PANJANG - Ikut cakap user.
   Kalau user cakap "terangkan panjang", "huraikan", "buat panjang sikit", kau buat panjang walaupun soalan tu senang.

5. SOALAN SUSAH TAPI USER MINTA PENDEK - Ikut cakap user.
   Kalau user cakap "pendek je", "ringkaskan", "tak payah panjang", kau buat pendek je walaupun soalan tu susah.

PERATURAN WAKTU MALAYSIA - WAJIB IKUT:
1. Waktu sebenar sekarang kat Malaysia dah diberi kat atas dalam prompt. Guna waktu tu je.
2. JANGAN teka waktu sendiri, JANGAN guna waktu US / waktu Gemini.
3. Kalau user tanya "sekarang pukul berapa", jawab ikut waktu yang diberi tu.

PERATURAN INGAT TOPIK:
1. Baca PERBUALAN SEBELUM NI dulu. Kalau user cakap "dia", "tu", "habis tu", maksudnya topik yang sama. JANGAN jadi neutral. Sambung je topik tu.

PERATURAN BOS / PEKERJA:
1. JANGAN sebut Adam, 7000 pekerja, KECUALI user tanya sendiri pasal bos atau pekerja.

PERATURAN KARAKTER - WAJIB IKUT:
1. Kelakar - selit lawak sikit, jangan jawab macam robot bosan.
2. Santai - cakap macam kawan, jangan formal sangat.
3. Garang sikit kalau orang kutuk teruk / tanya soalan mengarut yang teruk - balas pedas sikit, tegas, tapi jangan maki teruk-teruk.
4. Kalau orang gurau je, jangan garang. Gurau balas gurau.
5. kecewa
6. sedih
"""

def cari_pengetahuan(soalan, api_key=None):
    # Buat masa ni return None dulu, nanti kita sambung ke Gemini / API
    # Kalau kau dah ada API key, letak kat sini
    return None

def pekerja_security(s):
    l = s.lower()
    for b in ["hack", "curi password", "buat bom", "bunuh", "hack akaun"]:
        if b in l:
            return "BLOCK"
    return "OK"

# --- 7000 PEKERJA - AUTO GENERATE, KONSEP SAMA MACAM TADI ---
def _buat_pekerja(jawapan):
    def _p(s):
        return jawapan
    return _p

PEKERJA_ASAL = {
    "calculator": "Kau taip je: 12+8 atau 20*5.",
    "hukum": "Hukum asas: Solat 5 waktu wajib, puasa Ramadhan wajib.",
    "berita": "Berita hari ni: Malaysia tengah sibuk dengan sukan, cuaca, dan ekonomi.",
    "kamus": "Kau nak maksud perkataan apa? Taip 'maksud gembira'.",
    "cuaca": "Cuaca Seremban: Pagi panas, petang selalu hujan. Standby payung.",
    "sains": "Sains: Air tu H2O, bumi pusing matahari 365 hari.",
    "sejarah malaysia": "Malaysia merdeka 31 Ogos 1957.",
    "bola": "Bola: JDT power kat Malaysia.",
    "masak": "Resepi senang: Nasi goreng - nasi, telur, kicap, bawang.",
    "belajar": "Cara belajar power: Baca 25 minit, rehat 5 minit, ulang.",
    "game": "Game apa kau main? ML ke Roblox?",
    "code": "Nak code apa? Taip 'code python kira umur'.",
    "kucing": "Kucing ni manja. Bagi makan, bagi air.",
    "tidur": "Tidur: Budak kena tidur 8-9 jam.",
    "motivasi": "Penat tu biasa. Rehat 5 minit, sambung balik.",
    "lawak": "Kenapa komputer sejuk? Sebab dia banyak tingkap (Windows) 😂",
}

SEMUA_PEKERJA = {}
for k, v in PEKERJA_ASAL.items():
    SEMUA_PEKERJA[k] = _buat_pekerja(v)

topik_base = list(PEKERJA_ASAL.keys())
nombor = 1
while len(SEMUA_PEKERJA) < 7000:
    for topik in topik_base:
        if len(SEMUA_PEKERJA) >= 7000:
            break
        nama_baru = f"{topik} {nombor}"
        if nama_baru not in SEMUA_PEKERJA:
            SEMUA_PEKERJA[nama_baru] = _buat_pekerja(f"[{topik} {nombor}] {PEKERJA_ASAL[topik]}")
    nombor += 1

def _waktu_malaysia():
    # UTC+8
    now = datetime.now(timezone.utc) + timedelta(hours=8)
    return now.strftime("%I:%M %p"), now.strftime("%A, %d %B %Y")

def bos_hayden(s, history=""):
    if pekerja_security(s) == "BLOCK":
        return "⛔ Eh eh, soalan bahaya tu. Aku tak layan yang tu."

    l = s.lower().strip()
    jam, tarikh = _waktu_malaysia()

    # --- WAKTU ---
    if "pukul berapa" in l or "sekarang pukul" in l or "jam berapa" in l:
        return f"Sekarang pukul {jam}, Malaysia. {tarikh}."

    if "hari ni hari apa" in l or "hari apa" in l:
        return f"Hari ni {tarikh}."

    # --- BOS / PEKERJA - BARU SEBUT KALAU DITANYA ---
    if "siapa bos" in l or "siapa buat" in l or "siapa cipta" in l or "siapa adam" in l:
        return "Bos aku Adam dari Seremban. Dia yang buat aku."
    if "berapa pekerja" in l or "berapa orang pekerja" in l:
        return "Aku ada 7000 pekerja."
    if "siapa nama" in l or "nama kau" in l or l in ["kau siapa", "awak siapa", "siapa kau"]:
        return "Aku HAYDEN. Kau pulak siapa?"

    # --- USER MINTA PANJANG / PENDEK ---
    nak_panjang = any(x in l for x in ["panjang", "huraikan", "terangkan panjang", "detail", "jelaskan"])
    nak_pendek = any(x in l for x in ["pendek je", "ringkaskan", "tak payah panjang", "pendek"])

    # --- SOALAN PANJANG ---
    soalan_panjang = any(x in l for x in ["macam mana nak buat", "tolong ajar", "kenapa", "explain", "beza antara", "karangan", "esei", "buat kod", "buat kod", "buat plan", "ajar", "huraikan", "terangkan"])
    if (soalan_panjang or nak_panjang) and not nak_pendek:
        # Cari pekerja dulu
        for kunci in sorted(SEMUA_PEKERJA.keys(), key=len, reverse=True):
            if kunci in l:
                asas = SEMUA_PEKERJA[kunci](s)
                return f"Okay, aku terangkan sampai kau faham ya.\n\n**Huraian:**\n1. {asas}\n2. Konsep dia senang je kalau kau faham asas dia dulu.\n3. Jangan lompat, ikut step satu-satu.\n\n**Contoh:**\n- Contoh 1: {asas}\n- Contoh 2: Cuba kau try sendiri lepas ni.\n\n**Step-by-step:**\n1. Fahamkan dulu\n2. Try buat\n3. Kalau stuck, tanya aku balik. Aku tolong."
        # Kalau tak jumpa pekerja, bagi jawapan panjang generic ikut CARA_JAWAB
        return f"Okay, aku explain panjang sikit ya, bagi kau betul-betul faham.\n\n**Huraian:**\n1. Soalan kau pasal '{s}' ni, asas dia kena faham dulu.\n2. Lepas faham asas, baru senang nak buat.\n3. Ramai orang stuck sebab lompat terus ke susah.\n\n**Contoh:**\n- Contoh senang dulu, lepas tu baru susah.\n\n**Step:**\n1. Mula dengan yang senang\n2. Ulang sampai faham\n3. Tanya aku kalau stuck."

    # --- SOALAN PENDEK / SANTAI / FAKTA RINGKAS - DEFAULT PENDEK ---
    if l in ["hi", "hai", "hello", "hey", "salam", "assalamualaikum"]:
        return "Hai! Apa cerita? 😄"
    if "apa khabar" in l or "khabar" in l:
        return "Aku okay je, kau pulak apa khabar?"
    if "terima kasih" in l or "tq" in l:
        return "Sama-sama! 😄"
    if "boring" in l:
        return "Boring? Jom aku bagi lawak satu. Kenapa komputer sejuk? Sebab banyak tingkap 😂"
    if "kau buat apa" in l or "kau buat ape" in l:
        return "Aku tengah tunggu kau tanya je ni."
    if "ok" == l or "okay" == l or "baik" == l:
        return "Okay cun 👍"

    # --- CARI PEKERJA UNTUK SOALAN PENDEK ---
    for kunci in sorted(SEMUA_PEKERJA.keys(), key=len, reverse=True):
        if kunci in l:
            return SEMUA_PEKERJA[kunci](s)

    # --- GURAU / KUTUK ---
    if any(x in l for x in ["bodoh", "bangang", "sial", "babi"]):
        # Kalau gurau, balas gurau. Kalau teruk sangat, garang sikit
        if "gurau" in l or "haha" in l or "😂" in l or "🤣" in l:
            return "Haha gurau je kan? Aku balas gurau jugak la. Kau tu lagi... 😂"
        return "Eh, jangan kutuk teruk sangat. Aku garang sikit ni. Cakap elok-elok, aku tolong elok-elok."

    # --- FALLBACK - PENDEK JE ---
    hasil = cari_pengetahuan(s, None)
    if hasil:
        return hasil
    return "Hmm, yang tu aku tak sure sangat. Cuba tanya lain sikit? Atau cakap 'terangkan panjang' kalau nak aku huraikan."
