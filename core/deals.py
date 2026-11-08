import re

def determine_bulk_deal(retailer, brand, title, price_zar, weight_g, item_raw=None):
    """
    Evaluates multi-buy and bulk promotions across retailers.
    Supports fixed-price bundles (e.g. Clicks 2 for R599), 3-for-2 multi-buys,
    twin packs, and custom supplier bulk specials.
    """
    title_lower = (title or '').lower()
    raw_str = str(item_raw or '').lower() if item_raw else ''
    
    # 1. Clicks Purified Protein 1kg promotion: "Buy 2 Clicks Purified Protein 1kg for R599, Save R161"
    # Officially running at Clicks across all flavours (Chocolate, Vanilla, Strawberry)
    if retailer == 'Clicks' and 'purified' in title_lower and (weight_g == 1000 or '1kg' in title_lower or '1 kg' in title_lower):
        bundle_price = 599.00
        buy_qty = 2
        unit_price = round(bundle_price / buy_qty, 2)  # R 299.50
        savings = round((price_zar * buy_qty) - bundle_price, 2)  # 380*2 - 599 = 161.00
        savings_pct = round((savings / (price_zar * buy_qty)) * 100, 1) if price_zar > 0 else 21.2
        return {
            'eligible': True,
            'type': 'bundle',
            'label': '2 for R599',
            'tag': 'Buy 2 for R599',
            'buy_qty': buy_qty,
            'bundle_price_zar': bundle_price,
            'unit_price_zar': unit_price,
            'savings_zar': savings,
            'savings_pct': savings_pct,
            'description': 'Buy 2 Clicks Purified Protein 1kg for R599, Save R161 (effective R 299.50 / tub).'
        }

    # 2. Check for explicit 3 for 2 specials (e.g. Clicks Smartlife 3 for 2 or general 3 for 2)
    is_3for2 = (
        '3for2' in raw_str or '3 for 2' in raw_str or 'buy 3' in raw_str or
        (item_raw and isinstance(item_raw, dict) and item_raw.get('clicks_3_for_2_eligible'))
    )
    if is_3for2 and price_zar > 0:
        buy_qty = 3
        pay_qty = 2
        bundle_price = round(price_zar * pay_qty, 2)
        unit_price = round(bundle_price / buy_qty, 2)
        savings = round(price_zar, 2)
        savings_pct = 33.3
        return {
            'eligible': True,
            'type': '3_for_2',
            'label': '3 for 2',
            'tag': '3 for 2',
            'buy_qty': buy_qty,
            'pay_qty': pay_qty,
            'bundle_price_zar': bundle_price,
            'unit_price_zar': unit_price,
            'savings_zar': savings,
            'savings_pct': savings_pct,
            'description': 'Buy any 3 qualifying products and get the cheapest free (effective 33.3% savings per tub).'
        }

    # 3. Check for explicit bulk deal object already present on item_raw
    if item_raw and isinstance(item_raw, dict) and item_raw.get('bulk_deal'):
        bd = item_raw['bulk_deal']
        if isinstance(bd, dict) and bd.get('eligible', True):
            return bd

    return None

