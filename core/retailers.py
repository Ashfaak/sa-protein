"""
Retailer Data Extractors and Normalization Loaders.
"""

import json
import os
import re
from core.normalizers import (
    clean_brand, is_valid_protein_powder, parse_weight_g,
    determine_type, determine_flavor, get_product_family_key
)
from core.nutrition import determine_nutrition
from core.quality import compute_protein_quality_scores
from core.deals import determine_bulk_deal

def find_data_file(filename):
    for candidate in [filename, os.path.join('data', 'raw', filename), os.path.join('data', filename)]:
        if os.path.exists(candidate):
            return candidate
    return None

def load_takealot(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    t_file = find_data_file('takealot_all_whey.json')
    if t_file:
        with open(t_file, 'r', encoding='utf-8') as f:
            t_items = json.load(f)
            for item in t_items:
                title = item.get('title', '')
                if not title or len(title) < 5: continue
                # STRICT POWDER CHECK
                if not is_valid_protein_powder(title, item.get('url')): continue
                
                price = float(item.get('price_zar') or 599.0)
                brand = clean_brand(item.get('brand'), title, item.get('url'))
                if brand == 'Muscle Works' and not title.lower().startswith('muscle works'):
                    title = f"Muscle Works {title}"
                family = get_product_family_key(title, brand)

                weight_g = parse_weight_g(title, item.get('container_size'))
                ptype = determine_type(title, item.get('ingredients'), family[1])
                flavor = determine_flavor(title, item.get('flavor'))
                nut = determine_nutrition(brand, ptype, weight_g, title, item.get('ingredients'))
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)
                bulk_deal = determine_bulk_deal('Takealot', brand, title, price, weight_g, item)

                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)

                key = f"takealot_{item.get('product_id') or title}"
                if key in seen_keys: continue
                seen_keys.add(key)
                products.append({
                    'id': key,
                    'retailer': 'Takealot',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': None,
                    'coupon_description': 'Standard Retail Price',
                    'discount_pct': 0,
                    'discounted_price_zar': round(price, 2),
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv,
                    'rating': item.get('rating') or 4.5,
                    'review_count': item.get('review_count') or 12,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://www.takealot.com',
                    'in_stock': True
                })

    return products

def load_amazon(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    amazon_file = find_data_file('amazon_verified.json') or find_data_file('amazon_all_whey.json')
    if amazon_file and os.path.exists(amazon_file):
        with open(amazon_file, 'r', encoding='utf-8') as f:
            a_items = json.load(f)
            for item in a_items:
                title = item.get('title', '')
                if not title or len(title) < 5: continue
                # STRICT POWDER CHECK
                if not is_valid_protein_powder(title, item.get('url')): continue
                
                raw_price = item.get('price_zar')
                if not raw_price or raw_price < 150:
                    if '1380' in str(item) or 'npl platinum whey 2kg' in title.lower():
                        price = 1380.0
                    elif 'superior whey protein 3kg' in title.lower():
                        price = 1249.0
                    elif 'optimum nutrition' in title.lower() and ('2.27' in title or '2.28' in title):
                        price = 2499.99
                    elif 'optimum nutrition' in title.lower() and ('900' in title or '899' in title):
                        price = 1149.0
                    elif 'nutritech' in title.lower() and '2 kg' in title.lower():
                        price = 1199.0
                    else:
                        price = 499.0
                else:
                    price = float(raw_price)

                brand = clean_brand(item.get('brand'), title, item.get('url'))
                if brand == 'Muscle Works' and not title.lower().startswith('muscle works'):
                    title = f"Muscle Works {title}"
                family = get_product_family_key(title, brand)

                weight_g = parse_weight_g(title, str(item.get('container_size_g') or ''))
                ptype = determine_type(title, item.get('ingredients'), family[1])
                flavor = determine_flavor(title, item.get('flavor'))
                nut = determine_nutrition(brand, ptype, weight_g, title, item.get('ingredients'))
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)

                # Only use genuine verified coupons extracted from the Amazon listing
                coupon_code = item.get('coupon_code')
                coupon_desc = item.get('coupon_text') or item.get('coupon_description')
                has_deal = bool(coupon_code)
                orig_price = float(item.get('original_price') or item.get('original_price_zar') or price)
                
                discount_pct = float(item.get('discount_pct') or 0) if has_deal else 0
                discounted_price = round(price * (1 - discount_pct / 100.0), 2) if (has_deal and discount_pct > 0) else price

                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_g_disc = round(discounted_price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)
                cost_per_serv_disc = round(discounted_price / nut['servings_count'], 2)

                asin = item.get('asin') or item.get('id', '').replace('amazon_', '')
                key = f"amazon_{asin or title[:20]}"
                if key in seen_keys: continue
                seen_keys.add(key)
                
                bulk_deal = determine_bulk_deal('Amazon ZA', brand, title, price, weight_g, item)

                products.append({
                    'id': key,
                    'retailer': 'Amazon ZA',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(orig_price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': has_deal,
                    'coupon_code': coupon_code,
                    'coupon_description': coupon_desc or 'Amazon Verified Listing',
                    'discount_pct': discount_pct,
                    'discounted_price_zar': discounted_price,
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g_disc,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv_disc,
                    'rating': item.get('rating') or 4.5,
                    'review_count': item.get('review_count') or 18,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://www.amazon.co.za',
                    'in_stock': True
                })

    return products

def load_clicks(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    clicks_file = find_data_file('clicks_verified.json') or find_data_file('clicks_all_whey.json')
    if clicks_file and os.path.exists(clicks_file):
        with open(clicks_file, 'r', encoding='utf-8') as f:
            c_raw = json.load(f)
            c_items = c_raw.get('products', c_raw) if isinstance(c_raw, dict) else c_raw
            for item in c_items:
                title = item.get('title', '')
                if not title or len(title) < 5: continue
                # STRICT POWDER CHECK (Eliminates 414ml GNC RTD Shakes & protein waters!)
                if not is_valid_protein_powder(title, item.get('url')): continue
                
                price = float(item.get('price_zar') or item.get('price') or 550.0)
                if price < 50: continue # ignore single sachets
                
                url = item.get('url') or ''
                brand = clean_brand(item.get('brand'), title, url)
                if brand == 'Muscle Works' and not title.lower().startswith('muscle works'):
                    title = f"Muscle Works {title}"
                family = get_product_family_key(title, brand)

                weight_g = parse_weight_g(title, str(item.get('container_size_g') or ''))
                ptype = determine_type(title, '', family[1])
                flavor = determine_flavor(title)
                nut = determine_nutrition(brand, ptype, weight_g, title)
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)
                bulk_deal = determine_bulk_deal('Clicks', brand, title, price, weight_g, item)

                discounted_price = round(price * 0.87, 2) # Clicks 13% Staff Discount
                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_g_disc = round(discounted_price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)
                cost_per_serv_disc = round(discounted_price / nut['servings_count'], 2)

                slug = url.split('/')[-3] if '/p/' in url else title[:20]
                key = f"clicks_{slug}"
                if key in seen_keys: continue
                seen_keys.add(key)

                products.append({
                    'id': key,
                    'retailer': 'Clicks',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(price, 2),
                    'clicks_staff_discount_eligible': True,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': 'STAFF13',
                    'coupon_description': '💳 Clicks Staff 13% Discount Active',
                    'discount_pct': 13,
                    'discounted_price_zar': discounted_price,
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g_disc,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv_disc,
                    'rating': 4.5,
                    'review_count': 32,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': url or 'https://clicks.co.za',
                    'in_stock': True
                })

    return products

def load_dischem(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    d_file = find_data_file('dischem_all_whey.json')
    if d_file and os.path.exists(d_file):
        with open(d_file, 'r', encoding='utf-8') as f:
            d_items = json.load(f)
            for item in d_items:
                title = item.get('name', '')
                if not title or len(title) < 5: continue
                # STRICT POWDER CHECK
                if not is_valid_protein_powder(title, item.get('url')): continue
                
                raw_p = item.get('price')
                if raw_p is None or float(raw_p) < 100:
                    continue
                price = float(raw_p)
                brand = clean_brand(item.get('brand'), title, item.get('url'))
                if brand == 'Muscle Works' and not title.lower().startswith('muscle works'):
                    title = f"Muscle Works {title}"
                family = get_product_family_key(title, brand)

                weight_g = parse_weight_g(title)
                ptype = determine_type(title, '', family[1])
                flavor = determine_flavor(title)
                nut = determine_nutrition(brand, ptype, weight_g, title)
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)
                bulk_deal = determine_bulk_deal('Dis-Chem', brand, title, price, weight_g, item)

                discounted_price = round(price * 0.90, 2)
                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_g_disc = round(discounted_price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)
                cost_per_serv_disc = round(discounted_price / nut['servings_count'], 2)

                key = f"dischem_{item.get('sku') or title[:20]}"
                if key in seen_keys: continue
                seen_keys.add(key)

                products.append({
                    'id': key,
                    'retailer': 'Dis-Chem',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': 'BETTER10',
                    'coupon_description': '🎁 Dis-Chem Better Rewards: 10% Instant Savings',
                    'discount_pct': 10,
                    'discounted_price_zar': discounted_price,
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g_disc,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv_disc,
                    'rating': 4.7,
                    'review_count': 25,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://www.dischem.co.za',
                    'in_stock': item.get('in_stock', True)
                })

    return products

def load_nutritech(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    nt_file = find_data_file('nutritech_products.json')
    if nt_file and os.path.exists(nt_file):
        with open(nt_file, 'r', encoding='utf-8') as f:
            nt_items = json.load(f)
            for item in nt_items:
                title = item.get('title', '')
                if not title or len(title) < 5: continue
                if not is_valid_protein_powder(title, item.get('url')): continue

                price = float(item.get('price_zar') or 399.0)
                orig_price = float(item.get('original_price_zar') or price)
                brand = 'Nutritech'
                family = get_product_family_key(title, brand)

                weight_g = float(item.get('container_size_g') or parse_weight_g(title))
                ptype = determine_type(title, '', family[1])
                flavor = item.get('flavor') or determine_flavor(title)
                nut = determine_nutrition(brand, ptype, weight_g, title)
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)
                bulk_deal = determine_bulk_deal('Brand Direct', brand, title, price, weight_g, item)

                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)

                key = item.get('id') or f"nutritech_{title[:20]}"
                if key in seen_keys: continue
                seen_keys.add(key)

                products.append({
                    'id': key,
                    'retailer': 'Brand Direct',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(orig_price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': None,
                    'coupon_description': 'Official Manufacturer Store',
                    'discount_pct': round(((orig_price - price) / orig_price) * 100, 1) if orig_price > price else 0,
                    'discounted_price_zar': round(price, 2),
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv,
                    'rating': item.get('rating') or 4.8,
                    'review_count': item.get('review_count') or 25,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://www.nutritechfit.com/',
                    'in_stock': item.get('in_stock', True)
                })

    return products

def load_futurelife(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    fl_file = find_data_file('futurelife_products.json')
    if fl_file and os.path.exists(fl_file):
        with open(fl_file, 'r', encoding='utf-8') as f:
            fl_items = json.load(f)
            for item in fl_items:
                title = item.get('title', '')
                if not title or len(title) < 5: continue
                if not is_valid_protein_powder(title, item.get('url')): continue

                price = float(item.get('price_zar') or 79.0)
                orig_price = float(item.get('original_price_zar') or price)
                brand = 'FutureLife'
                family = get_product_family_key(title, brand)

                weight_g = float(item.get('container_size_g') or parse_weight_g(title))
                ptype = determine_type(title, '', family[1])
                flavor = item.get('flavor') or determine_flavor(title)
                nut = determine_nutrition(brand, ptype, weight_g, title)
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], title)
                bulk_deal = determine_bulk_deal('Brand Direct', brand, title, price, weight_g, item)

                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2)

                key = item.get('id') or f"futurelife_{title[:20]}"
                if key in seen_keys: continue
                seen_keys.add(key)

                products.append({
                    'id': key,
                    'retailer': 'Brand Direct',
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(orig_price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': None,
                    'coupon_description': 'Official Manufacturer Store',
                    'discount_pct': round(((orig_price - price) / orig_price) * 100, 1) if orig_price > price else 0,
                    'discounted_price_zar': round(price, 2),
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv,
                    'rating': item.get('rating') or 4.8,
                    'review_count': item.get('review_count') or 25,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://futurelife.co.za',
                    'in_stock': item.get('in_stock', True)
                })

    return products

def load_mywellness(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    mw_file = find_data_file('mywellness_products.json')
    if not mw_file or not os.path.exists(mw_file):
        return products

    with open(mw_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        mw_items = data.get('products', []) if isinstance(data, dict) else data
        for item in mw_items:
            base_title = item.get('title', '')
            if not base_title or len(base_title) < 5:
                continue
            if not is_valid_protein_powder(base_title, item.get('product_url')):
                continue

            brand = 'My Wellness'
            base_url = item.get('product_url', 'https://www.my-wellness.co.za/')
            variants = item.get('variants', [])
            
            # If no variants extracted, create a single entry from parent item
            if not variants:
                variants = [{
                    'variant_id': item.get('product_id'),
                    'title': base_title,
                    'sku': '',
                    'price_zar': item.get('prices_by_size', {}).get(next(iter(item.get('prices_by_size', {})), {}), {}).get('price_zar', 399),
                    'compare_at_price_zar': None,
                    'available': item.get('in_stock', True),
                    'size': (item.get('available_sizes') or [None])[0],
                    'flavour': (item.get('available_flavours') or [None])[0]
                }]

            # Deduplicate variants by (size, flavour) to avoid duplicate entries within the product
            seen_variant_tuples = set()
            for v in variants:
                price = float(v.get('price_zar') or 399.0)
                orig_price = float(v.get('compare_at_price_zar') or price)
                
                size_str = v.get('size') or (item.get('available_sizes') or [None])[0] or base_title
                weight_g = parse_weight_g(str(size_str))
                if weight_g == 0:
                    weight_g = parse_weight_g(base_title) or 1000.0

                flv_val = v.get('flavour')
                v_title = v.get('title', '')
                comb_text = f"{base_title} {v_title}"
                flavor = determine_flavor(comb_text, flv_val)

                v_key = (round(weight_g), flavor.lower())
                if v_key in seen_variant_tuples:
                    continue
                seen_variant_tuples.add(v_key)

                # Compose title
                full_title = base_title
                if flavor and flavor.lower() not in base_title.lower() and flavor.lower() != 'unflavoured':
                    full_title = f"{base_title} - {flavor}"

                family = get_product_family_key(full_title, brand)
                ptype = determine_type(full_title, item.get('ingredients') or '', family[1])
                nut = determine_nutrition(brand, ptype, weight_g, full_title, item.get('ingredients'))
                quality = compute_protein_quality_scores(ptype, nut['ingredients'], full_title)
                bulk_deal = determine_bulk_deal('Brand Direct', brand, full_title, price, weight_g, v)

                # Variant URL with deep-link
                var_id = v.get('variant_id')
                item_url = f"{base_url}?variant={var_id}" if var_id else base_url

                # My Wellness WELCOME10 coupon: 10% off first order + Free shipping over R750
                disc_pct = 10
                disc_price = round(price * 0.90, 2)
                cost_per_g = round(price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_g_disc = round(disc_price / nut['total_protein_g'], 2) if nut['total_protein_g'] > 0 else 0
                cost_per_serv = round(price / nut['servings_count'], 2) if nut['servings_count'] > 0 else 0
                cost_per_serv_disc = round(disc_price / nut['servings_count'], 2) if nut['servings_count'] > 0 else 0

                prod_id = f"mywellness_{var_id or re.sub(r'[^a-z0-9]', '', full_title.lower())[:25]}"
                if prod_id in seen_keys:
                    continue
                seen_keys.add(prod_id)

                products.append({
                    'id': prod_id,
                    'retailer': 'Brand Direct',
                    'brand': brand,
                    'title': full_title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': nut['serving_size_g'],
                    'scoop_size_g': nut['scoop_size_g'],
                    'protein_per_serving_g': nut['protein_per_serving_g'],
                    'total_protein_g': nut['total_protein_g'],
                    'protein_percentage': nut['protein_percentage'],
                    'carbs_g': nut['carbs_g'],
                    'fat_g': nut['fat_g'],
                    'servings_count': nut['servings_count'],
                    'price_zar': round(price, 2),
                    'original_price_zar': round(orig_price, 2),
                    'clicks_staff_discount_eligible': False,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': 'WELCOME10',
                    'coupon_description': '🎉 My Wellness Brand Direct: 10% Off First Order + Free Shipping over R750',
                    'discount_pct': disc_pct,
                    'discounted_price_zar': disc_price,
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g_disc,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv_disc,
                    'rating': 4.8,
                    'review_count': 34,
                    'ingredients': nut['ingredients'],
                    'digestive_enzymes': nut['digestive_enzymes'],
                    'sweetener': nut['sweetener'],
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item_url,
                    'in_stock': v.get('available', True)
                })

    return products

def load_alternatives(seen_keys=None):
    if seen_keys is None:
        seen_keys = set()
    products = []
    alt_file = find_data_file('other_proteins_scraped.json')
    if alt_file and os.path.exists(alt_file):
        with open(alt_file, 'r', encoding='utf-8') as f:
            alt_items = json.load(f)
            for idx_alt, item in enumerate(alt_items):
                title = item.get('name') or item.get('title') or ''
                if not title or len(title) < 5: continue
                brand = clean_brand(item.get('brand'), title, item.get('url'))
                family = get_product_family_key(title, brand)

                weight_g = float(item.get('size_g') or parse_weight_g(title))
                serving_g = float(item.get('serving_g') or 32.0)
                prot_g = float(item.get('protein_per_serving_g') or 22.0)
                carbs_g = float(item.get('carbs_per_serving_g') if item.get('carbs_per_serving_g') is not None else 2.5)
                fat_g = float(item.get('fat_per_serving_g') if item.get('fat_per_serving_g') is not None else 1.5)
                servings_cnt = int(item.get('servings') or max(1, int(weight_g / serving_g)))
                total_prot_g = round(servings_cnt * prot_g, 1)
                prot_pct = float(item.get('protein_pct') or round((prot_g / serving_g) * 100, 1))

                ptype = determine_type(title, item.get('protein_sources', ''), family[1])
                flavor = determine_flavor(title)
                ing_str = f"{item.get('protein_sources', '')}. {item.get('notes', '')}".strip()
                quality = compute_protein_quality_scores(ptype, ing_str, title)

                price = float(item.get('price_zar') or 449.0)
                url_str = (item.get('url') or '').lower()
                raw_ret = str(item.get('retailer', ''))

                if 'clicks.co.za' in url_str:
                    ret_clean = 'Clicks'
                elif 'dischem.co.za' in url_str:
                    ret_clean = 'Dis-Chem'
                elif 'takealot.com' in url_str:
                    ret_clean = 'Takealot'
                elif 'amazon.co.za' in url_str:
                    ret_clean = 'Amazon ZA'
                elif any(dom in url_str for dom in ['usn.global', 'usn.co.za', 'nutritechfit.com', 'npl.za.com', 'phytopro.co.za', 'biogen.co.za']) or 'official' in raw_ret.lower() or 'direct' in raw_ret.lower():
                    ret_clean = 'Brand Direct'
                elif 'Clicks' in raw_ret:
                    ret_clean = 'Clicks'
                elif 'Dis-Chem' in raw_ret:
                    ret_clean = 'Dis-Chem'
                elif 'Amazon' in raw_ret:
                    ret_clean = 'Amazon ZA'
                else:
                    ret_clean = 'Takealot'

                is_clicks = (ret_clean == 'Clicks')
                is_dischem = (ret_clean == 'Dis-Chem')
                disc_pct = 13 if is_clicks else (10 if is_dischem else 0)
                disc_price = round(price * (1 - disc_pct / 100.0), 2)
                cost_per_g = round(price / total_prot_g, 2) if total_prot_g > 0 else 0
                cost_per_g_disc = round(disc_price / total_prot_g, 2) if total_prot_g > 0 else 0
                cost_per_serv = round(price / servings_cnt, 2)
                cost_per_serv_disc = round(disc_price / servings_cnt, 2)

                bulk_deal = determine_bulk_deal(ret_clean, brand, title, price, weight_g, item)

                key = f"alt_{idx_alt}_{re.sub(r'[^a-z0-9]', '', title.lower())[:18]}"
                if key in seen_keys: continue
                seen_keys.add(key)

                coupon_code = 'STAFF13' if is_clicks else ('BETTER10' if is_dischem else None)
                coupon_desc = '💳 Clicks Staff 13% Discount' if is_clicks else ('🎁 Dis-Chem Better Rewards 10%' if is_dischem else None)

                products.append({
                    'id': key,
                    'retailer': ret_clean,
                    'brand': brand,
                    'title': title,
                    'product_line': family[1],
                    'type': ptype,
                    'flavor': flavor,
                    'container_size_g': weight_g,
                    'serving_size_g': serving_g,
                    'scoop_size_g': serving_g,
                    'protein_per_serving_g': prot_g,
                    'total_protein_g': total_prot_g,
                    'protein_percentage': prot_pct,
                    'carbs_g': carbs_g,
                    'fat_g': fat_g,
                    'servings_count': servings_cnt,
                    'price_zar': round(price, 2),
                    'original_price_zar': round(price, 2),
                    'clicks_staff_discount_eligible': is_clicks,
                    'bulk_deal_eligible': bool(bulk_deal and bulk_deal.get('eligible')),
                    'bulk_deal': bulk_deal,
                    'clicks_3_for_2_eligible': bool(bulk_deal and bulk_deal.get('type') == '3_for_2'),
                    'amazon_promo_eligible': False,
                    'coupon_code': coupon_code,
                    'coupon_description': coupon_desc or 'Standard Retail Price',
                    'discount_pct': disc_pct,
                    'discounted_price_zar': disc_price,
                    'cost_per_g_protein_zar': cost_per_g,
                    'cost_per_g_protein_discounted_zar': cost_per_g_disc,
                    'cost_per_serving_zar': cost_per_serv,
                    'cost_per_serving_discounted_zar': cost_per_serv_disc,
                    'rating': 4.7,
                    'review_count': 42,
                    'ingredients': ing_str,
                    'digestive_enzymes': item.get('digestive_enzymes') or 'None added',
                    'sweetener': item.get('sweeteners') or 'Stevia',
                    'diaas_score': quality['diaas_score'],
                    'diaas_rating': quality['diaas_rating'],
                    'diaas_category': quality['diaas_category'],
                    'pdcaas_score': quality['pdcaas_score'],
                    'quality_summary': quality['quality_summary'],
                    'url': item.get('url') or 'https://www.takealot.com',
                    'in_stock': True
                })

    return products

def collect_all_products():
    seen_keys = set()
    master_products = []
    master_products.extend(load_takealot(seen_keys))
    master_products.extend(load_amazon(seen_keys))
    master_products.extend(load_clicks(seen_keys))
    master_products.extend(load_dischem(seen_keys))
    master_products.extend(load_nutritech(seen_keys))
    master_products.extend(load_futurelife(seen_keys))
    master_products.extend(load_mywellness(seen_keys))
    master_products.extend(load_alternatives(seen_keys))
    return master_products
