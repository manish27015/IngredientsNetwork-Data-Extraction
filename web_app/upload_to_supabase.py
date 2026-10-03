"""
Upload Cleaned Scraped Data to Supabase Table
Relu Consultancy Hiring Challenge - Bonus Challenge

Usage:
    export SUPABASE_URL="https://your-project.supabase.co"
    export SUPABASE_KEY="your-anon-or-service-role-key"
    python upload_to_supabase.py
"""

import os
import sys
import pandas as pd
import requests

def upload_data():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("[!] SUPABASE_URL and SUPABASE_KEY environment variables are required.")
        print("    Example:")
        print("    set SUPABASE_URL=https://xyzcompany.supabase.co")
        print("    set SUPABASE_KEY=eyJhbGciOi...")
        print("    python upload_to_supabase.py")
        sys.exit(1)

    csv_path = os.path.join(os.path.dirname(__file__), "results.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results.csv")
    
    if not os.path.exists(csv_path):
        print(f"[!] Error: results.csv not found at {csv_path}")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    print(f"[*] Loaded {len(df)} records from {csv_path}")

    # Map CSV column names to Supabase table column names
    col_map = {
        "Company Name": "company_name",
        "Company Description": "company_description",
        "Sales Markets": "sales_markets",
        "Primary Business Activity": "primary_business_activity",
        "Categories": "categories",
        "Events": "events",
        "Address": "address",
        "Email": "email",
        "Telephone": "telephone",
        "Website": "website",
        "Profile URL": "profile_url"
    }
    
    records = []
    for _, row in df.iterrows():
        rec = {col_map[k]: (None if str(row[k]) == "Not Available" else str(row[k])) for k in col_map if k in row}
        records.append(rec)
        
    print(f"[*] Sending batch upload to Supabase endpoint: {supabase_url}/rest/v1/suppliers ...")
    endpoint = f"{supabase_url.rstrip('/')}/rest/v1/suppliers"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # Upload in chunks of 50
    chunk_size = 50
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i+chunk_size]
        res = requests.post(endpoint, json=chunk, headers=headers)
        if res.status_code in [200, 201]:
            print(f"    Uploaded {i+len(chunk)}/{len(records)} records successfully.")
        else:
            print(f"[!] Failed chunk {i}: {res.status_code} - {res.text}")
            
    print("[+] Supabase upload process completed.")

if __name__ == "__main__":
    upload_data()
