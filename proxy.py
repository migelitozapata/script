#!/data/data/com.termux/files/usr/bin/python3
import subprocess
import urllib.request
import json
import time
import os
import sys

PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
HOME = os.environ.get("HOME", "/data/data/com.termux/files/home")

BIN_DIR = os.path.join(PREFIX, "bin")
CFG_FILE = os.path.join(HOME, "3proxy.cfg")

proxy_proc = None
ngrok_proc = None

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def start_bg(exe, args):
    return subprocess.Popen(
        [os.path.join(BIN_DIR, exe)] + args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def get_ngrok_url(retries=10, delay=1):
    for _ in range(retries):
        try:
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2) as r:
                data = json.loads(r.read().decode())
                tunnels = data.get("tunnels", [])
                if tunnels:
                    return tunnels[0]["public_url"]
        except Exception:
            pass
        time.sleep(delay)
    return None

def cleanup():
    print(f"\n{YELLOW}Cerrando procesos...{RESET}")
    for p in (proxy_proc, ngrok_proc):
        if p:
            try:
                p.terminate()
            except Exception:
                pass
    time.sleep(1)
    for p in (proxy_proc, ngrok_proc):
        if p:
            try:
                p.kill()
            except Exception:
                pass
    print(f"{RED}Todo detenido.{RESET}")

def clear():
    os.system("clear")

def banner():
    print(f"{CYAN}{BOLD}")
    print(r"  ____                    __  __  ____ ")
    print(r" |  _ \ _ __ _____  ___   |  \/  |/ ___|")
    print(r" | |_) | '__/ _ \ \/ / | | | |\/| | |  _ ")
    print(r" |  __/| | | (_) >  <| |_| | |  | | |_| |")
    print(r" |_|   |_|  \___/_/\_\\__, |_|  |_|\____|")
    print(r"                     |___/               ")
    print(f"{RESET}")

def main():
    global proxy_proc, ngrok_proc
    clear()
    banner()
    print(f"{YELLOW}Iniciando 3proxy...{RESET}")
    proxy_proc = start_bg("3proxy-bin", [CFG_FILE])
    print(f"{YELLOW}Iniciando ngrok...{RESET}")
    ngrok_proc = start_bg("ngrok", ["tcp", "3128"])
    url = get_ngrok_url()
    proxy_addr = url.replace("tcp://", "") if url else None
    print()
    print(f"{GREEN}{'=' * 50}{RESET}")
    if proxy_addr:
        print(f"{GREEN}  PROXY ACTIVO{RESET}")
        print(f"{GREEN}{'=' * 50}{RESET}")
        print(f"  {BOLD}Direccion:{RESET} {CYAN}{proxy_addr}{RESET}")
    else:
        print(f"{RED}  No se pudo obtener la URL de ngrok{RESET}")
        print(f"{GREEN}{'=' * 50}{RESET}")
    print(f"{GREEN}{'=' * 50}{RESET}")
    print()
    print(f"{YELLOW}Escribe x y Enter para detener todo.{RESET}")
    print()
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            if line.strip().lower() == "x":
                break
    except KeyboardInterrupt:
        pass
    cleanup()

if __name__ == "__main__":
    main()
