---
name: ecommerce-bi
description: "Business Intelligence para eCommerce — 39 análisis desde un CSV de ventas. Auto-detecta Tiendanube, Shopify, WooCommerce."
---

<!--
  CLAUDE CODE SKILL
  Install: git clone https://github.com/mathiaschu/ecommerce-bi.git ~/.claude/skills/ecommerce-bi
-->

# eCommerce Business Intelligence Skill

Genera informes de BI a partir de un CSV de órdenes. Detecta Tiendanube, Shopify o WooCommerce automáticamente y corre desde 1 hasta 39 análisis.

## Modos

- **Lite** (21 análisis, ~30s): `python3 scripts/bi_analysis.py --csv "ordenes.csv" --mode lite --output /tmp/bi_results.json`
- **Full** (39 análisis, ~90s): `python3 scripts/bi_analysis.py --csv "ordenes.csv" --mode full --output /tmp/bi_results.json`
- **Individual**: `python3 scripts/bi_analysis.py --csv "ordenes.csv" --analysis 7,9 --output /tmp/bi_results.json`
- **Listar**: `python3 scripts/bi_analysis.py --list`

## Workflow

1. Identificar el CSV y detectar plataforma (headers de `references/csv_mapping.md`)
2. Preguntar al usuario: Lite / Full / Individual
3. Correr `python3 scripts/bi_analysis.py`
4. Leer JSON de resultados
5. Generar HTML usando `references/html_template.md` como base

## Referencias

- `references/analysis_catalog.md` — Metodología de los 39 análisis
- `references/csv_mapping.md` — Mapeo de columnas por plataforma
- `references/html_template.md` — Template HTML
- `references/required_columns.md` — Columnas requeridas por análisis

## Reglas

- SIEMPRE correr `bi_analysis.py` — no calcular manualmente
- Market Basket: solo `support > 1%` y `lift > 1.0`
- RFM: usar 11 labels estándar
- Cohortes: últimas 12 cohortes × 12 meses
- Insights accionables: decir qué hacer, no describir el dato
- El script no envía datos externos — todo local

## Requisitos

Python 3.9+, `pip3 install pandas numpy`
