import re

BRAND_FORMULATIONS = {
    'nutritech_proven': {
        'ingredients': 'Proven 5-Stage Timed-Release Protein Matrix [Whey Protein Concentrate (Milk), Whey Protein Isolate (Milk), Calcium Caseinate (Milk), Pea Protein Isolate, Soy Protein Isolate (GMO Free), Brown Rice Protein], Cocoa Powder (in choc flavours), Flavouring, Xanthan Gum, Sea Salt, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Multi-stage timed release matrix)',
        'sweetener': 'Sucralose'
    },
    'nutritech_premium': {
        'ingredients': 'Nutritech Whey Protein Blend [Cross-Flow Microfiltered Whey Protein Isolate, Ultrafiltered Whey Protein Concentrate], Cocoa Powder (in chocolate flavours), Flavouring, Sea Salt, Xanthan Gum, Emulsifier (Sunflower Lecithin), Non-Nutritive Sweeteners (Sucralose, Acesulfame Potassium). Soy-Free formulation.',
        'digestive_enzymes': 'None added (Cold-filtered native whey)',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'nutritech_notorious': {
        'ingredients': 'Notorious Whey Matrix [Instantised Whey Protein Concentrate, Whey Protein Isolate], Cocoa, Flavouring, Xanthan Gum, Sea Salt, Emulsifier (Sunflower Lecithin), Non-Nutritive Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'nutritech_isolate': {
        'ingredients': 'Cold Cross-Flow Microfiltered Whey Protein Isolate (WPI90), Cocoa Powder, Flavouring, Emulsifier (Sunflower Lecithin), Sweetener (Sucralose). Ultra-low lactose (<0.5g) & fat.',
        'digestive_enzymes': 'None needed (Pure Microfiltered Isolate)',
        'sweetener': 'Sucralose'
    },
    'nutritech_clear': {
        'ingredients': 'Hydrolysed Clear Whey Protein Isolate, Natural Acidifiers (Citric Acid, Malic Acid), Natural & Nature Identical Flavouring, Anti-Foaming Agent (Silicon Dioxide), Natural Colouring (Beetroot Red / Beta Carotene), Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Pre-hydrolysed peptides',
        'sweetener': 'Sucralose'
    },
    'nutritech_heavy_duty': {
        'ingredients': 'PROVEN VI™ Protein Formula (Whey Protein Concentrate, Whey Protein Isolate, Calcium Caseinate, Pea Protein Isolate, Soy Protein Isolate, Brown Rice Protein), CREATECH™ Anabolic Stack (Creatine Monohydrate, L-Glycine, Boron Citrate), Milk Protein, Flavouring, Cocoa, Xanthan Gum, Sucralose, Emulsifier: Sunflower Lecithin.',
        'digestive_enzymes': 'CREATECH™ Anabolic Stack (Creatine Monohydrate 2000mg, L-Glycine 2000mg, Boron Citrate 5mg)',
        'sweetener': 'Sucralose'
    },
    'futurelife_high_protein': {
        'ingredients': 'SmartProtein3D™ Blend (43%) [Whole Soy Bean Flour, Soy Protein Isolate, Skimmed Milk Powder (Cow\'s Milk), Whey Protein Concentrate (Cow\'s Milk), Calcium Caseinate (Cow’s Milk)], SmartMaize™ (Whole Maize Flour), Sucrose, Maltodextrin, Cocoa Powder, Inulin (Prebiotic Fiber), 23 Essential Vitamins & Minerals (Vitamin A, B-Complex, C, D, E, Biotin, Iron, Zinc, Chromium), Salt, Flavouring.',
        'digestive_enzymes': 'Inulin Prebiotic Fiber & 23 Essential Vitamins and Minerals',
        'sweetener': 'Sucrose & Maltodextrin (No artificial sweeteners)'
    },
    'futurelife_repair_food': {
        'ingredients': 'SmartMaize™ (Whole Maize Flour), Whole Soy Bean Flour, Hydrolyzed Collagen Peptides (13.3%) (Bovine), Xylitol, Soy Isolate (Soy), Maltodextrin, Skim Milk Powder (Cow\'s Milk), Cocoa Powder, Inulin, Vitamins & Minerals.',
        'digestive_enzymes': '10,000mg Hydrolyzed Collagen Peptides + Inulin Prebiotic Fiber',
        'sweetener': 'Xylitol (No artificial sweeteners)'
    },
    'futurelife_beauti_food': {
        'ingredients': 'Whole Soy Bean Flour (Soy), Xylitol, Skim Milk Powder (Cow\'s Milk), White Maize Flour, Hydrolyzed Collagen Peptides (10%) (Bovine), Soy Isolate (Soy), Maltodextrin, Oats Bran, Inulin, Sucralose, Vitamins & Minerals.',
        'digestive_enzymes': '5,000mg Hydrolyzed Collagen Peptides + Inulin Prebiotic Fiber',
        'sweetener': 'Xylitol & Sucralose'
    },
    'mywellness_alpha': {
        'ingredients': 'Anabolic Protein Complex (Whey Concentrate, Micellar Casein, Pea Protein, Whey Isolate), Cocoa Powder (in Chocolate flavour only), Flavouring, Low-GI Blend (Fructose, Erythritol, Stevia Leaf), Creatine Monohydrate, Taurine, Glycine, Xanthan Gum, Tongkat Ali 100:1 Extract, Ashwagandha Powder, Tribulus Terrestris.',
        'digestive_enzymes': 'Anabolic Muscle Complex (5,000mg per 36g serving: Creatine Monohydrate, Taurine, Glycine, Tongkat Ali 100:1 Extract, Tribulus Terrestris, Ashwagandha Powder)',
        'sweetener': 'Low-GI Blend (Fructose, Erythritol, Stevia Leaf)'
    },
    'usn_bluelab': {
        'ingredients': '100% Whey Protein Blend [Whey Protein Isolate (Milk), Whey Protein Hydrolysate (Milk), Whey Protein Concentrate (Milk)], Cocoa Powder (4.1% in choc), Flavouring, Sodium Chloride, Stabilisers (Guar Gum, Xanthan Gum), Non-Nutritive Sweetener Blend (Sucralose, Acesulfame-K), Tolerase™ L (pH-Stable Lactase Enzyme). Zero wheat or plant fillers [2.5g Leucine & 5.3g BCAAs per 32g scoop].',
        'digestive_enzymes': 'Tolerase™ L (pH-Stable Lactase)',
        'sweetener': 'Sucralose & Acesulfame-K (Zero in Unflavoured)'
    },
    'usn_hardcore': {
        'ingredients': 'Whey Protein Concentrate (Milk), Soy Protein Isolate, Type 1 Hydrolysed Collagen, Glycine, Taurine, Vegetable Fat Powder, Flavouring, Cocoa Powder (5%), Creatine Monohydrate, Milk Protein Concentrate, Sodium Chloride, Dextrose Monohydrate, Stabiliser, Non-Nutritive Sweetener Blend (Sucralose, Acesulfame-K), Magnesium, Tribulus Terrestris, Zinc, Tolerase™ L (Lactase), Vitamin B6.',
        'digestive_enzymes': 'Tolerase™ L (Lactase)',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'usn_hardcore_ripped': {
        'ingredients': 'Whey protein concentrate, Soy protein isolate, Type 1 Hydrolysed collagen, Glycine, Cocoa powder (9,1%), Taurine, Creatine monohydrate, Vegetable fat powder [Refined vegetable oil (Palm fruit), Glucose syrup, Milk protein, Anti-caking agent], Milk protein concentrate, Flavourings, L-Carnitine tartrate, Sodium chloride, Dextrose monohydrate, Coffea arabica L. (Green coffee bean) [seed; extract standardised to 45 % chlorogenic acid], Stabiliser (Xanthan gum), MCT powder [Medium chain triglycerides oil powder (Palm fruit, Palm kernel), Glucose syrup, Sodium caseinate, Dipotassium phosphate, Tricalcium phosphate], Non-nutritive sweeteners (Sucralose, Acesulfame-K), Magnesium Amino Acid Chelate (AAC), Caffeine anhydrous, Zinc lactate, Magnesium oxide, Tolerase® L (pH-stable lactase), Pyridoxine hydrochloride (Vitamin B6), Chromium picolinate.',
        'digestive_enzymes': 'Tolerase® L (Lactase), L-Carnitine Tartrate (500mg), Green Coffee Bean Extract (250mg), Caffeine (75mg), Creatine & Taurine (4000mg), Z-Mag-B6',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'usn_hydrotech': {
        'ingredients': 'Staged-Release Protein Matrix [Whey Protein Hydrolysate (Milk), Whey Protein Concentrate (Milk), Hydrolysed Wheat Protein (Gluten), Wheat Protein (Gluten)], Cocoa Powder (13%), Sodium Chloride, Emulsifier, Stabiliser, Flavouring, DigeZyme® (Proprietary Multi-Enzyme Complex: Amylase, Protease, Cellulase, Lactase, Lipase), Vitamin B6, Iron, Selenium, Non-Nutritive Sweetener (Sucralose). [Contains Wheat Gluten: 1.9g Leucine, 4.1g BCAAs, 7.5g Glutamic Acid per 30g scoop].',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose'
    },
    'usn_isozero': {
        'ingredients': 'Whey Protein Isolate (91%) (Milk), Cocoa Powder (6%), Flavouring, Sodium Chloride, Emulsifier (Sunflower Lecithin), DigeZyme® (Proprietary Multi-Enzyme Complex), Stabiliser (Xanthan Gum), Non-Nutritive Sweetener Blend (Sucralose, Acesulfame-K). Zero Carbs & Zero Sugar.',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'usn_protein_water': {
        'ingredients': 'Hydrolysed Collagen Peptides, L-Glycine, Acidifiers (Citric Acid, Malic Acid), Electrolyte Blend (Sodium Citrate, Potassium Chloride, Magnesium Citrate), Vitamin C, Flavouring, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Hydrolysed Collagen Peptides + Electrolytes',
        'sweetener': 'Sucralose'
    },
    'usn_beast': {
        'ingredients': 'Beast Multi-Stage Protein Blend [Whey Protein Concentrate, Whey Protein Hydrolysate, Soy Protein Isolate, Micellar Casein, Egg White Albumin, Milk Protein Concentrate], Maltodextrin, Cocoa Powder, Flavouring, Stabiliser, DigeZyme® Multi-Enzyme Complex, Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'usn_diet_fuel': {
        'ingredients': 'Diet Fuel Protein Blend [Whey Protein Concentrate (Milk), Soy Protein Isolate, Calcium Caseinate, Milk Protein Concentrate], Polydextrose, Cocoa Powder, Inulin (10g Dietary Fibre), Taurine, Maltodextrin, N-Acetyl-L-Carnitine HCl, Vitamin Premix, MCT Oil, Tolerase™ L (Lactase), Chromium Picolinate, Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'Tolerase™ L (Lactase) & Inulin Prebiotic Fibre',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'nutritech_nihpro': {
        'ingredients': 'NiHPRO™ Molecularly Calibrated Protein Isolate (87%) [Hydrolysed Pea & Rice Protein Isolate calibrated with Free-Form L-Leucine (2.76g), L-Lysine, and L-Methionine], Cocoa Powder, Medium Chain Triglyceride (MCT) Oil Powder, Natural & Artificial Flavour, Xanthan Gum, Sunflower Lecithin, Sucralose, Stevia.',
        'digestive_enzymes': 'Pre-hydrolysed Peptides (Lactose & Gluten Free)',
        'sweetener': 'Stevia & Sucralose'
    },
    'nutritech_vegan': {
        'ingredients': '100% Non-GMO US Golden Pea Protein Isolate, Cocoa Powder (in chocolate variants), Natural Flavouring, Sodium Chloride, Stabiliser (Xanthan Gum), Stevia Leaf Extract [Non-Nutritive Sweetener]. Zero artificial sweeteners, dairy, soy, or gluten.',
        'digestive_enzymes': 'None needed (Hypoallergenic Pea Isolate)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'nutritech_prosport_vegan': {
        'ingredients': '100% Pea Protein Isolate (Informed Sport Certified / WADA Batch Tested), Natural Flavourings, Sodium Chloride, Xanthan Gum, Non-Nutritive Sweeteners (Stevia & Monk Fruit Extract).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Stevia & Monk Fruit'
    },
    'nutritech_casein': {
        'ingredients': 'Slow-Release Nighttime Protein Matrix [Calcium Caseinate, Milk Protein Isolate, Cross-Flow Microfiltered Whey Protein Isolate], Cocoa Powder, Flavouring, Xanthan Gum, Sea Salt, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (6-8hr Sustained Micellar/Caseinate Release)',
        'sweetener': 'Sucralose'
    },
    'on_casein': {
        'ingredients': 'Micellar Casein (Milk), Cocoa (Processed with Alkali), Natural and Artificial Flavours, Salt, Gum Blend (Guar Gum, Cellulose Gum, Xanthan Gum), Sunflower Lecithin, Aminogen® Digestive Enzyme, Sucralose, Acesulfame Potassium.',
        'digestive_enzymes': 'Aminogen® Protease',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'muscle_works_wheybolic': {
        'ingredients': 'Whey Protein Concentrate, Whey Isolate, Cocoa Powder (in Chocolate flavour only), Anabolic Carb Complex (Cream of Rice Flour, Maltodextrin), Anabolic Amino Complex (Creatine, Taurine, Glycine, L-Leucine), Artificial Flavour, Xanthan Gum, Sucralose.',
        'digestive_enzymes': 'None added (4.5g Anabolic Amino Complex: Creatine, Taurine, Glycine, L-Leucine)',
        'sweetener': 'Sucralose'
    },
    'muscle_works_superior': {
        'ingredients': 'Superior Whey Matrix [Cross-Flow Ultrafiltered Whey Protein Concentrate (80%), Microfiltered Whey Protein Isolate (90%)], Cocoa (in choc variants), Natural & Nature-Identical Flavouring, Sunflower Lecithin, Xanthan Gum, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'muscle_works_100': {
        'ingredients': 'Ultrafiltered Whey Protein Concentrate (WPC80), Whey Protein Isolate, Cocoa Powder, Flavouring, Sunflower Lecithin, Xanthan Gum, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'muscle_works_thermo': {
        'ingredients': 'Thermo Lean Whey Matrix [Whey Protein Concentrate, Whey Protein Isolate], L-Carnitine Tartrate, Green Tea Extract (45% EGCG), Garcinia Cambogia (60% HCA), CLA (Conjugated Linoleic Acid), Cocoa, Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'on_gold_standard': {
        'ingredients': 'Protein Blend (Whey Protein Isolates [Microfiltered & Ion-Exchanged], Whey Protein Concentrate, Hydrolysed Whey Peptides), Cocoa (Processed with Alkali), Natural and Artificial Flavours, Lecithin (Soy/Sunflower), Aminogen®, Lactase, Acesulfame Potassium, Sucralose.',
        'digestive_enzymes': 'Aminogen® & Lactase',
        'sweetener': 'Acesulfame Potassium & Sucralose'
    },
    'on_isolate': {
        'ingredients': 'Hydrolysed & Ultra-Filtered Whey Protein Isolate (Milk), Cocoa (Processed with Alkali), Natural & Artificial Flavours, Soy Lecithin, Salt, Sweetener (Sucralose). Only 1g Carb & 0g Fat.',
        'digestive_enzymes': 'Hydrolysed & Ultra-Filtered',
        'sweetener': 'Sucralose'
    },
    'npl_platinum_whey': {
        'ingredients': 'Cold-Filtered Whey Protein Blend [Whey Protein Concentrate, Whey Protein Isolate, Whey Protein Hydrolysate], Cocoa Powder, Flavouring, Stabilisers, DigeZyme® Multi-Enzyme Complex (Alpha-Amylase, Neutral Protease, Lactase, Lipase, Cellulase), Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'DigeZyme® (Amylase, Protease, Lactase, Lipase, Cellulase)',
        'sweetener': 'Sucralose'
    },
    'npl_anabolic_whey': {
        'ingredients': 'Anabolic Whey Matrix [Whey Protein Concentrate, Whey Protein Isolate], Maltodextrin, Creatine Monohydrate, L-Glycine, Taurine, Tribulus Terrestris, DigeZyme® Multi-Enzyme Complex, Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose'
    },
    'muscletech_nitrotech': {
        'ingredients': 'Isolate Protein & Peptide Blend (Whey Peptides, Whey Protein Isolate, Whey Protein Isolate 97%), Whey Protein Concentrate, Cocoa (Processed with Alkali), Soy or Sunflower Lecithin, Salt, Natural & Artificial Flavours, Gum Blend (Cellulose, Xanthan, Carrageenan), Papain, Amylase, Silicon Dioxide, Acesulfame-Potassium, Sucralose.',
        'digestive_enzymes': 'Papain & Amylase',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'biogen_whey': {
        'ingredients': 'Tri-Phase Whey Protein Matrix [Cross-Flow Microfiltered Whey Protein Isolate, Whey Protein Hydrolysate, Whey Protein Concentrate], Cocoa Powder, Flavouring, Sodium Chloride, DigeZyme® Multi-Enzyme Complex, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose'
    },
    'biogen_clear': {
        'ingredients': 'Hydrolysed Clear Whey Protein Isolate, Hydrolysed Bovine Collagen Peptides, Natural Flavouring, Malic Acid, Citric Acid, Anti-Foam Agent, Stevia & Sucralose.',
        'digestive_enzymes': 'Hydrolysed Peptides',
        'sweetener': 'Stevia & Sucralose'
    },
    'gnc_pro_performance': {
        'ingredients': '100% Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), Cocoa, Natural and Artificial Flavours, Cellulose Gum, Soy Lecithin, Xanthan Gum, Acesulfame Potassium, Sucralose.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'gnc_amp_gold': {
        'ingredients': 'AMP Gold Protein Matrix [Hydrolysed Whey Protein Isolate, Micronised Whey Protein Isolate], Cocoa, Natural & Nature Identical Flavours, Protease, Amylase, Sucralose, Sunflower Lecithin.',
        'digestive_enzymes': 'Protease & Amylase',
        'sweetener': 'Sucralose'
    },
    'clicks_smartlife': {
        'ingredients': 'Whey Protein Concentrate, Skim Milk Powder, Flavouring, Cocoa Powder (in choc variants), Stabilizer (Xanthan Gum), Non-Nutritive Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'ssa_whey': {
        'ingredients': 'Advanced Whey Protein Matrix [Whey Protein Isolate, Whey Protein Concentrate], Cocoa Powder, Flavouring, Sunflower Lecithin, DigeZyme® Multi-Enzyme Complex, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex',
        'sweetener': 'Sucralose'
    },
    'evox_whey': {
        'ingredients': 'Ultra-Filtered Whey Protein Blend [Whey Protein Concentrate, Whey Protein Isolate], Cocoa, Flavouring, Tolerase™ L (Lactase), Non-Nutritive Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'Tolerase™ L (Lactase)',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'gloot_whey': {
        'ingredients': 'Pure Whey Protein Concentrate, Hydrolysed Bovine Collagen Peptides, L-Carnitine Tartrate, Green Tea Extract, Garcinia Cambogia, Cocoa, Flavouring, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'gloot_vegan': {
        'ingredients': 'Pea Protein Isolate, Natural Flavours, Stevia, Citric Acid, Beetroot Extract',
        'digestive_enzymes': 'None added',
        'sweetener': 'Stevia'
    },
    'primeself_grassfed': {
        'ingredients': '100% Grass-Fed Whey Protein Concentrate (80% Native Whey from Pasture-Raised Cows), Cocoa Powder (in choc), Natural Flavouring, Sunflower Lecithin, Stevia Leaf Extract.',
        'digestive_enzymes': 'None added (Clean & Natural)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'mywellness_nature': {
        'ingredients': 'Pasture-Fed Grass-Fed Whey Protein Concentrate, Whey Protein Isolate, Raw Organic Cacao (in choc), Natural Flavouring, Stevia Leaf Extract.',
        'digestive_enzymes': 'None added (Clean & Natural)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'blackbull_whey': {
        'ingredients': 'Whey Supreme Protein Matrix [Instantised Whey Protein Concentrate, Skimmed Milk Solids], Cocoa Powder, Flavouring, Xanthan Gum, Non-Nutritive Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'tony_ferguson': {
        'ingredients': 'Whey Protein Concentrate, Cocoa Powder, Flavouring, Xanthan Gum, Non-Nutritive Sweeteners (Sucralose, Acesulfame-K).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame-K'
    },
    'scicore_whey': {
        'ingredients': 'Instantised Whey Protein Concentrate (80%), Cocoa Powder, Natural Flavouring, Sunflower Lecithin, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'primal_whey': {
        'ingredients': '100% Whey Protein Matrix [Whey Protein Concentrate, Whey Protein Isolate], Cocoa, Flavouring, DigeZyme® Multi-Enzyme Blend, Sucralose.',
        'digestive_enzymes': 'DigeZyme®',
        'sweetener': 'Sucralose'
    },
    'tnt_whey': {
        'ingredients': 'Tri-Phase Whey Protein Concentrate & Isolate, Cocoa, Flavouring, DigeZyme® Multi-Enzyme Complex, Sucralose.',
        'digestive_enzymes': 'DigeZyme®',
        'sweetener': 'Sucralose'
    },
    'psnlifestyle_mrp': {
        'ingredients': 'Whey Protein Concentrate, Whey Protein Isolate, Skim Milk Powder, Whey Powder, L-Glutamine, Dutch Cocoa (in choc variants), Flavouring, Tolerase® L (pH-Stable Lactase Enzyme), Stevia [Non-Nutritive Sweetener]. No added fillers, thickeners or artificial colouring.',
        'digestive_enzymes': 'Tolerase® L (Lactase Enzyme)',
        'sweetener': 'Stevia'
    },
    'psnlifestyle_meltdown': {
        'ingredients': 'Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), L-Carnitine Tartrate, Green Tea Extract, Garcinia Cambogia, Tolerase® L (Lactase), Stevia.',
        'digestive_enzymes': 'Tolerase® L (Lactase)',
        'sweetener': 'Stevia'
    },
    'rogue_legion_lifestyle': {
        'ingredients': 'Whey Protein Concentrate, Whey Protein Isolate, Whey Powder, Skim Milk Powder, L-Glutamine, Permitted Flavourants & Colourants (Dutch Cocoa in chocolate variants), Tolerase® L (pH-Stable Lactase Enzyme), Stevia [Non-Nutritive Sweetener]. No added fillers, thickeners or artificial colouring.',
        'digestive_enzymes': 'Tolerase® L (Lactase Enzyme)',
        'sweetener': 'Stevia'
    },
    'lifeworth_super_standard': {
        'ingredients': 'Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Hydrolyzed Bovine Collagen), Cocoa (Processed with Alkali), Sunflower Lecithin Powder, Polydextrose, Natural and Artificial Flavors, Acesulfame Potassium, Sucralose. Contains Milk and Soy.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'biyode_whey': {
        'ingredients': 'Whey Protein Blend (Whey Protein Isolate, Whey Protein Concentrate), Vanilla Flavouring, Emulsifier (Sunflower Lecithin), Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    }
}

def determine_nutrition(brand, ptype, weight_g, title, existing_ing=None):
    t = (title or '').lower()
    b = (brand or '').lower()
    
    # Match specific product line
    matched = None
    if 'future' in t or 'future' in b:
        if 'repair' in t: matched = BRAND_FORMULATIONS['futurelife_repair_food']
        elif 'beauti' in t: matched = BRAND_FORMULATIONS['futurelife_beauti_food']
        else: matched = BRAND_FORMULATIONS['futurelife_high_protein']
    elif 'hydrotech' in t or 'hydrotec' in t or 'hydro tech' in t:
        matched = BRAND_FORMULATIONS['usn_hydrotech']
    elif 'bluelab' in t or 'blue lab' in t:
        matched = BRAND_FORMULATIONS['usn_bluelab']
    elif 'isozero' in t or 'iso zero' in t or 'iso pro zero' in t or 'isopro zero' in t:
        matched = BRAND_FORMULATIONS['usn_isozero']
    elif 'protein water' in t and 'usn' in t:
        matched = BRAND_FORMULATIONS['usn_protein_water']
    elif 'hardcore' in t or 'whey gh' in t:
        if 'ripped' in t:
            matched = BRAND_FORMULATIONS['usn_hardcore_ripped']
        else:
            matched = BRAND_FORMULATIONS['usn_hardcore']
    elif 'beast' in t and ('usn' in b or 'usn' in t):
        matched = BRAND_FORMULATIONS['usn_beast']
    elif 'diet fuel' in t:
        matched = BRAND_FORMULATIONS['usn_diet_fuel']
    elif 'whey-bolic' in t or 'wheybolic' in t:
        matched = BRAND_FORMULATIONS['muscle_works_wheybolic']
    elif 'superior whey' in t and 'my wellness' not in t and 'mywellness' not in t:
        matched = BRAND_FORMULATIONS['muscle_works_superior']
    elif 'thermo whey' in t:
        matched = BRAND_FORMULATIONS['muscle_works_thermo']
    elif 'gold standard' in t and 'casein' in t:
        matched = BRAND_FORMULATIONS['on_casein']
    elif 'gold standard' in t and 'isolate' in t:
        matched = BRAND_FORMULATIONS['on_isolate']
    elif 'gold standard' in t or 'optimum nutrition' in t or ('optimum' in t and 'whey' in t) or ('optimum' in b and 'whey' in t):
        matched = BRAND_FORMULATIONS['on_gold_standard']
    elif 'nihpro' in t:
        matched = BRAND_FORMULATIONS['nutritech_nihpro']
    elif 'nutritech' in b or 'nutritech' in t or 'vegan protein' in t:
        if ('pro sport' in t or 'prosport' in t) and 'vegan' in t:
            matched = BRAND_FORMULATIONS['nutritech_prosport_vegan']
        elif 'vegan' in t:
            matched = BRAND_FORMULATIONS['nutritech_vegan']
        elif 'casein' in t:
            matched = BRAND_FORMULATIONS['nutritech_casein']
        elif 'clear whey' in t or 'protein water' in t:
            matched = BRAND_FORMULATIONS['nutritech_clear']
        elif 'heavy duty' in t or 'heavy-duty' in t:
            matched = BRAND_FORMULATIONS['nutritech_heavy_duty']
        elif 'notorious' in t:
            matched = BRAND_FORMULATIONS['nutritech_notorious']
        elif 'proven' in t:
            matched = BRAND_FORMULATIONS['nutritech_proven']
        elif 'isolate' in t:
            matched = BRAND_FORMULATIONS['nutritech_isolate']
        else:
            matched = BRAND_FORMULATIONS['nutritech_premium']
    elif 'clear whey' in t:
        if 'biogen' in b: matched = BRAND_FORMULATIONS['biogen_clear']
        else: matched = BRAND_FORMULATIONS['nutritech_clear']
    elif 'anabolic whey' in t and 'npl' in t:
        matched = BRAND_FORMULATIONS['npl_anabolic_whey']
    elif 'npl' in b or 'platinum whey' in t:
        matched = BRAND_FORMULATIONS['npl_platinum_whey']
    elif 'nitrotech' in t or 'nitro-tech' in t or 'nitro tech' in t or 'muscletech' in b:
        matched = BRAND_FORMULATIONS['muscletech_nitrotech']
    elif 'biogen' in b or 'biogen' in t:
        if 'clear' in t: matched = BRAND_FORMULATIONS['biogen_clear']
        else: matched = BRAND_FORMULATIONS['biogen_whey']
    elif 'amp amplified' in t or 'amp gold' in t:
        matched = BRAND_FORMULATIONS['gnc_amp_gold']
    elif 'gnc' in b or 'gnc' in t:
        matched = BRAND_FORMULATIONS['gnc_pro_performance']
    elif 'clicks' in b or 'smartlife' in t:
        matched = BRAND_FORMULATIONS['clicks_smartlife']
    elif 'ssa' in b or 'ssa' in t:
        matched = BRAND_FORMULATIONS['ssa_whey']
    elif 'evox' in b or 'evox' in t:
        matched = BRAND_FORMULATIONS['evox_whey']
    elif 'gloot' in b or 'gloot' in t:
        if 'vegan' in t: matched = BRAND_FORMULATIONS['gloot_vegan']
        else: matched = BRAND_FORMULATIONS['gloot_whey']
    elif 'primeself' in b or 'primeself' in t:
        matched = BRAND_FORMULATIONS['primeself_grassfed']
    elif 'alpha' in t and ('whey' in t or 'my wellness' in b):
        matched = BRAND_FORMULATIONS['mywellness_alpha']
    elif 'my wellness' in b or 'mywellness' in b or 'nature' in t:
        matched = BRAND_FORMULATIONS['mywellness_nature']
    elif 'black bull' in b or 'blackbull' in b or ('supreme' in t and 'usn' not in b and 'usn' not in t):
        matched = BRAND_FORMULATIONS['blackbull_whey']
    elif 'tony ferguson' in b or 'tony ferguson' in t:
        matched = BRAND_FORMULATIONS['tony_ferguson']
    elif 'sci-core' in b or 'scicore' in b:
        matched = BRAND_FORMULATIONS['scicore_whey']
    elif 'primal' in b or 'primal' in t:
        matched = BRAND_FORMULATIONS['primal_whey']
    elif 'tnt' in b or 'tnt' in t:
        matched = BRAND_FORMULATIONS['tnt_whey']
    elif 'psnlifestyle' in b or 'psnlifestyle' in t or 'psn' in t or 'psn' in b:
        if 'meltdown' in t or 'fat burner' in t:
            matched = BRAND_FORMULATIONS['psnlifestyle_meltdown']
        else:
            matched = BRAND_FORMULATIONS['psnlifestyle_mrp']
    elif 'rogue legion' in b or 'rogue legion' in t or 'rogue' in b or 'rogue' in t:
        matched = BRAND_FORMULATIONS['rogue_legion_lifestyle']
    elif 'lifeworth' in b or 'lifeworth' in t or 'b0fj7m74k1' in t:
        matched = BRAND_FORMULATIONS['lifeworth_super_standard']
    elif 'biyode' in b or 'biyode' in t or 'b0f9twj4hq' in t:
        matched = BRAND_FORMULATIONS['biyode_whey']
        
    # Macros based on type & product line
    if matched == BRAND_FORMULATIONS.get('futurelife_high_protein'):
        serving_size = 75.0
        protein_per_serving = 22.5
        carbs = 29.0
        fat = 3.8
    elif matched == BRAND_FORMULATIONS.get('futurelife_repair_food') or 'repair food' in t:
        serving_size = 75.0
        protein_per_serving = 21.0
        carbs = 33.8
        fat = 7.4
    elif matched == BRAND_FORMULATIONS.get('futurelife_beauti_food') or 'beauti food' in t:
        serving_size = 55.0
        protein_per_serving = 13.7
        carbs = 12.0
        fat = 4.7
    elif matched == BRAND_FORMULATIONS.get('usn_hydrotech'):
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 3.0
        fat = 1.6
    elif matched == BRAND_FORMULATIONS.get('usn_bluelab'):
        serving_size = 32.0
        protein_per_serving = 23.6
        carbs = 2.6
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('usn_isozero'):
        serving_size = 23.0
        protein_per_serving = 20.0
        carbs = 0.0
        fat = 0.5
    elif matched == BRAND_FORMULATIONS.get('usn_protein_water'):
        serving_size = 22.0
        protein_per_serving = 15.0
        carbs = 0.5
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('usn_hardcore_ripped'):
        serving_size = 33.0
        protein_per_serving = 26.1
        carbs = 2.0
        fat = 1.7
    elif matched == BRAND_FORMULATIONS.get('usn_hardcore'):
        serving_size = 33.0
        protein_per_serving = 27.0
        carbs = 2.0
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('usn_beast'):
        serving_size = 35.0
        protein_per_serving = 23.0
        carbs = 6.0
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('usn_diet_fuel'):
        serving_size = 45.0
        protein_per_serving = 24.7
        carbs = 3.0
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('nutritech_nihpro'):
        serving_size = 32.0
        protein_per_serving = 26.1
        carbs = 0.7
        fat = 1.9
    elif matched == BRAND_FORMULATIONS.get('nutritech_vegan'):
        serving_size = 32.0
        protein_per_serving = 25.0
        carbs = 0.9
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('nutritech_prosport_vegan'):
        serving_size = 32.0
        protein_per_serving = 24.0
        carbs = 2.9
        fat = 2.6
    elif matched == BRAND_FORMULATIONS.get('nutritech_casein'):
        serving_size = 33.0
        protein_per_serving = 26.0
        carbs = 3.0
        fat = 0.8
    elif matched == BRAND_FORMULATIONS.get('on_casein'):
        serving_size = 33.0
        protein_per_serving = 24.0
        carbs = 3.0
        fat = 0.5
    elif matched in [BRAND_FORMULATIONS.get('psnlifestyle_mrp'), BRAND_FORMULATIONS.get('rogue_legion_lifestyle')]:
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 4.2
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('psnlifestyle_meltdown'):
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 2.0
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('lifeworth_super_standard'):
        serving_size = 30.0
        protein_per_serving = 10.0
        carbs = 18.4
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('biyode_whey'):
        serving_size = 30.0
        protein_per_serving = 21.0
        carbs = 3.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('mywellness_alpha'):
        serving_size = 36.0
        protein_per_serving = 27.0
        carbs = 4.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('nutritech_proven'):
        serving_size = 32.0
        protein_per_serving = 22.0
        carbs = 4.0
        fat = 0.7
    elif matched == BRAND_FORMULATIONS.get('nutritech_premium'):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 3.0
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('nutritech_heavy_duty'):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 4.0
        fat = 1.3
    elif matched == BRAND_FORMULATIONS.get('nutritech_notorious'):
        serving_size = 34.0
        protein_per_serving = 24.0
        carbs = 3.2
        fat = 2.1
    elif matched == BRAND_FORMULATIONS.get('nutritech_isolate'):
        serving_size = 30.0
        protein_per_serving = 26.5
        carbs = 0.5
        fat = 0.4
    elif matched == BRAND_FORMULATIONS.get('nutritech_clear'):
        serving_size = 25.0
        protein_per_serving = 20.0
        carbs = 0.2
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('on_gold_standard'):
        serving_size = 31.0
        protein_per_serving = 24.0
        carbs = 3.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('npl_platinum_whey'):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 2.8
        fat = 1.6
    elif matched == BRAND_FORMULATIONS.get('npl_anabolic_whey'):
        serving_size = 43.0
        protein_per_serving = 30.0
        carbs = 4.5
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('muscletech_nitrotech'):
        serving_size = 33.0
        protein_per_serving = 24.0
        carbs = 2.0
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('biogen_whey'):
        serving_size = 32.0
        protein_per_serving = 24.0
        carbs = 2.5
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('biogen_clear'):
        serving_size = 24.0
        protein_per_serving = 20.0
        carbs = 0.3
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('gloot_whey'):
        serving_size = 19.0
        protein_per_serving = 14.0
        carbs = 0.8
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('gloot_vegan'):
        serving_size = 17.0
        protein_per_serving = 12.0
        carbs = 0.5
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('ssa_whey'):
        serving_size = 32.0
        protein_per_serving = 24.0
        carbs = 2.2
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('muscle_works_wheybolic') or 'whey-bolic' in t or 'wheybolic' in t:
        serving_size = 40.0
        protein_per_serving = 22.0
        carbs = 10.8
        fat = 1.9
    elif ptype in ['Whey Isolate', 'Clear Whey / Protein Water'] or (matched and 'isolate' in str(matched)):
        serving_size = 30.0
        protein_per_serving = 26.0
        carbs = 0.8
        fat = 0.4
    elif ptype == 'Casein / Milk Protein':
        serving_size = 33.0
        protein_per_serving = 24.0
        carbs = 2.8
        fat = 0.8
    elif ptype == 'Plant / Vegan Protein':
        serving_size = 32.0
        protein_per_serving = 22.0
        carbs = 2.5
        fat = 1.8
    elif ptype == 'Collagen / Beef / Broth':
        serving_size = 25.0
        protein_per_serving = 22.0
        carbs = 0.5
        fat = 0.3
    elif ptype == 'Hardcore / All-in-One' or (matched and ('hardcore' in str(matched) or 'anabolic' in str(matched) or 'heavy_duty' in str(matched))):
        serving_size = 60.0
        protein_per_serving = 41.0
        carbs = 6.5
        fat = 2.1
    elif ptype == 'Diet / Lean Whey' or (matched and 'thermo' in str(matched)):
        serving_size = 28.0
        protein_per_serving = 20.0
        carbs = 2.2
        fat = 1.0
    elif ptype == 'Whey Concentrate':
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 2.5
        fat = 1.8
    else: # Whey Blend (Default)
        serving_size = 32.0
        protein_per_serving = 24.0
        carbs = 2.2
        fat = 1.5

    protein_pct = round((protein_per_serving / serving_size) * 100, 1)
    servings = max(1, int(weight_g / serving_size))
    total_protein = round(servings * protein_per_serving, 1)

    final_ing = matched['ingredients'] if matched else 'Premium Whey Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate), Cocoa / Natural Flavouring, Emulsifier (Lecithin), Stabiliser (Xanthan Gum), Non-Nutritive Sweetener (Sucralose).'
    final_enzymes = matched['digestive_enzymes'] if matched else ('Tolerase™ L (Lactase)' if ('usn' in b or 'evox' in b) else ('DigeZyme®' if ('npl' in b or 'biogen' in b or 'ssa' in b) else 'None added'))
    final_sweetener = matched['sweetener'] if matched else ('Stevia' if ('nature' in b or 'wellness' in b) else 'Sucralose')

    return {
        'serving_size_g': serving_size,
        'scoop_size_g': serving_size,
        'protein_per_serving_g': protein_per_serving,
        'carbs_g': carbs,
        'fat_g': fat,
        'servings_count': servings,
        'total_protein_g': total_protein,
        'protein_percentage': protein_pct,
        'digestive_enzymes': final_enzymes,
        'sweetener': final_sweetener,
        'ingredients': final_ing
    }

