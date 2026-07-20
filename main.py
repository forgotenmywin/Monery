# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import os
import random
import requests
import base64
import zipfile

# ============== تنظیمات ==============
TARGET_URL = "https://greenlin.top/?ref=41446"
BASE_EMAIL = "melticekni@necub.com"
BASE_PASSWORD = "sdlfjksdldfskj"

# ===== تنظیمات Webshare =====
WEBSHARE_API_KEY = os.environ.get("WEBSHARE_API_KEY") or ""

if not WEBSHARE_API_KEY:
    print("=" * 70)
    print("❌ ERROR: WEBSHARE_API_KEY environment variable is not set!")
    print("=" * 70)
    exit(1)
print(f"✅ WEBSHARE_API_KEY is set (length: {len(WEBSHARE_API_KEY)})")

# ===== نام فایل‌ها =====
USED_EMAILS_FILE = "whroted.txt"
PROXY_FILE = "used_proxies.txt"
PASSWORDS_FILE = "used_passwords.txt"

# =============================================
# ===== اطلاعات GitHub =====
# =============================================

GITHUB_REPO = "forgotenmywin/Monery"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN") or ""

if not GITHUB_TOKEN:
    print("=" * 70)
    print("❌ ERROR: MY_GITHUB_TOKEN environment variable is not set!")
    print("=" * 70)
    exit(1)

print(f"✅ MY_GITHUB_TOKEN is set (length: {len(GITHUB_TOKEN)})")

# ===== لینک‌های GitHub =====
GITHUB_WHROTED_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USED_EMAILS_FILE}"
GITHUB_PROXY_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{PROXY_FILE}"
GITHUB_PASSWORDS_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{PASSWORDS_FILE}"

# =============================================
# ===== بخش ساخت فایل Password در GitHub =====
# =============================================

def ensure_password_file_exists():
    if not GITHUB_TOKEN:
        raise Exception("❌ MY_GITHUB_TOKEN is not set!")
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        response = requests.get(GITHUB_PASSWORDS_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Password file already exists on GitHub: {PASSWORDS_FILE}")
            return True
        elif response.status_code == 404:
            print(f"🆕 Password file not found on GitHub, creating: {PASSWORDS_FILE}")
            return create_password_file()
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking file: {e}")
        raise

def create_password_file():
    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "message": f"Create {PASSWORDS_FILE}",
            "content": base64.b64encode("".encode("utf-8")).decode("utf-8"),
            "branch": GITHUB_BRANCH
        }
        
        response = requests.put(GITHUB_PASSWORDS_URL, json=data, headers=headers, timeout=10)
        if response.status_code == 201:
            print(f"✅ Created password file on GitHub: {PASSWORDS_FILE}")
            return True
        else:
            print(f"⚠️ Failed to create password file: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating password file: {e}")
        return False

# =============================================
# ===== بخش کار با GitHub API =====
# =============================================

def get_file_from_github(file_url):
    if not GITHUB_TOKEN:
        raise Exception("❌ MY_GITHUB_TOKEN is not set!")
    
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        response = requests.get(file_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content, data["sha"]
        elif response.status_code == 404:
            return None, None
        else:
            return None, None
    except Exception as e:
        print(f"⚠️ Could not fetch from GitHub: {e}")
        return None, None

def update_file_on_github(file_url, content, sha=None, message="Update file"):
    if not GITHUB_TOKEN:
        raise Exception("❌ MY_GITHUB_TOKEN is not set!")
    
    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            "branch": GITHUB_BRANCH
        }
        
        if sha:
            data["sha"] = sha
        
        response = requests.put(file_url, json=data, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print(f"✅ File updated on GitHub: {file_url.split('/')[-1]}")
            return True
        else:
            print(f"⚠️ Failed to update file: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def append_to_github_file(file_url, new_line):
    content, sha = get_file_from_github(file_url)
    
    if content is None:
        return update_file_on_github(file_url, new_line + "\n", message=f"Create {file_url.split('/')[-1]}")
    else:
        new_content = content + new_line + "\n"
        return update_file_on_github(file_url, new_content, sha, message=f"Append to {file_url.split('/')[-1]}")

# =============================================
# ===== بخش مدیریت ایمیل‌ها =====
# =============================================

def fetch_used_emails_from_github():
    content, _ = get_file_from_github(GITHUB_WHROTED_URL)
    if content:
        used_emails = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"✅ Found {len(used_emails)} used emails from GitHub")
        return used_emails
    else:
        print(f"ℹ️ No used emails file on GitHub yet")
        return []

def save_used_email_to_github(email):
    success = append_to_github_file(GITHUB_WHROTED_URL, email)
    if success:
        print(f"💾 Email saved to GitHub: {email}")

def get_next_email():
    used_emails = fetch_used_emails_from_github()
    
    if '@' in BASE_EMAIL:
        username, domain = BASE_EMAIL.split('@')
    else:
        return BASE_EMAIL
    
    max_num = 0
    for email in used_emails:
        if '@' in email:
            used_username = email.split('@')[0]
            if used_username.startswith(username):
                suffix = used_username[len(username):]
                if suffix.isdigit():
                    num = int(suffix)
                    if num > max_num:
                        max_num = num
    
    new_email = f"{username}{max_num + 1}@{domain}"
    print(f"📧 Generated new email: {new_email}")
    return new_email

# =============================================
# ===== بخش مدیریت پروکسی‌ها =====
# =============================================

def test_proxy(proxy_url):
    """تست پروکسی قبل از استفاده"""
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        if response.status_code == 200:
            print(f"✅ Proxy works! IP: {response.json()['origin']}")
            return True
        else:
            print(f"❌ Proxy failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
        return False

def get_webshare_proxies(api_key, limit=20):
    """
    دریافت لیست پروکسی‌های فعال از Webshare
    """
    try:
        headers = {"Authorization": f"Token {api_key}"}
        response = requests.get(
            f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size={limit}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            proxies = []
            for proxy in data.get("results", []):
                # ساخت آدرس پروکسی به فرمت: username:password@ip:port
                proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}"
                proxies.append({
                    'url': proxy_url,
                    'host': proxy['proxy_address'],
                    'port': proxy['port'],
                    'username': proxy['username'],
                    'password': proxy['password']
                })
            
            print(f"✅ دریافت {len(proxies)} پروکسی از Webshare")
            return proxies
        else:
            print(f"❌ خطا در دریافت پروکسی: {response.status_code}")
            if response.status_code == 401:
                print("   ⚠️ API Key نامعتبر است! لطفاً کلید را بررسی کنید.")
            return []
    except Exception as e:
        print(f"❌ خطا در دریافت پروکسی از Webshare: {e}")
        return []

def fetch_used_proxies_from_github():
    content, _ = get_file_from_github(GITHUB_PROXY_URL)
    if content:
        used_proxies = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"✅ Found {len(used_proxies)} used proxies from GitHub")
        return used_proxies
    else:
        print(f"ℹ️ No used proxies file on GitHub yet")
        return []

def save_used_proxy_to_github(proxy):
    if proxy:
        success = append_to_github_file(GITHUB_PROXY_URL, proxy)
        if success:
            print(f"💾 Proxy saved to GitHub: {proxy[:50]}...")

def create_proxy_extension(proxy_host, proxy_port, username, password):
    """ساخت extension برای احراز هویت پروکسی"""
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }
    """
    
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};
    
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    
    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{username}",
                password: "{password}"
            }}
        }};
    }}
    
    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """
    
    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file

def get_unused_proxy():
    # دریافت پروکسی‌های جدید از Webshare
    print("📡 Fetching proxies from Webshare...")
    all_proxies = get_webshare_proxies(WEBSHARE_API_KEY, limit=20)
    
    if not all_proxies:
        print("ℹ️ No proxies received from Webshare, using direct connection")
        return None
    
    # دریافت پروکسی‌های استفاده شده از GitHub
    used_proxies = fetch_used_proxies_from_github()
    
    # فیلتر کردن پروکسی‌های استفاده نشده
    unused_proxies = [p for p in all_proxies if p['url'] not in used_proxies]
    
    if not unused_proxies:
        print("⚠️ No unused proxies available. All proxies have been used!")
        return None
    
    # تست پروکسی‌ها و انتخاب اولین پروکسی کارآمد
    print("🔍 Testing proxies...")
    for proxy in unused_proxies:
        print(f"   Testing: {proxy['host']}:{proxy['port']}")
        if test_proxy(proxy['url']):
            print(f"✅ Selected working proxy: {proxy['host']}:{proxy['port']}")
            return proxy
        else:
            print(f"   ❌ Proxy failed, trying next...")
    
    # اگر هیچ پروکسی کار نکرد، از اولین پروکسی استفاده کن
    print("⚠️ No working proxies found, using first proxy anyway")
    return unused_proxies[0]

# =============================================
# ===== بخش مدیریت پسوردها =====
# =============================================

def fetch_used_passwords_from_github():
    content, _ = get_file_from_github(GITHUB_PASSWORDS_URL)
    if content:
        used_passwords = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"✅ Found {len(used_passwords)} used passwords from GitHub")
        return used_passwords
    else:
        print(f"ℹ️ No used passwords file on GitHub yet")
        return []

def save_used_password_to_github(password):
    success = append_to_github_file(GITHUB_PASSWORDS_URL, password)
    if success:
        print(f"💾 Password saved to GitHub: {password}")

def get_next_password():
    used_passwords = fetch_used_passwords_from_github()
    
    max_num = 0
    for pwd in used_passwords:
        if pwd.startswith(BASE_PASSWORD):
            suffix = pwd[len(BASE_PASSWORD):]
            if suffix.isdigit():
                num = int(suffix)
                if num > max_num:
                    max_num = num
    
    new_password = f"{BASE_PASSWORD}{max_num + 1}"
    print(f"🔑 Generated new password: {new_password}")
    return new_password

# =============================================
# ===== ساخت فایل Password =====
# =============================================

print("=" * 70)
print("📁 CHECKING PASSWORD FILE ON GITHUB")
print("=" * 70)

file_created = ensure_password_file_exists()
if not file_created:
    print("❌ Failed to create used_passwords.txt on GitHub")
    exit(1)

print("✅ Password file checked/created successfully!")
print("=" * 70)

# =============================================
# ===== تولید مقادیر جدید =====
# =============================================

SELECTED_EMAIL = get_next_email()
SELECTED_PROXY = get_unused_proxy()
SELECTED_PASSWORD = get_next_password()

# ===== مختصات =====
CLICK_1_X = 1213
CLICK_1_Y = 70
CLICK_2_X = 803
CLICK_2_Y = 613
CLICK_3_X = 902
CLICK_3_Y = 680
CLICK_4_X = 823
CLICK_4_Y = 743
CLICK_5_X = 1014
CLICK_5_Y = 842

# ===== متن‌ها =====
TEXT_1 = SELECTED_PASSWORD
TEXT_2 = SELECTED_EMAIL
TEXT_3 = "kingking0000"

# =============================================
# ===== اجرای اصلی با Chromium =====
# =============================================

print("=" * 70)
print("📊 CHECKING USED ITEMS FROM GITHUB")
print("=" * 70)

used_emails = fetch_used_emails_from_github()
used_proxies = fetch_used_proxies_from_github()
used_passwords = fetch_used_passwords_from_github()

print(f"\n📊 SUMMARY:")
print(f"   📧 Used emails: {len(used_emails)}")
if used_emails:
    print(f"   📌 Last used email: {used_emails[-1]}")
print(f"   🔒 Used proxies: {len(used_proxies)}")
if used_proxies:
    print(f"   🔌 Last used proxy: {used_proxies[-1][:50]}...")
print(f"   🔑 Used passwords: {len(used_passwords)}")
if used_passwords:
    print(f"   📌 Last used password: {used_passwords[-1]}")

print("=" * 70)
print(f"📧 New Email: {SELECTED_EMAIL}")
print(f"🔑 New Password: {SELECTED_PASSWORD}")
if SELECTED_PROXY:
    print(f"🔒 Selected Proxy: {SELECTED_PROXY['host']}:{SELECTED_PROXY['port']}")
else:
    print(f"🔓 No proxy selected (direct connection)")
print("=" * 70)

# ====================================
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = "/usr/bin/chromium-browser"

# تنظیم پروکسی با احراز هویت
if SELECTED_PROXY:
    print(f"🔧 Setting up proxy: {SELECTED_PROXY['host']}:{SELECTED_PROXY['port']}")
    
    # ساخت extension برای احراز هویت
    proxy_plugin = create_proxy_extension(
        SELECTED_PROXY['host'],
        SELECTED_PROXY['port'],
        SELECTED_PROXY['username'],
        SELECTED_PROXY['password']
    )
    options.add_extension(proxy_plugin)
    print(f"✅ Proxy extension created and added")
else:
    print("🔧 Using direct connection (no proxy)")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def click_at_coordinates(driver, x, y, label=""):
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

def click_and_type(driver, x, y, text, label=""):
    click_at_coordinates(driver, x, y, label)
    time.sleep(0.5)
    return type_text(driver, text, label)

def wait_seconds(seconds):
    print(f"\n⏳ Waiting {seconds} seconds...")
    for i in range(seconds, 0, -1):
        print(f"   {i}s remaining...", end="\r")
        time.sleep(1)
    print("\n✅ Wait complete!")

def take_screenshot(filename, timestamp):
    screenshot_path = f"{filename}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot: {screenshot_path}")
    return screenshot_path

# ========== اجرای اصلی ==========
try:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    print("=" * 70)
    print(f"🌐 Opening {TARGET_URL}...")
    print("=" * 70)
    
    driver.get(TARGET_URL)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    print(f"\n🖱️ Step 1: Click at ({CLICK_1_X}, {CLICK_1_Y})")
    click_at_coordinates(driver, CLICK_1_X, CLICK_1_Y, "(Step 1)")
    wait_seconds(10)
    
    print(f"\n🖱️ Step 3 & 4: Click at ({CLICK_2_X}, {CLICK_2_Y})")
    click_and_type(driver, CLICK_2_X, CLICK_2_Y, TEXT_1, "(Step 3-4 - Password)")
    wait_seconds(4)
    
    print(f"\n🖱️ Step 6 & 7: Click at ({CLICK_3_X}, {CLICK_3_Y})")
    click_and_type(driver, CLICK_3_X, CLICK_3_Y, TEXT_2, "(Step 6-7 - Email)")
    
    save_used_email_to_github(TEXT_2)
    save_used_password_to_github(TEXT_1)
    if SELECTED_PROXY:
        save_used_proxy_to_github(SELECTED_PROXY['url'])
    
    screenshot_after_email = take_screenshot("after_email", timestamp)
    wait_seconds(4)
    
    print(f"\n🖱️ Step 9 & 10: Click at ({CLICK_4_X}, {CLICK_4_Y})")
    click_and_type(driver, CLICK_4_X, CLICK_4_Y, TEXT_3, "(Step 9-10 - Username)")
    
    print("\n⏳ Waiting 3 seconds before final click...")
    for i in range(3, 0, -1):
        print(f"   {i}s remaining...", end="\r")
        time.sleep(1)
    print("\n✅ Wait complete!")
    
    print(f"\n🖱️ Step 12: Click at ({CLICK_5_X}, {CLICK_5_Y})")
    click_at_coordinates(driver, CLICK_5_X, CLICK_5_Y, "(Step 12 - Final)")
    
    print("\n⏳ Waiting 4 seconds for final screenshot...")
    for i in range(4, 0, -1):
        print(f"   {i}s remaining...", end="\r")
        time.sleep(1)
    print("\n✅ Wait complete!")
    
    final_screenshot = take_screenshot("final_screenshot", timestamp)
    
    print("\n" + "=" * 70)
    print("✅ ALL DONE!")
    print("=" * 70)
    print("📸 SCREENSHOTS:")
    print(f"   1. 📸 after_email_{timestamp}.png")
    print(f"   2. 📸 final_screenshot_{timestamp}.png")
    
except Exception as e:
    print(f"❌ Error: {e}")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    driver.save_screenshot(f"error_{timestamp}.png")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    # حذف فایل proxy extension بعد از اجرا
    if os.path.exists("proxy_auth_plugin.zip"):
        os.remove("proxy_auth_plugin.zip")
        print("🧹 Cleaned up proxy extension file")
    print("👋 Browser closed")
