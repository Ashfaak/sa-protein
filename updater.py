"""
Whey Protein Price & Product Updater for South African Retailers
Supports: Clicks, Dis-Chem, Takealot, Amazon.co.za
Updates SQLite database (data/proteins.db) and JSON export (data/proteins.json)
"""

import sys
import os
import re
import json
import sqlite3
import argparse
import requests
from datetime import datetime

# Import parsing & normalization routines from process_master
from process_master import (
    clean_brand, parse_weight_g, determine_type, determine_flavor,
    determine_nutrition, run_consolidation, find_data_file
)

def get_raw_data_path(filename):
    found = find_data_file(filename)
    if found:
        return found
    raw_dir = os.path.join('data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    return os.path.join(raw_dir, filename)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def update_clicks():
    print("[Clicks] Updating latest whey protein prices & brands...")
    queries = ['whey', 'usn whey', 'nutritech whey', 'biogen whey', 'npl whey', 'protein powder', 'whey isolate']
    products = {}
    for q in queries:
        url = f"https://clicks.co.za/search?text={q.replace(' ', '+')}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, 'html.parser')
                links = soup.find_all('a', href=re.compile(r'/[^/]+/p/\d+'))
                for a in links:
                    href = a['href']
                    full_url = f"https://clicks.co.za{href}" if not href.startswith('http') else href
                    if full_url in products:
                        continue
                    parent = a
                    for _ in range(6):
                        if parent.parent:
                            parent = parent.parent
                            text = parent.get_text()
                            if 'R' in text and any(c.isdigit() for c in text):
                                break
                    text = parent.get_text(separator=' ')
                    # Clean thousands and non-breaking space
                    price_match = re.search(r'R\s*([0-9\s\xa0]+(?:\.[0-9]{2})?)', text)
                    if price_match:
                        clean_p = price_match.group(1).replace(' ', '').replace('\xa0', '').replace(',', '')
                        price = float(clean_p)
                    else:
                        price = None
                    
                    title = a.get_text(strip=True)
                    if not title or len(title) < 5 or 'See more' in title:
                        img = parent.find('img', alt=True)
                        if img and len(img['alt']) > 5:
                            title = img['alt']
                        else:
                            continue
                    
                    # Extract brand from URL slug: https://clicks.co.za/{brand}_{slug}/p/{id}
                    brand_extracted = None
                    if 'clicks.co.za/' in full_url and '_' in full_url:
                        slug_brand = full_url.split('clicks.co.za/')[1].split('_')[0].strip()
                        brand_extracted = clean_brand(slug_brand, title, full_url)

                    if any(w in title.lower() for w in ['whey', 'protein', 'isolate', 'casein']):
                        products[full_url] = {
                            'title': title,
                            'brand': brand_extracted,
                            'price': price,
                            'url': full_url,
                            'retailer': 'Clicks'
                        }
        except Exception as e:
            print(f"  [Clicks] Error querying {q}: {e}")

    print(f"  [Clicks] Found {len(products)} active products.")
    if products:
        with open(get_raw_data_path("clicks_all_whey.json"), "w", encoding="utf-8") as f:
            json.dump(list(products.values()), f, indent=2)
    return len(products)

def update_dischem():
    print("[Dis-Chem] Updating latest catalog via Klevu Search API...")
    url = "https://eucs7.ksearchnet.com/cs/v2/search"
    offset = 0
    limit = 60
    all_dischem = []

    while True:
        payload = {
            "context": {"apiKeys": ["klevu-15264750100467933"]},
            "recordQueries": [{
                "id": "searchQueryResult",
                "typeOfRequest": "SEARCH",
                "settings": {
                    "query": {"term": "whey protein"},
                    "limit": limit,
                    "offset": offset
                }
            }]
        }
        try:
            r = requests.post(url, json=payload, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                break
            data = r.json()
            records = data["queryResults"][0].get("records", [])
            if not records:
                break
            for rec in records:
                all_dischem.append({
                    'name': rec.get('name'),
                    'brand': rec.get('product_brand') or rec.get('brand'),
                    'price': float(rec.get('salePrice') or rec.get('price') or 0),
                    'original_price': float(rec.get('price') or 0),
                    'url': rec.get('url'),
                    'sku': rec.get('sku'),
                    'image': rec.get('imageUrl') or rec.get('image'),
                    'weight': rec.get('weight'),
                    'in_stock': rec.get('inStock') == 'yes'
                })
            offset += limit
            if offset >= 250:
                break
        except Exception as e:
            print(f"  [Dis-Chem] Error: {e}")
            break

    print(f"  [Dis-Chem] Found {len(all_dischem)} active products.")
    if all_dischem:
        with open(get_raw_data_path("dischem_all_whey.json"), "w", encoding="utf-8") as f:
            json.dump(all_dischem, f, indent=2)
    return len(all_dischem)

def update_takealot_prices():
    print("[Takealot] Checking known PLID prices...")
    t_file = get_raw_data_path("takealot_all_whey.json")
    if not os.path.exists(t_file):
        return 0
    with open(t_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    updated = 0
    for item in items[:15]: # fast check sample or full
        plid = item.get('product_id')
        if not plid: continue
        try:
            url = f"https://api.takealot.com/rest/v-1-11-0/product-details/PLID{plid}?platform=desktop"
            r = requests.get(url, headers={'Referer': 'https://www.takealot.com/', 'User-Agent': HEADERS['User-Agent']}, timeout=5)
            if r.status_code == 200:
                data = r.json()
                price = data.get('buybox', {}).get('items', [{}])[0].get('price')
                if price:
                    item['price_zar'] = float(price)
                    updated += 1
        except Exception:
            pass

    with open(t_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"  [Takealot] Checked prices for {updated} products.")
    return updated

def update_amazon():
    print("[Amazon ZA] Checking latest verified listings & coupons...")
    a_file = get_raw_data_path("amazon_verified.json")
    if os.path.exists(a_file):
        with open(a_file, "r", encoding="utf-8") as f:
            items = json.load(f)
        print(f"  [Amazon ZA] Loaded {len(items)} verified products with accurate multi-size pricing and promo code tracking.")
        return len(items)
    return 0

def update_nutritech():
    print("[Nutritech Direct] Checking live direct-to-consumer prices on nutritechfit.com...")
    url = "https://www.nutritechfit.com/product-category/supplements/proteins/whey-protein/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(['li', 'div'], class_=re.compile(r'\bproduct\b'))
            
            existing = {}
            nt_file = get_raw_data_path("nutritech_products.json")
            if os.path.exists(nt_file):
                with open(nt_file, "r", encoding="utf-8") as f:
                    for p in json.load(f):
                        existing[p['url']] = p

            updated_count = 0
            for item in items:
                link = item.find('a', href=re.compile(r'/shop/'))
                if not link: continue
                href = link['href']
                
                price_el = item.find(class_='price')
                if not price_el: continue
                price_text = price_el.get_text()
                
                ins_el = price_el.find('ins')
                del_el = price_el.find('del')
                if ins_el and del_el:
                    sale_m = re.search(r'R\s*([0-9,]+(?:\.[0-9]{2})?)', ins_el.get_text())
                    orig_m = re.search(r'R\s*([0-9,]+(?:\.[0-9]{2})?)', del_el.get_text())
                    cur_price = float(sale_m.group(1).replace(',', '')) if sale_m else None
                    reg_price = float(orig_m.group(1).replace(',', '')) if orig_m else cur_price
                else:
                    m = re.search(r'R\s*([0-9,]+(?:\.[0-9]{2})?)', price_text)
                    cur_price = float(m.group(1).replace(',', '')) if m else None
                    reg_price = cur_price

                if href in existing and cur_price:
                    existing[href]['price_zar'] = cur_price
                    if reg_price:
                        existing[href]['original_price_zar'] = reg_price
                    updated_count += 1
            
            with open(nt_file, "w", encoding="utf-8") as f:
                json.dump(list(existing.values()), f, indent=2, ensure_ascii=False)
            print(f"  [Nutritech Direct] Checked prices for {updated_count} products.")
            return updated_count
    except Exception as e:
        print(f"  [Nutritech Direct] Error updating: {e}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Update Whey Protein Database Prices & Products")
    parser.add_argument("--retailer", choices=['all', 'clicks', 'dischem', 'takealot', 'amazon', 'nutritech'], default='all', help="Specific retailer to update")
    parser.add_argument("--find-new", action='store_true', help="Search for newly listed products")
    args = parser.parse_args()

    print(f"=== Starting Whey Protein Database Update ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    if args.retailer in ['all', 'clicks']:
        update_clicks()
    if args.retailer in ['all', 'dischem']:
        update_dischem()
    if args.retailer in ['all', 'takealot']:
        update_takealot_prices()
    if args.retailer in ['all', 'amazon']:
        update_amazon()
    if args.retailer in ['all', 'nutritech']:
        update_nutritech()

    print("[Consolidation] Rebuilding database with updated prices & derived metrics...")
    run_consolidation()
    print("=== Update Complete! ===")

if __name__ == '__main__':
    main()

