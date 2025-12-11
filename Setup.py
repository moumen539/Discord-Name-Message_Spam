#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

# قائمة المكتبات الأساسية التي يحتاجها سكربتك
required_packages = ["requests", "colorama"]

print("[*] جاري التحقق من الاعتماديات الأساسية...")

for package in required_packages:
    try:
        __import__(package)
        print(f"[+] مكتبة '{package}' موجودة بالفعل ✅")
    except ImportError:
        print(f"[!] مكتبة '{package}' غير موجودة، جاري تثبيتها...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[+] تم تثبيت '{package}' بنجاح ✅")

print("\n[*] جميع الاعتماديات جاهزة لتشغيل الأداة 🎉")
