# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

TARGET_URL = "https://example.com"

options = Options()
options.add_argument('--headless')  # برای GitHub Actions لازمه
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

driver = None

try:
    print("=" * 70)
    print("🚀 Starting browser...")
    print("=" * 70)
    
    driver = webdriver.Chrome(options=options)
    
    print(f"\n🌐 Opening {TARGET_URL}...")
    driver.get(TARGET_URL)
    time.sleep(3)
    
    print("\n✅ Page loaded!")
    
    # گرفتن اسکرین‌شات
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")
    
    # گرفتن title صفحه
    title = driver.title
    print(f"📄 Page title: {title}")
    
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
