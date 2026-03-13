#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
د ټیلیګرام راپور ورکوونکی بوټ
نویسه: پښتو
نویسنده: ستاسو نوم
"""

import os
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

# بهرنۍ کتابخانې
from telethon import TelegramClient, errors
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import InputReportReasonSpam
from prettytable import PrettyTable
from colorama import init, Fore, Style, Back
from dotenv import load_dotenv

# ============================================
# د env فایل بار کړئ
# ============================================
load_dotenv()

# ============================================
# رنګونه - د عصري ډیزاین سره
# ============================================
init(autoreset=True)

class Colors:
    """د رنګونو ټولګه"""
    RED = Fore.RED
    GREEN = Fore.GREEN
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    YELLOW = Fore.YELLOW
    LIGHT_RED = Fore.LIGHTRED_EX
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BLACK = Fore.BLACK
    ORANGE = Fore.LIGHTYELLOW_EX
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    
    # پس منظر رنګونه
    BG_BLUE = Back.BLUE
    BG_GREEN = Back.GREEN
    BG_RED = Back.RED
    BG_YELLOW = Back.YELLOW
    BG_RESET = Back.RESET

# ============================================
# ترتیبات (Settings)
# ============================================
class Config:
    """د پروژې ټول ترتیبات"""
    
    # د API معلومات (د env څخه)
    API_ID = int(os.getenv('API_ID', 24018803))
    API_HASH = os.getenv('API_HASH', '757565191ed0b1471247ed7c0f840e8c')
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    SESSION_NAME = os.getenv('SESSION_NAME', 'user_session')
    
    # د راپور ترتیبات
    MIN_REPORT = 9
    MAX_REPORT = 999
    REPORT_DELAY = 0.5  # ثانیې
    
    # د پروژې نوم
    PROJECT_NAME = "🚀 د ټیلیګرام راپور ورکوونکی"
    VERSION = "2.0.0"
    AUTHOR = "@Mannucybersecurity"

# ============================================
# د متن انیمیشن
# ============================================
class TextAnimation:
    """د متن د ښودلو لپاره انیمیشن"""
    
    @staticmethod
    def typewriter(text: str, delay: float = 0.001) -> None:
        """د ټایپ رایټر انیمیشن"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    async def loading(seconds: int, message: str = "ربورټ لیږل کیږي") -> None:
        """د لوډینګ انیمیشن"""
        for i in range(seconds):
            dots = '.' * (i % 4 + 1)
            spaces = ' ' * (3 - (i % 4 + 1))
            print(f"\r{Colors.CYAN}{message}{dots}{spaces}{Colors.RESET}", 
                  end="", flush=True)
            await asyncio.sleep(1)
        print()
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 30) -> str:
        """د پرمختګ بار جوړول"""
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{Colors.GREEN}{bar}{Colors.RESET}] {current}/{total}"

# ============================================
# د بینر ښودنه
# ============================================
def show_banner() -> None:
    """د پروژې بینر ښکاره کړئ"""
    
    banner = f"""
{Colors.LIGHT_RED}═══════════════════════════════════════════════════════════════
                                                                 
{Colors.ORANGE}                              -     -                            
                            .+       +.                          
                           :#         #:                         
                          =%           %-                        
   {Colors.LIGHT_RED} Telegram {Colors.ORANGE}  -{Colors.YELLOW} Jay Ghunawat{Colors.ORANGE}   .%+    {Colors.BLUE} Max Reporter   {Colors.ORANGE}       
                        #@:             -@#                      
                     :  #@:             :@*  :                   
                    -=  *@:             -@*  =-                  
                   -%   *@-             =@+   %-                 
                  -@=  .*@+             +@+.  =@-                
                 =@%   .+@%-    :.:    -@@+.   #@:               
                =@@#:     =%%-+@@@@@+-%%=     .#@@=              
                 .+%@%+:.   -#@@@@@@@#-   .:=#@%=                
                    -##%%%%%#*@@@@@@@*#%%%%%##-                  
                  .*#######%@@@@@@@@@@@%#######*.                
               .=#@%*+=--#@@@@@@@@@@@#--=+*%@#=.             
            .=#@%+:     *@@@@@+.   .+@@@@@*     :+%@#=.          
          :*@@=.    .=#@@@@@@@       @@@@@@@#=.    .=@@*.        
            =@+    .%@@*%@@@@@*     *@@@@@%*@@%.    +@=          
             :@=    +@# :@@@@@#     #@@@@%. #@+    =@:           
              .#-   :@@  .%@@#       #@@#.  @@:   -#.            
                +:   %@:   =%         %=   :@%   -+              
                 -.  +@+                   +@+  .-               
                  .  :@#                   #@:  .                
                    {Colors.CYAN}@Mannucybersecurity{Colors.ORANGE}@%                    
                      :+@:               =@+:                    
                        =@:             :@-                      
                         -%.           .%:                       
                          .#           #.                        
                            +         +                          
                             -       -                     
{Colors.LIGHT_RED}═══════════════════════════════════════════════════════════════{Colors.RESET}
"""
    print(banner)
    
    # د پروژې معلومات
    info_table = PrettyTable()
    info_table.field_names = [f"{Colors.CYAN}ځانګړنه", f"{Colors.YELLOW}معلومات"]
    info_table.add_row([f"{Colors.GREEN}نوم", f"{Colors.WHITE}{Config.PROJECT_NAME}"])
    info_table.add_row([f"{Colors.GREEN}نسخه", f"{Colors.WHITE}{Config.VERSION}"])
    info_table.add_row([f"{Colors.GREEN}نویسنده", f"{Colors.WHITE}{Config.AUTHOR}"])
    info_table.add_row([f"{Colors.GREEN}وخت", f"{Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    print(info_table)
    
    # اخطار
    print(f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD} اخطار! {Colors.BG_RESET}")
    print(f"{Colors.LIGHT_RED}دا یو ازمایښتي پروګرام دی. هر ډول ناوړه ګټه اخیستنه د کارن مسؤلیت دی!{Colors.RESET}\n")

# ============================================
# د راپور مدیریت
# ============================================
class ReportManager:
    """د راپورونو د مدیریت کلاس"""
    
    def __init__(self, client: TelegramClient):
        self.client = client
        self.success = 0
        self.fail = 0
        self.total = 0
        self.start_time = None
    
    async def report_target(self, target, reason: str, count: int) -> Tuple[int, int]:
        """هدف ته راپور ولیږئ"""
        
        self.total = count
        self.success = 0
        self.fail = 0
        self.start_time = time.time()
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.YELLOW}📊 د راپور لیږل پیل شول:")
        print(f"   🎯 هدف: {Colors.CYAN}{target}{Colors.RESET}")
        print(f"   📝 دلیل: {Colors.WHITE}{reason}{Colors.RESET}")
        print(f"   🔢 شمېر: {Colors.LIGHT_GREEN}{count}{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
        
        for i in range(1, count + 1):
            try:
                await self.client(ReportRequest(
                    peer=target,
                    id=[],
                    reason=InputReportReasonSpam(),
                    message=reason
                ))
                self.success += 1
                
                # د پرمختګ ښودنه
                progress = TextAnimation.progress_bar(i, count)
                elapsed = time.time() - self.start_time
                remaining = (elapsed / i) * (count - i) if i > 0 else 0
                
                print(f"\r{progress} "
                      f"| {Colors.GREEN}بریالي: {self.success}{Colors.RESET} "
                      f"| {Colors.RED}ناکامه: {self.fail}{Colors.RESET} "
                      f"| {Colors.CYAN}وخت:{elapsed:.1f}ث/{remaining:.1f}ث{Colors.RESET} "
                      f"| {Colors.YELLOW}سرعت:{i/elapsed:.1f}/ث{Colors.RESET}", 
                      end="", flush=True)
                
            except errors.FloodWaitError as e:
                wait = e.seconds
                print(f"\n{Colors.RED}⏳ د {wait} ثانیو انتظار...{Colors.RESET}")
                await asyncio.sleep(wait)
                self.fail += 1
                
            except Exception as e:
                self.fail += 1
                if i % 10 == 0:  # هر 10 ځله یو ځل خطا وښایه
                    print(f"\n{Colors.RED}خطا: {e}{Colors.RESET}")
            
            await asyncio.sleep(Config.REPORT_DELAY)
        
        return self.success, self.fail
    
    def show_results(self):
        """پایلې وښایه"""
        
        elapsed = time.time() - self.start_time
        
        print(f"\n\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}📊 نهایی پایلې:{Colors.RESET}")
        
        table = PrettyTable()
        table.field_names = [f"{Colors.CYAN}شرح", f"{Colors.YELLOW}شمېر", f"{Colors.GREEN}فیصدي"]
        
        success_percent = (self.success / self.total * 100) if self.total > 0 else 0
        fail_percent = (self.fail / self.total * 100) if self.total > 0 else 0
        
        table.add_row([
            f"{Colors.GREEN}بریالي راپورونه", 
            f"{Colors.WHITE}{self.success}",
            f"{Colors.GREEN}{success_percent:.1f}%"
        ])
        table.add_row([
            f"{Colors.RED}ناکامه راپورونه", 
            f"{Colors.WHITE}{self.fail}",
            f"{Colors.RED}{fail_percent:.1f}%"
        ])
        table.add_row([
            f"{Colors.BLUE}ټولټال", 
            f"{Colors.WHITE}{self.total}",
            f"{Colors.BLUE}100%"
        ])
        
        print(table)
        print(f"\n{Colors.CYAN}⏱ ټول وخت: {elapsed:.2f} ثانیې")
        print(f"{Colors.YELLOW}⚡ اوسط سرعت: {self.total/elapsed:.2f} راپور/ثانیه{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*60}{Colors.RESET}")

# ============================================
# د کارن مدیریت
# ============================================
class UserManager:
    """د کارن د ننوتلو مدیریت"""
    
    def __init__(self, client: TelegramClient):
        self.client = client
        self.me = None
    
    async def login(self) -> bool:
        """کارن ته ننوځئ"""
        
        if await self.client.is_user_authorized():
            self.me = await self.client.get_me()
            return True
        
        # د موبایل نمبر
        print(f"\n{Colors.YELLOW}📱 مهرباني وکړئ خپل موبایل نمبر ولیکئ (د هیواد کوډ سره):{Colors.CYAN}")
        phone = input().strip()
        
        try:
            # د کوډ غوښتنه
            await self.client.send_code_request(phone)
            print(f"{Colors.GREEN}✅ کوډ مو ولیږل شو!{Colors.RESET}")
            print(f"{Colors.YELLOW}🔢 د ۵ عددي کوډ ولیکئ:{Colors.CYAN}")
            code = input().strip()
            
            # ننوتل
            await self.client.sign_in(phone, code)
            
        except errors.SessionPasswordNeededError:
            # د دو مرحلې تایید
            print(f"{Colors.YELLOW}🔐 د دو مرحلې تایید پاسورډ ولیکئ:{Colors.CYAN}")
            password = input().strip()
            await self.client.sign_in(password=password)
        
        except Exception as e:
            print(f"{Colors.RED}❌ خطا: {e}{Colors.RESET}")
            return False
        
        self.me = await self.client.get_me()
        return True
    
    async def show_info(self):
        """د کارن معلومات وښایه"""
        
        if not self.me:
            self.me = await self.client.get_me()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}📋 ستاسو د اکاونټ معلومات:{Colors.RESET}")
        
        info_table = PrettyTable()
        info_table.field_names = [f"{Colors.CYAN}ځانګړنه", f"{Colors.YELLOW}ارزښت"]
        info_table.align = "l"
        
        info_table.add_row([f"{Colors.GREEN}نوم", f"{Colors.WHITE}{self.me.first_name} {self.me.last_name or ''}"])
        info_table.add_row([f"{Colors.GREEN}یوزرنیم", f"{Colors.WHITE}@{self.me.username or 'نه لري'}"])
        info_table.add_row([f"{Colors.GREEN}آی ډي", f"{Colors.WHITE}{self.me.id}"])
        info_table.add_row([f"{Colors.GREEN}نمبر", f"{Colors.WHITE}{self.me.phone or 'نامعلوم'}"])
        
        print(info_table)
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")

# ============================================
# اصلي فنکشن
# ============================================
async def main():
    """د پروګرام اصلي برخه"""
    
    # بینر وښایه
    show_banner()
    
    # مینو وښایه
    menu = PrettyTable()
    menu.field_names = [f"{Colors.CYAN}شمېره", f"{Colors.YELLOW}څانګه"]
    menu.add_row([f"{Colors.LIGHT_GREEN}1", f"{Colors.GREEN}د کارن په توګه ننوتل (User)"])
    menu.add_row([f"{Colors.LIGHT_GREEN}2", f"{Colors.GREEN}د بوټ په توګه ننوتل (Bot) {Colors.RED}⚡ نوی"])
    menu.add_row([f"{Colors.LIGHT_GREEN}3", f"{Colors.RED}وتل"])
    print(menu)
    
    # د انتخاب غوښتنه
    print(f"\n{Colors.YELLOW}📌 مهرباني وکړئ یوه شمېره وټاکئ (1-3):{Colors.CYAN}")
    choice = input().strip()
    
    client = None
    
    if choice == "1":
        # د کارن په توګه ننوتل
        TextAnimation.typewriter(f"{Colors.GREEN}🚀 د کارن په توګه ننوتل پیل شو...{Colors.RESET}")
        client = TelegramClient(Config.SESSION_NAME, Config.API_ID, Config.API_HASH)
        await client.connect()
        
        user_mgr = UserManager(client)
        if not await user_mgr.login():
            print(f"{Colors.RED}❌ ننوتل ناکام شول!{Colors.RESET}")
            return
        
        await user_mgr.show_info()
        
    elif choice == "2":
        # د بوټ په توګه ننوتل
        if not Config.BOT_TOKEN or Config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print(f"{Colors.RED}❌ مهرباني وکړئ لومړی د .env فایل کې BOT_TOKEN ولیکئ!{Colors.RESET}")
            return
        
        TextAnimation.typewriter(f"{Colors.GREEN}🤖 د بوټ په توګه ننوتل پیل شو...{Colors.RESET}")
        client = TelegramClient('bot_session', Config.API_ID, Config.API_HASH)
        await client.start(bot_token=Config.BOT_TOKEN)
        
        bot_info = await client.get_me()
        print(f"{Colors.GREEN}✅ بوټ ننوتل: @{bot_info.username}{Colors.RESET}")
        
    elif choice == "3":
        print(f"{Colors.YELLOW}👋 په امنیت!{Colors.RESET}")
        return
    
    else:
        print(f"{Colors.RED}❌ ناسم انتخاب!{Colors.RESET}")
        return
    
    # د هدف معلومات
    print(f"\n{Colors.YELLOW}🎯 د هغه چا یوزرنیم یا لینک ولیکئ چې راپور غواړئ:{Colors.CYAN}")
    target_input = input().strip()
    target = target_input.replace("https://t.me/", "").replace("@", "")
    
    try:
        entity = await client.get_entity(target)
        print(f"{Colors.GREEN}✅ هدف وموندل شو: {entity.first_name or entity.title}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ هدف ونه موندل شو: {e}{Colors.RESET}")
        return
    
    # د راپور متن
    print(f"\n{Colors.YELLOW}📝 د راپور متن ولیکئ:{Colors.CYAN}")
    reason_text = input().strip()
    
    # د راپور شمېره
    print(f"\n{Colors.YELLOW}🔢 څو ځله راپور ولیږئ؟ (له {Config.MIN_REPORT} څخه تر {Config.MAX_REPORT} پورې):{Colors.CYAN}")
    try:
        count = int(input().strip())
        if count < Config.MIN_REPORT or count > Config.MAX_REPORT:
            print(f"{Colors.RED}❌ مهرباني وکړئ له {Config.MIN_REPORT} څخه تر {Config.MAX_REPORT} پورې ولیکئ!{Colors.RESET}")
            return
    except ValueError:
        print(f"{Colors.RED}❌ مهرباني وکړئ یوه شمېره ولیکئ!{Colors.RESET}")
        return
    
    # راپور پیل کړئ
    reporter = ReportManager(client)
    success, fail = await reporter.report_target(entity, reason_text, count)
    
    # پایلې وښایه
    reporter.show_results()
    
    # د سیشن بندول
    await client.disconnect()
    
    # بیا پیل
    print(f"\n{Colors.YELLOW}🔄 ایا غواړئ بیا پیل کړئ؟ (ه/ک):{Colors.CYAN}")
    again = input().strip().lower()
    if again in ['ه', 'yes', 'y', 'هو']:
        await main()

# ============================================
# د پروګرام پیل
# ============================================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 په امنیت!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ خطا: {e}{Colors.RESET}") 
