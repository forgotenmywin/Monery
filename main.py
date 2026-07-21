# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

TARGET_URL = "https://hashora.net/register?ref=KINGKINGPLM0073637"

# ===== مختصات کلیک =====
CLICK_X = 877
CLICK_Y = 929

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
# ===== توابع کلیک =====
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

def click_with_retry(driver, x, y, max_retries=3):
    """کلیک با چند بار تلاش"""
    for attempt in range(max_retries):
        try:
            # روش 1: کلیک با ActionChains
            actions = ActionChains(driver)
            actions.move_by_offset(x, y).click().perform()
            print(f"✅ Clicked at ({x}, {y}) - Method 1")
            return True
        except:
            try:
                # روش 2: کلیک با JavaScript
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
                    print(f"✅ Clicked at ({x}, {y}) - Method 2 (JavaScript)")
                    return True
            except:
                try:
                    # روش 3: کلیک با offset از عنصر اصلی
                    body = driver.find_element(By.TAG_NAME, "body")
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(body, x, y).click().perform()
                    print(f"✅ Clicked at ({x}, {y}) - Method 3 (Body offset)")
                    return True
                except Exception as e:
                    print(f"❌ Attempt {attempt + 1} failed: {e}")
                    time.sleep(1)
    
    print(f"❌ All {max_retries} attempts failed")
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
    
    # منتظر بارگذاری کامل صفحه
    wait_for_page_load(driver)
    time.sleep(2)
    
    # اسکرول به بالای صفحه
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    # بررسی وجود المان در مختصات
    element_at_point = driver.execute_script(f"""
        var element = document.elementFromPoint({CLICK_X}, {CLICK_Y});
        if (element) {{
            return {{
                tag: element.tagName,
                text: element.textContent.trim().substring(0, 50),
                id: element.id || 'no-id',
                class: element.className || 'no-class'
            }};
        }}
        return null;
    """)
    
    if element_at_point:
        print(f"🔍 Element at ({CLICK_X}, {CLICK_Y}):")
        print(f"   Tag: {element_at_point.get('tag')}")
        print(f"   Text: {element_at_point.get('text')}")
        print(f"   ID: {element_at_point.get('id')}")
        print(f"   Class: {element_at_point.get('class')}")
    else:
        print(f"⚠️ No element found at ({CLICK_X}, {CLICK_Y})")
    
    print(f"\n🖱️ Clicking at ({CLICK_X}, {CLICK_Y})...")
    click_success = click_with_retry(driver, CLICK_X, CLICK_Y)
    
    if not click_success:
        print("⚠️ Click failed, trying to click on the page anyway...")
        driver.execute_script("document.body.click();")
    
    print("\n⏳ Waiting 4 seconds...")
    time.sleep(4)
    
    # گرفتن اسکرین‌شات
    screenshot_path = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")
    
    # اطلاعات بیشتر برای دیباگ
    page_title = driver.title
    page_url = driver.current_url
    print(f"📄 Page title: {page_title}")
    print(f"🔗 Current URL: {page_url}")
    
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
