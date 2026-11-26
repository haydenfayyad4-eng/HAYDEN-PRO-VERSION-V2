import requests
HAYDEN_INFO = "HAYDEN-PRO-VERSION V2 dibuat oleh Bos Adam dari Seremban. Ada 7000 pekerja."
CARA_JAWAB = "Kau adalah HAYDEN, AI dari Seremban. Jawab dalam Bahasa Melayu santai macam kawan. Bos kau nama Adam. Kau ada 7000 pekerja."
def cari_pengetahuan(tanya, news_api_key=""):
    t = tanya.lower()
    if "berita" in t or "news" in t:
        if not news_api_key:
            return "Berita: NEWS_API_KEY takde lagi kat Secrets, Bos."
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
        return "CUACA: Kat Seremban sekarang selalunya panas tengah hari, petang hujan."
    if "harga emas" in t or "emas" in t:
        return "HARGA EMAS: Harga emas naik turun setiap hari Bos."
    return ""
