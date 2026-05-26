---
name: ecommerce-bi
description: "Genera informes de Business Intelligence para eCommerce a partir de un CSV de ventas. Auto-detecta plataforma (Tiendanube, Shopify, WooCommerce) y produce 20 (Lite) o 38 (Full) análisis: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded. Usar cuando el usuario mencione 'business intelligence', 'BI', 'análisis de ventas', 'market basket', 'RFM', 'cohortes', 'CLV', 'lifetime value', 'cross-sell', 'basket analysis', 'afinidad de productos', 'análisis ecommerce', 'informe de ventas', 'análisis de clientes'."
---

# eCommerce Business Intelligence Skill

Genera un informe completo de Business Intelligence a partir de un CSV de órdenes de eCommerce. Detecta automáticamente la plataforma, normaliza columnas y corre hasta 38 análisis estructurados en 6 categorías (Producto, Cliente, Revenue, Geográfico, Operativo, Estratégico).

---

## Cuándo usar esta skill

Activar cuando el usuario mencione cualquiera de:

- "business intelligence", "BI", "análisis de ventas"
- "market basket", "basket analysis", "afinidad de productos", "cross-sell"
- "RFM", "segmentación de clientes", "clientes VIP", "churn"
- "CLV", "lifetime value", "valor del cliente"
- "cohortes", "retención", "recompra"
- "informe de ventas", "análisis ecommerce", "diagnóstico de tienda"

Inputs aceptados:

- CSV de exportación de pedidos de **Tiendanube**, **Shopify** o **WooCommerce** (autodetectado).
- CSV genérico si las columnas matchean los nombres canónicos (ver `references/csv_mapping.md`).

---

## Workflow

### Paso 1 — Detectar y validar el CSV

1. Identificar el archivo CSV (path indicado por el usuario o carpeta del cliente).
2. Leer los primeros bytes para detectar encoding (`utf-8` vs `latin-1`) y delimitador (`,` vs `;`).
3. Hacer fingerprint de plataforma comparando headers contra los patrones de `references/csv_mapping.md`:
   - **Tiendanube**: `Número de orden`, `Estado de la orden`, `Nombre del producto`, `Medio de envío`
   - **Shopify**: `Name`, `Financial Status`, `Lineitem name`, `Lineitem quantity`
   - **WooCommerce**: `Order ID`, `Order Status`, `Product Name`, `Order Total`
   - **Genérico**: si no matchea, requiere columnas con los nombres canónicos del mapeo.
4. Confirmar al usuario: plataforma detectada, cantidad de filas, rango de fechas.

### Paso 2 — Elegir modo (AskUserQuestion)

- **Lite** (20 análisis) — los más accionables, ideal para primera revisión. ~30 segundos.
- **Full** (38 análisis) — agrega forecasting, clustering, análisis de variantes y patrones avanzados. ~60-90 segundos.

Default: **Lite**.

### Paso 3 — Ejecutar el script

```bash
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --mode lite \
  --output "/tmp/bi_results.json"
```

El script:

- Auto-detecta encoding, delimitador y plataforma.
- Normaliza nombres de columnas a los canónicos internos.
- Ejecuta los análisis del modo elegido.
- Genera un JSON con `mode`, `platform`, `summary` (métricas hero) y `analyses` (resultado por análisis).
- Cada análisis devuelve `status: "ok"`, `"skipped"` (con razón) o `"error"`.
- Sale con código 0 si terminó, 1 si falló al leer el CSV.

### Paso 4 — Generar el HTML

1. Leer el JSON de resultados.
2. Tomar `references/html_template.md` como base.
3. Armar el informe siguiendo el orden:
   - **Header**: nombre del negocio, rango de fechas, modo badge (LITE/FULL), métricas hero (revenue, órdenes, clientes únicos, ticket promedio).
   - **Secciones por categoría**: Producto → Cliente → Revenue → Geográfico → Operativo → Estratégico.
   - **Cada análisis**: título, tabla/chart, insight, recomendación accionable.
   - **Footer**: branding propio del template.
4. Guardar el HTML en el path indicado por el usuario o sugerir uno.

---

## Catálogo de análisis

Cada análisis devuelve un bloque JSON con `status` + `data` + `insight_template`. Si faltan columnas requeridas, el análisis se marca `skipped` con el motivo y el HTML lo omite.

### Lite — 20 análisis

#### Producto

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 1 | **Market Basket Analysis** | Qué productos se compran juntos. Pares y tríos con support, confidence y lift. | `order_id`, `product_name` |
| 2 | **Afinidad entre categorías** | Qué categorías se combinan en la misma orden. | `order_id`, `product_name` |
| 3 | **Ranking de productos** | Top productos por revenue, unidades y tendencia (últimos 3M vs anteriores 3M). | `product_name`, `product_price`, `product_qty`, `date` |
| 4 | **Productos ancla** | Productos que más aparecen en órdenes multi-producto (drivers de cross-sell). | `order_id`, `product_name` |
| 5 | **Long tail 80/20** | Concentración Pareto: cuántos SKUs hacen el 80% del revenue. | `product_name`, `product_price`, `product_qty` |
| 6 | **Cancelaciones por producto** | Productos con tasa de cancelación más alta que la media. | `product_name`, `order_status` |

#### Cliente

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 7 | **Segmentación RFM** | Clasifica clientes en 11 segmentos: Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost. | `email`, `date`, `total` |
| 8 | **Customer Lifetime Value** | CLV estimado a 3 años por cliente y cuartiles. | `email`, `date`, `total` |
| 9 | **Cohortes de retención** | Matriz mensual de retención (última 12 cohortes × 12 meses). | `email`, `date` |
| 10 | **Tasa de recompra** | % de clientes que vuelven a comprar y tiempo medio entre compras. | `email`, `date` |

#### Revenue

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 11 | **Evolución mensual** | Serie mensual de revenue, órdenes y ticket. Tendencia y picos. | `date`, `total` |
| 12 | **Ticket promedio** | AOV global, por mes y distribución por tramo. | `total` |
| 13 | **Revenue por categoría** | Mix de revenue por categoría (extraída de `product_name`). | `product_name`, `product_price`, `product_qty` |
| 14 | **Impacto de descuentos** | AOV con vs sin cupón, % de órdenes con descuento, descuento medio. | `total`, `discount`, `coupon` |

#### Geográfico

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 15 | **Heatmap por provincia** | Revenue, órdenes y AOV por provincia. | `state`, `total` |
| 16 | **Costo de envío vs conversión** | Distribución de shipping cost por tramo y su correlación con cancelación. | `shipping_cost`, `order_status` |

#### Operativo

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 17 | **Tasa de cancelación** | % global de canceladas, top motivos, evolución mensual. | `order_status` |
| 18 | **Mix de medios de pago** | Distribución de órdenes y revenue por medio de pago. | `payment_method`, `total` |

#### Estratégico

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 19 | **Oportunidades de bundling** | Combinaciones con alto lift candidatas a bundle/pack. | `order_id`, `product_name`, `product_price` |
| 20 | **Estacionalidad** | Picos semanales/mensuales y patrones por día de semana. | `date`, `total` |

### Full — agrega 18 análisis más

#### Producto

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 21 | **Afinidad de colores** | Color combos preferidos (parseo de `product_name`). | `order_id`, `product_name` |
| 22 | **Afinidad de talles** | Combos de talles en la misma orden. | `order_id`, `product_name` |
| 23 | **Análisis de SKU/variantes** | Performance por variante (color/talle/etc). | `sku`, `product_name`, `product_qty` |
| 24 | **Ciclo de vida del producto** | Identifica productos emergentes, en madurez y decaying. | `product_name`, `product_qty`, `date` |

#### Cliente

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 25 | **Patrón de upgrade** | Si los clientes aumentan AOV en compras sucesivas. | `email`, `date`, `total` |
| 26 | **Clientes VIP (top 10%)** | Perfil del top 10% por revenue: AOV, frecuencia, productos preferidos. | `email`, `total`, `product_name` |
| 27 | **Análisis de churn** | Clientes que dejaron de comprar y su valor histórico. | `email`, `date`, `total` |

#### Revenue

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 28 | **Revenue por canal** | Mix de revenue por canal de venta (web/POS/mobile). | `channel`, `total` |
| 29 | **Análisis de precio** | Histograma de precios y elasticidad por tramo. | `product_price`, `product_qty` |

#### Geográfico

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 30 | **Penetración por ciudad** | Top ciudades por revenue y AOV. | `city`, `total` |
| 31 | **Medio de envío por zona** | Mix de shipping methods por provincia. | `state`, `shipping_method` |

#### Operativo

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 32 | **Tiempo de fulfillment** | Días entre orden y despacho, distribución y outliers. | `date`, `shipping_date` |
| 33 | **Análisis de canal** | Comparativa de canales en AOV, cancelación y mix. | `channel`, `total`, `order_status` |
| 34 | **Eficiencia de envío gratis** | AOV y conversión con vs sin envío gratis. | `shipping_cost`, `total` |

#### Estratégico

| # | Análisis | Qué responde | Necesita |
|---|----------|-------------|----------|
| 35 | **Forecast de ventas** | Proyección de revenue 3 meses con ajuste estacional. | `date`, `total` |
| 36 | **Recomendaciones de cross-sell** | Para cada producto top, qué otro recomendar. | `order_id`, `product_name` |
| 37 | **Análisis de pricing** | Productos sobre/sub-precio vs su categoría. | `product_name`, `product_price` |
| 38 | **Identificación de nichos** | Segmentos de productos con alta afinidad y bajo overlap. | `order_id`, `product_name` |

Detalle metodológico completo de cada uno en `references/analysis_catalog.md`.

---

## Reglas

- **SIEMPRE** correr `bi_analysis.py` — no calcular análisis manualmente. El script ya maneja todas las plataformas y normaliza columnas.
- Si un análisis falla por columnas faltantes, queda `status: "skipped"` con el motivo. **Mostrarlo en el HTML** como nota al pie de la sección, no ocultarlo.
- **Market Basket**: solo mostrar asociaciones con `support > 1%` y `lift > 1.0`. Por debajo es ruido.
- **RFM**: usar los 11 labels estándar (Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost).
- **Cohortes**: limitar a últimas 12 cohortes × 12 meses para legibilidad.
- **Insights accionables**: no describir el dato (eso ya está en la tabla). Decir qué hacer con él (acción concreta).
- **Privacidad**: el script no envía datos a ningún servicio externo. Todo corre local.

---

## Estructura

```
ecommerce-bi/
├── SKILL.md                          ← Este archivo
├── scripts/
│   └── bi_analysis.py                ← Script principal (Python 3 + pandas)
├── references/
│   ├── analysis_catalog.md           ← Metodología detallada (38 análisis)
│   ├── csv_mapping.md                ← Mapeo de columnas por plataforma
│   ├── html_template.md              ← Template HTML del informe
│   └── required_columns.md           ← Tabla cruzada: qué columnas necesita cada análisis
└── examples/
    ├── sample_orders.csv             ← CSV de prueba (~80 órdenes sintéticas)
    └── sample_report.html            ← HTML de ejemplo generado con el sample
```

## Requisitos

- Python 3.9 o superior
- `pandas` y `numpy` (`pip3 install pandas numpy`)

## Instalación como skill de Claude Code

```bash
# Clonar el repo
git clone https://github.com/mathiaschu/ecommerce-bi.git ~/.claude/skills/ecommerce-bi

# O symlinkear desde donde lo tengas
ln -s "$(pwd)/ecommerce-bi" ~/.claude/skills/ecommerce-bi
```

Reiniciar Claude Code y pedirle "hace un análisis de BI sobre `ordenes.csv`".
