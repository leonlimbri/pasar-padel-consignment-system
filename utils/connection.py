import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

# Connect to the database
DB_URL = os.getenv("DB_SUPABASE_URL")
DB_KEY = os.getenv("DB_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
CLIENT = create_client(DB_URL, DB_KEY)

print(f"Connected to Supabase at {DB_URL}")
test_response = (CLIENT.table("CONSIGNMENTS").select("*").limit(1).execute())
print(test_response)