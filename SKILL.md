---
name: ecommerce-bi
description: "Genera informes de Business Intelligence para eCommerce a partir de un CSV de ventas. Auto-detecta plataforma (Tiendanube, Shopify, WooCommerce) y produce 20 (Lite), 38 (Full) o análisis individuales: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded. Usar cuando el usuario mencione 'business intelligence', 'BI', 'análisis de ventas', 'market basket', 'RFM', 'cohortes', 'CLV', 'lifetime value', 'cross-sell', 'basket analysis', 'afinidad de productos', 'análisis ecommerce', 'informe de ventas', 'análisis de clientes'."
---

# eCommerce Business Intelligence Skill

Genera informes de Business Intelligence a partir de un CSV de órdenes de eCommerce. Detecta automáticamente la plataforma, normaliza columnas y corre desde **un análisis individual** hasta **38 análisis completos**, en 6 categorías (Producto, Cliente, Revenue, Geográfico, Operativo, Estratégico).

Puede correr en tres modos: **Lite** (20 análisis core), **Full** (38 análisis completos) o **Individual** (uno o varios análisis específicos).

---

## Análisis disponibles

Los 38 análisis que puede generar la skill, ordenados de mayor a menor impacto típico al negocio. Cada uno se puede correr individualmente o como parte de los modos Lite / Full.

Formato de cada bloque:
- **Qué hace**: la mecánica.
- **Para qué sirve**: la decisión que habilita.
- **Necesita**: columnas mínimas en el CSV.
- **ID + modo**: el ID interno del script (para `--analysis N`) y en qué modos aparece.

---

### 1. Segmentación RFM
- **Qué hace**: clasifica a cada cliente en uno de 11 segmentos según Recency (cuándo compró por última vez), Frequency (cuántas veces) y Monetary (cuánto gastó). Segmentos: Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost.
- **Para qué sirve**: es la base de toda estrategia de CRM y email. A quién mimar (Champions, Loyal), a quién reactivar (At Risk, About to Sleep), a quién dar bienvenida (New) y a quién dejar de gastar pauta (Lost). Sin RFM, mandás los mismos mails a todo el mundo.
- **Necesita**: `email`, `date`, `total`
- **ID interno**: #7 · Lite + Full

### 2. Ranking de productos
- **Qué hace**: ordena el catálogo por revenue, unidades vendidas y tendencia (últimos 3 meses vs 3 anteriores). Identifica héroes y estrellas emergentes.
- **Para qué sirve**: te dice qué *es* tu negocio. De acá salen las decisiones de qué destacar en home, qué pautar, qué reabastecer prioritariamente y dónde concentrar el esfuerzo creativo.
- **Necesita**: `product_name`, `product_price`, `product_qty`, `date`
- **ID interno**: #3 · Lite + Full

### 3. Análisis de cohortes (retención)
- **Qué hace**: matriz mensual de retención (últimas 12 cohortes × 12 meses). Para cada grupo de clientes adquiridos en un mes, qué porcentaje sigue comprando 1, 2, 3 meses después.
- **Para qué sirve**: te dice si el negocio realmente *funciona*. Si la retención cae a cero al M1, cada cliente nuevo es un gasto. Si la cohorte nueva retiene peor que la vieja, algo se está rompiendo.
- **Necesita**: `email`, `date`
- **ID interno**: #9 · Lite + Full

### 4. Customer Lifetime Value (CLV)
- **Qué hace**: estima el CLV a 3 años por cliente (AOV × frecuencia × lifespan). Reporta promedio, mediana, cuartiles y top 10.
- **Para qué sirve**: establece tu techo de CAC. Si un cliente vale $100 en 3 años, no podés pagar $80 para adquirirlo. Define cuánto invertir en pauta, descuentos y retención.
- **Necesita**: `email`, `date`, `total`
- **ID interno**: #8 · Lite + Full

### 5. Evolución mensual de revenue
- **Qué hace**: serie mensual de revenue, órdenes y AOV. Calcula tendencia y detecta picos/valles.
- **Para qué sirve**: es la línea de base. Toda lectura de las demás métricas se contextualiza contra esta tendencia.
- **Necesita**: `date`, `total`
- **ID interno**: #11 · Lite + Full

### 6. Tasa de recompra
- **Qué hace**: porcentaje de clientes que compraron más de una vez y tiempo medio entre compras (mediana y promedio).
- **Para qué sirve**: health metric esencial. Si la recompra es &lt;20%, sos un negocio de adquisición pura. Si es &gt;40%, podés invertir más en retención. La mediana entre compras le da el ritmo a tus automations.
- **Necesita**: `email`, `date`
- **ID interno**: #10 · Lite + Full

### 7. Productos ancla (gateway products)
- **Qué hace**: identifica los productos que más aparecen en órdenes multi-producto. Para cada ancla, lista los 5 co-productos más frecuentes.
- **Para qué sirve**: son tus productos gateway, los que abren la primera compra y arrastran al carrito otros. Exhibirlos primero acelera el AOV. También: invertir pauta en ellos rinde doble porque traen acompañantes.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #4 · Lite + Full

### 8. Market Basket Analysis
- **Qué hace**: identifica qué productos se compran juntos. Calcula pares y tríos con support (frecuencia), confidence (probabilidad condicional) y lift (cuánto más probable que por azar).
- **Para qué sirve**: cross-sell directo, bundles, recomendaciones en PDP, módulos "compraron junto" en checkout, lógica de upsell por email. Cualquier combo con lift &gt; 2 es una oportunidad de revenue incremental.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #1 · Lite + Full

### 9. Oportunidades de bundling
- **Qué hace**: filtra los combos del Market Basket con mejor lift y propone bundles concretos con precio combinado.
- **Para qué sirve**: cierra el bucle del análisis en una acción concreta. "Armá este bundle con 10% off" en vez de "estos se compran juntos".
- **Necesita**: `order_id`, `product_name`, `product_price`
- **ID interno**: #19 · Lite + Full

### 10. Clientes VIP (top 10%)
- **Qué hace**: identifica el top 10% de clientes por revenue. Reporta su AOV, frecuencia, productos preferidos y mes de adquisición.
- **Para qué sirve**: el VIP suele hacer 40-60% del revenue total. Saber quiénes son habilita programas VIP, ofertas tempranas, acceso anticipado y customer service diferenciado.
- **Necesita**: `email`, `total`, `product_name`
- **ID interno**: #26 · Full only

### 11. Análisis de churn
- **Qué hace**: identifica clientes que dejaron de comprar (sin actividad por más del doble de su intervalo medio). Reporta cuáles, su valor histórico y los últimos productos comprados antes del churn.
- **Para qué sirve**: detección temprana de fuga. Los últimos productos comprados antes del churn muchas veces revelan problemas de calidad o experiencia. Habilita campañas de reactivación con oferta dirigida.
- **Necesita**: `email`, `date`, `total` (idealmente ≥6 meses de histórico)
- **ID interno**: #27 · Full only

### 12. Estacionalidad
- **Qué hace**: detecta picos y valles por mes y por día de la semana. Identifica mes pico, mes valle y día más fuerte.
- **Para qué sirve**: planificación anual de pauta y stock. Cuándo apretar el acelerador, cuándo soltar, cuándo programar lanzamientos. Rotar contenido orgánico según día de mayor tráfico.
- **Necesita**: `date`, `total`
- **ID interno**: #20 · Lite + Full

### 13. Long tail 80/20
- **Qué hace**: cuántos SKUs hacen el 80% del revenue. Distribución Pareto del catálogo.
- **Para qué sirve**: decisiones de stock e inversión. Si el 10% de los SKUs hace el 80%, el resto puede ser candidato a descatalogar, liquidar o pasar a print-on-demand.
- **Necesita**: `product_name`, `product_price`, `product_qty`
- **ID interno**: #5 · Lite + Full

### 14. Ticket promedio (AOV)
- **Qué hace**: AOV global, AOV mediano, distribución por tramo y evolución mensual. Compara AOV de clientes nuevos vs recurrentes.
- **Para qué sirve**: KPI core de cualquier optimización (bundles, free-shipping threshold, descuentos por volumen). Si AOV mediano &lt;&lt; AOV promedio, hay outliers que distorsionan: limpiar antes de tomar decisiones.
- **Necesita**: `total`
- **ID interno**: #12 · Lite + Full

### 15. Revenue por categoría
- **Qué hace**: mix de revenue por categoría (extraída del nombre del producto). Top N categorías + % de mix.
- **Para qué sirve**: balance del catálogo. Si una categoría concentra 70%, hay riesgo de dependencia. Si todas reparten parejo, oportunidad de empujar una para crecer.
- **Necesita**: `product_name`, `product_price`, `product_qty`
- **ID interno**: #13 · Lite + Full

### 16. Impacto de descuentos
- **Qué hace**: AOV con cupón vs sin cupón, % de órdenes con descuento, top cupones usados, monto total descontado.
- **Para qué sirve**: medir si el descuento *agrega* valor o *canibaliza* margen. Si el AOV con cupón es igual o menor al sin cupón, regalás margen sin contrapartida. Si es mayor, el cupón está sirviendo.
- **Necesita**: `total`, `discount` (idealmente `coupon`)
- **ID interno**: #14 · Lite + Full

### 17. Afinidad entre categorías
- **Qué hace**: market basket pero a nivel categoría: qué categorías se combinan en la misma orden.
- **Para qué sirve**: cross-merchandising en home y landings. Categorías afines son material para colecciones combinadas, carruseles "outfit completo" y diseño de navegación.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #2 · Lite + Full

### 18. Recomendaciones de cross-sell
- **Qué hace**: para cada producto top, qué otro recomendar (basado en lift y co-ocurrencia).
- **Para qué sirve**: tabla lista para alimentar el motor de recomendaciones del store. "Si compraste X, te recomendamos Y" derivado del dato real, no de heurísticas genéricas.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #36 · Full only

### 19. Análisis de pricing
- **Qué hace**: identifica productos sobre-precio o sub-precio comparados con el promedio de su categoría.
- **Para qué sirve**: detecta candidatos a ajuste de precio. Cada producto fuera de rango es una conversación pendiente con catálogo o con el proveedor.
- **Necesita**: `product_name`, `product_price`
- **ID interno**: #37 · Full only

### 20. Análisis de precio (distribución)
- **Qué hace**: histograma de precios y unidades vendidas por tramo. Identifica price points con mejor performance.
- **Para qué sirve**: encontrar el sweet spot del catálogo. Muchas veces el 80% de las ventas se concentra en un rango estrecho; saberlo guía la curaduría de futuras incorporaciones.
- **Necesita**: `product_price`, `product_qty`
- **ID interno**: #29 · Full only

### 21. Heatmap por provincia
- **Qué hace**: revenue, órdenes y AOV por provincia/estado.
- **Para qué sirve**: decisiones de pauta geo, negociación de tarifas de envío en zonas con volumen, y detección de provincias con AOV alto y pocos pedidos (ventana de crecimiento).
- **Necesita**: `state`, `total`
- **ID interno**: #15 · Lite + Full

### 22. Costo de envío vs conversión
- **Qué hace**: distribución del costo de envío por tramo y correlación con cancelación.
- **Para qué sirve**: el envío es uno de los principales drivers de abandono. Si la tasa de cancelación se dispara cuando el envío supera $X, ese es tu umbral psicológico y tu palanca para el threshold de envío gratis.
- **Necesita**: `shipping_cost`, `order_status`
- **ID interno**: #16 · Lite + Full

### 23. Penetración por ciudad
- **Qué hace**: top ciudades por revenue, AOV y órdenes (granularidad más fina que provincia).
- **Para qué sirve**: pauta geográfica fina, decisiones de cobertura (¿abrir un punto físico o pickup?), patrones de concentración urbana.
- **Necesita**: `city`, `total`
- **ID interno**: #30 · Full only

### 24. Eficiencia de envío gratis
- **Qué hace**: compara AOV y conversión de órdenes con envío gratis vs con envío pago.
- **Para qué sirve**: evaluar la política de envío gratis. Si el AOV gratis es solo poco mayor al threshold, el regalo no empuja AOV: bajar el threshold o eliminar la promo. Si es muy mayor, vale la pena bajarlo para empujar más.
- **Necesita**: `shipping_cost`, `total`
- **ID interno**: #34 · Full only

### 25. Tiempo de fulfillment
- **Qué hace**: días entre orden y despacho. Distribución, mediana y outliers.
- **Para qué sirve**: SLA operativo. Si la mediana sube mes a mes, hay un problema de logística por venir. Outliers (&gt;10 días) son los que generan tickets de soporte y reviews negativas.
- **Necesita**: `date`, `shipping_date`
- **ID interno**: #32 · Full only

### 26. Tasa de cancelación
- **Qué hace**: % global de canceladas, top motivos de cancelación, evolución mensual, mix por medio de pago.
- **Para qué sirve**: health metric operativo. Tendencia ascendente = problema (stock, pricing, expectativa). Los motivos te dicen dónde está la fuga.
- **Necesita**: `order_status`
- **ID interno**: #17 · Lite + Full

### 27. Productos con alta cancelación
- **Qué hace**: identifica productos con tasa de cancelación significativamente sobre la media.
- **Para qué sirve**: detectar productos problemáticos (calidad, stock, expectativa vs realidad). Cada uno es una conversación con catálogo o el proveedor.
- **Necesita**: `product_name`, `order_status`
- **ID interno**: #6 · Lite + Full

### 28. Mix de medios de pago
- **Qué hace**: distribución de órdenes y revenue por medio de pago (MP, tarjeta, transferencia, etc.).
- **Para qué sirve**: optimizar comisiones y checkout. Si una procesadora concentra mucho con comisión alta, hay negociación pendiente. Si un medio tiene AOV mayor, empujarlo con descuento.
- **Necesita**: `payment_method`, `total`
- **ID interno**: #18 · Lite + Full

### 29. Medio de envío por zona
- **Qué hace**: mix de shipping methods por provincia.
- **Para qué sirve**: detectar dónde la oferta de envíos está incompleta. Si en una provincia solo hay un courier y la conversión cae, es señal para sumar otro.
- **Necesita**: `state`, `shipping_method`
- **ID interno**: #31 · Full only

### 30. Forecast de ventas
- **Qué hace**: proyección de revenue a 3 meses con ajuste estacional (mínimo 6 meses de histórico).
- **Para qué sirve**: planificación financiera, presupuestos, cash flow, decisiones de stock para temporada alta.
- **Necesita**: `date`, `total`
- **ID interno**: #35 · Full only

### 31. Identificación de nichos
- **Qué hace**: clusters de productos con alta afinidad interna y bajo overlap entre sí.
- **Para qué sirve**: detectar sub-marcas o líneas implícitas dentro del catálogo. Habilita decisiones de marca paraguas, landings por nicho y curaduría editorial.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #38 · Full only

### 32. Patrón de upgrade
- **Qué hace**: detecta si los clientes aumentan su AOV en compras sucesivas.
- **Para qué sirve**: si el AOV crece, el storytelling de marca funciona y se puede empujar premium. Si no crece, el techo de cada cliente es el AOV de la primera compra.
- **Necesita**: `email`, `date`, `total`
- **ID interno**: #25 · Full only

### 33. Análisis de SKU/variantes
- **Qué hace**: performance por variante (color, talle, SKU). Detecta variantes muertas y heroínas.
- **Para qué sirve**: stock fino. Discontinuar variantes que no rotan, reforzar las heroínas. Diferencia entre "este producto vende" y "este producto vende solo en talle M negro".
- **Necesita**: `sku`, `product_name`, `product_qty`
- **ID interno**: #23 · Full only

### 34. Ciclo de vida del producto
- **Qué hace**: clasifica productos en emergente, madurez o declive según evolución de unidades.
- **Para qué sirve**: lifecycle management. Promover emergentes, exprimir maduros, liquidar declive antes de que generen stock muerto.
- **Necesita**: `product_name`, `product_qty`, `date`
- **ID interno**: #24 · Full only

### 35. Revenue por canal
- **Qué hace**: distribución de revenue por canal (web, mobile, POS).
- **Para qué sirve**: priorizar inversión en UX por canal. Si mobile concentra órdenes pero el AOV baja, hay friction en el checkout mobile.
- **Necesita**: `channel`, `total`
- **ID interno**: #28 · Full only

### 36. Análisis de canal (profundo)
- **Qué hace**: comparativa profunda por canal — AOV, tasa de cancelación, mix de productos.
- **Para qué sirve**: detectar diferencias de comportamiento que no son obvias. POS puede tener AOV alto pero alta devolución; mobile bajo AOV pero alta repetición.
- **Necesita**: `channel`, `total`, `order_status`
- **ID interno**: #33 · Full only

### 37. Afinidad entre colores
- **Qué hace**: combos de colores comprados juntos (parsea el nombre del producto buscando colores conocidos).
- **Para qué sirve**: merchandising fino. Qué colores se llevan en outfits, qué paletas funcionan, qué nuevos colores agregar al próximo drop.
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #21 · Full only

### 38. Afinidad entre talles
- **Qué hace**: combos de talles en la misma orden.
- **Para qué sirve**: stock por talle, decisiones de curva de producción, detección de "compra para pareja/familia" (talles muy distintos en la misma orden).
- **Necesita**: `order_id`, `product_name`
- **ID interno**: #22 · Full only

---

## Cuándo usar esta skill

Activar cuando el usuario mencione cualquiera de:

- "business intelligence", "BI", "análisis de ventas"
- "market basket", "basket analysis", "afinidad de productos", "cross-sell"
- "RFM", "segmentación de clientes", "clientes VIP", "churn"
- "CLV", "lifetime value", "valor del cliente"
- "cohortes", "retención", "recompra"
- "informe de ventas", "análisis ecommerce", "diagnóstico de tienda"
- Un análisis puntual: "armame un RFM", "quiero ver el market basket", "necesito un análisis de cohortes"

Inputs aceptados:

- CSV de exportación de pedidos de **Tiendanube**, **Shopify** o **WooCommerce** (autodetectado).
- CSV genérico si las columnas matchean los nombres canónicos (ver `references/csv_mapping.md`).

---

## Modos disponibles

Antes de ejecutar, preguntar al usuario cuál querer con `AskUserQuestion`:

### Modo Lite (20 análisis)

Los 20 análisis core (corresponden a los IDs internos #1 al #20). Default cuando el usuario no especifica. ~30 segundos.

### Modo Full (38 análisis)

Lite + 18 análisis avanzados (forecasting, clustering, variantes, churn detallado, etc.). Para deep dives. ~60-90 segundos.

### Modo Individual

El usuario pide un análisis puntual ("armame un RFM", "solo el market basket"). Esto:

- Es más rápido.
- Genera un HTML focalizado en lo pedido.
- Resuelve dependencias automáticamente (si pedís #19 Bundling, el script corre #1 Market Basket como dependencia interna).

---

## Workflow

### Paso 1 — Detectar y validar el CSV

1. Identificar el archivo CSV (path indicado por el usuario o carpeta del cliente).
2. Detectar encoding (`utf-8` vs `latin-1`) y delimitador (`,` vs `;`).
3. Fingerprint de plataforma comparando headers contra patrones en `references/csv_mapping.md`:
   - **Tiendanube**: `Número de orden`, `Estado de la orden`, `Nombre del producto`, `Medio de envío`
   - **Shopify**: `Name`, `Financial Status`, `Lineitem name`, `Lineitem quantity`
   - **WooCommerce**: `Order ID`, `Order Status`, `Product Name`, `Order Total`
   - **Genérico**: requiere las columnas canónicas del mapeo.
4. Confirmar al usuario: plataforma detectada, cantidad de filas, rango de fechas.

### Paso 2 — Determinar qué correr (AskUserQuestion)

Tres opciones a ofrecer:

- **Lite** (20 análisis) — informe completo de primera vista.
- **Full** (38 análisis) — deep dive.
- **Individual** — el usuario indica cuáles. Si menciona nombres ("RFM y cohortes"), resolver a IDs internos usando el catálogo de arriba (#7 y #9).

### Paso 3 — Ejecutar el script

**Modo Lite o Full:**

```bash
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --mode lite \
  --output "/tmp/bi_results.json"
```

**Modo Individual:**

```bash
# Uno solo
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --analysis 7 \
  --output "/tmp/bi_results.json"

# Varios separados por coma
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --analysis 1,4,7,9 \
  --output "/tmp/bi_results.json"
```

**Listar análisis disponibles:**

```bash
python3 scripts/bi_analysis.py --list
```

El script:

- Auto-detecta encoding, delimitador y plataforma.
- Normaliza nombres de columnas a los canónicos internos.
- Ejecuta los análisis solicitados.
- Resuelve dependencias (Market Basket si pediste Bundling o Cross-sell).
- Genera un JSON con `mode`, `analysis_ids`, `platform`, `summary` y `analyses`.
- Cada análisis devuelve `status: "ok"`, `"skipped"` (con razón) o `"error"`.

### Paso 4 — Generar el HTML

1. Leer el JSON de resultados.
2. Tomar `references/html_template.md` como base.
3. Armar el informe:
   - **Header**: nombre del negocio, rango de fechas, modo badge (LITE/FULL/INDIVIDUAL), métricas hero.
   - **Secciones por categoría**: Producto → Cliente → Revenue → Geográfico → Operativo → Estratégico. Si es modo Individual, agrupar solo las categorías que tienen al menos un análisis.
   - **Cada análisis**: título, tabla/chart, insight, recomendación accionable.
   - **Footer**: branding propio del template.
4. Guardar el HTML en el path indicado por el usuario o sugerir uno.

---

## Reglas

- **SIEMPRE** correr `bi_analysis.py` — no calcular análisis manualmente. El script ya maneja todas las plataformas y normaliza columnas.
- Si un análisis falla por columnas faltantes, queda `status: "skipped"` con el motivo. **Mostrarlo en el HTML** como nota al pie de la sección, no ocultarlo.
- **Market Basket**: solo mostrar asociaciones con `support > 1%` y `lift > 1.0`. Por debajo es ruido.
- **RFM**: usar los 11 labels estándar (Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost).
- **Cohortes**: limitar a últimas 12 cohortes × 12 meses para legibilidad.
- **Modo Individual**: si el usuario menciona análisis por nombre, resolver a IDs internos usando el catálogo de arriba antes de invocar el script.
- **Dependencias**: el script resuelve sola la dependencia de Bundling/Cross-sell con Market Basket — no hace falta agregar #1 manualmente cuando piden #19 o #36.
- **Insights accionables**: no describir el dato (eso ya está en la tabla). Decir qué hacer con él (acción concreta).
- **Privacidad**: el script no envía datos a ningún servicio externo. Todo corre local.

---

## Estructura

```
ecommerce-bi/
├── SKILL.md                          ← Este archivo
├── README.md                         ← Pública del repo
├── LICENSE                           ← MIT
├── CONTRIBUTING.md
├── scripts/
│   └── bi_analysis.py                ← Script principal (Python 3 + pandas)
├── references/
│   ├── analysis_catalog.md           ← Metodología detallada de los 38 análisis
│   ├── csv_mapping.md                ← Mapeo de columnas por plataforma
│   ├── html_template.md              ← Template HTML del informe
│   └── required_columns.md           ← Tabla cruzada: columnas requeridas por análisis
└── examples/
    ├── sample_orders.csv             ← CSV sintético (~80 órdenes)
    ├── sample_results.json           ← Output del script sobre el sample
    ├── sample_report.html            ← HTML branded de ejemplo
    ├── generate_sample.py            ← Genera el CSV sintético
    └── generate_sample_html.py       ← Renderiza JSON → HTML
```

## Requisitos

- Python 3.9 o superior
- `pandas` y `numpy` (`pip3 install pandas numpy`)

## Instalación como skill de Claude Code

```bash
git clone https://github.com/mathiaschu/ecommerce-bi.git ~/.claude/skills/ecommerce-bi
```

Reiniciar Claude Code y pedirle:

- "Hacé un análisis de BI completo sobre `ordenes.csv`" → modo Lite/Full
- "Armame un RFM sobre `ordenes.csv`" → modo Individual
- "Quiero el market basket y la afinidad de categorías" → modo Individual
