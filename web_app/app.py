"""
IngredientsNetwork Data Explorer Web Application
Bonus Challenge - Relu Consultancy Hiring Challenge

Features:
- Live interactive dashboard of scraped data
- Tabular display with sorting, searching, pagination
- Detail modal for each supplier
- Dynamic Supabase / CSV data source support
- Export to CSV / JSON
"""

import os
import json
import pandas as pd
import requests
from flask import Flask, render_template, jsonify, send_file, request

app = Flask(__name__)

DATA_CSV_PATH = os.path.join(os.path.dirname(__file__), "results.csv")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def load_data():
    """
    Loads data dynamically from Supabase if configured,
    otherwise loads from the cleaned results.csv dataset.
    """
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            endpoint = f"{SUPABASE_URL.rstrip('/')}/rest/v1/suppliers?select=*"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            res = requests.get(endpoint, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    return df.to_dict(orient="records"), "Supabase Database"
        except Exception as e:
            print(f"[!] Warning: Failed to fetch from Supabase ({e}), falling back to CSV.")

    # Fallback to CSV
    if os.path.exists(DATA_CSV_PATH):
        df = pd.read_csv(DATA_CSV_PATH).fillna("Not Available")
        return df.to_dict(orient="records"), "Cleaned CSV File"
    return [], "No Data Source Found"


METRICS = {
    "total_scraped": 288,
    "total_ingredients": "41,000+",
    "total_finished_products": "21,000+",
    "herbs_spices_companies": 399,
    "physical_formats_companies": 764,
    "cognitive_mental_health_companies": 587
}


@app.route("/")
def index():
    records, source_name = load_data()
    return render_template(
        "index.html",
        suppliers=records,
        source=source_name,
        metrics=METRICS,
        total_count=len(records)
    )


@app.route("/api/suppliers")
def api_suppliers():
    records, source_name = load_data()
    return jsonify({
        "status": "success",
        "data_source": source_name,
        "count": len(records),
        "data": records
    })


@app.route("/api/metrics")
def api_metrics():
    return jsonify({
        "status": "success",
        "metrics": METRICS
    })


@app.route("/download/csv")
def download_csv():
    if os.path.exists(DATA_CSV_PATH):
        return send_file(DATA_CSV_PATH, as_attachment=True, download_name="ingredientsnetwork_results.csv")
    return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
