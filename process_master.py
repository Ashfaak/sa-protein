"""
Master Processing and Consolidation Pipeline for SA Protein Tracker.

This module coordinates ingestion across South African retailers (Takealot,
Amazon ZA, Clicks, Dis-Chem, Nutritech Direct, FutureLife, and specialized brands),
applies nutritional normalization, DIAAS bioavailability scoring, and bulk deal simulation,
and writes out the master SQLite database, JSON, and JavaScript datasets.

The underlying domain logic is cleanly split into modular components under `core/`:
- `core.normalizers`: Brand resolution, weight parsing, powder validation, flavor & family mapping
- `core.nutrition`: Active formulation profiles, amino acid metrics, digestive enzymes & sweeteners
- `core.quality`: DIAAS & PDCAAS bioavailability scoring and quality summaries
- `core.deals`: Bulk deals, 3-for-2 multi-buys, and 2-for-R599 bundle logic
- `core.retailers`: Dedicated extractors and parsers for each retail catalog
- `core.storage`: Database persistence (SQLite), JSON exports, and timestamping

All functions remain directly re-exported here for full backwards compatibility
with `updater.py` and existing automation workflows.
"""

from core import (
    clean_brand,
    is_valid_protein_powder,
    parse_weight_g,
    determine_type,
    determine_flavor,
    get_product_family_key,
    FAMILY_TYPE_MAP,
    determine_nutrition,
    BRAND_FORMULATIONS,
    compute_protein_quality_scores,
    determine_bulk_deal,
    find_data_file,
    collect_all_products,
    load_takealot,
    load_amazon,
    load_clicks,
    load_dischem,
    load_nutritech,
    load_futurelife,
    load_alternatives,
    save_products
)

def run_consolidation():
    """
    Ingests all retailer datasets, normalizes and validates formulations,
    calculates DIAAS and bulk pricing, and persists to SQLite, JSON, and JS.
    """
    master_products = collect_all_products()
    save_products(master_products)

if __name__ == '__main__':
    run_consolidation()
