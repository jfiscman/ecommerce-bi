# ecommerce-bi

> Multi-platform skill para generar informes de Business Intelligence sobre tu tienda eCommerce a partir de un CSV de ventas.

Apuntá la skill a tu export de Tiendanube, Shopify o WooCommerce y obtené un informe con hasta 39 análisis: Market Basket, RFM, cohortes, CLV, cross-sell, churn, producto gateway de retención, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded.

Podés correrla en tres modos: **Lite** (21 análisis core), **Full** (39 análisis completos) o **Individual** (análisis específicos como RFM o Market Basket + Cohortes).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## Supported Platforms

| Platform | Install Command | Type |
|:---------|:---------------|:-----|
| **Hermes Agent** | `bash scripts/install.sh hermes` | Skill |
| **Claude Code** | `bash scripts/install.sh claude-code` | Skill |
| **Cursor** | `bash scripts/install.sh cursor` | Rules |
| **GitHub Copilot** | `bash scripts/install.sh copilot` | Instructions |
| **OpenCode** | `bash scripts/install.sh opencode` | Skill |
| **Windsurf** | `bash scripts/install.sh windsurf` | Rules |
| **Aider** | `bash scripts/install.sh aider` | Rules |

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/mathiaschu/ecommerce-bi.git
cd ecommerce-bi
pip3 install pandas numpy
bash scripts/install.sh hermes  # or: claude-code, cursor, copilot, etc.
```

### 2. Run (CLI standalone)

```bash
# Lite mode: 21 core analyses
python3 scripts/bi_analysis.py --csv orders.csv --mode lite --output results.json

# Full mode: all 39 analyses
python3 scripts/bi_analysis.py --csv orders.csv --mode full --output results.json

# Single analysis (RFM)
python3 scripts/bi_analysis.py --csv orders.csv --analysis 7 --output results.json

# List available analyses
python3 scripts/bi_analysis.py --list

# Generate HTML report
python3 examples/generate_sample_html.py results.json report.html
```

### 3. Ask your AI

> "Hacé un análisis de BI completo sobre `mi_export_tiendanube.csv`" → Lite/Full
> "Armame un RFM sobre `ordenes.csv`" → Individual
> "Quiero solo el market basket y la afinidad de categorías" → Individual

---

## Plataformas soportadas

| Plataforma | Detección | Encoding | Delimitador |
|---|---|---|---|
| **Tiendanube** | Por headers | `latin-1` | `;` |
| **Shopify** | Por headers | `utf-8` | `,` |
| **WooCommerce** | Por headers | `utf-8` | `,` |
| **Genérico** | Si las columnas matchean | Autodetectado | Autodetectado |

Mapeo completo en [`references/csv_mapping.md`](references/csv_mapping.md).

---

## Top 10 Análisis

1. **Segmentación RFM** — 11 segmentos de clientes (Champions, Loyal, At Risk, Lost...)
2. **Ranking de productos** — Héroes y estrellas emergentes por revenue y tendencia
3. **Análisis de cohortes** — Matriz mensual de retención (¿el negocio funciona?)
4. **Customer Lifetime Value (CLV)** — Techo de CAC a 3 años
5. **Evolución mensual de revenue** — Línea de base contra todo
6. **Tasa de recompra** — Health metric esencial
7. **Producto gateway de retención** — Qué producto captura clientes que *vuelven*
8. **Productos ancla** — Qué abre el carrito y arrastra otros productos
9. **Market Basket Analysis** — Pares y tríos con support, confidence, lift
10. **Oportunidades de bundling** — Combos accionables con precio

[Ver los 39 análisis completos →](references/analysis_catalog.md)

---

## Repository Structure

```
ecommerce-bi/
├── SKILL.md                    ← Platform-agnostic skill definition
├── README.md
├── LICENSE
├── references/                 ← 4 domain docs (shared by all platforms)
│   ├── analysis_catalog.md     ← Methodology for all 39 analyses
│   ├── csv_mapping.md          ← Column mapping per platform
│   ├── html_template.md        ← HTML report template
│   └── required_columns.md     ← Required columns per analysis
├── platforms/                  ← Platform-specific adapters
│   ├── hermes/                 ← Hermes Agent skill
│   ├── claude-code/            ← Claude Code skill
│   ├── cursor/                 ← Cursor rules
│   ├── copilot/                ← GitHub Copilot instructions
│   ├── opencode/               ← OpenCode skill
│   ├── windsurf/               ← Windsurf rules
│   └── aider/                  ← Aider rules
├── scripts/
│   ├── bi_analysis.py          ← Core engine (Python + pandas)
│   └── install.sh              ← Universal installer
└── examples/
    ├── sample_orders.csv       ← Synthetic CSV (~80 orders)
    ├── sample_results.json     ← Script output on sample
    ├── sample_report.html      ← Generated HTML report
    ├── generate_sample.py      ← CSV generator
    └── generate_sample_html.py ← JSON → HTML renderer
```

## Requirements

- Python 3.9+
- `pip3 install pandas numpy`

No cloud services, no API keys, no GPU. Everything runs locally.

## Privacy

- The script does NOT send data to any external service
- No API keys or accounts required
- All processing is local
- `.gitignore` excludes `*_real.csv` and `*_client.csv` by default

## License

MIT — Copyright (c) 2026 Mathias Chu
