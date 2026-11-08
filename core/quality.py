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
    if ptype == 'Plant / Vegan Protein' or any(k in t for k in ['vegan', 'plant', 'phyto pro', '32gi']):
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

