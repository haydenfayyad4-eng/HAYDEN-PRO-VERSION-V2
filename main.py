# test_api.py - TEST API KEY GEMINI 1.5 / 2.0 / 2.5 / 3.0 / 4.0
# Cara run: python test_api.py

import requests

print("🤖 HAYDEN - TEST API KEY GEMINI SAMPAI 4.0")
print("="*50)
API_KEY = input("Paste API Key kau kat sini: ").strip()

# Senarai semua model dari 1.5 sampai 4.0
MODELS = [
    # --- 1.5 ---
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    # --- 2.0 ---
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-pro-exp",
    # --- 2.5 ---
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    # --- 3.0 ---
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3-pro",
    "gemini-3-flash",
    # --- 4.0 ---
    "gemini-4.0-pro",
    "gemini-4.0-flash",
    "gemini-4.0-flash-lite",
    "gemini-4-pro",
    "gemini-4-flash",
]

def test_model(model, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    data = {
        "contents": [{"parts": [{"text": "Hi, jawab 'ok' je"}]}]
    }
    try:
        r = requests.post(url, json=data, timeout=20)
        if r.status_code == 200:
            jawapan = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            return True, jawapan.strip()[:100]
        else:
            err = r.json().get("error", {}).get("message", str(r.status_code))
            return False, f"Error {r.status_code}: {err[:150]}"
    except Exception as e:
        return False, str(e)

print("\nTengah test 1.5 sampai 4.0... tunggu sikit...\n")

yang_hidup = []
for m in MODELS:
    ok, msg = test_model(m, API_KEY)
    if ok:
        print(f"✅ {m} - HIDUP! Jawab: {msg}")
        yang_hidup.append(m)
    else:
        print(f"❌ {m} - MATI! {msg}")
    print("-"*50)

print("\n=== KEPUTUSAN ===")
if yang_hidup:
    print(f"API Key kau boleh pakai model ni:")
    for x in yang_hidup:
        print(f"  - {x}")
    # Ambil yang paling baru yang hidup
    paling_baru = yang_hidup[-1]
    print(f"\nYang paling baru & paling elok kau pakai: {paling_baru}")
    print(f"\nCopy ni letak dalam main.py kau:")
    print(f'MODEL_GEMINI = "{paling_baru}"')
else:
    print("Semua mati! API Key kau salah / belum on / dah habis kuota.")
    print("Pergi https://aistudio.google.com buat API Key baru.")
