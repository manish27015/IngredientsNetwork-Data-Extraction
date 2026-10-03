"""
IngredientsNetwork.com - Browser Automation Scraper (Playwright)
Relu Consultancy Hiring Challenge - Objective 2

Demonstrates full browser automation:
- Launches Chromium browser
- Navigates to https://www.ingredientsnetwork.com/
- Locates search box and types "Featured Suppliers"
- Programmatically clicks the Search button
- Waits for results page and dynamic cards to render
- Extracts card metadata directly from the browser DOM
"""

import asyncio
import os
import pandas as pd
from playwright.async_api import async_playwright

async def run_browser_automation():
    print("[*] Launching Chromium browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        # Step 1: Navigate to homepage
        url = "https://www.ingredientsnetwork.com/"
        print(f"[*] Step 1: Navigating to {url}...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        print(f"[+] Loaded: {await page.title()}")

        # Step 2: Search for Featured Suppliers
        print("[*] Step 2: Entering 'Featured Suppliers' into search input and submitting...")
        search_input = await page.wait_for_selector("input[name='name'], input[type='search'], input[placeholder*='looking for']", timeout=10000)
        await search_input.fill("Featured Suppliers")
        
        # Click search button
        search_button = await page.wait_for_selector("button[type='submit'], input[type='submit'][value*='Search'], .search-container button", timeout=10000)
        await search_button.click()

        # Step 3: Wait for results to load
        print("[*] Step 3: Waiting for search result cards to load...")
        await page.wait_for_url("**/searchresults*", timeout=30000)
        await page.wait_for_timeout(4000)
        print(f"[+] Reached Search Results: {page.url}")

        # Wait for dynamic cards to render
        await page.wait_for_selector(".results, [id^='result'], .category-card-list", state="attached", timeout=15000)
        await page.wait_for_timeout(3000)
        
        # Scroll down to load more content
        print("[*] Scrolling page to trigger lazy loading...")
        for _ in range(5):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(800)

        # Extract visible cards
        print("[*] Extracting card information from page DOM...")
        cards = await page.query_selector_all("[id^='result'], .company-card, .search-result, .card")
        print(f"[+] Detected {len(cards)} card containers in DOM.")

        extracted = []
        for i, card in enumerate(cards[:20]):
            text = await card.text_content()
            links = await card.query_selector_all("a")
            hrefs = [await l.get_attribute("href") for l in links if await l.get_attribute("href")]
            extracted.append({
                "index": i + 1,
                "text_snippet": (text or "").strip()[:100],
                "first_link": hrefs[0] if hrefs else ""
            })

        print(f"[+] Sample of {len(extracted)} extracted DOM cards:")
        for item in extracted[:5]:
            print(f"    Card {item['index']}: {item['text_snippet']} -> {item['first_link']}")

        await browser.close()
        print("[+] Browser automation completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_browser_automation())
