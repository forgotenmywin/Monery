import requests
import time
import json
import os

def create_email():
    try:
        # 1. دریافت دامنه
        print("📡 دریافت دامنه...")
        response = requests.get("https://api.mail.tm/domains")
        domains = response.json()
        domain = domains['hydra:member'][0]['domain']
        print(f"✅ دامنه: {domain}")
        
        # 2. ساخت ایمیل یکتا
        timestamp = int(time.time())
        email = f"user_{timestamp}@{domain}"
        password = "MyPass123!"
        print(f"📧 ایمیل: {email}")
        print(f"🔑 رمز: {password}")
        
        # 3. ثبت حساب
        print("🔄 در حال ثبت حساب...")
        account_data = {
            "address": email,
            "password": password
        }
        
        response = requests.post(
            "https://api.mail.tm/accounts",
            json=account_data
        )
        
        if response.status_code == 201:
            print("✅ حساب با موفقیت ایجاد شد!")
            
            # 4. دریافت توکن
            print("🔄 دریافت توکن...")
            token_response = requests.post(
                "https://api.mail.tm/token",
                json={
                    "address": email,
                    "password": password
                }
            )
            
            if token_response.status_code == 200:
                token_data = token_response.json()
                token = token_data.get('token', '')
                account_id = token_data.get('id', '')
                print(f"✅ توکن دریافت شد: {token[:30]}...")
                
                # 5. ذخیره اطلاعات
                info = {
                    "email": email,
                    "password": password,
                    "token": token,
                    "account_id": account_id,
                    "domain": domain,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "service": "mail.tm"
                }
                
                # ذخیره به صورت JSON
                with open("email_info.json", "w") as f:
                    json.dump(info, f, indent=2, ensure_ascii=False)
                
                # ذخیره به صورت متن ساده
                with open("email_info.txt", "w") as f:
                    f.write("=== اطلاعات ایمیل موقت ===\n")
                    f.write(f"ایمیل: {email}\n")
                    f.write(f"رمز: {password}\n")
                    f.write(f"توکن: {token}\n")
                    f.write(f"ID حساب: {account_id}\n")
                    f.write(f"دامنه: {domain}\n")
                    f.write(f"ساخته شده: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                print("\n✅ اطلاعات ذخیره شد!")
                print(f"📁 email_info.json")
                print(f"📁 email_info.txt")
                
                return info
            else:
                print(f"❌ خطا در دریافت توکن: {token_response.status_code}")
                return None
        else:
            print(f"❌ خطا در ساخت حساب: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None

if __name__ == "__main__":
    create_email()
