import re

def clean_brand(brand_raw, title, url=""):
    t = (title or '').lower()
    b_raw_low = (brand_raw or '').lower()
    
    # Priority 0: Muscle Works
    if any(k in t for k in ['muscle works', 'muscleworks', 'whey-bolic', 'wheybolic', 'thermo whey', 'iso-tech', 'isotech']) or any(k in b_raw_low for k in ['muscle works', 'muscleworks', 'whey-bolic', 'wheybolic', 'thermo whey', 'iso-tech']):
        if not ('my wellness' in t or 'mywellness' in t or 'my wellness' in b_raw_low or 'mywellness' in b_raw_low):
            return 'Muscle Works'
    if 'superior whey' in t or 'superior whey' in b_raw_low:
        if 'my wellness' in t or 'mywellness' in t or 'my wellness' in b_raw_low or 'mywellness' in b_raw_low:
            return 'My Wellness'
        return 'Muscle Works'
    if any(k in t for k in ['nutella waffle', 'blueberry cheesecake', 'malted chocolate']) or ('100% whey protein' in t and any(k in t for k in ['double choc', 'creamy vanilla', 'strawberries & cream', '22g protein per serving'])):
        if not ('my wellness' in t or 'primeself' in t or 'clear nutrition' in t or 'psnlifestyle' in t or 'psn' in t or 'psnlifestyle' in b_raw_low or 'psn' in b_raw_low or 'rogue legion' in t or 'rogue' in t or 'rogue legion' in b_raw_low or 'rogue' in b_raw_low):
            return 'Muscle Works'

    # Specific Brands
    if 'psnlifestyle' in t or 'psn' in t or 'psnlifestyle' in b_raw_low or 'psn' in b_raw_low:
        return 'PSNLifestyle'
    if 'rogue legion' in t or 'rogue legion' in b_raw_low or 'rogue' in b_raw_low or 'rogue' in t:
        return 'Rogue Legion'
    if 'future' in t or 'futurelife' in b_raw_low or 'future life' in b_raw_low:
        return 'FutureLife'
    if 'biogen' in t or 'biogen' in b_raw_low:
        return 'Biogen'
    if any(k in t for k in ['my wellness', 'mywellness', 'alpha whey', 'clean diet whey', 'natures whey', 'clear whey iso', 'super clean protein']) or ('alpha' in b_raw_low and 'whey' in t):
        return 'My Wellness'
    if 'grass fed whey' in t or 'grass-fed whey' in t:
        if 'primeself' in t or 'primeself' in b_raw_low:
            return 'PrimeSelf'
        return 'My Wellness'
    if 'primeself' in t or 'primeself' in b_raw_low or 'salted dark chocolate | whey' in t:
        return 'PrimeSelf'
    if 'just protein' in t or ('premium' in t and 'whey protein powder 400' in t):
        return 'Just Protein'
    if 'muscle dynamix' in t or 'iso gold' in t or 'whey one premium' in t:
        return 'Muscle Dynamix'
    if 'atp whey' in t or 'atp fitness' in t:
        return 'ATP Fitness'
    if 'sa vitamins' in t or 'b0hj2lcxs4' in (url or '').lower():
        return 'SA Vitamins'
    if 'my whey' in t or 'milk protein isolate 85%' in t:
        return 'My Whey'
    if 'myprotein' in t:
        return 'Myprotein'
    if 'clear nutrition' in t:
        return 'Clear Nutrition'
    if 'tony ferguson' in t or 'tferg' in t or 'tony ferguson' in b_raw_low:
        return 'Tony Ferguson'
    if 'sci-core' in t or 'scicore' in t or 'sci-core' in b_raw_low:
        return 'Sci-Core'
    if 'lifeworth' in t or 'lifeworth' in b_raw_low or 'b0fj7m74k1' in (url or '').lower() or 'super standard' in t:
        return 'Lifeworth'
    if 'biyode' in t or 'biyode' in b_raw_low or 'b0f9twj4hq' in (url or '').lower():
        return 'Biyode'

    # Priority 1: Extract brand from Clicks URL slug if applicable
    if 'clicks.co.za/' in (url or ''):
        slug = url.split('clicks.co.za/')[1].split('/p/')[0] if '/p/' in url else ''
        b_prefix = slug.split('_')[0].lower() if '_' in slug else ''
        if b_prefix == 'nutritech': return 'Nutritech'
        if b_prefix == 'usn': return 'USN'
        if b_prefix == 'gnc': return 'GNC'
        if b_prefix == 'clicks': return 'Clicks Smartlife'
        if b_prefix == 'gloot': return 'Gloot'
        if b_prefix in ['black-bull', 'blackbull']: return 'Black Bull'
        if b_prefix == 'biogen': return 'Biogen'

    # Priority 2: Use provided brand attribute if clean
    if brand_raw and len(brand_raw) > 1 and brand_raw.lower() not in ['100%', '3-in-1', 'one', 'whey', 'other brands', 'other', 'unknown']:
        b = brand_raw.strip().title()
        b_lower = b.lower()
        if b_lower == 'usn': return 'USN'
        if b_lower == 'npl': return 'NPL'
        if b_lower == 'gnc': return 'GNC'
        if b_lower == 'ssa' or 'ssa supplements' in b_lower: return 'SSA Supplements'
        if b_lower == 'tnt mercury' or b_lower == 'tnt': return 'TNT Mercury'
        if 'biogen' in b_lower: return 'Biogen'
        if b_lower == 'clicks' or 'smartlife' in b_lower: return 'Clicks Smartlife'
        if 'optimum nutrition' in b_lower or b_lower == 'on': return 'Optimum Nutrition'
        if 'muscletech' in b_lower or 'muscle tech' in b_lower: return 'MuscleTech'
        if 'nutritech' in b_lower: return 'Nutritech'
        if 'gloot' in b_lower: return 'Gloot'
        if 'black bull' in b_lower or 'blackbull' in b_lower: return 'Black Bull'
        if 'primal' in b_lower: return 'Primal'
        if 'evox' in b_lower: return 'Evox'
        if 'my wellness' in b_lower or 'mywellness' in b_lower or 'super clean' in b_lower: return 'My Wellness'
        if 'protein feed' in b_lower: return 'Protein Feed'
        if 'tony ferguson' in b_lower: return 'Tony Ferguson'
        if 'nature' in b_lower and 'whey' in b_lower: return "Nature's Whey"
        return b

    # Priority 3: Title pattern matching
    if 'usn' in t: return 'USN'
    if 'nutritech' in t: return 'Nutritech'
    if 'npl' in t: return 'NPL'
    if 'biogen' in t: return 'Biogen'
    if 'optimum nutrition' in t or 'on gold standard' in t or 'gold standard' in t: return 'Optimum Nutrition'
    if 'muscletech' in t or 'muscle tech' in t or 'nitro-tech' in t or 'nitrotech' in t: return 'MuscleTech'
    if 'gnc' in t or 'amplified gold' in t: return 'GNC'
    if 'gloot' in t: return 'Gloot'
    if 'rogue legion' in t: return 'Rogue Legion'
    if 'my wellness' in t or 'mywellness' in t or 'super clean' in t: return 'My Wellness'
    if 'blackbull' in t or 'black bull' in t: return 'Black Bull'
    if 'evox' in t: return 'Evox'
    if 'primal' in t: return 'Primal'
    if 'tnt' in t: return 'TNT Mercury'
    if 'ssa' in t: return 'SSA Supplements'
    if 'lifestyle food' in t: return 'Lifestyle Food'
    if 'clicks' in t or 'smartlife' in t: return 'Clicks Smartlife'
    if 'collagen & co' in t: return 'Collagen & Co'
    if 'psnlifestyle' in t: return 'PSNLifestyle'
    if 'phyto pro' in t or 'phytopro' in t or 'phyto pro' in b_raw_low: return 'Phyto Pro'
    if 'harvest table' in t or 'harvest table' in b_raw_low: return 'The Harvest Table'
    if 'youthful living' in t or 'youthful living' in b_raw_low: return 'Youthful Living'
    if '32gi' in t or '32gi' in b_raw_low: return '32Gi'
    if 'peak' in t or 'peak' in b_raw_low: return 'Peak'
    if 'health connection' in t or 'health connection' in b_raw_low: return 'Health Connection'
    return 'Other Brands'

def is_valid_protein_powder(title, url=""):
    t = (str(title) + " " + str(url or "")).lower()
    
    # Exclude empty category landing pages
    if str(title).strip().lower() in ['proteins', 'protein', 'supplements', 'all whey']:
        return False
    if 'catalog/category/view/id/1135' in (url or ''):
        return False

    # Exclude baby / infant formula / medical clinical nutrition drinks
    if any(k in t for k in ['nankid', 'infant', 'baby', 'molkosan', 'albumax', 'medidrink', 'fresubin']):
        return False

    # Exclude pure creatine / amino / preworkout powders that are not protein powders
    if ('creatine' in t or 'amino' in t) and not any(k in t for k in ['whey', 'protein', 'isolate', 'casein', 'vegan', 'plant', 'mass', 'anabolic']):
        return False

    # Exclude single-serving 32g sachets
    if re.search(r'\b(32g|30g|25g|sachet)\b', t) and not any(k in t for k in ['per serving', 'serving', '20 x', 'box']):
        return False

    # Exclude liquid RTD drinks, ready-to-drink bottled shakes (e.g. 414ml, 330ml, ready to drink, rtd)
    if re.search(r'\b\d+\s*ml\b', t) or any(k in t for k in ['414ml', '330ml', '500ml', '250ml', 'ready to drink', 'ready-to-drink', ' rtd ']):
        return False
    if 'shake' in t and any(k in t for k in ['ml', 'drink', 'bottle', 'liquid', 'ready']):
        return False

    # Exclude bars, snacks, biscuits, bites, chips, nougats, pouches, oils, pills
    if re.search(r'\b(bar|bars|snack|nougat|chips|pasta|oil|drops|capsule|tablet|pill)\b', t):
        return False
    if 'pouch meal' in t or 'cookie bite' in t or 'protein cookie' in t or 'baked cookie' in t or 'protein wafers' in t:
        return False
        
    # Exclude accessories
    if any(k in t for k in ['shaker', 'bottle', 'gym bag', 'funnel']):
        return False

    # Must be a protein powder (Whey, Casein, Plant/Vegan, NiHPRO, Collagen, Bone Broth, Beef, Hybrid Meal)
    if not any(k in t for k in ['whey', 'protein', 'isolate', 'iso', 'casein', 'future', 'nitro-tech', 'nitrotech', 'nitro tech', 'halo pro', 'whey-bolic', 'wheybolic', 'vegan', 'plant', 'nihpro', 'collagen', 'bone broth', 'beef', 'phyto']):
        return False
        
    return True

def parse_weight_g(title, container_size_str=None):
    search_str = f"{title} {container_size_str or ''}".strip()
    # Normalize decimal commas (e.g. 1,6kg -> 1.6kg)
    search_str = re.sub(r'(\d+),(\d+)', r'\1.\2', search_str)
    
    # Check for kg and g patterns, excluding nutrient matches (e.g. 24g protein, 5g bcaa)
    matches = list(re.finditer(r'(\d+(?:\.\d+)?)\s*(k?g)\b', search_str, re.IGNORECASE))
    valid_weights = []
    for m in matches:
        after = search_str[m.end():m.end()+15].strip().lower()
        if re.match(r'^(?:protein|bcaa|sugar|carb|fat|dietary|serving|amino|leucine|glutamine)', after):
            continue
        is_kg = m.group(2).lower() == 'kg'
        val = float(m.group(1))
        grams = round(val * 1000.0) if is_kg else round(val)
        if grams >= 150:
            if 1590 <= grams <= 1620:
                grams = 1600
            elif 890 <= grams <= 920 and grams != 900:
                grams = 908
            valid_weights.append(grams)
            
    if valid_weights:
        return float(valid_weights[-1])
        
    s_low = search_str.lower()
    if '4.53' in s_low or '4.54' in s_low or '10 lb' in s_low or '10lb' in s_low: return 4530.0
    if '3kg' in s_low or '3 kg' in s_low: return 3000.0
    if '2.28' in s_low or '2.27' in s_low or '5 lb' in s_low or '5lb' in s_low: return 2270.0
    if '2kg' in s_low or '2 kg' in s_low: return 2000.0
    if '1.92' in s_low or '1920' in s_low: return 1920.0
    if '1.8' in s_low or '1800' in s_low: return 1800.0
    if '1.6' in s_low or '1600' in s_low: return 1600.0
    if '1.5' in s_low or '1500' in s_low: return 1500.0
    if '1kg' in s_low or '1 kg' in s_low or '2 lb' in s_low or '1000g' in s_low: return 1000.0
    if '957' in s_low: return 957.0
    if '930' in s_low: return 930.0
    if '908' in s_low or '900' in s_low: return 908.0
    if '899' in s_low or '896' in s_low or '891' in s_low: return 900.0
    if '800' in s_low: return 800.0
    if '769' in s_low or '750' in s_low or '704' in s_low or '700' in s_low: return 750.0
    if '500' in s_low: return 500.0
    if '454' in s_low or '1 lb' in s_low or '426' in s_low or '408' in s_low or '400' in s_low: return 454.0
    return 1000.0

FAMILY_TYPE_MAP = {
    'Nutritech Heavy Duty Whey': 'Hardcore / All-in-One',
    'Nutritech Premium Whey Protein': 'Whey Blend',
    'Nutritech Proven Protein': 'Multi-Source / Meal Blend',
    'Nutritech Isolate Protein': 'Whey Isolate',
    'Nutritech Clear Whey Isolate': 'Clear Whey / Protein Water',
    'Nutritech 100% Vegan Protein': 'Plant / Vegan Protein',
    'Nutritech ProSport Vegan Protein': 'Plant / Vegan Protein',
    'Nutritech Casein Slow Release': 'Casein / Milk Protein',
    'USN BlueLab 100% Whey': 'Whey Blend',
    'USN Hydrotec Whey (HydroTech)': 'Whey Blend',
    'USN Hardcore Whey gH': 'Hardcore / All-in-One',
    'USN Hardcore Whey gH Ripped': 'Hardcore / All-in-One',
    'USN IsoZero 100% Whey Isolate': 'Whey Isolate',
    'USN IsoPro 100% Beef Isolate': 'Collagen / Beef / Broth',
    'USN Diet Fuel UltraLean': 'Multi-Source / Meal Blend',
    'USN Protein Water + Hydration': 'Clear Whey / Protein Water',
    'Optimum Nutrition Gold Standard 100% Whey': 'Whey Blend',
    'Optimum Nutrition Gold Standard 100% Isolate': 'Whey Isolate',
    'Optimum Nutrition Gold Standard 100% Casein': 'Casein / Milk Protein',
    'Optimum Nutrition Platinum HydroWhey': 'Whey Isolate',
    'NPL Platinum Whey +': 'Whey Blend',
    'NPL Anabolic Whey': 'Hardcore / All-in-One',
    'NPL 100% Whey Isolate': 'Whey Isolate',
    'NPL 100% Plant Protein': 'Plant / Vegan Protein',
    'Muscle Works Whey-Bolic': 'Hardcore / All-in-One',
    'Muscle Works 100% Whey Protein': 'Whey Blend',
    'Muscle Works Superior Whey': 'Whey Blend',
    'Muscle Works Thermo Whey': 'Diet / Lean Whey',
    'MuscleTech Nitro-Tech 100% Whey Gold': 'Whey Blend',
    'MuscleTech Nitro-Tech Ripped': 'Diet / Lean Whey',
    'Biogen 100% Whey Isolate': 'Whey Isolate',
    'Biogen Iso-Whey Premium': 'Whey Blend',
    'Biogen Pro Series 100% Whey': 'Whey Blend',
    'Biogen Complete Blended Protein': 'Multi-Source / Meal Blend',
    'My Wellness Super Clean Protein x5': 'Multi-Source / Meal Blend',
    'My Wellness Alpha Whey': 'Hardcore / All-in-One',
    'Gloot Vegan Protein Water': 'Plant / Vegan Protein',
    'FutureLife High Protein Smart Food': 'Multi-Source / Meal Blend',
    'FutureLife Repair Food Shake': 'Collagen / Beef / Broth',
    'FutureLife Beauti Food Shake': 'Collagen / Beef / Broth',
}

def determine_type(title, ing="", family_name=""):
    if family_name and family_name in FAMILY_TYPE_MAP:
        return FAMILY_TYPE_MAP[family_name]
    t = (title or "").lower()
    if any(k in t for k in ['vegan', 'plant', 'nihpro', 'phyto pro', 'pea protein']) and not any(k in t for k in ['proven', 'complete whey', 'blended protein', 'super clean', 'diet fuel', 'diet pro']):
        return 'Plant / Vegan Protein'
    if 'casein' in t or 'milk protein' in t or "nature's milk" in t:
        return 'Casein / Milk Protein'
    if 'beef' in t or 'bone broth' in t or ('collagen' in t and not any(k in t for k in ['whey', 'vegan', 'phyto', 'water', 'clear'])):
        return 'Collagen / Beef / Broth'
    if 'future' in t or 'proven' in t or 'super clean' in t or 'complete whey' in t or 'blended protein' in t or 'beast' in t or 'diet fuel' in t or 'diet pro' in t:
        return 'Multi-Source / Meal Blend'
    if 'clear whey' in t or 'protein water' in t or 'collagen pro' in t:
        return 'Clear Whey / Protein Water'
    if ('isolate' in t or 'iso-tech' in t or 'iso gold' in t or 'isopro' in t or 'iso pro' in t or 'isozero' in t or 'iso zero' in t or 'iso-whey' in t) and not any(k in t for k in ['blend', 'matrix', 'proven', 'heavy duty', 'heavy-duty', 'premium whey', 'beef', 'plant', 'vegan', 'bluelab', 'blue lab']):
        return 'Whey Isolate'
    if 'hardcore' in t or 'whey gh' in t or 'anabolic' in t or 'heavy duty' in t or 'heavy-duty' in t or 'whey-bolic' in t or 'wheybolic' in t:
        return 'Hardcore / All-in-One'
    if ('diet' in t or 'ripped' in t or 'for her' in t or 'carnitine' in t or 'lite' in t or 'meltdown' in t or 'thermo' in t or 'whey slim' in t or ('lean' in t and not any(m in t for m in ['lean muscle', 'lean mass']))) and not any(k in t for k in ['bluelab', 'blue lab', 'hydrotech', 'hydrotec', 'gold standard', 'premium whey']):
        return 'Diet / Lean Whey'
    if 'concentrate' in t or 'grass-fed whey' in t or 'grass fed whey' in t or 'naked pure whey' in t:
        return 'Whey Concentrate'
    return 'Whey Blend'

def get_product_family_key(title, brand):
    t = (title or '').lower()
    b = (brand or '').lower()
    
    # 1. Nutritech Families
    if 'nutritech' in b or 'nutritech' in t:
        if 'nihpro' in t: return ('Nutritech', 'Nutritech NiHPRO Protein Isolate')
        if ('pro sport' in t or 'prosport' in t) and 'vegan' in t: return ('Nutritech', 'Nutritech ProSport Vegan Protein')
        if 'vegan' in t and 'water' in t: return ('Nutritech', 'Nutritech Vegan Protein Water')
        if 'vegan' in t: return ('Nutritech', 'Nutritech 100% Vegan Protein')
        if 'clear whey' in t or 'protein water' in t: return ('Nutritech', 'Nutritech Clear Whey Isolate')
        if 'proven' in t: return ('Nutritech', 'Nutritech Proven Protein')
        if 'heavy duty' in t or 'heavy-duty' in t: return ('Nutritech', 'Nutritech Heavy Duty Whey')
        if 'notorious' in t: return ('Nutritech', 'Nutritech Notorious Whey')
        if 'isolate' in t: return ('Nutritech', 'Nutritech Isolate Protein')
        if 'pro sport' in t or 'prosport' in t: return ('Nutritech', 'Nutritech Pro Sport Premium Whey')
        if 'casein' in t: return ('Nutritech', 'Nutritech Casein Slow Release')
        return ('Nutritech', 'Nutritech Premium Whey Protein')
        
    # 2. USN Families
    if 'usn' in b or 'usn' in t:
        if 'hydrotech' in t or 'hydrotec' in t or 'hydro tech' in t:
            return ('USN', 'USN Hydrotec Whey (HydroTech)')
        if 'bluelab' in t or 'blue lab' in t:
            if 'plant' in t and ('plato' in t or 'matcha' in t): return ('USN', 'USN BlueLab Plato Plant Protein')
            if 'plant' in t: return ('USN', 'USN BlueLab 100% Plant Protein')
            return ('USN', 'USN BlueLab 100% Whey')
        if 'hardcore' in t or 'whey gh' in t:
            if 'ripped' in t: return ('USN', 'USN Hardcore Whey gH Ripped')
            return ('USN', 'USN Hardcore Whey gH')
        if 'isozero' in t or 'iso zero' in t:
            return ('USN', 'USN IsoZero 100% Whey Isolate')
        if 'isopro' in t or 'iso pro' in t:
            if 'beef' in t: return ('USN', 'USN IsoPro 100% Beef Isolate')
            return ('USN', 'USN IsoPro Zero Carb')
        if 'beast' in t: return ('USN', 'USN Beast Multi-Protein')
        if 'diet fuel' in t: return ('USN', 'USN Diet Fuel UltraLean')
        if 'protein water' in t: return ('USN', 'USN Protein Water + Hydration')
        if 'collagen' in t: return ('USN', 'USN 100% Pure Collagen Peptides')
        return ('USN', 'USN BlueLab 100% Whey')
        
    # 3. Muscle Works Families
    if 'muscle works' in b or 'muscleworks' in b:
        if 'whey-bolic' in t or 'wheybolic' in t: return ('Muscle Works', 'Muscle Works Whey-Bolic')
        if 'superior whey' in t: return ('Muscle Works', 'Muscle Works Superior Whey')
        if 'thermo whey' in t: return ('Muscle Works', 'Muscle Works Thermo Whey')
        if 'iso-tech' in t or 'isotech' in t: return ('Muscle Works', 'Muscle Works Iso-Tech Whey')
        return ('Muscle Works', 'Muscle Works 100% Whey Protein')
        
    # 4. Optimum Nutrition Families
    if 'optimum nutrition' in b or 'on' == b or 'optimum' in b or 'optimum' in t:
        if 'hydro whey' in t or 'hydrowhey' in t: return ('Optimum Nutrition', 'Optimum Nutrition Platinum HydroWhey')
        if 'isolate' in t: return ('Optimum Nutrition', 'Optimum Nutrition Gold Standard 100% Isolate')
        if 'casein' in t: return ('Optimum Nutrition', 'Optimum Nutrition Gold Standard 100% Casein')
        return ('Optimum Nutrition', 'Optimum Nutrition Gold Standard 100% Whey')
        
    # 5. NPL Families
    if 'npl' in b or 'npl' in t:
        if 'plant' in t or 'vegan' in t: return ('NPL', 'NPL 100% Plant Protein')
        if 'collagen pro' in t: return ('NPL', 'NPL Collagen Pro Hybrid Water')
        if 'diet pro' in t: return ('NPL', 'NPL Diet Pro Meal Replacement')
        if 'platinum whey' in t: return ('NPL', 'NPL Platinum Whey +')
        if 'anabolic whey' in t: return ('NPL', 'NPL Anabolic Whey')
        if 'whey isolated' in t or 'isolate' in t: return ('NPL', 'NPL 100% Whey Isolate')
        if 'halo pro' in t: return ('NPL', 'NPL Halo Pro Whey')
        if 'whey slim' in t: return ('NPL', 'NPL Whey Slim')
        return ('NPL', 'NPL Platinum Whey +')
        
    # 6. Biogen Families
    if 'biogen' in b or 'biogen' in t:
        if 'plant' in t: return ('Biogen', 'Biogen Plant Based Protein')
        if 'clear' in t: return ('Biogen', 'Biogen Clear Whey Collagen')
        if 'peptan' in t or ('collagen' in t and 'whey' not in t): return ('Biogen', 'Biogen Peptan Collagen Powder')
        if 'collagen & whey' in t: return ('Biogen', 'Biogen Collagen & Whey Protein')
        if 'complete whey' in t or 'blended protein' in t: return ('Biogen', 'Biogen Complete Blended Protein')
        if 'whey isolate' in t or 'pure isolate' in t or (('isolate' in t or 'iso' in t) and 'tri-matrix' not in t and 'tri matrix' not in t and 'premium iso' not in t and 'iso whey' not in t):
            return ('Biogen', 'Biogen 100% Whey Isolate')
        if 'iso' in t or 'isolate' in t: return ('Biogen', 'Biogen Iso-Whey Premium')
        if 'diet' in t or 'lean' in t: return ('Biogen', 'Biogen Diet Protein Shake')
        return ('Biogen', 'Biogen Pro Series 100% Whey')
        
    # 7. MuscleTech Families
    if 'muscletech' in b or 'muscletech' in t:
        if 'ripped' in t: return ('MuscleTech', 'MuscleTech Nitro-Tech Ripped')
        if 'nitro-tech' in t or 'nitrotech' in t or 'nitro tech' in t: return ('MuscleTech', 'MuscleTech Nitro-Tech 100% Whey Gold')
        if 'phase8' in t: return ('MuscleTech', 'MuscleTech Phase8 Sustained Release')
        return ('MuscleTech', 'MuscleTech Nitro-Tech 100% Whey Gold')
        
    # 8. My Wellness Families
    if 'my wellness' in b or 'mywellness' in b or 'alpha whey' in t:
        if 'alpha' in t: return ('My Wellness', 'My Wellness Alpha Whey')
        if 'vegan' in t: return ('My Wellness', 'My Wellness Super Vegan Protein')
        if 'milk protein' in t: return ('My Wellness', "My Wellness Nature's Milk Protein")
        if 'clean diet whey' in t: return ('My Wellness', 'My Wellness Clean Diet Whey')
        if 'clean whey' in t or 'clean protein' in t or 'super clean' in t:
            if 'isolate' in t: return ('My Wellness', 'My Wellness Clean Whey Isolate')
            return ('My Wellness', 'My Wellness Super Clean Protein x5')
        if 'clear whey' in t: return ('My Wellness', 'My Wellness Clear Whey ISO')
        if 'grass fed' in t or 'grass-fed' in t:
            if 'isolate' in t: return ('My Wellness', 'My Wellness Grass-Fed Whey Isolate')
            return ('My Wellness', 'My Wellness Grass-Fed Whey Concentrate')
        if 'isolate' in t: return ('My Wellness', 'My Wellness Clean Whey Isolate')
        if 'superior whey' in t: return ('My Wellness', 'My Wellness Superior Whey')
        return ('My Wellness', 'My Wellness Natures Whey')
        
    # 9. Myprotein Families
    if 'myprotein' in b or 'myprotein' in t:
        if 'clear whey' in t: return ('Myprotein', 'Myprotein Clear Whey Isolate')
        if 'isolate' in t: return ('Myprotein', 'Myprotein Impact Whey Isolate')
        return ('Myprotein', 'Myprotein Impact Whey Protein')
        
    # 10. SSA Supplements Families
    if 'ssa' in b or 'ssa' in t:
        if 'vegan' in t: return ('SSA Supplements', 'SSA Supplements Vegan Protein')
        if 'extreme' in t: return ('SSA Supplements', 'SSA Supplements Whey Extreme')
        if 'pure whey' in t or '100% whey' in t: return ('SSA Supplements', 'SSA Supplements Pure Whey')
        if 'diet whey' in t: return ('SSA Supplements', 'SSA Supplements Diet Whey')
        return ('SSA Supplements', 'SSA Supplements Whey Extreme')
        
    # 11. Evox Families
    if 'evox' in b or 'evox' in t:
        if 'leanpro' in t or 'diet' in t: return ('Evox', 'Evox Leanpro Diet Protein')
        return ('Evox', 'Evox 100% Whey Protein Advanced')
        
    # 12. GNC Families
    if 'gnc' in b or 'gnc' in t:
        if 'amp' in t: return ('GNC', 'GNC Pro Performance AMP Amplified Gold')
        return ('GNC', 'GNC Pro Performance 100% Whey')
        
    # 13. Gloot
    if 'gloot' in b or 'gloot' in t:
        if 'vegan' in t: return ('Gloot', 'Gloot Vegan Protein Water')
        if 'water' in t: return ('Gloot', 'Gloot Collagen & Whey Protein Water')
        return ('Gloot', 'Gloot Whey Protein For Her')
        
    # 14. FutureLife
    if 'future' in b or 'future' in t:
        if 'repair' in t: return ('FutureLife', 'FutureLife Repair Food Shake')
        if 'beauti' in t: return ('FutureLife', 'FutureLife Beauti Food Shake')
        return ('FutureLife', 'FutureLife High Protein Smart Food')
        
    # 15. PrimeSelf
    if 'primeself' in b or 'primeself' in t:
        return ('PrimeSelf', 'PrimeSelf Grass-Fed Whey Protein')
        
    # 16. Black Bull
    if 'black bull' in b or 'blackbull' in b:
        return ('Black Bull', 'Black Bull Whey Supreme')
        
    # 17. Tony Ferguson
    if 'tony ferguson' in b or 'tony ferguson' in t:
        return ('Tony Ferguson', 'Tony Ferguson 100% Whey Protein')
        
    # 18. Sci-Core
    if 'sci-core' in b or 'scicore' in b:
        if 'one whey' in t: return ('Sci-Core', 'Sci-Core One Whey Protein')
        return ('Sci-Core', 'Sci-Core Naked Pure Whey')

    # 19. PSNLifestyle Families
    if 'psnlifestyle' in b or 'psn' in b or 'psnlifestyle' in t or 'psn' in t:
        if 'meltdown' in t or 'fat burner' in t:
            return ('PSNLifestyle', 'PSNLifestyle Meltdown Whey Fat Burner')
        return ('PSNLifestyle', 'PSNLifestyle MRP Whey Protein')

    # 20. Rogue Legion Families
    if 'rogue legion' in b or 'rogue legion' in t or 'rogue' in b or 'rogue' in t:
        return ('Rogue Legion', 'Rogue Legion Lifestyle Whey Protein')

    # 21. Phyto Pro Families
    if 'phyto pro' in b or 'phyto pro' in t:
        if 'sport' in t: return ('Phyto Pro', 'Phyto Pro Sport Active Recovery')
        if 'collagen' in t: return ('Phyto Pro', 'Phyto Pro Vegan Collagen Protein')
        if 'muscle' in t: return ('Phyto Pro', 'Phyto Pro Muscle Lean Protein')
        return ('Phyto Pro', 'Phyto Pro Thrive Daily Pea Protein')

    # 22. The Harvest Table & Lifestyle Food
    if 'harvest table' in b or 'harvest table' in t:
        if 'bone broth' in t: return ('The Harvest Table', 'The Harvest Table Organic Bone Broth')
        return ('The Harvest Table', 'The Harvest Table Pure Collagen')
    if 'lifestyle food' in b or 'lifestyle food' in t:
        if 'bone broth' in t: return ('Lifestyle Food', 'Lifestyle Food Pure Bone Broth')
        return ('Lifestyle Food', 'Lifestyle Food Whey Protein')
    if 'primal' in b or 'primal' in t:
        if 'casein' in t: return ('Primal', 'Primal Micellar Casein')
        if 'isolate' in t: return ('Primal', 'Primal 100% Whey Isolate')
        return ('Primal', 'Primal 100% Whey Protein')
    if 'youthful living' in b or 'youthful living' in t:
        return ('Youthful Living', 'Youthful Living Vegan Protein')
    if '32gi' in b or '32gi' in t:
        return ('32Gi', '32Gi Plant Based Protein Shake')
    if 'peak' in b or 'peak' in t:
        return ('Peak', 'Peak Plant Protein Shake')
    if 'lifeworth' in b or 'lifeworth' in t or 'b0fj7m74k1' in t:
        return ('Lifeworth', 'Lifeworth Super Standard 100% Whey')
    if 'biyode' in b or 'biyode' in t or 'b0f9twj4hq' in t:
        return ('Biyode', 'Biyode Whey Protein Powder')

    # 23. Clicks Smartlife
    if 'smartlife' in b or 'smartlife' in t or ('clicks' in b and 'purified' in t):
        if 'purified' in t: return ('Clicks Smartlife', 'Clicks Smartlife Purified Protein')
        return ('Clicks Smartlife', 'Clicks Smartlife Whey Protein')

    # 24. Just Protein
    if 'just protein' in b or 'just protein' in t:
        if 'isolate' in t: return ('Just Protein', 'Just Protein Pure Whey Isolate')
        return ('Just Protein', 'Just Protein Premium Whey Protein')

    # 25. Alpha Whey (My Wellness)
    if 'alpha whey' in t or ('alpha' in b and 'whey' in t):
        return ('My Wellness', 'My Wellness Alpha Whey')

    # 26. Nature's Whey (standalone brand, distinct from My Wellness Nature's Whey)
    if ('nature\'s whey' in b or 'natures whey' in b) and 'my wellness' not in b:
        return ("Nature's Whey", "Nature's Whey Protein Powder")

    # 27. Muscle Dynamix
    if 'muscle dynamix' in b or 'dynamix' in b or ('muscle dynamix' in t and 'muscle works' not in b):
        if 'iso gold' in t: return ('Muscle Dynamix', 'Muscle Dynamix Iso Gold')
        if 'whey one' in t: return ('Muscle Dynamix', 'Muscle Dynamix Whey One Premium')
        return ('Muscle Dynamix', 'Muscle Dynamix Whey Protein')

    # 28. TNT Mercury
    if 'tnt mercury' in b or 'tnt mercury' in t or 'tnt' in b:
        if 'mega whey' in t or 'atomic' in t: return ('TNT Mercury', 'TNT Mercury Atomic Mega Whey')
        if 'prime whey' in t: return ('TNT Mercury', 'TNT Mercury Prime Whey')
        return ('TNT Mercury', 'TNT Mercury Whey Protein')

    # 29. Blast Vitality
    if 'blast vitality' in b or (b.strip() == 'blast') or ('blast vitality' in t):
        return ('Blast Vitality', 'Blast Vitality Daily Protein')

    # 30. Clear Nutrition
    if 'clear nutrition' in b or 'clear nutrition' in t:
        return ('Clear Nutrition', 'Clear Nutrition 100% Whey Protein')

    # Generic
    clean_t = re.sub(r'[\d\.]+\s*(?:kg|g|lb)\b', '', title, flags=re.IGNORECASE)
    # Strip common flavor descriptors from product line name so all flavors group together under the parent product
    clean_t = re.sub(r'\b(?:double chocolate|rich chocolate|creamy vanilla|vanilla ice cream|chocolate truffle|chocolate milk|chocolate|choc|vanilla|strawberry|berries|berry|banana|caramel latte|salted caramel|caramel|coffee|peanut butter|cookies|cinnamon|hazelnut|unflavoured|unflavored|natural|mocha|chocotella)\b', '', clean_t, flags=re.IGNORECASE)
    clean_t = re.sub(r'-\s*[^$]*', '', clean_t).strip(' -_,|')
    clean_t = re.sub(r'\s+', ' ', clean_t).strip()
    return (brand, clean_t or f"{brand} Whey Protein")

# Authentic Formulations

def determine_flavor(title, flavor_raw=None):
    t = (title or '').lower()
    flavors = [
        ('Dark Chocolate & Sea Salt', 'Dark Chocolate & Sea Salt'),
        ('Dark Chocolate', 'Dark Chocolate'),
        ('Berries & Cream', 'Berries & Cream'),
        ('Café Mocha', 'Café Mocha'),
        ('Cafe Mocha', 'Café Mocha'),
        ('Chocolate Peanut Butter', 'Choc Peanut Butter'),
        ('Chocolate Cookie Dough', 'Choc Cookie Dough'),
        ('Vanilla Cookie Dough', 'Vanilla Cookie Dough'),
        ('Double Chocolate', 'Double Chocolate'),
        ('Chocolate Nougat', 'Chocolate Nougat'),
        ('Double Rich Chocolate', 'Double Rich Chocolate'),
        ('Chocolate Supreme', 'Chocolate Supreme'),
        ('Chocolate Wafer', 'Chocolate Wafer'),
        ('Chocolate Truffle', 'Chocolate Truffle'),
        ('Cinnamon Doughnut', 'Cinnamon Doughnut'),
        ('Cinnamon Donut', 'Cinnamon Doughnut'),
        ('Wafer Biscuit', 'Wafer Biscuit'),
        ('Double Decker', 'Double Decker'),
        ('Nutella Waffle', 'Nutella Waffle'),
        ('Hazelnut Praline', 'Hazelnut Praline'),
        ('Speckled Eggs', 'Speckled Eggs'),
        ('Blueberry Muffin', 'Blueberry Muffin'),
        ('Vanilla Ice Cream', 'Vanilla Ice Cream'),
        ('Vanilla Milkshake', 'Vanilla Milkshake'),
        ('Vanilla Bean', 'Vanilla Bean'),
        ('Vanilla Cream', 'Vanilla Cream'),
        ('Caramel Latte', 'Caramel Latte'),
        ('Caramel Fudge', 'Caramel Fudge'),
        ('Tin Roof', 'Tin Roof'),
        ('Watermelon', 'Watermelon'),
        ('Peach', 'Peach'),
        ('Berry', 'Berry'),
        ('Peanut Butter', 'Peanut Butter'),
        ('Mocha', 'Mocha'),
        ('Strawberry', 'Strawberry'),
        ('Chocolate', 'Chocolate'),
        ('Vanilla', 'Vanilla'),
        ('Banana', 'Banana'),
        ('Coffee', 'Coffee'),
        ('Salted Caramel', 'Salted Caramel'),
        ('Unflavoured', 'Unflavoured / Natural'),
        ('Unflavored', 'Unflavoured / Natural')
    ]
    for key, name in flavors:
        if key.lower() in t:
            return name
    if flavor_raw and len(flavor_raw) > 2:
        return flavor_raw.strip().title()
    return 'Classic (Vanilla / Chocolate)'

