"""
Core Processing Package for South African Protein Powder Tracker.
"""

from core.normalizers import (
    clean_brand,
    is_valid_protein_powder,
    parse_weight_g,
    determine_type,
    determine_flavor,
    get_product_family_key,
    FAMILY_TYPE_MAP
)

from core.nutrition import (
    determine_nutrition,
    BRAND_FORMULATIONS
)

from core.quality import (
    compute_protein_quality_scores,
    assign_product_archetype
)

from core.deals import (
    determine_bulk_deal
)

from core.retailers import (
    find_data_file,
    collect_all_products,
    load_takealot,
    load_amazon,
    load_clicks,
    load_dischem,
    load_nutritech,
    load_futurelife,
    load_mywellness,
    load_alternatives
)

from core.storage import (
    save_products
)

__all__ = [
    'clean_brand',
    'is_valid_protein_powder',
    'parse_weight_g',
    'determine_type',
    'determine_flavor',
    'get_product_family_key',
    'FAMILY_TYPE_MAP',
    'determine_nutrition',
    'BRAND_FORMULATIONS',
    'compute_protein_quality_scores',
    'assign_product_archetype',
    'determine_bulk_deal',
    'find_data_file',
    'collect_all_products',
    'load_takealot',
    'load_amazon',
    'load_clicks',
    'load_dischem',
    'load_nutritech',
    'load_futurelife',
    'load_mywellness',
    'load_alternatives',
    'save_products'
]

