import requests
import os
import time
import csv

# ==== CONFIG ====
API_KEY = "PUTAPIKEYHERE"
SETS_FILE = "sets.txt"
OUTPUT_DIR = "instructions"
LOG_FILE = "download_log.csv"

API_URL = "https://brickset.com/api/v3.asmx/getInstructions2"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_instructions_by_set_number(set_number):
    """Calls getInstructions2 on Brickset using setNumber directly."""
    payload = {
        "apiKey": API_KEY,
        "setNumber": set_number
    }
    r = requests.post(API_URL, data=payload)
    if r.status_code != 200:
        print(f"  [ERROR] HTTP {r.status_code} for {set_number}")
        return None
    data = r.json()
    if data.get("status", "") != "success":
        print(f"  [ERROR] API error for {set_number}: {data.get('message')}")
        return None
    return data.get("instructions", [])

def download_file(url, filepath):
    if os.path.exists(filepath):
        print(f"[SKIP] {os.path.basename(filepath)} exists")
        return "skipped"
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"[OK] Downloaded {os.path.basename(filepath)}")
        return "downloaded"
    except Exception as e:
        print(f"[ERROR] {e}")
        return f"error: {e}"

def log_entry(set_number, pdf_url, status):
    header = ["Set", "PDF URL", "Status"]
    is_new = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as cf:
        writer = csv.writer(cf)
        if is_new:
            writer.writerow(header)
        writer.writerow([set_number, pdf_url, status])

def main():
    if not os.path.exists(SETS_FILE):
        print(f"[ERROR] {SETS_FILE} not found.")
        return

    with open(SETS_FILE) as f:
        sets = [s.strip() for s in f if s.strip() and not s.startswith("#")]

    for set_number in sets:
        print(f"\n=== {set_number} ===")
        instructions = get_instructions_by_set_number(set_number)
        if not instructions:
            print(f"  [WARN] No instructions found for {set_number}")
            continue

        set_dir = os.path.join(OUTPUT_DIR, set_number)
        os.makedirs(set_dir, exist_ok=True)

        for instr in instructions:
            desc = instr.get("description", "").upper()
            if not any(tag in desc for tag in ["NA", "V39"]):
                continue

            pdf_url = instr.get("URL")
            if not pdf_url or not pdf_url.lower().endswith(".pdf"):
                continue

            filename = os.path.basename(pdf_url.split("?")[0])
            filepath = os.path.join(set_dir, filename)
            status = download_file(pdf_url, filepath)
            log_entry(set_number, pdf_url, status)

            time.sleep(0.3)

if __name__ == "__main__":
    main()
