import requests
import json
import os
import sys

# Path to .env.local
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.local')

def get_env_vars():
    vars = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle quoted values
                    key, value = line.split('=', 1)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    vars[key] = value
    return vars

def debug_auth():
    env = get_env_vars()
    url = env.get('NEXT_PUBLIC_SUPABASE_URL')
    key = env.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("❌ Could not find Supabase credentials in .env.local")
        return

    print(f"✅ Found Supabase URL: {url}")
    print(f"✅ Found Anon Key: {key[:10]}...")

    # 1. Login/Signup
    auth_url = f"{url}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": key,
        "Content-Type": "application/json"
    }
    
    # ... (imports stay same) ...

    # Try multiple credentials
    creds = [
        ("test@example.com", "password123"),
        ("user@example.com", "password123"),
        ("test@test.com", "password")
    ]
    
    access_token = None
    
    for email, password in creds:
        print(f"\n🔄 Attempting login for {email}...")
        response = requests.post(auth_url, headers=headers, json={"email": email, "password": password})
        
        if response.status_code == 200:
            print(f"✅ Login successful for {email}!")
            access_token = response.json().get("access_token")
            break
        else:
            print(f"⚠️ Login failed: {response.text}")
    
    if not access_token:
        # Try signup one last time with a random email
        import random
        rand_email = f"debug_{random.randint(1000,9999)}@example.com"
        print(f"\n🔄 Attempting signup for {rand_email}...")
        signup_url = f"{url}/auth/v1/signup"
        response = requests.post(signup_url, headers=headers, json={"email": rand_email, "password": "password123"})
        
        if response.status_code == 200:
            print("✅ Signup request sent! Checking response...")
            # Sometimes signup returns session immediately, sometimes requires email confirmation
            data = response.json()
            if data.get("access_token"):
                 access_token = data.get("access_token")
                 print("✅ Got token from signup!")
            else:
                 print("⚠️ Signup successful but no token (Email confirmation likely required):", response.text)
        else:
            print(f"❌ Signup failed: {response.text}")

    if not access_token:
        print("\n❌ Could not get an access token. Cannot test backend.")
        return

    # ... (rest of backend test stays similar) ...
    # 2. Test Backend
    backend_url = "https://zuno-production-production.up.railway.app"
    print(f"\n🔄 Testing Backend: {backend_url}/daily-plan")
    
    backend_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Try a protected route
    try:
        response = requests.get(f"{backend_url}/daily-plan", headers=backend_headers)
        
        print(f"\n📊 Backend Response Status: {response.status_code}")
        print(f"📄 Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS: Backend accepted the token!")
        else:
            print("\n❌ FAILURE: Backend rejected the token.")
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        
    # 3. Decode Token (Manual)
    parts = access_token.split('.')
    if len(parts) == 3:
        try:
            header = json.loads(base64_decode(parts[0]))
            payload = json.loads(base64_decode(parts[1]))
            print("\n🔍 Token Details:")
            print(f"   Algorithm: {header.get('alg')}")
            print(f"   Issuer: {payload.get('iss')}")
            print(f"   Expiry: {payload.get('exp')}")
            print(f"   Subject: {payload.get('sub')}")
        except Exception as e:
            print(f"Error decoding token: {e}")

def base64_decode(data):
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    import base64
    return base64.urlsafe_b64decode(data).decode('utf-8')

if __name__ == "__main__":
    # Redirect output to file
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        debug_auth()
    # Restore stdout
    sys.stdout = sys.__stdout__
    print("Execution complete. Check debug_output.txt")

