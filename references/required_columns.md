# Columnas requeridas por análisis

Tabla cruzada de qué columnas canónicas necesita cada análisis. Si una columna falta, el análisis devuelve `status: "skipped"` con la razón y el HTML omite la sección.

Los nombres son los **canónicos internos** del script. El mapeo desde cada plataforma a los canónicos está en [`csv_mapping.md`](csv_mapping.md).

---

## Resumen rápido

**Lo mínimo para que la skill devuelva algo útil**:

- `order_id`, `date`, `total`, `product_name` → habilita ~70% de los análisis.
- Sumá `email` → desbloquea todos los análisis de cliente (RFM, CLV, cohortes, churn).
- Sumá `state` o `city` → desbloquea geográfico.
- Sumá `shipping_cost`, `shipping_date`, `shipping_method` → desbloquea operativo/logística.

---

## Tabla por análisis

| # | Análisis | Columnas requeridas | Si falta… |
|---|----------|--------------------|----------|
| 1 | Market Basket | `order_id`, `product_name` | Skip |
| 2 | Afinidad categorías | `order_id`, `product_name` | Skip |
| 3 | Ranking productos | `product_name`, `product_price`, `product_qty`, `date` | Skip si falta `product_name`; si falta `date` se omite la tendencia |
| 4 | Productos ancla | `order_id`, `product_name` | Skip |
| 5 | Long tail 80/20 | `product_name`, `product_price`, `product_qty` | Skip |
| 6 | Cancelaciones por producto | `product_name`, `order_status` | Skip |
| 7 | RFM | `email`, `date`, `total` | Skip |
| 8 | CLV | `email`, `date`, `total` | Skip |
| 9 | Cohortes | `email`, `date` | Skip |
| 10 | Tasa de recompra | `email`, `date` | Skip |
| 11 | Evolución mensual | `date`, `total` | Skip |
| 12 | Ticket promedio | `total` | Skip |
| 13 | Revenue por categoría | `product_name`, `product_price`, `product_qty` | Skip |
| 14 | Impacto de descuentos | `total`, `discount` | Skip si faltan ambas; si falta `coupon` solo se reporta % con descuento |
| 15 | Heatmap provincia | `state`, `total` | Skip |
| 16 | Envío vs conversión | `shipping_cost`, `order_status` | Skip |
| 17 | Tasa de cancelación | `order_status` | Skip |
| 18 | Mix medios de pago | `payment_method`, `total` | Skip |
| 19 | Bundling | `order_id`, `product_name`, `product_price` | Skip |
| 20 | Estacionalidad | `date`, `total` | Skip |
| 21 | Afinidad colores | `order_id`, `product_name` | Skip si no detecta colores en `product_name` |
| 22 | Afinidad talles | `order_id`, `product_name` | Skip si no detecta talles |
| 23 | SKU/variantes | `sku`, `product_name`, `product_qty` | Skip si falta `sku` |
| 24 | Ciclo de vida producto | `product_name`, `product_qty`, `date` | Skip |
| 25 | Patrón de upgrade | `email`, `date`, `total` | Skip |
| 26 | Clientes VIP | `email`, `total`, `product_name` | Skip si falta `email` o `total` |
| 27 | Churn | `email`, `date`, `total` | Skip; necesita ≥6 meses de histórico |
| 28 | Revenue por canal | `channel`, `total` | Skip |
| 29 | Análisis de precio | `product_price`, `product_qty` | Skip |
| 30 | Penetración por ciudad | `city`, `total` | Skip |
| 31 | Medio de envío por zona | `state`, `shipping_method` | Skip |
| 32 | Tiempo de fulfillment | `date`, `shipping_date` | Skip |
| 33 | Análisis de canal | `channel`, `total`, `order_status` | Skip |
| 34 | Envío gratis | `shipping_cost`, `total` | Skip |
| 35 | Forecast | `date`, `total` | Skip si <3 meses de datos |
| 36 | Cross-sell | `order_id`, `product_name` | Skip |
| 37 | Pricing | `product_name`, `product_price` | Skip |
| 38 | Nichos | `order_id`, `product_name` | Skip |
| 39 | Producto gateway de retención | `email`, `date`, `product_name` | Skip si falta cualquiera o si hay &lt;5 clientes únicos |

---

## Columnas opcionales que enriquecen sin ser bloqueantes

| Columna | Análisis que mejora |
|---------|---------------------|
| `payment_status` | Permite filtrar órdenes pagas vs pendientes en todos los análisis de revenue |
| `cancellation_reason` | Análisis #17 muestra top motivos de cancelación |
| `cancellation_date` | Análisis #17 permite ver tiempo entre orden y cancelación |
| `currency` | Si hay múltiples monedas, el script avisa y usa la modal |
| `zip_code` | Reserved para análisis futuro de penetración fina |
| `customer_name`, `phone` | Reserved para outputs de identificación de VIPs |

---

## Cómo testear si tu CSV tiene lo necesario

```bash
python3 scripts/bi_analysis.py --csv tu_archivo.csv --mode lite --output /tmp/check.json
```

Después, contar análisis con `status: ok` vs `skipped`:

```bash
python3 -c "import json; r = json.load(open('/tmp/check.json')); a = r['analyses']; ok = sum(1 for x in a.values() if x['data'].get('status') == 'ok'); sk = sum(1 for x in a.values() if x['data'].get('status') == 'skipped'); print(f'OK: {ok} | Skipped: {sk}')"
```

Si tenés más de 5 skipped en modo Lite, revisá el mapeo de columnas de tu CSV.
