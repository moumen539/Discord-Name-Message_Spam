#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import itertools
import re
import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

#=========================================
#          زخرفة + أنيميشن
#=========================================

def anime_text(text, delay=0.03, color=Fore.RED):
    for ch in text:
        print(color + ch, end="", flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def banner():
    os.system("clear")
    anime_text("██████╗ ██╗      █████╗  ██████╗██╗  ██╗", 0.002)
    anime_text("██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝", 0.002)
    anime_text("██████╔╝██║     ███████║██║     █████╔╝ ", 0.002)
    anime_text("██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ", 0.002)
    anime_text("██████╔╝███████╗██║  ██║╚██████╗██║  ██╗", 0.002)
    anime_text("╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝", 0.002)
    anime_text("            ✦ BLACK TOOL ✦", 0.05)

def clean(s):
    return re.sub(r"[\u00A0\x00-\x1F\x7F-\x9F]", " ", s).strip()

#=========================================
#           واجهة إدخال البيانات
#=========================================

banner()
anime_text("[+] أدخل البيانات المطلوبة ↓", 0.02)

TOKEN = input(Fore.RED + "\n[•] أدخل التوكن: " + Style.RESET_ALL)
CHANNEL = input(Fore.RED + "[•] أدخل ايدي القروب: " + Style.RESET_ALL)

# واجهة الخيارات
anime_text("\n[1] إرسال رسائل متكررة", 0.01)
anime_text("[2] تبديل الاسماء بالتناوب", 0.01)
choice = input(Fore.RED + "[•] اختر الخيار: " + Style.RESET_ALL)

NAMES = []
MESSAGES = []
DELAY = 1  # افتراضي

if choice == "1":
    count = int(input(Fore.RED + "[•] كم رسالة تريد إرسالها بالتناوب؟ " + Style.RESET_ALL))
    for i in range(count):
        msg = input(Fore.RED + f"[+] أدخل الرسالة رقم {i+1}: " + Style.RESET_ALL)
        MESSAGES.append(msg)
    DELAY = float(input(Fore.RED + "[•] أدخل التأخير بين كل رسالة بالثواني: " + Style.RESET_ALL))
elif choice == "2":
    count = int(input(Fore.RED + "[•] كم اسم تريد تغييره بالتناوب؟ " + Style.RESET_ALL))
    for i in range(count):
        name = input(Fore.RED + f"[+] أدخل الاسم رقم {i+1}: " + Style.RESET_ALL)
        NAMES.append(name)
    DELAY = float(input(Fore.RED + "[•] أدخل التأخير بين كل تغيير بالثواني: " + Style.RESET_ALL))
else:
    anime_text("[!] خيار غير صالح. سيتم الإغلاق.")
    exit()

#=========================================
#             API Setup
#=========================================

hdr = {"Authorization": TOKEN, "Content-Type": "application/json"}
url_name = f"https://discord.com/api/v9/channels/{CHANNEL}"

#=========================================
#          بدء العملية
#=========================================

anime_text("\n[*] بدء العملية — استخدم Ctrl+C للإيقاف")

try:
    cycle_names = itertools.cycle(NAMES) if NAMES else []
    cycle_msgs = itertools.cycle(MESSAGES) if MESSAGES else []

    while True:
        # تغيير الاسم
        if NAMES:
            nm = clean(next(cycle_names))
            try:
                r = requests.patch(url_name, headers=hdr, json={"name": nm}, timeout=10)
                if r.status_code == 200:
                    anime_text("[+] تم التغيير إلى: " + nm)
                elif r.status_code == 401:
                    anime_text("[!] فشل العملية: التوكن غير صالح (401)")
                    break
                else:
                    anime_text(f"[!] خطأ HTTP عند تغيير الاسم: {r.status_code}")
            except Exception as e:
                anime_text(f"[!] خطأ شبكي عند تغيير الاسم: {e}")

        # ارسال الرسائل
        if MESSAGES:
            msg = next(cycle_msgs)
            url_msg = f"https://discord.com/api/v9/channels/{CHANNEL}/messages"
            try:
                r = requests.post(url_msg, headers=hdr, json={"content": msg}, timeout=10)
                if r.status_code == 200:
                    anime_text("[+] تم الإرسال: " + msg)
                elif r.status_code == 401:
                    anime_text("[!] فشل العملية: التوكن غير صالح (401)")
                    break
                else:
                    anime_text(f"[!] فشل الإرسال (كود {r.status_code})")
            except Exception as e:
                anime_text(f"[!] خطأ شبكي عند ارسال الرسالة: {e}")

        time.sleep(DELAY)

except KeyboardInterrupt:
    anime_text("\n[*] تم الإيقاف بنجاح. ✅")
