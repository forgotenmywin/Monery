# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

TARGET_URL = "https://example.com"

# ===== مختصات کلیک =====
CLICK_X = 925
CLICK_Y = 867

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
# ===== تابع کلیک =====
# =============================================

def click_at_coordinates(driver, x, y):
    """کلیک کردن در مختصات مشخص"""
    try:
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().perform()
        print(f"✅ Clicked at ({x}, {y})")
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
                print(f"✅ Clicked at ({x}, {y}) with JavaScript")
                return True
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False

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
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    print(f"\n🖱️ Clicking at ({CLICK_X}, {CLICK_Y})...")
    click_at_coordinates(driver, CLICK_X, CLICK_Y)
    
    print("\n⏳ Waiting 4 seconds...")
    time.sleep(4)
    
    # گرفتن اسکرین‌شات
    screenshot_path = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")
    
    print("\n✅ DONE!")
    
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
