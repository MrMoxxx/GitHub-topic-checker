import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import requests

os.system('')

# ================= CONFIGURATION =================
INPUT_FILE = "topics.txt"

# Output files
RESULT_ACTIVE = "active_topics.txt"  # Has repos
RESULT_EMPTY = "empty_topics.txt"    # 0 repos
RESULT_BANNED = "banned_topics.txt"  # 404 / Banned

MAX_WORKERS = 4       # Number of threads (3-5 recommended)
REQUEST_DELAY = 0.35  # Delay between requests in seconds
# =================================================

# Terminal Colors
C_GREEN = "\x1b[92m"
C_RED = "\x1b[91m"
C_YELLOW = "\x1b[93m"
C_CYAN = "\x1b[96m"
C_GRAY = "\x1b[90m"
C_WHITE = "\x1b[97m"
C_BOLD = "\x1b[1m"
C_RESET = "\x1b[0m"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

print_lock = Lock()
file_lock = Lock()

active_count = 0
empty_count = 0
banned_count = 0
error_count = 0
processed_count = 0

def print_banner():
    print(f"{C_CYAN}{C_BOLD}")
    print(" ╔══════════════════════════════════════════════════════╗")
    print(" ║          🔍 GITHUB TOPIC CHECKER v3.0               ║")
    print(" ╚══════════════════════════════════════════════════════╝")
    print(f"{C_RESET}")

def check_topic(topic, total_topics):
    global active_count, empty_count, banned_count, error_count, processed_count

    url = f"https://github.com/topics/{topic}"
    status = "error"
    code = 0

    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=HEADERS, timeout=8)
        code = resp.status_code

        if code == 200:
            if "<article" in resp.text:
                status = "active"
            else:
                status = "empty"
        elif code == 404:
            status = "banned"
        elif code == 429:
            status = "ratelimit"
    except Exception:
        status = "exception"

    with print_lock:
        processed_count += 1
        progress = f"{C_GRAY}[{processed_count:>3}/{total_topics}]{C_RESET}"

        if status == "active":
            active_count += 1
            print(f" {progress}  {C_GREEN}✔ ACTIVE {C_RESET} | {C_WHITE}{topic:<32}{C_RESET} {C_GRAY}(Has repositories){C_RESET}")
            with file_lock:
                with open(RESULT_ACTIVE, "a", encoding="utf-8") as f:
                    f.write(topic + "\n")

        elif status == "empty":
            empty_count += 1
            print(f" {progress}  {C_YELLOW}⚪ EMPTY  {C_RESET} | {C_YELLOW}{topic:<32}{C_RESET} {C_GRAY}(0 repositories){C_RESET}")
            with file_lock:
                with open(RESULT_EMPTY, "a", encoding="utf-8") as f:
                    f.write(topic + "\n")

        elif status == "banned":
            banned_count += 1
            print(f" {progress}  {C_RED}✖ BANNED {C_RESET} | {C_GRAY}{topic:<32} (HTTP 404){C_RESET}")
            with file_lock:
                with open(RESULT_BANNED, "a", encoding="utf-8") as f:
                    f.write(topic + "\n")

        elif status == "ratelimit":
            error_count += 1
            print(f" {progress}  {C_YELLOW}⚠ LIMIT  {C_RESET} | {topic:<32} {C_YELLOW}(429 Rate Limit){C_RESET}")

        else:
            error_count += 1
            print(f" {progress}  {C_YELLOW}⚠ ERROR  {C_RESET} | {topic:<32} {C_GRAY}(Code: {code}){C_RESET}")

def main():
    print_banner()

    if not os.path.exists(INPUT_FILE):
        print(f" {C_RED}[!] File '{INPUT_FILE}' not found!{C_RESET}\n")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        topics = [line.strip().lower() for line in f if line.strip() and not line.startswith("#")]

    total_topics = len(topics)

    if total_topics == 0:
        print(f" {C_YELLOW}[!] File '{INPUT_FILE}' is empty.{C_RESET}\n")
        return

    # Clear output files before running
    open(RESULT_ACTIVE, "w", encoding="utf-8").close()
    open(RESULT_EMPTY, "w", encoding="utf-8").close()
    open(RESULT_BANNED, "w", encoding="utf-8").close()

    print(f" {C_WHITE}📊 Loaded topics:{C_RESET} {C_BOLD}{total_topics}{C_RESET}")
    print(f" {C_WHITE}⚡ Threads:{C_RESET}        {C_BOLD}{MAX_WORKERS}{C_RESET}")
    print(f" {C_GRAY}──────────────────────────────────────────────────────{C_RESET}\n")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_topic, topic, total_topics) for topic in topics]
        for future in as_completed(futures):
            pass

    elapsed = round(time.time() - start_time, 2)

    # Summary
    print(f"\n {C_GRAY}──────────────────────────────────────────────────────{C_RESET}")
    print(f" {C_BOLD}📊 RESULTS:{C_RESET}")
    print(f" {C_GREEN}  ► Active (with repos): {active_count:<5} (saved to {RESULT_ACTIVE}){C_RESET}")
    print(f" {C_YELLOW}  ► Empty (0 repos):     {empty_count:<5} (saved to {RESULT_EMPTY}){C_RESET}")
    print(f" {C_RED}  ► Banned (404):        {banned_count:<5} (saved to {RESULT_BANNED}){C_RESET}")
    if error_count > 0:
        print(f" {C_YELLOW}  ► Errors/Limits:       {error_count}{C_RESET}")
    print(f" {C_CYAN}  ⏱ Time elapsed: {elapsed}s{C_RESET}")
    print(f" {C_GRAY}──────────────────────────────────────────────────────{C_RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n {C_RED}[!] Stopped by user.{C_RESET}\n")
