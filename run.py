#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
د پروژې د چلولو ساده فایل
"""

import os
import sys
import subprocess

def main():
    """پروژه چل کړئ"""
    
    print("=" * 60)
    print("🚀 د ټیلیګرام راپور ورکوونکی بوټ")
    print("=" * 60)
    
    # چک کړئ چې requirements نصب دي که نه
    try:
        import telethon
        import prettytable
        import colorama
        import dotenv
    except ImportError:
        print("📦 اړین کتابخانې نصبېږي...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ نصب بشپړ شو!")
    
    # اصلي پروګرام چل کړئ
    os.system(f"{sys.executable} main.py")

if __name__ == "__main__":
    main()
