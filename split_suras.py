import os
import json
import requests

# ১. ড্রপবক্স থেকে ফাইল ডাউনলোড করা
URL = "https://www.dropbox.com/scl/fi/6olbrzcscvrj9xm4q9mqv/tafsir.json?rlkey=o1cpyt6j1jb8og6lrg0c9a0sd&st=ihwu62p0&dl=1"
RAW_FILE = "tafsir.json"
OUTPUT_DIR = "suras"

print("Downloading tafsir.json...")
response = requests.get(URL)
response.raise_for_status()

# ডাউনলোড করা ফাইল সেভ করা
with open(RAW_FILE, "wb") as f:
    f.write(response.content)

print("Processing JSON data...")
with open(RAW_FILE, "r", encoding="utf-8") as f:
    tafsir_data = json.load(f)

# ২. প্রতিটি সূরার আয়াত ও তথ্য আলাদা করা
sura_groups = {}
for item in tafsir_data:
    sura_id = item.get("sura")
    if sura_id:
        if sura_id not in sura_groups:
            sura_groups[sura_id] = []
        sura_groups[sura_id].append(item)

# ৩. suras ফোল্ডার তৈরি না থাকলে তা তৈরি করা
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ৪. প্রতিটি সূরার জন্য ১টি করে আলাদা .json ফাইল তৈরি করা
for sura_id, verses in sura_groups.items():
    file_path = os.path.join(OUTPUT_DIR, f"{sura_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)

print(f"Successfully created {len(sura_groups)} sura files inside '{OUTPUT_DIR}/' folder!")
