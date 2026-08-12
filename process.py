import os
import json
import requests

# ১. ড্রপবক্স থেকে ফাইল ডাউনলোড করা
URL = "https://www.dropbox.com/scl/fi/6olbrzcscvrj9xm4q9mqv/tafsir.json?rlkey=o1cpyt6j1jb8og6lrg0c9a0sd&st=ihwu62p0&dl=1"
RAW_FILE = "tafsir.json"
SURA_FILE = "sura.json"

print("Downloading tafsir.json...")
response = requests.get(URL)
response.raise_for_status()

# ডাউনলোড করা ফাইল সেভ করা
with open(RAW_FILE, "wb") as f:
    f.write(response.content)

print("Processing JSON data...")
with open(RAW_FILE, "r", encoding="utf-8") as f:
    tafsir_data = json.load(f)

# ২. ইউনিক সূরার তথ্য আলাদা করা
suras_dict = {}
for item in tafsir_data:
    sura_id = item.get("sura")
    if sura_id and sura_id not in suras_dict:
        suras_dict[sura_id] = {
            "sura": item.get("sura"),
            "suraName": item.get("suraName"),
            "type": item.get("type"),
            "versess": item.get("versess"),
            "suraArabic": item.get("suraArabic")
        }

sura_list = list(suras_dict.values())

# ৩. sura.json ফাইল তৈরি করা
with open(SURA_FILE, "w", encoding="utf-8") as f:
    json.dump(sura_list, f, ensure_ascii=False, indent=2)

print(f"Successfully processed {len(sura_list)} suras and saved to {SURA_FILE}")
