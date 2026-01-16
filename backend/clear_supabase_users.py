"""
Script to clear all users from Supabase Authentication.
This syncs Supabase Auth with your local database after truncation.
"""

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://dcjsmglxckhllafocexe.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Need service role key

if not SUPABASE_SERVICE_KEY:
    print("❌ Error: SUPABASE_SERVICE_ROLE_KEY not found in .env")
    print()
    print("To fix this:")
    print("1. Go to your Supabase Dashboard")
    print("2. Settings → API")
    print("3. Copy the 'service_role' key (NOT the anon key)")
    print("4. Add to backend/.env:")
    print("   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here")
    print()
    print("⚠️  Alternative: Manually delete users in Supabase Dashboard")
    print("   Go to: Authentication → Users → Delete each user")
    exit(1)

def clear_supabase_users():
    """Delete all users from Supabase Auth."""
    
    try:
        # Create Supabase client with service role key
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        print("🔍 Fetching users from Supabase Auth...")
        
        # Get all users (requires service role key)
        response = supabase.auth.admin.list_users()
        users = response if isinstance(response, list) else []
        
        if not users:
            print("✅ No users found in Supabase Auth")
            return
        
        print(f"Found {len(users)} user(s)")
        print()
        
        # Delete each user
        deleted_count = 0
        for user in users:
            user_id = user.id if hasattr(user, 'id') else user.get('id')
            user_email = user.email if hasattr(user, 'email') else user.get('email')
            
            try:
                supabase.auth.admin.delete_user(user_id)
                print(f"  ✓ Deleted: {user_email}")
                deleted_count += 1
            except Exception as e:
                print(f"  ✗ Failed to delete {user_email}: {e}")
        
        print()
        print(f"✅ Successfully deleted {deleted_count} user(s) from Supabase Auth")
        print("You can now sign up with fresh accounts!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("If you don't have the service role key, manually delete users:")
        print("1. Go to: https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Authentication → Users")
        print("4. Delete each user manually")

if __name__ == "__main__":
    print("⚠️  This will delete ALL users from Supabase Authentication!")
    print("This is necessary after truncating the local database.")
    print()
    response = input("Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        clear_supabase_users()
    else:
        print("Operation cancelled.")
