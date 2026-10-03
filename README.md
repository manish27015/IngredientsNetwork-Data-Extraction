# Relu Consultancy Hiring Challenge — Objective 2: IngredientsNetwork.com

This folder contains the complete project deliverables for the Full-Time Data Extraction Engineer Hiring Challenge.

---

## 1. Verified Answers to Analysis Questions

Enter these answers into the terminal output and the [Official Google Form](https://forms.gle/88e7tcW1boyZdL1y9):

| # | Question | Answer | Details / Source |
|---|---|:---:|---|
| **(i)** | **How many total ingredients are there? (count)** | **41,000+** | Official platform stats counter on [IngredientsNetwork.com](https://www.ingredientsnetwork.com/). *(In search facet database: 6,024 across 552 categories: 2,704 products, 2,419 companies)* |
| **(ii)** | **How many total finished products are there?** | **21,000+** | Official platform stats counter on [IngredientsNetwork.com](https://www.ingredientsnetwork.com/). *(In search facet database: 4,100 across 33 categories: 820 products, 2,198 companies)* |
| **(iii)** | **How many companies have herbs and spices?** | **399** | Category code `code016020` & search facet bit 413: `Suppliers (399)`. *(Subcategories: Herbs: 218, Spices: 243)* |
| **(iv)** | **How many companies have physical delivery formats?** | **764** | Category code `code016198` & search facet bit 649: `Suppliers (764)`. |
| **(v)** | **How many companies are in Cognitive & Mental Health?** | **587** *(or **590**)* | Search facet bit 671: **587** active suppliers; Landing page directory count on `code016162`: **590**. |

---

## 2. Deliverables & File Guide

- **`results.csv`**: The primary output file. Contains all 288 cleansed supplier records with all 10 required columns, zero missing values, and duplicates removed.
- **`raw_results.csv`**: Temporary raw dataset (291 records) collected prior to cleaning per Step 4.
- **`scrape_featured_suppliers.py`**: Production extraction & data cleaning pipeline script. Handles concurrent fetching, Cloudflare email de-obfuscation, data normalization, deduplication, and prints analysis answers.
- **`IngredientsNetwork_Scraper.ipynb`**: Google Colab Jupyter Notebook ready to upload to Colab to get a shareable link.
- **`browser_automation.py`**: Headless Playwright Chromium automation script verifying navigation, search entry, scrolling, and card DOM extraction.
- **`analysis_answers.json`**: Machine-readable JSON containing the verified answers to questions (i)–(v).
- **`web_app/`**: Full Bonus Challenge web application with Flask, responsive DataTables UI, Supabase integration schema & uploader, Dockerfile, and Procfile for cloud deployment.

---

## 3. How to Submit

1. **Google Colab Notebook Link**:
   - Go to [Google Colab](https://colab.research.google.com/).
   - Click **Upload** -> Select `IngredientsNetwork_Scraper.ipynb` from this folder.
   - Click **Share** (top right) -> Under General access, select **Anyone with the link can view** -> Click **Copy link**.
2. **Submit the Official Form**:
   - Open the form: [https://forms.gle/88e7tcW1boyZdL1y9](https://forms.gle/88e7tcW1boyZdL1y9).
   - Enter your Colab link.
   - Upload `results.csv`.
   - Enter the answers to questions (i)–(v) as listed in the table above.

---

## 4. How to Run Locally

### Run the Scraper:
```bash
python scrape_featured_suppliers.py
```

### Run the Playwright Browser Automation:
```bash
python browser_automation.py
```

### Run the Bonus Challenge Web Application:
```bash
cd web_app
python app.py
```
Open `http://localhost:5000` in your web browser to explore the interactive table, metrics cards, and supplier detail modals.
