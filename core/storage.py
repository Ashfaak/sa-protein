"""
Database and Persistence Module for Protein Tracker.
Handles SQLite export (data/proteins.db), JSON export (data/proteins.json),
JS embedded payload (data/products_data.js), and index.html timestamp synchronization.
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from core.quality import assign_product_archetype

def save_products(master_products, db_path='data/proteins.db', json_path='data/proteins.json', js_path='data/products_data.js', tombstones_path='data/tombstones.json'):
    print(f"Total consolidated pure protein powders: {len(master_products)}")
    
    os.makedirs('data', exist_ok=True)

    # Format current date (e.g. "8 Nov 2026")
    today_str = datetime.now().strftime("%d %b %Y").lstrip("0")

    # Load existing tombstones if present
    tombstones = {}
    if os.path.exists(tombstones_path):
        try:
            with open(tombstones_path, 'r', encoding='utf-8') as f:
                tombstones = json.load(f)
        except Exception as e:
            print(f"Warning reading existing tombstones: {e}")
            tombstones = {}

    # Enrich products with internal archetype and standout metrics
    for p in master_products:
        arch_data = assign_product_archetype(p)
        p['internal_archetype'] = arch_data['internal_archetype']
        p['standout_metric'] = arch_data['standout_metric']

    # Track products dropped from previous catalog into tombstone archive
    incoming_ids = {p['id'] for p in master_products}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                prev_products = json.load(f)
            for p in prev_products:
                pid = p.get('id')
                if pid and pid not in incoming_ids and pid not in tombstones:
                    arch_data = assign_product_archetype(p)
                    tombstones[pid] = {
                        'id': pid,
                        'retailer': p.get('retailer'),
                        'brand': p.get('brand'),
                        'title': p.get('title'),
                        'product_line': p.get('product_line') or p.get('title'),
                        'type': p.get('type', 'Whey Blend'),
                        'flavor': p.get('flavor', 'Unflavoured'),
                        'container_size_g': p.get('container_size_g', 1000.0),
                        'serving_size_g': p.get('serving_size_g', 30.0),
                        'scoop_size_g': p.get('scoop_size_g', 30.0),
                        'protein_per_serving_g': p.get('protein_per_serving_g', 24.0),
                        'protein_percentage': p.get('protein_percentage', 75.0),
                        'carbs_g': p.get('carbs_g', 2.0),
                        'fat_g': p.get('fat_g', 1.5),
                        'price_zar': p.get('price_zar', 0.0),
                        'cost_per_g_protein_zar': p.get('cost_per_g_protein_zar', 0.0),
                        'diaas_score': p.get('diaas_score', 1.22),
                        'diaas_rating': p.get('diaas_rating', 'Excellent'),
                        'diaas_category': p.get('diaas_category', p.get('type')),
                        'pdcaas_score': p.get('pdcaas_score', 1.00),
                        'quality_summary': p.get('quality_summary', ''),
                        'url': p.get('url', ''),
                        'ingredients': p.get('ingredients', ''),
                        'internal_archetype': arch_data['internal_archetype'],
                        'standout_metric': arch_data['standout_metric'],
                        'delisted_date': today_str,
                        'in_stock': False,
                        'status': 'delisted'
                    }
        except Exception as e:
            print(f"Warning tracking previous products for tombstones: {e}")

    # Ensure existing tombstones have archetype & standout metric
    for tid, tomb in tombstones.items():
        if 'internal_archetype' not in tomb or 'standout_metric' not in tomb:
            t_arch = assign_product_archetype(tomb)
            tomb['internal_archetype'] = t_arch['internal_archetype']
            tomb['standout_metric'] = t_arch['standout_metric']

    # Save tombstones JSON
    with open(tombstones_path, 'w', encoding='utf-8') as f:
        json.dump(tombstones, f, indent=2)

    # Save to SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS products')
    c.execute('''
        CREATE TABLE products (
            id TEXT PRIMARY KEY,
            retailer TEXT,
            brand TEXT,
            title TEXT,
            product_line TEXT,
            type TEXT,
            flavor TEXT,
            container_size_g REAL,
            serving_size_g REAL,
            scoop_size_g REAL,
            protein_per_serving_g REAL,
            total_protein_g REAL,
            protein_percentage REAL,
            carbs_g REAL,
            fat_g REAL,
            servings_count INTEGER,
            price_zar REAL,
            original_price_zar REAL,
            clicks_staff_discount_eligible INTEGER,
            clicks_3_for_2_eligible INTEGER,
            bulk_deal_eligible INTEGER,
            bulk_deal_label TEXT,
            amazon_promo_eligible INTEGER,
            coupon_code TEXT,
            coupon_description TEXT,
            discount_pct REAL,
            discounted_price_zar REAL,
            cost_per_g_protein_zar REAL,
            cost_per_g_protein_discounted_zar REAL,
            cost_per_serving_zar REAL,
            cost_per_serving_discounted_zar REAL,
            rating REAL,
            review_count INTEGER,
            ingredients TEXT,
            digestive_enzymes TEXT,
            sweetener TEXT,
            diaas_score REAL,
            diaas_rating TEXT,
            diaas_category TEXT,
            pdcaas_score REAL,
            quality_summary TEXT,
            url TEXT,
            in_stock INTEGER,
            internal_archetype TEXT,
            standout_metric_label TEXT,
            standout_metric_value TEXT,
            standout_metric_icon TEXT,
            standout_metric_badge_class TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            price_zar REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    unique_ids = set()
    for idx, p in enumerate(master_products):
        base_id = p['id']
        pid = base_id
        count = 1
        while pid in unique_ids:
            pid = f"{base_id}_{count}"
            count += 1
        unique_ids.add(pid)
        p['id'] = pid
        
        c.execute('''
            INSERT OR REPLACE INTO products VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ''', (
            p['id'], p['retailer'], p['brand'], p['title'], p['product_line'], p['type'], p['flavor'],
            p['container_size_g'], p['serving_size_g'], p['scoop_size_g'], p['protein_per_serving_g'],
            p['total_protein_g'], p['protein_percentage'], p['carbs_g'], p['fat_g'],
            p['servings_count'], p['price_zar'], p['original_price_zar'],
            1 if p.get('clicks_staff_discount_eligible') else 0,
            1 if p.get('clicks_3_for_2_eligible') else 0,
            1 if p.get('bulk_deal_eligible') else 0,
            p.get('bulk_deal', {}).get('label') if p.get('bulk_deal') else None,
            1 if p.get('amazon_promo_eligible') else 0,
            p.get('coupon_code'), p.get('coupon_description'), p.get('discount_pct'),
            p.get('discounted_price_zar'), p.get('cost_per_g_protein_zar'), p.get('cost_per_g_protein_discounted_zar'),
            p.get('cost_per_serving_zar'), p.get('cost_per_serving_discounted_zar'), p.get('rating'),
            p.get('review_count'), p.get('ingredients'), p.get('digestive_enzymes'), p.get('sweetener'),
            p.get('diaas_score'), p.get('diaas_rating'), p.get('diaas_category'), p.get('pdcaas_score'),
            p.get('quality_summary'), p.get('url'), 1 if p.get('in_stock', True) else 0,
            p.get('internal_archetype'),
            p.get('standout_metric', {}).get('label'),
            p.get('standout_metric', {}).get('value'),
            p.get('standout_metric', {}).get('icon'),
            p.get('standout_metric', {}).get('badge_class')
        ))
        c.execute('INSERT INTO price_history (product_id, price_zar) VALUES (?, ?)', (p['id'], p['price_zar']))

    conn.commit()
    conn.close()

    # Format current date (e.g. "8 Nov 2026")
    today_str = datetime.now().strftime("%d %b %Y").lstrip("0")

    # Automatically update lastUpdatedDate in index.html
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        updated_html = re.sub(
            r'(<b[^>]*id=["\']lastUpdatedDate["\'][^>]*>)[^<]*(</b>)',
            rf'\g<1>{today_str}\g<2>',
            html_content
        )
        if updated_html != html_content:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(updated_html)
            print(f"Updated index.html lastUpdatedDate to {today_str}")

    # Save finalized JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(master_products, f, indent=2)

    # Save as JS for direct browser loading with window.LAST_UPDATED timestamp and tombstone registry
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(
            f"window.LAST_UPDATED = '{today_str}';\n"
            f"window.EMBEDDED_PROTEINS = " + json.dumps(master_products, indent=2) + ";\n"
            f"window.ARCHIVED_PRODUCTS = " + json.dumps(tombstones, indent=2) + ";\n"
        )

    print(f"Database successfully updated! {len(master_products)} pure whey protein powders stored.")

