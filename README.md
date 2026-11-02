# 🇿🇦 South Africa Protein Powder Database & Tracker

A comprehensive database and cost-per-gram comparison tool for protein powders across South African retailers (Takealot, Amazon ZA, Clicks, Dis-Chem, and Nutritech Direct).

Covers **Whey Blends, 100% Whey Isolates, Plant & Vegan, Micellar Casein, Beef Isolate, Bone Broth, Collagen Peptides, Clear Whey, and Multi-Source Blends**.

## ✨ Features

- **Cost-per-Gram of Pure Protein:** Accurate pricing calculated against actual protein purity, not gross tub weight.
- **DIAAS & PDCAAS Quality Ratings:** Protein digestibility and amino acid bioavailability scores for every formulation.
- **Verified Manufacturer Ingredients:** Sourced directly from South African manufacturer labels, including full digestive enzymes and sweetener profiles.
- **Tub Size Value Highlighting:** Automatically calculates and flags the best-value tub size (`★ Best Value`) for each product line.
- **Live Search & Category Filters:** One-click category tabs, brand filters, and instant keyword searching.
- **No Backend Required:** Runs 100% client-side in any modern browser.

## 🚀 Running Locally

Simply open `index.html` in any web browser, or start a local server:

```bash
python -m http.server 8080
```
Then navigate to `http://localhost:8080`.

## 📦 Updating the Data

To scrape/refresh retailer prices and recompile the master database:

```bash
python process_master.py
```
This updates `data/proteins.db`, `data/proteins.json`, and `data/products_data.js`.

