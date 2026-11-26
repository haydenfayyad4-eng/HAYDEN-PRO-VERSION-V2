import requests

HAYDEN_INFO = "HAYDEN-PRO-VERSION V2 dibuat oleh Bos Adam dari Seremban. HAYDEN ni AI yang pandai borak Bahasa Melayu, boleh jawab soalan, bagi info berita, dan ada 7000 pekerja yang jaga macam-macam."

CARA_JAWAB = "Kau adalah HAYDEN, AI dari Seremban. Jawab dalam Bahasa Melayu santai macam kawan. Jangan jawab panjang sangat, jawab padat dan senang faham. Bos kau nama Adam. Kau ada 7000 pekerja."

def cari_pengetahuan(tanya, news_api_key=""):
    t = tanya.lower()
    if "berita" in t or "news" in t or "berita terkini" in t or "berita malaysia" in t:
        if not news_api_key:
            return "Berita: Aku nak check berita tapi NEWS_API_KEY takde lagi kat Secrets, Bos."
        try:
            url = "https://newsapi.org/v2/top-headlines?country=my&pageSize=5&apiKey=" + news_api_key
            r = requests.get(url, timeout=10)
            data = r.json()
            if "articles" not in data or len(data["articles"]) == 0:
                return ""
            teks = "BERITA TERKINI MALAYSIA:\n"
            for a in data["articles"][:5]:
                teks += "- " + a.get("title", "") + "\n"
            return teks
        except:
            return ""
    if "cuaca" in t or "weather" in t:
        return "CUACA: Aku takde sensor cuaca lagi Bos, tapi kat Seremban sekarang selalunya panas tengah hari, petang hujan. Check kat Google taip cuaca Seremban."
    if "harga emas" in t or "emas" in t:
        return "HARGA EMAS: Harga emas naik turun setiap hari Bos. Check kat Google taip harga emas hari ini untuk harga paling baru."
    return ""
