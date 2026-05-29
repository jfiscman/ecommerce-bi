---
name: ecommerce-bi
description: "Business Intelligence para eCommerce — 39 análisis desde un CSV de ventas. Auto-detecta Tiendanube, Shopify, WooCommerce. Market Basket, RFM, cohortes, CLV, cross-sell, churn y más."
version: 2.0.0
author: Mathias Chu
license: MIT
tags:
  - ecommerce
  - business-intelligence
  - bi
  - rfm
  - market-basket
  - cohortes
  - clv
  - cross-sell
  - churn
  - tiendanube
  - shopify
  - woocommerce
  - analytics
  - csv
  - pandas
---

<!--
  HERMES AGENT SKILL
  Install: hermes skills install ecommerce-bi --from .
  Reference docs in references/ are loaded automatically.
-->

# eCommerce Business Intelligence Skill

Genera informes de Business Intelligence a partir de un CSV de órdenes de eCommerce. Detecta automáticamente la plataforma, normaliza columnas y corre desde **un análisis individual** hasta **39 análisis completos**, en 6 categorías (Producto, Cliente, Revenue, Geográfico, Operativo, Estratégico).

Puede correr en tres modos: **Lite** (21 análisis core), **Full** (39 análisis completos) o **Individual** (uno o varios análisis específicos).

## Plataformas Soportadas

| Plataforma | Detección | Encoding | Delimitador |
|---|---|---|---|
| **Tiendanube** | Por headers | `latin-1` | `;` |
| **Shopify** | Por headers | `utf-8` | `,` |
| **WooCommerce** | Por headers | `utf-8` | `,` |
| **Genérico** | Si las columnas matchean | Autodetectado | Autodetectado |

Mapeo completo: `references/csv_mapping.md`.

## Referencias

Cargar estos documentos de referencia antes de ejecutar cualquier análisis:

1. `references/analysis_catalog.md` — Metodología detallada de los 39 análisis (más de 1000 líneas)
2. `references/csv_mapping.md` — Mapeo de columnas por plataforma (Tiendanube, Shopify, WooCommerce)
3. `references/html_template.md` — Template HTML del informe
4. `references/required_columns.md` — Tabla cruzada: columnas requeridas por análisis

## Análisis Disponibles (39)

| # | Análisis | Modo | Necesita |
|---|----------|------|----------|
| 1 | Market Basket Analysis | Lite | `order_id`, `product_name` |
| 2 | Afinidad entre categorías | Lite | `order_id`, `product_name` |
| 3 | Ranking de productos | Lite | `product_name`, `product_price`, `product_qty`, `date` |
| 4 | Productos ancla (gateway carrito) | Lite | `order_id`, `product_name` |
| 5 | Long tail 80/20 | Lite | `product_name`, `product_price`, `product_qty` |
| 6 | Productos con alta cancelación | Lite | `product_name`, `order_status` |
| 7 | Segmentación RFM | Lite | `email`, `date`, `total` |
| 8 | Customer Lifetime Value (CLV) | Lite | `email`, `date`, `total` |
| 9 | Análisis de cohortes (retención) | Lite | `email`, `date` |
| 10 | Tasa de recompra | Lite | `email`, `date` |
| 11 | Evolución mensual de revenue | Lite | `date`, `total` |
| 12 | Ticket promedio (AOV) | Lite | `total` |
| 13 | Revenue por categoría | Lite | `product_name`, `product_price`, `product_qty` |
| 14 | Impacto de descuentos | Lite | `total`, `discount` |
| 15 | Heatmap por provincia | Lite | `state`, `total` |
| 16 | Costo de envío vs conversión | Lite | `shipping_cost`, `order_status` |
| 17 | Tasa de cancelación | Lite | `order_status` |
| 18 | Mix de medios de pago | Lite | `payment_method`, `total` |
| 19 | Oportunidades de bundling | Lite | `order_id`, `product_name`, `product_price` |
| 20 | Estacionalidad | Lite | `date`, `total` |
| 21+ | 18 análisis avanzados | Full | Varias columnas |

## Modos de Ejecución

### Modo Lite (default) — 21 análisis, ~30s

```bash
python3 scripts/bi_analysis.py --csv "ordenes.csv" --mode lite --output /tmp/bi_results.json
```

### Modo Full — 39 análisis, ~60-90s

```bash
python3 scripts/bi_analysis.py --csv "ordenes.csv" --mode full --output /tmp/bi_results.json
```

### Modo Individual — análisis específicos

```bash
# Listar análisis disponibles
python3 scripts/bi_analysis.py --list

# Uno solo (RFM)
python3 scripts/bi_analysis.py --csv "ordenes.csv" --analysis 7 --output /tmp/bi_results.json

# Varios
python3 scripts/bi_analysis.py --csv "ordenes.csv" --analysis 1,4,7,9 --output /tmp/bi_results.json
```

## Workflow

### Paso 1 — Detectar y validar el CSV

1. Identificar el archivo CSV (path indicado por el usuario).
2. Detectar encoding (`utf-8` vs `latin-1`) y delimitador (`,` vs `;`).
3. Fingerprint de plataforma comparando headers contra patrones en `references/csv_mapping.md`.
4. Confirmar al usuario: plataforma detectada, cantidad de filas, rango de fechas.

### Paso 2 — Determinar modo

Preguntar al usuario:
- **Lite** (21 análisis) — informe completo de primera vista.
- **Full** (39 análisis) — deep dive.
- **Individual** — análisis específicos por nombre o ID.

### Paso 3 — Ejecutar el script

Correr `python3 scripts/bi_analysis.py` con los argumentos apropiados.

### Paso 4 — Generar el HTML

1. Leer el JSON de resultados.
2. Tomar `references/html_template.md` como base.
3. Armar el informe con header, secciones por categoría, tabla/chart por análisis, insight y recomendación.
4. Guardar el HTML.

## Reglas

- **SIEMPRE** correr `bi_analysis.py` — no calcular análisis manualmente.
- Si un análisis falla por columnas faltantes, queda `status: "skipped"` con el motivo. **Mostrarlo en el HTML.**
- **Market Basket**: solo mostrar asociaciones con `support > 1%` y `lift > 1.0`.
- **RFM**: usar los 11 labels estándar (Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost).
- **Cohortes**: limitar a últimas 12 cohortes × 12 meses.
- **Insights accionables**: no describir el dato — decir qué hacer con él.
- **Privacidad**: el script no envía datos externos. Todo corre local.

## Requisitos

- Python 3.9+
- `pip3 install pandas numpy`

## Ejemplo incluido

```bash
python3 scripts/bi_analysis.py \
  --csv examples/sample_orders.csv \
  --mode lite \
  --output examples/sample_results.json

python3 examples/generate_sample_html.py
```

Resultado: `examples/sample_report.html`.
