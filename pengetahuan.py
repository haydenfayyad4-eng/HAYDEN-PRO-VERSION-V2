import requests
import urllib.parse

# --- 1. WIKIPEDIA (Tak payah API Key, free) ---
def cari_wikipedia(soalan):
    try:
        q = urllib.parse.quote(soalan)
        url = f"https://ms.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "extract" in data:
                return data["extract"][:800]
        # Kalau BM takde, cuba English
        url2 = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        r2 = requests.get(url2, timeout=5)
        if r2.status_code == 200:
            data = r2.json()
            if "extract" in data:
                return data["extract"][:800]
    except Exception as e:
        print(e)
    return None

# --- 2. KAMUS DBP / KAMUS MELAYU (Free, pakai Dewan Bahasa punya API) ---
def cari_kamus(perkataan):
    try:
        # Guna kamus API free - Wiktionary Melayu
        q = urllib.parse.quote(perkataan)
        url = f"https://ms.wiktionary.org/api/rest_v1/page/definition/{q}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            # Ambik definisi pertama
            for lang in data.values():
                for item in lang:
                    for d in item.get("definitions", []):
                        return d.get("definition", "")[:500]
    except:
        pass
    return None

# --- 3. BERITA (Perlu NEWS_API_KEY) ---
def cari_berita(topik, news_api_key=""):
    if not news_api_key:
        return None
    try:
        url = f"https://newsapi.org/v2/everything?q={topik}&language=ms&sortBy=publishedAt&pageSize=3&apiKey={news_api_key}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            hasil = []
            for a in data.get("articles", [])[:3]:
                hasil.append(f"- {a['title']} ({a['source']['name']})")
            if hasil:
                return "Berita terkini:\n" + "\n".join(hasil)
        # Kalau BM takde berita, cuba English
        url2 = f"https://newsapi.org/v2/everything?q={topik}&language=en&sortBy=publishedAt&pageSize=3&apiKey={news_api_key}"
        r2 = requests.get(url2, timeout=5)
        if r2.status_code == 200:
            data = r2.json()
            hasil = []
            for a in data.get("articles", [])[:3]:
                hasil.append(f"- {a['title']} ({a['source']['name']})")
            if hasil:
                return "Berita terkini:\n" + "\n".join(hasil)
    except:
        pass
    return None

# --- 4. HUKUM SYARAK & PERATURAN ISLAM ---
# Ni kita pakai 2 sumber: Al-Quran API (free) + Hadis API (free) + Jakim punya info static
def cari_hukum_syarak(soalan):
    # Database Hukum Syarak - dari JAKIM / Mazhab Syafie (Malaysia)
    HUKUM_DB = {
        "solat": "Solat 5 waktu wajib bagi orang Islam. Subuh 2 rakaat, Zohor 4, Asar 4, Maghrib 3, Isyak 4. Mazhab Syafie yang dipakai di Malaysia.",
        "puasa": "Puasa Ramadhan wajib. Tak boleh makan/minum dari Subuh sampai Maghrib. Kalau sakit / musafir, boleh ganti kemudian.",
        "zakat": "Zakat fitrah wajib bayar sebelum solat raya. Zakat harta 2.5% kalau cukup nisab dan haul. Di Malaysia, bayar kat Pusat Zakat Negeri.",
        "aurat": "Aurat lelaki dari pusat sampai lutut. Aurat perempuan seluruh badan kecuali muka dan tapak tangan, mengikut Mazhab Syafie.",
        "halal": "Makanan halal mesti disembelih cara Islam, tak ada babi, tak ada arak. Cari logo Halal JAKIM.",
        "haram": "Haram: babi, arak, judi, riba, zina. Riba tu haram dalam Islam, termasuk faedah pinjaman yang zalim.",
        "wuduk": "Wuduk: niat, basuh muka, tangan sampai siku, sapu kepala, basuh kaki sampai buku lali. Kalau batal, kena ambik wuduk balik.",
        "nikah": "Nikah wajib ada wali, 2 saksi, ijab kabul, dan mas kahwin. Di Malaysia kena daftar kat Jabatan Agama Islam Negeri.",
        "judi": "Judi haram dalam Islam. Termasuklah tikam, kasino, dan pertaruhan duit.",
        "riba": "Riba haram. Jangan ambik / bagi faedah yang menindas. Di Malaysia ada perbankan Islam untuk elak riba.",
    }
    l = soalan.lower()
    for k, v in HUKUM_DB.items():
        if k in l:
            return v
    return None

def cari_quran(surah_no=1):
    try:
        # Al-Quran Cloud API - Free, tak payah key
        url = f"https://api.alquran.cloud/v1/surah/{surah_no}/ms.asad"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()["data"]
            return f"Surah {data['englishName']} ({data['name']}): {data['ayahs'][0]['text'][:300]}"
    except:
        pass
    return None

# --- FUNGSI UTAMA: HAYDEN CARI PENGETAHUAN ---
def cari_pengetahuan(soalan, news_api_key=""):
    l = soalan.lower()
    # Kalau soalan pasal Islam / hukum, cari hukum dulu
    if any(x in l for x in ["solat", "puasa", "zakat", "aurat", "halal", "haram", "wuduk", "nikah", "judi", "riba", "hukum", "islam", "syarak"]):
        h = cari_hukum_syarak(soalan)
        if h:
            return f"[Hukum Syarak - Mazhab Syafie / JAKIM]\n{h}"
    # Kalau soalan pasal berita / terkini
    if any(x in l for x in ["berita", "terkini", "semasa", "hari ni", "apa jadi"]):
        b = cari_berita(soalan, news_api_key)
        if b:
            return b
    # Kalau soalan "apa maksud ...", cari kamus
    if "maksud" in l or "erti" in l or "apa makna" in l:
        perkataan = soalan.replace("apa maksud", "").replace("maksud", "").strip()
        k = cari_kamus(perkataan)
        if k:
            return f"[Kamus Dewan]\n{k}"
    # Last, cari Wikipedia
    w = cari_wikipedia(soalan.replace("apa itu", "").replace("siapa", "").strip())
    if w:
        return f"[Wikipedia]\n{w}"
    return None

HAYDEN_INFO = "HAYDEN-PRO-VERSION V2 | Bos: Adam dari Seremban"
CARA_JAWAB = "Kau HAYDEN, kawan Malaysia, jawab santai pendek 2-3 ayat, jangan kaku."
