# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

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

# ===== متن‌ها برای تایپ =====
TEXT_1 = "kljwefowijowe"
TEXT_2 = "sdlkfjwoidfj@fslkdjf.com"
TEXT_3 = "kingking000"
TEXT_4 = "kingking000"

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
    print(f"⏳ Waiting {seconds} seconds {label}...")
    time.sleep(seconds)

def take_screenshot(driver, name, timestamp, crop_area=None):
    """گرفتن اسکرین‌شات کامل یا برش خورده"""
    filename = f"{name}_{timestamp}.png"
    
    if crop_area:
        # گرفتن اسکرین‌شات کامل و برش
        driver.save_screenshot(filename)
        # برش با استفاده از PIL (اگر نصب باشه)
        try:
            from PIL import Image
            img = Image.open(filename)
            # crop_area: (x1, y1, x2, y2)
            cropped = img.crop(crop_area)
            cropped.save(filename)
            print(f"📸 Cropped screenshot saved: {filename}")
        except:
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
    print("🚀 Starting browser...")
    print("=" * 70)
    
    driver = webdriver.Chrome(options=options)
    
    print(f"\n🌐 Opening {TARGET_URL}...")
    driver.get(TARGET_URL)
    
    # منتظر بارگذاری کامل صفحه
    wait_for_page_load(driver)
    wait(2)
    
    # اسکرول به بالای صفحه
    driver.execute_script("window.scrollTo(0, 0);")
    wait(1)
    
    # ===== کلیک اول =====
    print(f"\n🖱️ Step 1: Click at ({CLICK_1_X}, {CLICK_1_Y})")
    click_at(driver, CLICK_1_X, CLICK_1_Y, "(First click)")
    wait(4, "after first click")
    
    # ===== کلیک دوم + تایپ =====
    print(f"\n🖱️ Step 2: Click at ({CLICK_2_X}, {CLICK_2_Y})")
    click_at(driver, CLICK_2_X, CLICK_2_Y, "(Click for text 1)")
    wait(1)
    type_text(driver, TEXT_1, "(Text 1)")
    wait(1)
    
    # گرفتن اسکرین‌شات از بخش تایپ شده (مختصات حدودی)
    take_screenshot(driver, f"typing_1_{timestamp}", timestamp, crop_area=(800, 250, 1100, 350))
    wait(1)
    
    # ===== کلیک سوم + تایپ =====
    print(f"\n🖱️ Step 3: Click at ({CLICK_3_X}, {CLICK_3_Y})")
    click_at(driver, CLICK_3_X, CLICK_3_Y, "(Click for text 2)")
    wait(1)
    type_text(driver, TEXT_2, "(Text 2 - Email)")
    wait(1)
    
    # گرفتن اسکرین‌شات از بخش تایپ شده
    take_screenshot(driver, f"typing_2_{timestamp}", timestamp, crop_area=(800, 350, 1100, 450))
    wait(1)
    
    # ===== کلیک چهارم + تایپ =====
    print(f"\n🖱️ Step 4: Click at ({CLICK_4_X}, {CLICK_4_Y})")
    click_at(driver, CLICK_4_X, CLICK_4_Y, "(Click for text 3)")
    wait(1)
    type_text(driver, TEXT_3, "(Text 3 - Username)")
    wait(1)
    
    # گرفتن اسکرین‌شات از بخش تایپ شده
    take_screenshot(driver, f"typing_3_{timestamp}", timestamp, crop_area=(800, 450, 1100, 550))
    wait(1)
    
    # ===== کلیک پنجم + تایپ =====
    print(f"\n🖱️ Step 5: Click at ({CLICK_5_X}, {CLICK_5_Y})")
    click_at(driver, CLICK_5_X, CLICK_5_Y, "(Click for text 4)")
    wait(1)
    type_text(driver, TEXT_4, "(Text 4 - Password)")
    wait(1)
    
    # گرفتن اسکرین‌شات از بخش تایپ شده
    take_screenshot(driver, f"typing_4_{timestamp}", timestamp, crop_area=(800, 550, 1100, 650))
    wait(1)
    
    # ===== کلیک ششم (نهایی) =====
    print(f"\n🖱️ Step 6: Final click at ({CLICK_6_X}, {CLICK_6_Y})")
    click_at(driver, CLICK_6_X, CLICK_6_Y, "(Final click)")
    wait(4, "after final click")
    
    # اسکرین‌شات نهایی
    final_screenshot = take_screenshot(driver, f"final_{timestamp}", timestamp)
    
    print("\n" + "=" * 70)
    print("✅ ALL DONE!")
    print("=" * 70)
    print("📸 Screenshots taken:")
    print(f"   1. typing_1_{timestamp}.png (Text 1)")
    print(f"   2. typing_2_{timestamp}.png (Text 2 - Email)")
    print(f"   3. typing_3_{timestamp}.png (Text 3 - Username)")
    print(f"   4. typing_4_{timestamp}.png (Text 4 - Password)")
    print(f"   5. final_{timestamp}.png (Final page)")
    
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
