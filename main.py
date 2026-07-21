# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import requests
import json

TARGET_URL = "https://hashora.net/register?ref=KINGKINGPLM0073637"

# ===== مختصات کلیک =====
CLICK_1_X = 877
CLICK_1_Y = 929

CLICK_2_X = 1010
CLICK_2_Y = 282

CLICK_3_X = 1063
CLICK_3_Y = 393

CLICK_4_X = 923
CLICK_4_Y = 508

CLICK_5_X = 965
CLICK_5_Y = 625

CLICK_6_X = 771
CLICK_6_Y = 865

# ===== متن‌ها برای تایپ (به جز ایمیل که از API میاد) =====
TEXT_1 = "kljwefowijowe"  # این متغیر استفاده نمیشه (می‌تونیم حذفش کنیم)
TEXT_3 = "kingking000"
TEXT_4 = "kingking000"

# =============================================
# ===== ساخت ایمیل موقت با Mail.tm =====
# =============================================

def create_temporary_email():
    """ساخت ایمیل موقت با استفاده از API Mail.tm"""
    try:
        print("\n📡 Creating temporary email...")
        
        # 1. دریافت دامنه
        response = requests.get("https://api.mail.tm/domains")
        domains = response.json()
        domain = domains['hydra:member'][0]['domain']
        print(f"   ✅ Domain: {domain}")
        
        # 2. ساخت ایمیل یکتا
        timestamp = int(time.time())
        email = f"user_{timestamp}@{domain}"
        password = "MyPass123!"
        print(f"   📧 Email: {email}")
        
        # 3. ثبت حساب
        account_data = {
            "address": email,
            "password": password
        }
        
        response = requests.post(
            "https://api.mail.tm/accounts",
            json=account_data
        )
        
        if response.status_code != 201:
            print(f"   ❌ Failed to create account: {response.status_code}")
            return None
        
        print("   ✅ Account created!")
        
        # 4. دریافت توکن
        token_response = requests.post(
            "https://api.mail.tm/token",
            json={
                "address": email,
                "password": password
            }
        )
        
        if token_response.status_code != 200:
            print(f"   ❌ Failed to get token: {token_response.status_code}")
            return None
        
        token_data = token_response.json()
        token = token_data.get('token', '')
        account_id = token_data.get('id', '')
        
        # 5. ذخیره اطلاعات
        info = {
            "email": email,
            "password": password,
            "token": token,
            "account_id": account_id,
            "domain": domain
        }
        
        # ذخیره به صورت JSON برای استفاده بعدی
        with open("email_info.json", "w") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        # ذخیره به صورت متن ساده
        with open("email_info.txt", "w") as f:
            f.write("=== Temporary Email Info ===\n")
            f.write(f"Email: {email}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Token: {token}\n")
            f.write(f"Account ID: {account_id}\n")
            f.write(f"Domain: {domain}\n")
        
        print("   💾 Email info saved to email_info.txt")
        print(f"   ✅ Email: {email}")
        
        return info
        
    except Exception as e:
        print(f"   ❌ Error creating email: {e}")
        return None

# =============================================
# ===== تنظیمات مرورگر =====
# =============================================

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# =============================================
# ===== توابع =====
# =============================================

def wait_for_page_load(driver, timeout=10):
    """منتظر بارگذاری کامل صفحه"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✅ Page loaded completely")
        return True
    except:
        print("⚠️ Page load timeout, continuing anyway")
        return False

def click_at(driver, x, y, label=""):
    """کلیک در مختصات مشخص"""
    try:
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().perform()
        print(f"✅ Clicked at ({x}, {y}) {label}")
        return True
    except:
        try:
            result = driver.execute_script(f"""
                var element = document.elementFromPoint({x}, {y});
                if (element) {{
                    element.click();
                    element.focus();
                    return true;
                }}
                return false;
            """)
            if result:
                print(f"✅ Clicked at ({x}, {y}) with JavaScript {label}")
                return True
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False

def type_text(driver, text, label=""):
    """تایپ کردن در فیلد فعال"""
    try:
        driver.execute_script("document.activeElement.click();")
        time.sleep(0.3)
        actions = ActionChains(driver)
        actions.send_keys(text).perform()
        print(f"✅ Typed: '{text}' {label}")
        return True
    except:
        try:
            driver.execute_script(f"""
                var activeElement = document.activeElement;
                if (activeElement) {{
                    activeElement.value = '{text}';
                    var event = new Event('input', {{ bubbles: true }});
                    activeElement.dispatchEvent(event);
                    var changeEvent = new Event('change', {{ bubbles: true }});
                    activeElement.dispatchEvent(changeEvent);
                }}
            """)
            print(f"✅ Typed: '{text}' with JavaScript {label}")
            return True
        except Exception as e:
            print(f"❌ Type failed: {e}")
            return False

def wait(seconds, label=""):
    """انتظار با لاگ"""
    if label:
        print(f"⏳ Waiting {seconds} seconds {label}...")
    else:
        print(f"⏳ Waiting {seconds} seconds ...")
    time.sleep(seconds)

def take_screenshot(driver, name, timestamp, crop_area=None):
    """گرفتن اسکرین‌شات کامل یا برش خورده"""
    filename = f"{name}_{timestamp}.png"
    
    if crop_area:
        driver.save_screenshot(filename)
        try:
            from PIL import Image
            img = Image.open(filename)
            cropped = img.crop(crop_area)
            cropped.save(filename)
            print(f"📸 Cropped screenshot saved: {filename}")
        except ImportError:
            print(f"📸 Full screenshot saved: {filename} (PIL not installed)")
    else:
        driver.save_screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")
    
    return filename

# =============================================
# ===== اجرای اصلی =====
# =============================================

driver = None
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

try:
    print("=" * 70)
    print("🚀 Starting...")
    print("=" * 70)
    
    # ===== مرحله 1: ساخت ایمیل موقت =====
    email_info = create_temporary_email()
    
    if not email_info:
        print("❌ Failed to create temporary email!")
        exit(1)
    
    EMAIL = email_info['email']
    print(f"\n📧 Using email: {EMAIL}")
    
    # ===== مرحله 2: راه‌اندازی مرورگر =====
    print("\n" + "=" * 70)
    print("🚀 Starting browser...")
    print("=" * 70)
    
    driver = webdriver.Chrome(options=options)
    
    print(f"\n🌐 Opening {TARGET_URL}...")
    driver.get(TARGET_URL)
    
    wait_for_page_load(driver)
    wait(2)
    
    driver.execute_script("window.scrollTo(0, 0);")
    wait(1)
    
    # ===== مرحله 3: کلیک اول =====
    print(f"\n🖱️ Step 1: Click at ({CLICK_1_X}, {CLICK_1_Y})")
    click_at(driver, CLICK_1_X, CLICK_1_Y, "(First click)")
    wait(4, "after first click")
    
    # ===== مرحله 4: کلیک دوم + تایپ =====
    print(f"\n🖱️ Step 2: Click at ({CLICK_2_X}, {CLICK_2_Y})")
    click_at(driver, CLICK_2_X, CLICK_2_Y, "(Click for password)")
    wait(1)
    type_text(driver, TEXT_4, "(Password)")  # استفاده از TEXT_4 به جای TEXT_1
    wait(1)
    
    take_screenshot(driver, f"typing_password", timestamp, crop_area=(800, 250, 1100, 350))
    wait(1)
    
    # ===== مرحله 5: کلیک سوم + تایپ ایمیل =====
    print(f"\n🖱️ Step 3: Click at ({CLICK_3_X}, {CLICK_3_Y})")
    click_at(driver, CLICK_3_X, CLICK_3_Y, "(Click for email)")
    wait(1)
    type_text(driver, EMAIL, "(Email - from Mail.tm)")
    wait(1)
    
    take_screenshot(driver, f"typing_email", timestamp, crop_area=(800, 350, 1100, 450))
    wait(1)
    
    # ===== مرحله 6: کلیک چهارم + تایپ یوزرنیم =====
    print(f"\n🖱️ Step 4: Click at ({CLICK_4_X}, {CLICK_4_Y})")
    click_at(driver, CLICK_4_X, CLICK_4_Y, "(Click for username)")
    wait(1)
    type_text(driver, TEXT_3, "(Username)")
    wait(1)
    
    take_screenshot(driver, f"typing_username", timestamp, crop_area=(800, 450, 1100, 550))
    wait(1)
    
    # ===== مرحله 7: کلیک پنجم + تایپ (تکرار پسورد) =====
    print(f"\n🖱️ Step 5: Click at ({CLICK_5_X}, {CLICK_5_Y})")
    click_at(driver, CLICK_5_X, CLICK_5_Y, "(Click for confirm password)")
    wait(1)
    type_text(driver, TEXT_4, "(Confirm Password)")
    wait(1)
    
    take_screenshot(driver, f"typing_confirm_password", timestamp, crop_area=(800, 550, 1100, 650))
    wait(1)
    
    # ===== مرحله 8: کلیک نهایی =====
    print(f"\n🖱️ Step 6: Final click at ({CLICK_6_X}, {CLICK_6_Y})")
    click_at(driver, CLICK_6_X, CLICK_6_Y, "(Final click - Submit)")
    wait(4, "after final click")
    
    final_screenshot = take_screenshot(driver, f"final", timestamp)
    
    print("\n" + "=" * 70)
    print("✅ ALL DONE!")
    print("=" * 70)
    print(f"📧 Email used: {EMAIL}")
    print(f"🔑 Password used: {TEXT_4}")
    print(f"👤 Username used: {TEXT_3}")
    print("\n📸 Screenshots taken:")
    print(f"   1. typing_password_{timestamp}.png")
    print(f"   2. typing_email_{timestamp}.png")
    print(f"   3. typing_username_{timestamp}.png")
    print(f"   4. typing_confirm_password_{timestamp}.png")
    print(f"   5. final_{timestamp}.png")
    
    print(f"\n💾 Email info saved to email_info.txt and email_info.json")
    
except Exception as e:
    print(f"❌ Error: {e}")
    if driver:
        driver.save_screenshot(f"error_{timestamp}.png")
    import traceback
    traceback.print_exc()
    
finally:
    if driver:
        driver.quit()
        print("👋 Browser closed")
