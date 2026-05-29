# eCommerce BI — GitHub Copilot Instructions

<!--
  GITHUB COPILOT INTEGRATION
  Copy to: .github/copilot-instructions.md
-->

## eCommerce Business Intelligence

Generate BI reports from eCommerce order CSVs. Auto-detects Tiendanube, Shopify, WooCommerce.

### Execution
| Mode | Command |
|------|---------|
| Lite (21 analyses) | `python3 scripts/bi_analysis.py --csv "file.csv" --mode lite --output out.json` |
| Full (39 analyses) | `python3 scripts/bi_analysis.py --csv "file.csv" --mode full --output out.json` |
| Individual | `python3 scripts/bi_analysis.py --csv "file.csv" --analysis N --output out.json` |
| List | `python3 scripts/bi_analysis.py --list` |

### Key Analyses
| # | Name | Required Columns |
|---|------|-----------------|
| 7 | RFM | email, date, total |
| 1 | Market Basket | order_id, product_name |
| 9 | Cohorts | email, date |
| 8 | CLV | email, date, total |
| 3 | Product Ranking | product_name, product_price, product_qty, date |

### Workflow
1. Detect platform from CSV headers
2. Ask mode (Lite/Full/Individual)
3. Run `python3 scripts/bi_analysis.py`
4. Generate HTML from JSON using template

### Rules
- Always run the script — never calculate manually
- Market Basket: support > 1%, lift > 1.0 only
- RFM: 11 standard labels
- Cohorts: max 12×12
- All local processing — no external APIs

### Requirements
Python 3.9+, pandas, numpy
