#!/usr/bin/env python3
import sys, socket, requests
from urllib.parse import urlparse
import whois

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return "IP alınamadı"

def scan_ports(ip):
    ports = [21, 22, 80, 443, 8080]
    open_ports = []
    for port in ports:
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((ip, port))
            open_ports.append(port)
        except:
            continue
        s.close()
    return open_ports

def get_headers(url):
    try:
        r = requests.get(url, timeout=5)
        return r.headers
    except:
        return {}

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python3 nullsec_recon.py https://site.com")
        sys.exit()

    url = sys.argv[1]
    domain = urlparse(url).netloc

    print(f"[*] Hedef: {domain}")
    ip = get_ip(domain)
    print(f"[+] IP Adresi: {ip}")

    print("[+] Whois Bilgisi:")
    try:
        w = whois.whois(domain)
        print(w)
    except:
        print("Whois alınamadı.")

    print("[+] Açık Portlar:")
    for p in scan_ports(ip):
        print(f" - {p}")

    print("[+] HTTP Headers:")
    headers = get_headers(url)
    for k, v in headers.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
