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
    'mywellness_alpha_plant': {
        'ingredients': 'Hardcore Plant Protein Matrix (Fava Bean Protein, Pea Protein Isolate, Brown Rice Protein), Super Anabolic Herbs & Actives (Tongkat Ali 100:1, Ashwagandha, Tribulus Terrestris, Creatine Monohydrate, Taurine, Glycine), Raw Cacao, Stevia Leaf Extract.',
        'digestive_enzymes': 'Hardcore Male Anabolic Complex (Tongkat Ali, Ashwagandha, Tribulus, Creatine, Taurine, Glycine)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'mywellness_superior': {
        'ingredients': 'Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), Cocoa Powder (in chocolate flavours), Flavouring, Xanthan Gum, Non-Nutritive Sweetener (Sucralose, Stevia).',
        'digestive_enzymes': 'None added (Pure Ultra-Filtered Whey)',
        'sweetener': 'Sucralose & Stevia'
    },
    'mywellness_isolate': {
        'ingredients': '100% Pure Cross-Flow Microfiltered Whey Protein Isolate, Colostrum Powder (2,000mg), Cocoa (in choc variants), Stevia Leaf Extract.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Stevia'
    },
    'mywellness_natures': {
        'ingredients': 'Grass-Fed Whey Protein Concentrate, Organic Raw Cacao (chocolate), Creamy Chai Spices (in chai), Stevia Leaf Extract, Erythritol, Fructose.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Stevia & Erythritol'
    },
    'mywellness_super_clean': {
        'ingredients': 'Clean Non-GMO Protein Blend (Whey Protein Concentrate, Yellow Pea Protein Isolate, Whey Protein Isolate, Rice Protein Isolate, Hemp Protein Powder), Wheatgrass Powder, Cacao Powder (in Chocolate variant only), Coffee Granules (in Chocochino variant only), Vanilla Extract (in Vanilla Bean variant only), Low GI Natural Sweetener Blend (Erythritol, Fructose, Stevia Leaf).',
        'digestive_enzymes': 'Wheatgrass Powder & 5-Stage Multi-Source Protein Complex',
        'sweetener': 'Low GI Natural Sweetener Blend (Erythritol, Fructose, Stevia Leaf)'
    },
    'natures_nutrition_plant': {
        'ingredients': 'Plant Protein Blend (Pea Protein, Rice Protein), Organic Dehydrated Coconut Flower Sap, Cocoa Powder (in Chocolate variant), Flavouring, Xanthan Gum, Acacia Gum, Sodium Chloride, Non-Nutritive Sweetener: Steviol Glycosides (from Organic Stevia Leaf).',
        'digestive_enzymes': 'Organic Coconut Flower Sap & Acacia Prebiotic Fibre',
        'sweetener': 'Organic Stevia Leaf (Steviol Glycosides)'
    },
    'mywellness_collagen': {
        'ingredients': '100% Pure Hydrolysed Bovine Collagen Peptides (Type 1 & 3). Grass-fed, hormone-free, zero fillers or additives.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Unsweetened (Natural)'
    },
    'mywellness_soy': {
        'ingredients': 'Soy Protein Isolate.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Unflavoured / None'
    },
    'mywellness_pure_pea': {
        'ingredients': 'Pea Protein Isolate.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Unflavoured / None'
    },
    'mywellness_yeast': {
        'ingredients': 'Yeast protein isolate, Fava Bean Protein, Cocoa powder, Low GI Sweetener blend (Xylitol, Fructose, Stevia), Inulin (Prebiotic Fibre), Nature Identical Flavour, Himalayan Salt, Xanthan Gum, DigeZyme® (Amylolytic, Neutral Protease, Cellulase, Lactase, Lipase), LactoSpore® (Heyndrickxia coagulans - 6 Billion CFU).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex + Inulin Prebiotic Fibre & LactoSpore® Probiotics (6 Billion CFU)',
        'sweetener': 'Low GI Sweetener blend (Xylitol, Fructose, Stevia)'
    },
    'mywellness_clean_diet_plant': {
        'ingredients': 'Protein Blend (Pea Protein, Hemp Seed Protein), Cocoa Powder (Chocolate Flavour Only), Low GI Sweetener Blend (Fructose, Erythritol, Stevia), Vanilla Extract (in Vanilla flavour only), Chai Blend in Chai flavour only (Cloves, Cinnamon, Nutmeg), CLA Powder, Inulin Fibre, Vitamin Premix, Baobab Powder, Maca Powder, Flaxseed Powder, Xanthan Gum, L-Carnitine, Garcinia Cambogia Extract.',
        'digestive_enzymes': 'Inulin Prebiotic Fibre + CLA (1000mg), L-Carnitine (500mg), Garcinia Cambogia (500mg) & Maca',
        'sweetener': 'Low GI Sweetener Blend (Fructose, Erythritol, Stevia)'
    },
    'usn_plant': {
        'ingredients': 'Pea Protein Isolate, Pumpkin Seed Protein (Smooth Protein™), Watermelon Seed Protein, Flavouring, Cocoa Powder (in chocolate flavours), Sodium Chloride, Non-Nutritive Sweeteners (Sucralose, Steviol Glycosides), Iron (Ferrous Fumarate), Vitamin B12 (Cyanocobalamin).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Stevia'
    },
    'biogen_plant': {
        'ingredients': 'Pea Protein Isolate (31%), Rice Protein Concentrate (20%), Fava Bean Protein (8%), Chickpea Protein (<1%), Hemp Seed Protein (<1%), Pumpkin Seed Protein (<1%), Flavouring, Cocoa Powder (in chocolate), Inulin, Salt, Non-Nutritive Sweetener (Sucralose, Steviol Glycosides).',
        'digestive_enzymes': 'Inulin Prebiotic Fibre',
        'sweetener': 'Sucralose & Steviol Glycosides'
    },
    'npl_plant': {
        'ingredients': 'Pea Protein Isolate, Rice Protein Concentrate, Hemp Seed Protein, Chickpea Protein, Cocoa Powder (in choc), Flavouring, Salt, Non-Nutritive Sweetener (Sucralose, Stevia).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose & Stevia'
    },
    'ssa_vegan': {
        'ingredients': 'Non-GMO Pea Protein Isolate, Non-GMO Hemp Protein, Cocoa Powder (in chocolate), Flavouring, Salt, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'mywellness_vegan': {
        'ingredients': 'Plant Protein Matrix (Yellow Pea Protein Isolate, Hemp Seed Protein), Organic Raw Cacao, Wheatgrass Powder, Stevia Leaf, Erythritol.',
        'digestive_enzymes': 'None added',
        'sweetener': 'Stevia & Erythritol'
    },
    'mywellness_casein': {
        'ingredients': 'Pure Micellar Casein, Raw Organic Cacao, Natural Flavouring, Stevia Leaf Extract.',
        'digestive_enzymes': 'Slow-release micellar matrix',
        'sweetener': 'Stevia Leaf Extract'
    },
    'mywellness_game_changer': {
        'ingredients': 'Wholefood Plant Protein & Carbohydrate Blend (Pea Protein, Oat Flour, Sweet Potato Powder), Superfood Greens, Healthy Fats (MCT Oil), Stevia.',
        'digestive_enzymes': 'Digestive Superfood Blend',
        'sweetener': 'Stevia'
    },
    'mywellness_vegainer': {
        'ingredients': 'Wholefood Carbohydrate Blend (Potato Starch, Oat Flour, Rice Flour, Barley Malt Extract), Protein Blend (Pea Protein, Hemp Protein, Whole Chia Seeds, Spirulina Powder), Cocoa Powder (in Chocolate version only), Maltodextrin, Natural Sweetener blend (Erythritol, Fructose, Stevia).',
        'digestive_enzymes': 'Hyper Grow Stack (6,000mg per 120g serving: Creatine Monohydrate, Taurine)',
        'sweetener': 'Natural Sweetener Blend (Erythritol, Fructose, Stevia)'
    },
    'mywellness_hard_mass': {
        'ingredients': 'Multi-Stage Carbohydrate Matrix (Maltodextrin, Waxy Maize Starch), Anabolic Protein Complex (Whey Concentrate, Micellar Casein, Pea Protein), Creatine Monohydrate, Taurine, L-Glycine, Cocoa Powder, Stevia Leaf.',
        'digestive_enzymes': 'Hyper Anabolic Stack (Creatine, Taurine, L-Glycine)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'mywellness_keto_diet_shake': {
        'ingredients': 'High-Fat Keto Blend (MCT Oil Powder, Butter Powder, Vegetable Fat), Protein Blend (Hydrolysed Bovine Collagen Peptides, Whey Protein Isolate), Baobab Fruit Powder, Xanthan Gum, Kalahari Sea Salt, BHB (Beta-Hydroxybutyrate) Salts, Stevia Leaf Powder, Vitamin C (Ascorbic Acid), Cocoa Powder (in Chocolate) / Natural Spices (in Vanilla Chai).',
        'digestive_enzymes': 'Enriched with BHB Salts & Prebiotic Baobab Fibre',
        'sweetener': 'Stevia Leaf Powder'
    },
    'mywellness_ketobolic': {
        'ingredients': 'Keto-Bolic Fat Blend (Vegetable Fat Powder, MCT Oil Powder), Keto-Bolic Protein Blend (Pea Protein Isolate, Whey Protein Isolate), Cocoa Powder (in Chocolate) / Natural Spices (in Creamy Chai), Taurine, Creatine HCL, Xanthan Gum, Baobab Powder, Sea Salt, BHB Salts, Stevia Leaf Powder, Vitamin C (Ascorbic Acid).',
        'digestive_enzymes': 'Enriched with Creatine HCL, Taurine & BHB Salts',
        'sweetener': 'Stevia Leaf Powder'
    },
    'mywellness_her_cheat_meal': {
        'ingredients': 'Multi-Source Protein Blend (Milk Protein Isolate, Hydrolysed Bovine Collagen Peptides, Fava Bean Protein, Pea Protein Isolate), Maltodextrin, Inulin Prebiotic Fibre, CLA (Conjugated Linoleic Acid) Powder, Garcinia Cambogia Extract, Green Tea Extract, Cocoa Powder (in Chocolate) / Matcha (in Matcha), Flavouring, Salt, Stevia Leaf Extract.',
        'digestive_enzymes': 'Inulin Prebiotic Fibre + CLA & Garcinia Cambogia',
        'sweetener': 'Stevia Leaf Extract'
    },
    'mywellness_clean_diet_shake': {
        'ingredients': 'Multi-Protein Lean Matrix (Pasture-Fed Whey Protein Concentrate, Micellar Casein, Grass-Fed Collagen Peptides), Inulin Prebiotic Fibre, Maca Root Powder, Ashwagandha Root Extract, L-Carnitine Tartrate, Cocoa Powder (in Chocolate), Natural Flavouring, Xanthan Gum, Low GI Sweetener Blend (Erythritol, Fructose, Stevia Leaf).',
        'digestive_enzymes': 'Inulin Prebiotic Fibre + L-Carnitine, Ashwagandha & Maca',
        'sweetener': 'Erythritol, Fructose & Stevia Leaf'
    },
    'mywellness_clean_diet_matcha': {
        'ingredients': 'Grass-Fed Whey Protein Concentrate, Micellar Casein, Grass-Fed Collagen Peptides, Authentic Japanese Matcha Green Tea Powder, MCT Oil Powder, Inulin Dietary Fibre, Maca Root Powder, L-Carnitine Tartrate, Xanthan Gum, Low GI Sweetener Blend (Erythritol, Fructose, Stevia Leaf).',
        'digestive_enzymes': 'Inulin Prebiotic Fibre + L-Carnitine & Maca Root',
        'sweetener': 'Erythritol, Fructose & Stevia Leaf'
    },
    'weider_mega_mass': {
        'ingredients': 'Carbohydrate Blend (Maltodextrin, Native Wheat Starch, Oat Flour), Protein Blend (Milk Protein Isolate, Whey Protein Concentrate, Dried Egg Albumin), Cocoa Powder, Creatine Monohydrate, Vitamin & Mineral Complex (Vitamin E, C, B1, B2, B6, B12, Niacin, Folic Acid, Biotin, Pantothenic Acid, Calcium, Iron, Zinc, Iodine), Sweetener (Sucralose).',
        'digestive_enzymes': 'Creatine Monohydrate (3,400mg per serving) & Complete Vitamin-Mineral Stack',
        'sweetener': 'Maltodextrin, Dextrose, Fructose & Sucralose'
    },
    'primal_mass_gain': {
        'ingredients': 'Triple-Action Carbohydrate Blend (73% Maltodextrin, 2% Ground Oatmeal Powder, 2% Brown Rice Powder), Protein Blend (Whey Protein Concentrate, Soy Protein Isolate, Skim Milk Powder), Tolerase™ L (pH-Stable Lactase Enzyme), Cocoa Powder, Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': 'Tolerase™ L (Lactase)',
        'sweetener': 'Sucralose'
    },
    'primal_skinny_whey': {
        'ingredients': 'Whey Protein Blend (Whey Protein Isolate, Whey Protein Concentrate, Whey Protein Hydrolysate), DigeZyme® Multi-Enzyme Complex, Inulin Prebiotic Fibre, Cocoa Powder, Flavouring, Stevia.',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex & Inulin Prebiotic Fibre',
        'sweetener': 'Stevia'
    },
    'primal_diet_shake': {
        'ingredients': 'Whey Protein Matrix (Whey Protein Isolate, Whey Protein Concentrate, Whey Protein Hydrolysate), L-Carnitine Tartrate, Inulin Fibre, DigeZyme® Multi-Enzyme Complex, Probiotics, Vitamins & Minerals, Sweeteners (Sucralose, Stevia).',
        'digestive_enzymes': 'L-Carnitine, DigeZyme® & Probiotics',
        'sweetener': 'Sucralose & Stevia'
    },
    'npl_pro_gains': {
        'ingredients': 'Multi-Stage Carbohydrate Blend (Maltodextrin, Waxy Maize Starch, Oat Flour), Multi-Stage Protein Blend (Whey Protein Concentrate, Milk Protein Isolate, Micellar Casein), Creatine Monohydrate, L-Glutamine, Taurine, DigeZyme® Multi-Enzyme Complex, Sweetener (Sucralose).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex & Creatine/Taurine Anabolic Stack (5,000mg)',
        'sweetener': 'Sucralose'
    },
    'biogen_bulk': {
        'ingredients': 'Advanced Carbohydrate Matrix (Maltodextrin, Corn Syrup Solids, Dextrose), Multi-Source Protein Blend (Whey Protein Concentrate, Calcium Caseinate, Soy Protein Isolate), Tolerase™ L (pH-Stable Lactase Enzyme), Multivitamin & Mineral Premix, Sweetener (Sucralose).',
        'digestive_enzymes': 'Tolerase™ L (Lactase) & Multivitamin/Antioxidant Complex',
        'sweetener': 'Sucralose'
    },
    'lifegain': {
        'ingredients': 'Triple Protein Matrix (Soy Protein Isolate, Whey Protein Isolate, Milk Protein Isolate), Maltodextrin, Inulin / Chicory Root Fibre, 24 Essential Vitamins and Minerals Complex, L-Glutamine, Essential Fatty Acids (Omega-3 & 6), Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': '24 Essential Vitamins & Minerals, L-Glutamine & Omega-3/6 Fatty Acids',
        'sweetener': 'Sucralose'
    },
    'usn_hyperbolic': {
        'ingredients': '4-Stage Glyco-Matrix Carb System (Maltodextrin, Waxy Maize Starch, Dextrose, Fructose), 5-Stage Anabolic Protein Matrix (Whey Concentrate, Soy Isolate, Calcium Caseinate, Egg Albumin, Milk Protein), Creatine Monohydrate, Tolerase™ L, Sweeteners.',
        'digestive_enzymes': 'Tolerase™ L (Lactase) & Creatine Anabolic Stack',
        'sweetener': 'Sucralose & Acesulfame-K'
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
        'ingredients': 'Protein Blend (Whey Protein Concentrate, Soy Isolate, Skim Milk Powder), Flavourant, Sodium Chloride, Emulsifier (Carboxymethyl Cellulose E466), Anti-Caking Agent (Silicone Dioxide E551) and Non-Nutritive Sweetener (Sucralose Acesulfame K Blend E950, E955).',
        'digestive_enzymes': 'None added (Whey, Soy & Milk Multi-Source Blend)',
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
        'ingredients': '100% Pasture-Fed Whey Protein Concentrate, Cocoa Powder (in chocolate flavours), Natural Flavouring, Stevia Leaf Extract.',
        'digestive_enzymes': 'None added (Pasture-Fed Natural Whey)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'blackbull_whey': {
        'ingredients': 'Blackbull Protein Stack (Whey Protein Concentrate, Whey Protein Isolate, Hydrolysed Whey Protein, Milk Protein), Flavouring, Cocoa Powder, Stabilizer, Blackbull Anabolic Vitamin and Mineral Stack (Vitamin A, B1, B2, B3, B5, B6, B9, B12, C, D, E, H, Chromium AAC, Copper AAC, Potassium Iodide, Ferrous Fumarate), Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Blackbull Anabolic Vitamin & Mineral Matrix',
        'sweetener': 'Sucralose'
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
    },
    '32gi_plant': {
        'ingredients': 'Plant-Based Protein Blend (Pea Protein Isolate, Rice Protein Concentrate), Cocoa Powder (10% in Choc) / Cinnamon (in Vanilla), Erythritol, Salt, Rice Starch, Stabilizer (Xanthan Gum, Gum Acacia), Steviol Glycosides, Flavouring, Trehalose, Inulin.',
        'digestive_enzymes': 'Inulin Prebiotic Fibre (4596mg BCAAs)',
        'sweetener': 'Erythritol & Steviol Glycosides'
    },
    'peak_plant': {
        'ingredients': 'Faba Bean Protein Isolate, Pea Protein Isolate, Flavouring (Natural & Artificial), Flaxseed Oil Powder, Peak Micronutrient Blend (Vitamins & Minerals), Pumpkin Seed Protein Isolate, Vegetable Fibre (Inulin), Sunflower Lecithin, Xanthan Gum, Steviol Glycosides, Sucralose.',
        'digestive_enzymes': 'Inulin Vegetable Fibre & Peak Micronutrient Blend',
        'sweetener': 'Steviol Glycosides & Sucralose'
    },
    'mywellness_peptide_hydro': {
        'ingredients': 'Hydrolysed Whey Peptide Protein, Raw Organic Cacao (in choc variant), Fructose, Salt, Stevia Leaf Extract.',
        'digestive_enzymes': 'Pre-Hydrolysed Whey Peptides (Fast Digestion & Maximum Nitrogen Retention)',
        'sweetener': 'Fructose & Stevia Leaf Extract'
    },
    'mywellness_protein_smoothie': {
        'ingredients': 'Superfood Protein Blend (Pea Protein, Hemp Seed Powder), Superfood Complex (Maca Root, Cacao Powder, Baobab Powder, Chia Seeds, Flaxseed Powder, Lucuma Powder, Mesquite Powder, Wheat Grass Powder, Matcha Powder, Red Beet Powder, Turmeric Powder), Stevia Leaf Extract.',
        'digestive_enzymes': '11 Organic Superfood Functional Complex',
        'sweetener': 'Stevia Leaf Extract'
    },
    'evox_lean_pro': {
        'ingredients': 'Lean-Pro Protein Matrix (Whey Protein Concentrate, Soy Protein Isolate, Calcium Caseinate), Cocoa, Garcinia Cambogia Extract (60% HCA), L-Carnitine Tartrate, Green Tea Extract, Tolerase® L (Lactase), Sucralose.',
        'digestive_enzymes': 'Tolerase® L (Lactase) + Garcinia & L-Carnitine Thermogenic Stack',
        'sweetener': 'Sucralose'
    },
    'scicore_naked': {
        'ingredients': '100% Cross-Flow Instantised Whey Protein Concentrate (80%), Sunflower Lecithin. Pure unflavoured, zero artificial sweeteners, zero thickeners.',
        'digestive_enzymes': 'None added (Native Pure Whey)',
        'sweetener': 'None (Unsweetened / Natural)'
    },
    'scicore_one_whey': {
        'ingredients': 'Instantised Whey Protein Concentrate, Whey Protein Isolate, Cocoa Powder (in choc variants), Flavouring, Sunflower Lecithin, Xanthan Gum, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Pure Ultra-Filtered Whey)',
        'sweetener': 'Sucralose'
    },
    'ssa_clear_whey': {
        'ingredients': 'Hydrolysed Clear Whey Protein Isolate, Citric Acid, Malic Acid, Flavouring, Colourant, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Pre-Hydrolysed Clear Peptides',
        'sweetener': 'Sucralose'
    },
    'ssa_whey_extreme': {
        'ingredients': 'Advanced Multi-Stage Whey Complex (Whey Protein Concentrate, Whey Protein Isolate, Hydrolysed Whey Peptides), Maltodextrin, Glycine, ZMB-6 Pro Stack (Zinc Monomethionine, Magnesium Aspartate, Vitamin B6), DigeZyme® Multi-Enzyme Complex, Flavouring, Cocoa Powder, Sucralose.',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex + ZMB-6 Recovery Stack',
        'sweetener': 'Sucralose'
    },
    'tnt_atomic_mega': {
        'ingredients': 'Tri-Phase Whey Protein Complex (Whey Protein Concentrate, Whey Protein Isolate, Whey Hydrolysate), L-Glycine, Creatine Monohydrate, Taurine, BCAAs, EAAs, Tolerase® L (Lactase), Flavouring, Cocoa Powder, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Tolerase® L (Lactase) + Creatine & EAA Anabolic Stack',
        'sweetener': 'Sucralose'
    },
    'tony_ferguson_go_shake': {
        'ingredients': 'Skim Milk Powder, Soy Protein Isolate, Whey Protein Concentrate, Inulin Prebiotic Fibre, Vitamins & Minerals Blend, Flavouring, Colouring (Beetroot Red), Stabiliser, Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Inulin Prebiotic Fibre & 18 Essential Vitamins and Minerals',
        'sweetener': 'Sucralose'
    },
    'phytopro_thrive': {
        'ingredients': '100% Nutralys® EU Non-GMO Water-Extracted Pea Protein Isolate (88% protein), Cocoa Powder / Madagascan Vanilla Powder (in flavoured variants), Xylitol, Stevia Leaf Extract.',
        'digestive_enzymes': 'None needed (Alkalizing Water-Extracted Pea Isolate)',
        'sweetener': 'Xylitol & Stevia (Unsweetened in Unflavoured)'
    },
    'phytopro_sport': {
        'ingredients': 'Nutralys® Pea Protein Isolate, L-Glutamine, Taurine, L-Carnitine, Creatine, Potassium AAC (1500mg), Magnesium AAC (750mg), Selenium AAC (50mg), C3 Turmeric Extract (200mg), Green Tea Extract (200mg), Maca Root Extract (500mg), Bioperine (5mg), Aminogen / DigeZyme Digestive Enzyme (200mg), B-Vitamin Complex, Cocoa Powder, Xylitol, Stevia, Kalahari Desert Salt.',
        'digestive_enzymes': 'Aminogen / DigeZyme Multi-Enzyme Complex (200mg) + Bioperine (5mg)',
        'sweetener': 'Xylitol & Stevia'
    },
    'phytopro_vegan_collagen': {
        'ingredients': 'Nutralys® Pea Protein Isolate, PhytoColl® Collagen-Generating Amino Complex (Glycine, Proline, L-Glutamine, Lysine, Serine, Arginine, Calcium HMB), Xylitol, Horsetail Extract (7% Silica), Vanilla Bean Powder, Salt, Stevia, Vitamin B7 (Biotin).',
        'digestive_enzymes': 'PhytoColl® Biomimetic Plant Collagen Matrix with Horsetail Silica & Biotin',
        'sweetener': 'Xylitol & Stevia'
    },
    'phytopro_muscle': {
        'ingredients': 'Nutralys® Pea Protein Isolate, GMO-Free Xylitol, Inulin (from Chicory Root Prebiotic), PhytaMin® A-Z Vitamin and Mineral Blend (23 vitamins & minerals), Calcium HMB, L-Carnitine, Taurine, Madagascan Vanilla Powder / UTZ-Certified Cocoa Powder, Steviol Glycosides, Oryx Desert Salt.',
        'digestive_enzymes': 'Chicory Root Inulin Prebiotic (3g) + Calcium HMB Muscle Protector',
        'sweetener': 'GMO-Free Xylitol & Steviol Glycosides'
    },
    'myprotein_impact_whey': {
        'ingredients': 'Whey Protein Concentrate (Milk) (96%), Emulsifier (Soy Lecithin), Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Pure Cross-Flow Concentrated Whey)',
        'sweetener': 'Sucralose'
    },
    'myprotein_impact_isolate': {
        'ingredients': 'Whey Protein Isolate (Milk) (96%), Emulsifier (Soy / Sunflower Lecithin), Flavouring, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Microfiltered Isolate)',
        'sweetener': 'Sucralose'
    },
    'myprotein_clear': {
        'ingredients': 'Hydrolysed Clear Whey Protein Isolate, Natural Acidifiers (Citric Acid, Malic Acid), Natural & Nature Identical Flavouring, Anti-Foaming Agent (Silicon Dioxide), Natural Colouring (Beetroot Red / Beta Carotene), Non-Nutritive Sweetener (Sucralose).',
        'digestive_enzymes': 'Pre-Hydrolysed Clear Whey Peptides',
        'sweetener': 'Sucralose'
    },
    'justprotein_premium': {
        'ingredients': 'Whey Protein Concentrate, Milk Protein Concentrate, Cocoa Powder (in chocolate flavours), Flavouring, Salt, Emulsifier, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added',
        'sweetener': 'Sucralose'
    },
    'muscleworks_100_whey': {
        'ingredients': 'Ultra-microfiltered Whey Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate), Low GI Sweetener Blend (Erythritol, Fructose, Stevia), Permitted Flavourants, Xanthan Gum, L-Glutamine, Instantised Branched Chain Amino Acids (BCAAs), Cocoa Powder (in chocolate flavours).',
        'digestive_enzymes': 'L-Glutamine & BCAAs (No digestive enzymes added)',
        'sweetener': 'Erythritol, Fructose & Stevia'
    },
    'muscleworks_isotech': {
        'ingredients': 'Multi-Stage Isolate Matrix (Whey Protein Isolate, Hydrolysed Whey, Milk Protein Isolate, Nihpro® Hydrolysed Isolate, Whey Protein Concentrate, Pea Protein Isolate), Cocoa Powder (in chocolate flavours), Flavouring, Taurine, Salt, Emulsifier, Stabiliser, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Multi-Stage Fast & Medium Isolate Matrix)',
        'sweetener': 'Sucralose'
    },
    'lifestyle_food_whey': {
        'ingredients': "100% Pure Whey Protein Concentrate (Cow's Milk).",
        'digestive_enzymes': 'None added',
        'sweetener': 'None (Unsweetened / 100% Pure)'
    },
    'health_connection_just_whey': {
        'ingredients': "Whey Protein Concentrate (Cow's Milk) (98.5%), Non-GMO Soya Lecithin (1.5%).",
        'digestive_enzymes': 'None added',
        'sweetener': 'None (Unsweetened / 100% Pure)'
    },
    'clear_nutrition_whey': {
        'ingredients': '100% Whey Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate), Cocoa Powder (in chocolate flavours), Natural & Artificial Flavours, Soy Lecithin, Xanthan Gum, Sweetener (Sucralose).',
        'digestive_enzymes': '5g Naturally Occurring BCAAs',
        'sweetener': 'Sucralose'
    },
    'muscle_dynamix_whey_one': {
        'ingredients': 'Ultra-Microfiltered Whey Protein Blend (Whey Protein Concentrate, Whey Protein Isolate), L-Leucine (4g), L-Glutamine, Cocoa Powder (in chocolate flavours), Flavouring, Emulsifier (Lecithin), Stabiliser (Xanthan Gum), Sweetener (Sucralose).',
        'digestive_enzymes': 'Enriched with 4g L-Leucine & Glutamine precursors',
        'sweetener': 'Sucralose'
    },
    'muscle_dynamix_iso_gold': {
        'ingredients': 'Cross-Flow Microfiltered Whey Protein Isolate, Hydrolysed Whey Protein, Cocoa Powder (in chocolate flavours), Flavouring, Emulsifier (Lecithin), Thickener, Sweetener (Sucralose).',
        'digestive_enzymes': 'None added (Pre-hydrolyzed)',
        'sweetener': 'Sucralose'
    },
    'nestle_resource_whey': {
        'ingredients': "Soluble Whey Protein Powder (88% Cow's Milk Protein), Emulsifier (Soya Lecithin INS 322i).",
        'digestive_enzymes': 'None added (Clinical grade soluble whey)',
        'sweetener': 'None (Neutral / Unsweetened)'
    },
    'blast_vitality_daily': {
        'ingredients': '100% Plant-Based Protein Blend (Pea Protein Isolate, Rice Protein Concentrate), DigeZyme® Multi-Enzyme Complex (50mg), Natural Vanilla / Cocoa Flavouring, Sweetener (Stevia Leaf Extract).',
        'digestive_enzymes': 'DigeZyme® Multi-Enzyme Complex (50mg)',
        'sweetener': 'Stevia Leaf Extract'
    },
    'on_platinum_hydrowhey': {
        'ingredients': 'Hydrolysed Whey Protein Isolate (87%) [Emulsifier: Soy Lecithin], Micronized Branched-Chain Amino Acid Blend (5%) (L-Leucine, L-Isoleucine, L-Valine [Emulsifier: Sunflower Lecithin]), Cocoa Powder (in chocolate flavours), Thickener (Carrageenan), Flavourings, Sweeteners (Sucralose, Acesulfame Potassium), Sodium Chloride.',
        'digestive_enzymes': 'Micronized BCAAs (9g+)',
        'sweetener': 'Sucralose & Acesulfame Potassium'
    },
    'collagen_co_isolate': {
        'ingredients': "100% Pure Cross-Flow Microfiltered Whey Protein Isolate (Cow's Milk), Instantising Agent (Sunflower Lecithin).",
        'digestive_enzymes': 'Naturally Occurring BCAAs',
        'sweetener': 'None (Taste Neutral / Unsweetened)'
    },
    'sa_vitamins_isolate': {
        'ingredients': "100% Pure Cross-Flow Microfiltered Whey Protein Isolate (Cow's Milk), Sunflower Lecithin.",
        'digestive_enzymes': 'None added',
        'sweetener': 'None (Natural / Unflavoured)'
    },
    'atp_fitness_whey': {
        'ingredients': "100% Pure Whey Protein Concentrate (Cow's Milk), Cocoa (in Belgian Cocoa flavour only).",
        'digestive_enzymes': 'None added',
        'sweetener': 'None (Unsweetened / 100% Pure)'
    },
    'my_whey_mpi': {
        'ingredients': "100% Pure Milk Protein Isolate (Cow's Milk: 80% Micellar Casein, 20% Whey).",
        'digestive_enzymes': 'None added',
        'sweetener': 'None (Unsweetened / 100% Pure)'
    },
    'beauty_gen_creamer': {
        'ingredients': 'Peptan® Hydrolysed Bovine Collagen Peptides (Type I & III), Medium Chain Triglycerides (MCT) Oil Powder, Coconut Milk Powder, Prebiotic Acacia Fibre.',
        'digestive_enzymes': 'Prebiotic Acacia Fibre',
        'sweetener': 'None (Sugar-Free, Unsweetened)'
    },
    'remedy_greens_mobility': {
        'ingredients': 'Peptan® Hydrolysed Bovine Collagen Peptides (Type I), Active Collagen Type-II™ (Standardised Undenatured Chicken Cartilage), Organic Beetroot Powder, Buffered Vitamin C (Calcium Ascorbate), Flaxseed Powder (Omega-3 ALA), Flavouring, Sweetener (Stevia Extract).',
        'digestive_enzymes': 'Active Collagen Type-II™ & Buffered Vitamin C',
        'sweetener': 'Stevia Extract'
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
        if 'plant' in t or 'vegan' in t:
            matched = BRAND_FORMULATIONS['usn_plant']
        else:
            matched = BRAND_FORMULATIONS['usn_bluelab']
    elif 'isozero' in t or 'iso zero' in t or 'iso pro zero' in t or 'isopro zero' in t:
        matched = BRAND_FORMULATIONS['usn_isozero']
    elif 'protein water' in t and 'usn' in t:
        matched = BRAND_FORMULATIONS['usn_protein_water']
    elif 'plant' in t and ('usn' in b or 'usn' in t):
        matched = BRAND_FORMULATIONS['usn_plant']
    elif ('hardcore' in t or 'whey gh' in t) and 'my wellness' not in b and 'mywellness' not in b and 'alpha' not in t:
        if 'ripped' in t:
            matched = BRAND_FORMULATIONS['usn_hardcore_ripped']
        else:
            matched = BRAND_FORMULATIONS['usn_hardcore']
    elif 'beast' in t and ('usn' in b or 'usn' in t):
        matched = BRAND_FORMULATIONS['usn_beast']
    elif 'diet fuel' in t:
        matched = BRAND_FORMULATIONS['usn_diet_fuel']
    elif 'muscle works' in b or 'muscleworks' in b or ('muscle works' in t and 'dynamix' not in t):
        if 'iso-tech' in t or 'isotech' in t or 'iso tech' in t:
            matched = BRAND_FORMULATIONS['muscleworks_isotech']
        elif 'whey-bolic' in t or 'wheybolic' in t:
            matched = BRAND_FORMULATIONS['muscle_works_wheybolic']
        elif 'thermo' in t:
            matched = BRAND_FORMULATIONS['muscle_works_thermo']
        else:
            matched = BRAND_FORMULATIONS['muscleworks_100_whey']
    elif 'hydro whey' in t or 'hydrowhey' in t or 'hydro-whey' in t:
        matched = BRAND_FORMULATIONS['on_platinum_hydrowhey']
    elif 'casein' in t and ('optimum' in b or 'on' == b or 'optimum' in t or 'gold' in t):
        matched = BRAND_FORMULATIONS['on_casein']
    elif 'gold standard' in t and 'isolate' in t:
        matched = BRAND_FORMULATIONS['on_isolate']
    elif 'gold standard' in t or 'optimum nutrition' in t or ('optimum' in t and 'whey' in t) or ('optimum' in b and 'whey' in t):
        matched = BRAND_FORMULATIONS['on_gold_standard']
    elif 'nihpro' in t:
        matched = BRAND_FORMULATIONS['nutritech_nihpro']
    elif 'nutritech' in b or 'nutritech' in t:
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
        elif 'ssa' in b: matched = BRAND_FORMULATIONS['ssa_clear_whey']
        else: matched = BRAND_FORMULATIONS['nutritech_clear']
    elif 'anabolic whey' in t and 'npl' in t:
        matched = BRAND_FORMULATIONS['npl_anabolic_whey']
    elif 'pro gains' in t or ('npl' in b and 'gain' in t):
        matched = BRAND_FORMULATIONS['npl_pro_gains']
    elif ('npl' in b or 'npl' in t) and ('plant' in t or 'vegan' in t):
        matched = BRAND_FORMULATIONS['npl_plant']
    elif 'npl' in b or 'platinum whey' in t:
        matched = BRAND_FORMULATIONS['npl_platinum_whey']
    elif 'nitrotech' in t or 'nitro-tech' in t or 'nitro tech' in t or 'muscletech' in b:
        matched = BRAND_FORMULATIONS['muscletech_nitrotech']
    elif 'biogen' in b or 'biogen' in t:
        if 'bulk' in t: matched = BRAND_FORMULATIONS['biogen_bulk']
        elif 'clear' in t: matched = BRAND_FORMULATIONS['biogen_clear']
        elif 'plant' in t or 'vegan' in t: matched = BRAND_FORMULATIONS['biogen_plant']
        else: matched = BRAND_FORMULATIONS['biogen_whey']
    elif 'amp amplified' in t or 'amp gold' in t:
        matched = BRAND_FORMULATIONS['gnc_amp_gold']
    elif 'gnc' in b or 'gnc' in t:
        matched = BRAND_FORMULATIONS['gnc_pro_performance']
    elif 'clicks' in b or 'smartlife' in t:
        matched = BRAND_FORMULATIONS['clicks_smartlife']
    elif 'ssa' in b or 'ssa' in t:
        if 'clear' in t: matched = BRAND_FORMULATIONS['ssa_clear_whey']
        elif 'vegan' in t or 'plant' in t: matched = BRAND_FORMULATIONS['ssa_vegan']
        elif 'extreme' in t: matched = BRAND_FORMULATIONS['ssa_whey_extreme']
        else: matched = BRAND_FORMULATIONS['ssa_whey']
    elif 'evox' in b or 'evox' in t:
        if 'lean' in t or 'diet' in t or 'lite' in t: matched = BRAND_FORMULATIONS['evox_lean_pro']
        else: matched = BRAND_FORMULATIONS['evox_whey']
    elif 'gloot' in b or 'gloot' in t:
        if 'vegan' in t: matched = BRAND_FORMULATIONS['gloot_vegan']
        else: matched = BRAND_FORMULATIONS['gloot_whey']
    elif 'primeself' in b or 'primeself' in t:
        matched = BRAND_FORMULATIONS['primeself_grassfed']
    elif 'lifegain' in b or 'lifegain' in t:
        matched = BRAND_FORMULATIONS['lifegain']
    elif 'weider' in b or 'mega mass' in t:
        matched = BRAND_FORMULATIONS['weider_mega_mass']
    elif 'alpha plant' in t or ('alpha' in t and 'plant' in t):
        matched = BRAND_FORMULATIONS['mywellness_alpha_plant']
    elif 'alpha' in t and ('whey' in t or 'my wellness' in b or 'alpha' in b):
        matched = BRAND_FORMULATIONS['mywellness_alpha']
    elif "nature's nutrition" in b or "natures nutrition" in b or "nature's nutrition" in t or "natures nutrition" in t:
        matched = BRAND_FORMULATIONS['natures_nutrition_plant']
    elif 'my wellness' in b or 'mywellness' in b or 'superior whey' in t or 'natures whey' in t or "nature's whey" in t:
        if 'soy' in t: matched = BRAND_FORMULATIONS['mywellness_soy']
        elif 'yeast' in t: matched = BRAND_FORMULATIONS['mywellness_yeast']
        elif 'clean diet plant' in t or ('clean diet' in t and 'plant' in t) or ('diet' in t and 'plant' in t): matched = BRAND_FORMULATIONS['mywellness_clean_diet_plant']
        elif ('pure pea' in t or 'pea protein' in t) and 'super' not in t and 'vegan' not in t: matched = BRAND_FORMULATIONS['mywellness_pure_pea']
        elif 'super vegan' in t: matched = BRAND_FORMULATIONS['mywellness_vegan']
        elif 'super clean' in t or ('clean protein' in t and 'x5' in t): matched = BRAND_FORMULATIONS['mywellness_super_clean']
        elif 'vegainer' in t: matched = BRAND_FORMULATIONS['mywellness_vegainer']
        elif 'hard mass' in t: matched = BRAND_FORMULATIONS['mywellness_hard_mass']
        elif 'superior whey' in t: matched = BRAND_FORMULATIONS['mywellness_superior']
        elif 'peptide' in t or 'hydro protein' in t: matched = BRAND_FORMULATIONS['mywellness_peptide_hydro']
        elif 'smoothie' in t: matched = BRAND_FORMULATIONS['mywellness_protein_smoothie']
        elif 'isolate' in t: matched = BRAND_FORMULATIONS['mywellness_isolate']
        elif 'collagen' in t: matched = BRAND_FORMULATIONS['mywellness_collagen']
        elif 'keto-bolic' in t or 'ketobolic' in t: matched = BRAND_FORMULATIONS['mywellness_ketobolic']
        elif 'keto' in t: matched = BRAND_FORMULATIONS['mywellness_keto_diet_shake']
        elif 'cheat meal' in t: matched = BRAND_FORMULATIONS['mywellness_her_cheat_meal']
        elif 'diet matcha' in t or ('matcha' in t and 'diet' in t): matched = BRAND_FORMULATIONS['mywellness_clean_diet_matcha']
        elif 'diet shake' in t or 'clean diet' in t: matched = BRAND_FORMULATIONS['mywellness_clean_diet_shake']
        elif any(k in t for k in ['vegan', 'plant', 'pea']): matched = BRAND_FORMULATIONS['mywellness_vegan']
        elif 'casein' in t or 'milk protein' in t: matched = BRAND_FORMULATIONS['mywellness_casein']
        elif 'game changer' in t: matched = BRAND_FORMULATIONS['mywellness_game_changer']
        else: matched = BRAND_FORMULATIONS['mywellness_nature']
    elif 'nature' in t and ('whey' in t or 'protein' in t):
        matched = BRAND_FORMULATIONS['mywellness_nature']
    elif 'black bull' in b or 'blackbull' in b or ('supreme' in t and 'usn' not in b and 'usn' not in t):
        matched = BRAND_FORMULATIONS['blackbull_whey']
    elif 'tony ferguson' in b or 'tony ferguson' in t or 'tferg' in t:
        if 'go shake' in t or 'go-shake' in t: matched = BRAND_FORMULATIONS['tony_ferguson_go_shake']
        else: matched = BRAND_FORMULATIONS['tony_ferguson']
    elif 'sci-core' in b or 'scicore' in b:
        if 'one whey' in t: matched = BRAND_FORMULATIONS['scicore_one_whey']
        elif 'naked' in t or 'pure' in t: matched = BRAND_FORMULATIONS['scicore_naked']
        else: matched = BRAND_FORMULATIONS['scicore_whey']
    elif '32gi' in b or '32gi' in t:
        matched = BRAND_FORMULATIONS['32gi_plant']
    elif 'peak' in b or 'peak' in t:
        matched = BRAND_FORMULATIONS['peak_plant']
    elif 'phyto pro' in b or 'phytopro' in b or 'phyto pro' in t or 'phytopro' in t:
        if 'sport' in t: matched = BRAND_FORMULATIONS['phytopro_sport']
        elif 'collagen' in t: matched = BRAND_FORMULATIONS['phytopro_vegan_collagen']
        elif 'muscle' in t or 'lean' in t: matched = BRAND_FORMULATIONS['phytopro_muscle']
        else: matched = BRAND_FORMULATIONS['phytopro_thrive']
    elif 'primal' in b or 'primal' in t:
        if 'mass' in t or 'gain' in t: matched = BRAND_FORMULATIONS['primal_mass_gain']
        elif 'skinny' in t: matched = BRAND_FORMULATIONS['primal_skinny_whey']
        elif 'diet' in t: matched = BRAND_FORMULATIONS['primal_diet_shake']
        else: matched = BRAND_FORMULATIONS['primal_whey']
    elif 'tnt' in b or 'tnt' in t:
        if 'atomic' in t or 'mega whey' in t: matched = BRAND_FORMULATIONS['tnt_atomic_mega']
        else: matched = BRAND_FORMULATIONS['tnt_whey']
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
    elif 'myprotein' in b or 'myprotein' in t:
        if 'clear' in t: matched = BRAND_FORMULATIONS['myprotein_clear']
        elif 'isolate' in t: matched = BRAND_FORMULATIONS['myprotein_impact_isolate']
        else: matched = BRAND_FORMULATIONS['myprotein_impact_whey']
    elif 'just protein' in b or 'just protein' in t:
        matched = BRAND_FORMULATIONS['justprotein_premium']
    elif 'lifestyle food' in b or 'lifestyle food' in t:
        if 'bone broth' in t: matched = BRAND_FORMULATIONS.get('harvest_table_broth')
        else: matched = BRAND_FORMULATIONS['lifestyle_food_whey']
    elif 'health connection' in b or 'health connection' in t or 'just whey' in t:
        matched = BRAND_FORMULATIONS['health_connection_just_whey']
    elif 'clear nutrition' in b or 'clear nutrition' in t:
        matched = BRAND_FORMULATIONS['clear_nutrition_whey']
    elif 'muscle dynamix' in b or 'muscle dynamix' in t or ('dynamix' in b and 'muscle works' not in b):
        if 'iso gold' in t or 'isogold' in t: matched = BRAND_FORMULATIONS['muscle_dynamix_iso_gold']
        else: matched = BRAND_FORMULATIONS['muscle_dynamix_whey_one']
    elif 'nestle' in b or 'nestle' in t or 'resorce' in t or 'resource whey' in t:
        matched = BRAND_FORMULATIONS['nestle_resource_whey']
    elif 'blast vitality' in b or 'blast vitality' in t or (b.strip() == 'blast' and 'daily protein' in t):
        matched = BRAND_FORMULATIONS['blast_vitality_daily']
    elif 'collagen & co' in b or 'collagen & co' in t:
        matched = BRAND_FORMULATIONS['collagen_co_isolate']
    elif 'sa vitamins' in b or 'sa vitamins' in t:
        matched = BRAND_FORMULATIONS['sa_vitamins_isolate']
    elif 'atp fitness' in b or 'atp fitness' in t or 'atp whey' in t:
        matched = BRAND_FORMULATIONS['atp_fitness_whey']
    elif 'my whey' in b or 'my whey' in t:
        matched = BRAND_FORMULATIONS['my_whey_mpi']
    elif 'beauty gen' in b or 'beauty gen' in t:
        matched = BRAND_FORMULATIONS['beauty_gen_creamer']
    elif 'remedy greens' in b or 'remedy greens' in t:
        matched = BRAND_FORMULATIONS['remedy_greens_mobility']
        
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
    elif matched == BRAND_FORMULATIONS.get('mywellness_alpha_plant'):
        serving_size = 36.0
        protein_per_serving = 25.0
        carbs = 4.5
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('mywellness_superior'):
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 2.5
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('mywellness_isolate'):
        serving_size = 25.0
        protein_per_serving = 22.5
        carbs = 0.5
        fat = 0.2
    elif matched == BRAND_FORMULATIONS.get('mywellness_soy'):
        serving_size = 23.0
        protein_per_serving = 19.55
        carbs = 0.23
        fat = 0.97
    elif matched == BRAND_FORMULATIONS.get('mywellness_pure_pea'):
        serving_size = 23.0
        protein_per_serving = 19.55
        carbs = 0.46
        fat = 0.69
    elif matched == BRAND_FORMULATIONS.get('mywellness_yeast'):
        serving_size = 30.0
        protein_per_serving = 21.0
        carbs = 3.0
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_clean_diet_plant'):
        serving_size = 25.0
        protein_per_serving = 18.0
        carbs = 3.1
        fat = 1.12
    elif matched == BRAND_FORMULATIONS.get('mywellness_vegan'):
        serving_size = 30.0
        protein_per_serving = 22.0
        carbs = 2.5
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('usn_plant'):
        serving_size = 31.0
        protein_per_serving = 22.0
        carbs = 2.5
        fat = 2.1
    elif matched == BRAND_FORMULATIONS.get('biogen_plant'):
        serving_size = 32.0
        protein_per_serving = 21.0
        carbs = 3.2
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('npl_plant'):
        serving_size = 30.0
        protein_per_serving = 21.0
        carbs = 2.8
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('ssa_vegan'):
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 2.5
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('mywellness_collagen'):
        serving_size = 10.0
        protein_per_serving = 9.0
        carbs = 0.0
        fat = 0.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_game_changer'):
        serving_size = 75.0
        protein_per_serving = 25.0
        carbs = 40.0
        fat = 3.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_super_clean') or ('super clean' in t and ('my wellness' in b or 'mywellness' in b or 'clean protein' in t)):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 4.2
        fat = 2.6
    elif matched == BRAND_FORMULATIONS.get('natures_nutrition_plant') or "nature's nutrition" in t or "natures nutrition" in t or "nature's nutrition" in b or "natures nutrition" in b:
        serving_size = 25.0
        protein_per_serving = 15.2
        carbs = 3.3
        fat = 0.7
    elif matched == BRAND_FORMULATIONS.get('clicks_smartlife') or 'clicks' in b or 'smartlife' in t or 'purified protein' in t:
        serving_size = 32.0
        protein_per_serving = 21.4
        carbs = 3.7
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('mywellness_vegainer') or 'vegainer' in t:
        serving_size = 120.0
        protein_per_serving = 36.0
        carbs = 66.0
        fat = 4.8
    elif matched == BRAND_FORMULATIONS.get('mywellness_hard_mass') or 'hard mass' in t:
        serving_size = 150.0
        protein_per_serving = 50.0
        carbs = 85.0
        fat = 3.0
    elif matched == BRAND_FORMULATIONS.get('weider_mega_mass') or 'mega mass' in t:
        serving_size = 150.0
        protein_per_serving = 30.0
        carbs = 103.0
        fat = 2.5
    elif matched == BRAND_FORMULATIONS.get('primal_mass_gain') or ('primal' in t and 'mass' in t):
        serving_size = 167.0
        protein_per_serving = 25.0
        carbs = 122.5
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('npl_pro_gains') or 'pro gains' in t:
        serving_size = 150.0
        protein_per_serving = 50.0
        carbs = 82.0
        fat = 3.5
    elif matched == BRAND_FORMULATIONS.get('biogen_bulk') or 'bulk 45' in t:
        serving_size = 226.0
        protein_per_serving = 45.3
        carbs = 150.0
        fat = 3.6
    elif matched == BRAND_FORMULATIONS.get('usn_hyperbolic') or 'hyperbolic' in t:
        serving_size = 300.0
        protein_per_serving = 60.0
        carbs = 206.0
        fat = 5.0
    elif matched == BRAND_FORMULATIONS.get('lifegain') or 'lifegain' in t:
        serving_size = 30.0
        protein_per_serving = 15.0
        carbs = 8.5
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('primal_skinny_whey'):
        serving_size = 30.0
        protein_per_serving = 20.6
        carbs = 0.5
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('primal_diet_shake'):
        serving_size = 35.0
        protein_per_serving = 21.0
        carbs = 4.5
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('primal_whey'):
        serving_size = 30.0
        protein_per_serving = 21.0
        carbs = 1.4
        fat = 2.4
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
    elif matched == BRAND_FORMULATIONS.get('32gi_plant'):
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 3.0
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('peak_plant'):
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 1.2
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('mywellness_peptide_hydro'):
        serving_size = 30.0
        protein_per_serving = 21.6
        carbs = 2.5
        fat = 2.2
    elif matched == BRAND_FORMULATIONS.get('mywellness_protein_smoothie'):
        serving_size = 32.0
        protein_per_serving = 15.0
        carbs = 9.0
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_nature'):
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 2.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('mywellness_keto_diet_shake') or ('keto' in t and 'shake' in t and 'ketobolic' not in t and 'keto-bolic' not in t):
        serving_size = 40.0
        protein_per_serving = 9.0
        carbs = 3.0
        fat = 28.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_ketobolic') or 'ketobolic' in t or 'keto-bolic' in t:
        serving_size = 80.0
        protein_per_serving = 25.0
        carbs = 10.0
        fat = 50.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_her_cheat_meal') or 'cheat meal' in t:
        serving_size = 40.0
        protein_per_serving = 20.0
        carbs = 12.0
        fat = 2.5
    elif matched == BRAND_FORMULATIONS.get('mywellness_clean_diet_matcha') or 'diet matcha' in t:
        serving_size = 35.0
        protein_per_serving = 21.0
        carbs = 4.5
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('mywellness_clean_diet_shake') or 'diet shake' in t:
        serving_size = 35.0
        protein_per_serving = 21.0
        carbs = 4.5
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('blackbull_whey'):
        serving_size = 32.0
        protein_per_serving = 22.0
        carbs = 4.5
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('gnc_pro_performance'):
        serving_size = 33.0
        protein_per_serving = 24.0
        carbs = 3.0
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('gnc_amp_gold'):
        serving_size = 33.0
        protein_per_serving = 24.0
        carbs = 2.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('evox_whey'):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 2.5
        fat = 1.7
    elif matched == BRAND_FORMULATIONS.get('evox_lean_pro'):
        serving_size = 35.0
        protein_per_serving = 21.0
        carbs = 5.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('scicore_naked'):
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 1.06
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('scicore_one_whey'):
        serving_size = 29.0
        protein_per_serving = 22.4
        carbs = 3.3
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('ssa_clear_whey'):
        serving_size = 26.0
        protein_per_serving = 21.0
        carbs = 0.3
        fat = 0.1
    elif matched == BRAND_FORMULATIONS.get('ssa_whey_extreme'):
        serving_size = 38.0
        protein_per_serving = 22.0
        carbs = 10.1
        fat = 2.2
    elif matched == BRAND_FORMULATIONS.get('tnt_atomic_mega'):
        serving_size = 33.0
        protein_per_serving = 25.0
        carbs = 2.8
        fat = 0.8
    elif matched == BRAND_FORMULATIONS.get('tony_ferguson_go_shake'):
        serving_size = 35.0
        protein_per_serving = 17.4
        carbs = 11.0
        fat = 0.9
    elif matched == BRAND_FORMULATIONS.get('tony_ferguson'):
        serving_size = 28.0
        protein_per_serving = 20.0
        carbs = 2.6
        fat = 1.6
    elif matched == BRAND_FORMULATIONS.get('phytopro_thrive'):
        serving_size = 20.0
        protein_per_serving = 18.0
        carbs = 0.6
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('phytopro_sport'):
        serving_size = 40.0
        protein_per_serving = 27.5
        carbs = 0.6
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('phytopro_vegan_collagen'):
        serving_size = 30.0
        protein_per_serving = 25.0
        carbs = 0.6
        fat = 1.4
    elif matched == BRAND_FORMULATIONS.get('phytopro_muscle'):
        serving_size = 62.0
        protein_per_serving = 40.0
        carbs = 7.6
        fat = 3.3
    elif matched == BRAND_FORMULATIONS.get('myprotein_impact_whey'):
        serving_size = 25.0
        protein_per_serving = 20.0
        carbs = 1.0
        fat = 1.9
    elif matched == BRAND_FORMULATIONS.get('myprotein_impact_isolate'):
        serving_size = 25.0
        protein_per_serving = 23.0
        carbs = 0.6
        fat = 0.1
    elif matched == BRAND_FORMULATIONS.get('myprotein_clear'):
        serving_size = 25.0
        protein_per_serving = 20.0
        carbs = 0.7
        fat = 0.1
    elif matched == BRAND_FORMULATIONS.get('justprotein_premium'):
        serving_size = 30.0
        protein_per_serving = 23.0
        carbs = 2.0
        fat = 1.5
    elif matched == BRAND_FORMULATIONS.get('muscleworks_100_whey'):
        serving_size = 34.0
        protein_per_serving = 22.0
        carbs = 3.5
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('muscleworks_isotech'):
        serving_size = 30.0
        protein_per_serving = 20.0
        carbs = 1.5
        fat = 0.8
    elif matched == BRAND_FORMULATIONS.get('lifestyle_food_whey'):
        serving_size = 20.0
        protein_per_serving = 15.2
        carbs = 1.0
        fat = 1.2
    elif matched == BRAND_FORMULATIONS.get('health_connection_just_whey'):
        serving_size = 30.0
        protein_per_serving = 23.4
        carbs = 1.5
        fat = 2.0
    elif matched == BRAND_FORMULATIONS.get('clear_nutrition_whey'):
        serving_size = 32.0
        protein_per_serving = 23.0
        carbs = 2.5
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('muscle_dynamix_whey_one'):
        serving_size = 35.0
        protein_per_serving = 24.0
        carbs = 3.2
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('muscle_dynamix_iso_gold'):
        serving_size = 32.0
        protein_per_serving = 29.0
        carbs = 0.9
        fat = 0.4
    elif matched == BRAND_FORMULATIONS.get('nestle_resource_whey'):
        serving_size = 12.0
        protein_per_serving = 10.6
        carbs = 0.04
        fat = 0.12
    elif matched == BRAND_FORMULATIONS.get('blast_vitality_daily'):
        serving_size = 20.0
        protein_per_serving = 15.0
        carbs = 1.3
        fat = 1.3
    elif matched == BRAND_FORMULATIONS.get('on_platinum_hydrowhey'):
        serving_size = 39.0
        protein_per_serving = 30.0
        carbs = 2.0
        fat = 1.0
    elif matched == BRAND_FORMULATIONS.get('collagen_co_isolate'):
        serving_size = 30.0
        protein_per_serving = 27.0
        carbs = 0.5
        fat = 0.3
    elif matched == BRAND_FORMULATIONS.get('sa_vitamins_isolate'):
        serving_size = 25.0
        protein_per_serving = 21.6
        carbs = 0.5
        fat = 0.3
    elif matched == BRAND_FORMULATIONS.get('atp_fitness_whey'):
        serving_size = 30.0
        protein_per_serving = 24.0
        carbs = 1.8
        fat = 1.8
    elif matched == BRAND_FORMULATIONS.get('my_whey_mpi'):
        serving_size = 30.0
        protein_per_serving = 25.5
        carbs = 1.2
        fat = 0.4
    elif matched == BRAND_FORMULATIONS.get('beauty_gen_creamer'):
        serving_size = 15.0
        protein_per_serving = 10.0
        carbs = 1.5
        fat = 2.5
    elif matched == BRAND_FORMULATIONS.get('remedy_greens_mobility'):
        serving_size = 15.0
        protein_per_serving = 9.6
        carbs = 2.0
        fat = 0.5
    elif ptype in ['Whey Isolate', 'Clear Whey / Protein Water'] or (matched and 'isolate' in str(matched) and ptype != 'Plant / Vegan Protein'):
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
    elif ptype == 'Mass Gainer' or (matched and 'mass' in str(matched)) or any(k in t for k in ['mega mass', 'vegainer', 'hard mass', 'mass gain', 'weight gainer', 'mass gainer', 'pro gains', 'bulk 45', 'hyperbolic']) or (any(m in t for m in ['mass', 'gainer', 'gain', 'gains']) and not any(p in t for p in ['lean muscle', 'muscle gain', 'gain lean', 'muscle growth', 'lifegain'])):
        serving_size = 150.0
        protein_per_serving = 30.0
        carbs = 95.0
        fat = 3.0
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

    final_ing = matched['ingredients'] if matched else (
        'Multi-Stage Carbohydrate Blend (Maltodextrin, Waxy Maize Starch, Oat Flour), Multi-Stage Protein Matrix (Whey Protein Concentrate, Milk Protein Isolate, Calcium Caseinate), Cocoa Powder, Flavouring, Sweetener (Sucralose).' if ptype == 'Mass Gainer' else
        'Premium Whey Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate), Cocoa / Natural Flavouring, Emulsifier (Lecithin), Stabiliser (Xanthan Gum), Non-Nutritive Sweetener (Sucralose).'
    )
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

