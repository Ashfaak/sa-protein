import re

def compute_protein_quality_scores(ptype, ingredients="", title=""):
    text = (str(ingredients) + " " + str(title)).lower()
    t = (title or "").lower()
    
    # 0. USN Hydrotec / HydroTech (Whey + Wheat Gluten Blend)
    if 'hydrotech' in t or 'hydrotec' in t or 'hydro tech' in t or 'wheat protein' in text:
        if 'plato' in t and 'plant' in t:
            return {
                'diaas_score': 0.78,
                'diaas_rating': '🌱 Plant + Wheat (78%)',
                'diaas_category': 'Wheat, Pea, Pumpkin & Watermelon Blend',
                'pdcaas_score': 0.82,
                'quality_summary': 'Blend of Wheat protein (gluten), Pea protein isolate, Pumpkin seed, and Watermelon seed protein with 48mg caffeine from Plato Matcha.'
            }
        return {
            'diaas_score': 0.96,
            'diaas_rating': '⚠️ Moderate (96% - Wheat Blend)',
            'diaas_category': 'Whey + Wheat Gluten Blend (Hydrotec™)',
            'pdcaas_score': 0.92,
            'quality_summary': 'Staged-release blend of Whey (WPH, WPC) diluted with Hydrolysed Wheat Protein & Wheat Gluten. Delivers 20g protein (1.9g Leucine, 4.1g BCAAs, 7.5g Glutamic Acid) per 30g scoop with DigeZyme®.'
        }

    # 0.2. USN BlueLab 100% Whey (100% Pure 3-Stage Whey)
    if ('bluelab' in t or 'blue lab' in t) and 'plant' not in t:
        return {
            'diaas_score': 1.25,
            'diaas_rating': '⭐ Excellent (125%)',
            'diaas_category': '100% Pure 3-Stage Whey (WPI + WPH + WPC)',
            'pdcaas_score': 1.00,
            'quality_summary': '100% pure 3-stage dairy whey (Isolate, Hydrolysate, Concentrate) with zero wheat or plant fillers. High leucine (2.5g) & BCAAs (5.3g) per 32g scoop with Tolerase™ L lactase.'
        }

    # 0.3. Nutritech NiHPRO Molecularly Calibrated Isolate
    if 'nihpro' in text:
        return {
            'diaas_score': 1.16,
            'diaas_rating': '🌱 Calibrated Isolate (116%)',
            'diaas_category': 'EAA-Calibrated Pea & Rice Isolate (NiHPRO™)',
            'pdcaas_score': 1.00,
            'quality_summary': 'Hydrolysed Pea & Rice protein isolate fortified with free-form L-Leucine (2.76g), L-Lysine, and L-Methionine to match whey amino acid bioavailability (81.6% protein purity).'
        }

    # 0.4. Plant / Vegan Protein Powders
    if ptype == 'Plant / Vegan Protein' or any(k in t for k in ['vegan', 'plant', 'phyto pro', '32gi', 'soy', 'yeast']):
        if 'yeast' in text or 'yeast' in t:
            return {
                'diaas_score': 0.96,
                'diaas_rating': '🌱 Fermented Yeast Isolate (96%)',
                'diaas_category': 'Fermentation-Derived Yeast Protein Isolate',
                'pdcaas_score': 1.00,
                'quality_summary': 'Fermentation-derived complete protein isolate paired with fava bean, fortified with DigeZyme® multi-enzyme complex and LactoSpore® probiotics (0.96 DIAAS, 1.00 PDCAAS).'
            }
        if 'soy' in text or 'soy' in t:
            return {
                'diaas_score': 0.88,
                'diaas_rating': '🌱 Pure Soy Isolate (88%)',
                'diaas_category': '100% Soy Protein Isolate',
                'pdcaas_score': 0.98,
                'quality_summary': '100% non-GMO Soy Protein Isolate delivering a complete essential amino acid profile with high ileal digestibility (~88% DIAAS, 0.98 PDCAAS) and zero dairy.'
            }
        if any(k in text for k in ['rice', 'hemp', 'pumpkin', 'faba', 'fava', 'chickpea', 'quinoa']):
            return {
                'diaas_score': 0.91,
                'diaas_rating': '🌱 Multi-Plant (91%)',
                'diaas_category': 'Complementary Multi-Plant Matrix',
                'pdcaas_score': 0.93,
                'quality_summary': 'Complementary plant protein blend (Pea + Rice/Hemp/Seed) balances methionine and lysine limitations for a more complete vegan amino acid profile.'
            }
        return {
            'diaas_score': 0.82,
            'diaas_rating': '🌱 Pure Pea Isolate (82%)',
            'diaas_category': '100% Golden Pea Protein Isolate',
            'pdcaas_score': 0.89,
            'quality_summary': 'Hypoallergenic, dairy-free 100% Pea Protein Isolate. Naturally rich in arginine and branched-chain amino acids (~82% DIAAS, limited slightly by methionine).'
        }

    # 0.45. Lifeworth Super Standard 100% Whey (Whey + Bovine Collagen Blend)
    if 'lifeworth' in t or 'b0fj7m74k1' in t:
        return {
            'diaas_score': 0.88,
            'diaas_rating': '⚠️ Moderate (88% - Collagen Blend)',
            'diaas_category': 'Whey + Bovine Collagen + Polydextrose',
            'pdcaas_score': 0.85,
            'quality_summary': 'Blend of Whey Isolate, Whey Concentrate, and Hydrolyzed Bovine Collagen with Polydextrose. Delivers 10g protein (33.3% purity) and 18.4g carbohydrates per 30g serving.'
        }

    # 0.5. Casein & Slow-Release Milk Protein
    if ptype == 'Casein / Milk Protein' or 'casein' in t or "nature's milk" in t:
        return {
            'diaas_score': 1.28,
            'diaas_rating': '🌙 Elite Slow-Release (128%)',
            'diaas_category': 'Micellar Casein / Milk Protein Isolate',
            'pdcaas_score': 1.00,
            'quality_summary': 'Slow-digesting anti-catabolic dairy protein (6-8 hour sustained amino acid release) with exceptional ileal digestibility (128% DIAAS).'
        }

    # 0.6. Beef Isolate, Bone Broth & Pure Collagen
    if ptype == 'Collagen / Beef / Broth' or 'beef' in t or 'bone broth' in t or ('collagen' in t and 'whey' not in t):
        if 'beef' in t or 'bone broth' in t:
            return {
                'diaas_score': 0.38,
                'diaas_rating': '🥩 Hydrolysed Beef Collagen (38%)',
                'diaas_category': 'Hydrolysed Bovine Connective Tissue Peptides',
                'pdcaas_score': 0.42,
                'quality_summary': '100% dairy-free hydrolysed bovine collagen isolate. Extremely rich in Glycine (5.3g) and Proline (2.9g) for joints, tendons, and gut health, but heavily deficient in EAAs (only 4.3g EAAs/scoop) and BCAAs (0.7g Leucine) with an ileal DIAAS of 38%.'
            }
        return {
            'diaas_score': 0.45,
            'diaas_rating': '🦴 Connective Tissue (45%)',
            'diaas_category': 'Pure Hydrolysed Collagen Peptides',
            'pdcaas_score': 0.40,
            'quality_summary': '90-97% protein purity specialized for tendons, ligaments, cartilage, skin, and gut lining (high Glycine/Proline/Hydroxyproline, lacks Tryptophan for standalone muscle building).'
        }

    # 0.65. FutureLife SmartProtein3D / Hybrid Meal
    if 'future' in text or 'smartprotein3d' in text:
        return {
            'diaas_score': 0.88,
            'diaas_rating': '⚠️ Moderate (88%)',
            'diaas_category': 'Soy & Grain Dominant Hybrid (SmartProtein3D™)',
            'pdcaas_score': 0.92,
            'quality_summary': 'Formulated with 43% SmartProtein3D™ (Soy flour, soy isolate, skim milk, whey concentrate, caseinate) and SmartMaize™. Primary protein is plant-based (soy), with moderate DIAAS (88%) and higher carbohydrate content (39%).'
        }

    # 0.7. Muscle Works Whey-Bolic (Post-Workout Anabolic Glycogen & Amino Complex)
    if 'whey-bolic' in text or 'wheybolic' in text:
        return {
            'diaas_score': 1.08,
            'diaas_rating': '💪 Anabolic Matrix (108%)',
            'diaas_category': 'Post-Workout Whey + Glycogen Complex',
            'pdcaas_score': 0.98,
            'quality_summary': 'Anabolic post-workout formulation: 22g protein (WPC & WPI) paired with Anabolic Carb Complex (Cream of Rice & Maltodextrin, 10.8g carbs) for glycogen replenishment, plus 4.5g Anabolic Amino Complex (Creatine, Taurine, Glycine, L-Leucine).'
        }

    # 1. Multi-Source Timed-Release Blends (Nutritech Proven, Super Clean X5, Biogen Complete, Beast)
    if 'proven' in text or ptype == 'Multi-Source / Meal Blend':
        return {
            'diaas_score': 1.10,
            'diaas_rating': '⭐ High Hybrid (110%)',
            'diaas_category': 'Multi-Source Timed-Release Matrix (Dairy + Plant)',
            'pdcaas_score': 1.00,
            'quality_summary': 'Multi-stage timed-release matrix combining fast dairy whey with plant isolates and/or micellar casein for extended amino acid delivery.'
        }
        
    # 2. Pure Whey Hydrolysate (Platinum HydroWhey, AMP Gold)
    if 'hydrowhey' in t or 'hydro whey' in t or 'amp amplified' in t or 'amp gold' in t:
        return {
            'diaas_score': 1.32,
            'diaas_rating': '🏆 Maximum (132%)',
            'diaas_category': 'Whey Protein Hydrolysate',
            'pdcaas_score': 1.00,
            'quality_summary': 'Enzymatically pre-cleaved peptide bonds maximize ileal absorption rate and rapid hyperaminoacidemia.'
        }
        
    # 3. Clear Whey / Pure Whey Isolate
    if (ptype in ['Whey Isolate', 'Clear Whey / Protein Water'] or ('isolate' in t and not any(k in t for k in ['blend', 'proven', 'matrix']))) and 'collagen' not in text:
        return {
            'diaas_score': 1.30,
            'diaas_rating': '🏆 Elite (130%)',
            'diaas_category': 'Pure Whey Isolate (WPI)',
            'pdcaas_score': 1.00,
            'quality_summary': 'Exceeds FAO reference standard (130% DIAAS) for all indispensable amino acids, high leucine (~11-12%), ultra-low lactose.'
        }
        
    # 3.9 Mass Gainer (High Carbohydrate to Protein Ratio)
    if ptype == 'Mass Gainer' or any(k in t for k in ['mega mass', 'vegainer', 'hard mass', 'mass gain', 'weight gainer', 'mass gainer']):
        return {
            'diaas_score': 1.00,
            'diaas_rating': '⚖️ High-Carb Gainer (100%)',
            'diaas_category': 'High-Calorie Mass Gainer (Carb-Dominant)',
            'pdcaas_score': 0.95,
            'quality_summary': 'Calorie-dense mass gainer formula with a high carbohydrate-to-protein ratio (55-75% carbs, 15-30% protein) designed for weight gain and bulking.'
        }

    # 4. Hardcore / All-in-One (Creatine, Glycine, Taurine)
    if 'alpha whey' in t or ('alpha' in t and 'anabolic' in text):
        return {
            'diaas_score': 1.05,
            'diaas_rating': '💪 Anabolic All-in-One (105%)',
            'diaas_category': 'Anabolic Multi-Stage & Adaptogen Complex',
            'pdcaas_score': 0.98,
            'quality_summary': 'Anabolic multi-stage protein matrix (Whey Concentrate, Micellar Casein, Pea Protein, Whey Isolate) providing 27g protein (75% purity) fortified with 5,000mg Anabolic Muscle Complex (Creatine, Taurine, Glycine, Tongkat Ali 100:1, Ashwagandha, Tribulus Terrestris).'
        }
    if ptype == 'Hardcore / All-in-One' or 'creatine' in text or 'anabolic' in text:
        return {
            'diaas_score': 1.05,
            'diaas_rating': '💪 Good (105%)',
            'diaas_category': 'Strength Enhanced Complex',
            'pdcaas_score': 0.98,
            'quality_summary': 'High total nitrogen and ergogenic support from added Creatine, Glycine, and Taurine; tailored for strength & mass recovery (105% DIAAS).'
        }

    # 5. Diet / Lean Whey (Check if blended with collagen)
    if 'collagen' in text:
        return {
            'diaas_score': 0.90,
            'diaas_rating': '⚠️ Moderate (90%)',
            'diaas_category': 'Whey + Collagen Hybrid',
            'pdcaas_score': 0.90,
            'quality_summary': 'Combines Whey Protein with Hydrolysed Bovine Collagen Peptides. Collagen supports joints/skin but lacks tryptophan, moderating overall muscle DIAAS to 90%.'
        }
    if ptype == 'Diet / Lean Whey':
        return {
            'diaas_score': 1.15,
            'diaas_rating': '⭐ High (115%)',
            'diaas_category': 'Lean Metabolic Whey',
            'pdcaas_score': 1.00,
            'quality_summary': 'Premium whey concentrate fortified with L-Carnitine, CLA, and Garcinia for metabolic enhancement (115% DIAAS).'
        }
        
    # 6. Whey Concentrate
    if ptype == 'Whey Concentrate':
        return {
            'diaas_score': 1.18,
            'diaas_rating': '⭐ Very High (118%)',
            'diaas_category': 'Whole Whey Concentrate',
            'pdcaas_score': 1.00,
            'quality_summary': 'Natural WPC80 preserving native immunoglobulins, lactoferrin, and high biological value (118% DIAAS).'
        }
        
    # 7. 100% Native Whey Blend (Default)
    return {
        'diaas_score': 1.22,
        'diaas_rating': '⭐ Excellent (122%)',
        'diaas_category': '100% Native Whey Matrix (WPC + WPI)',
        'pdcaas_score': 1.00,
        'quality_summary': '100% dairy native whey sourced from pasture-fed cows. High biological value with complete essential amino acid profile (122% DIAAS).'
    }


def assign_product_archetype(p):
    """
    Evaluates product nutritional and market profile to determine its primary
    value proposition / internal archetype (strictly hidden from user) and the
    associated standout metric displayed on alternative cards beneath the modal.
    """
    cpg = p.get('cost_per_g_protein_zar') or 0.0
    rating = p.get('rating') or 0.0
    reviews = p.get('review_count') or 0
    diaas = p.get('diaas_score') or 1.15
    pdcaas = p.get('pdcaas_score') or 1.00
    purity = p.get('protein_percentage') or 75.0
    ptype = (p.get('type') or '').lower()
    title = (p.get('title') or '').lower()
    size = p.get('container_size_g') or 1000.0
    enzymes = (p.get('digestive_enzymes') or '').lower()
    carbs = p.get('carbs_g') or 0.0
    fat = p.get('fat_g') or 0.0
    prot_g = p.get('protein_per_serving_g', 24.0)
    sc_g = p.get('scoop_size_g', 30.0)

    # 1. Bioavailable Plant / Vegan
    if 'plant' in ptype or 'vegan' in ptype:
        return {
            'internal_archetype': 'bioavailable_plant',
            'standout_metric': {
                'label': 'Complete Plant',
                'value': f"DIAAS {diaas:.2f} • PDCAAS {pdcaas:.2f}",
                'icon': 'fa-solid fa-seedling',
                'badge_class': 'badge-archetype-plant'
            }
        }

    # 2. Sustained Release (Casein / Milk Protein)
    if 'casein' in ptype:
        return {
            'internal_archetype': 'sustained_release',
            'standout_metric': {
                'label': 'Slow Release',
                'value': f"Micellar Casein (7-8h)",
                'icon': 'fa-solid fa-moon',
                'badge_class': 'badge-archetype-casein'
            }
        }

    # 3. Clear Whey / Refreshing Juice-style
    if 'clear' in ptype or 'water' in ptype or 'clear' in title:
        return {
            'internal_archetype': 'clear_refreshing',
            'standout_metric': {
                'label': 'Juice Style',
                'value': f"{purity:.0f}% Prot • Light & Fruity",
                'icon': 'fa-solid fa-droplet',
                'badge_class': 'badge-archetype-clear'
            }
        }

    # 4. Joint & Skin Peptides (Collagen / Beef)
    if 'collagen' in ptype or 'beef' in ptype or 'broth' in ptype or 'collagen' in title:
        return {
            'internal_archetype': 'joint_collagen',
            'standout_metric': {
                'label': 'Joint & Skin',
                'value': 'Pure Hydrolysed Peptides',
                'icon': 'fa-solid fa-bone',
                'badge_class': 'badge-archetype-collagen'
            }
        }

    # 5. Diet / Lean Whey (Calorie Control)
    if 'diet' in ptype or 'lean' in ptype:
        return {
            'internal_archetype': 'diet_lean',
            'standout_metric': {
                'label': 'Calorie Control',
                'value': f"Lean Whey ({carbs:.1f}g C / {fat:.1f}g F)",
                'icon': 'fa-solid fa-fire-flame-curved',
                'badge_class': 'badge-archetype-diet'
            }
        }

    # 6. Ultra-Lean Isolate / High Purity
    if purity >= 84.0 or 'isolate' in ptype:
        return {
            'internal_archetype': 'lean_purity',
            'standout_metric': {
                'label': 'Ultra Purity',
                'value': f"{purity:.0f}% Protein ({prot_g}g / {sc_g}g)",
                'icon': 'fa-solid fa-bolt',
                'badge_class': 'badge-archetype-purity'
            }
        }

    # 7. Bulk Saver (Economy volume 2.5kg+)
    if size >= 2500:
        serv = p.get('servings_count') or int(size / (sc_g if sc_g > 0 else 30))
        return {
            'internal_archetype': 'bulk_saver',
            'standout_metric': {
                'label': 'Bulk Economy',
                'value': f"{size/1000:.1f}kg • {serv} Servings",
                'icon': 'fa-solid fa-box-open',
                'badge_class': 'badge-archetype-bulk'
            }
        }

    # 8. Best Value / Cost Leader (top cost efficiency)
    if cpg > 0 and cpg <= 0.45:
        return {
            'internal_archetype': 'cost_leader',
            'standout_metric': {
                'label': 'Best Value',
                'value': f"R {cpg:.2f} / g prot",
                'icon': 'fa-solid fa-coins',
                'badge_class': 'badge-archetype-value'
            }
        }

    # 9. Community Favorite (proven rating + high review count)
    if rating >= 4.6 and reviews >= 20:
        return {
            'internal_archetype': 'community_favorite',
            'standout_metric': {
                'label': 'Top Rated',
                'value': f"★ {rating:.1f} ({reviews} reviews)",
                'icon': 'fa-solid fa-star',
                'badge_class': 'badge-archetype-favorite'
            }
        }

    # 10. Digestive System Fortified
    if any(k in enzymes for k in ['digezyme', 'lactase', 'tolerase', 'protease']):
        enz_name = 'DigeZyme® Multi-Enzyme' if 'digezyme' in enzymes else ('Tolerase™ L Lactase' if 'tolerase' in enzymes else 'Active Digestive Enzymes')
        return {
            'internal_archetype': 'digestive_friendly',
            'standout_metric': {
                'label': 'Digestive Comfort',
                'value': enz_name,
                'icon': 'fa-solid fa-leaf',
                'badge_class': 'badge-archetype-digestive'
            }
        }

    # 11. Elite Bioavailability
    if diaas >= 1.25:
        return {
            'internal_archetype': 'elite_bioavailability',
            'standout_metric': {
                'label': 'Elite Uptake',
                'value': f"DIAAS {diaas:.2f} (Elite BV)",
                'icon': 'fa-solid fa-dna',
                'badge_class': 'badge-archetype-elite'
            }
        }

    # 12. Good Value Tier
    if cpg > 0 and cpg <= 0.58:
        return {
            'internal_archetype': 'cost_leader',
            'standout_metric': {
                'label': 'Good Value',
                'value': f"R {cpg:.2f} / g prot",
                'icon': 'fa-solid fa-coins',
                'badge_class': 'badge-archetype-value'
            }
        }

    # 13. Daily Standard (Default balanced whey)
    return {
        'internal_archetype': 'balanced_standard',
        'standout_metric': {
            'label': 'Daily Standard',
            'value': f"{prot_g}g Prot / {sc_g}g Scoop",
            'icon': 'fa-solid fa-shield-halved',
            'badge_class': 'badge-archetype-standard'
        }
    }

