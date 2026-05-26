---
name: ecommerce-bi
description: "Genera informes de Business Intelligence para eCommerce a partir de un CSV de ventas. Auto-detecta plataforma (Tiendanube, Shopify, WooCommerce) y produce 20 (Lite), 38 (Full) o análisis individuales: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded. Usar cuando el usuario mencione 'business intelligence', 'BI', 'análisis de ventas', 'market basket', 'RFM', 'cohortes', 'CLV', 'lifetime value', 'cross-sell', 'basket analysis', 'afinidad de productos', 'análisis ecommerce', 'informe de ventas', 'análisis de clientes'."
---

# eCommerce Business Intelligence Skill

Genera informes de Business Intelligence a partir de un CSV de órdenes de eCommerce. Detecta automáticamente la plataforma, normaliza columnas y corre desde **un análisis individual** hasta **38 análisis completos**, en 6 categorías (Producto, Cliente, Revenue, Geográfico, Operativo, Estratégico).

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

La skill puede correr de tres maneras. Antes de ejecutar, preguntar al usuario cuál querer con `AskUserQuestion`:

### Modo Lite (20 análisis)

Los 20 análisis más accionables. Ideal para una primera revisión completa de la tienda. **Default cuando el usuario no especifica.** Corre en ~30 segundos.

### Modo Full (38 análisis)

Los 20 de Lite + 18 análisis avanzados (forecasting, clustering, variantes, churn detallado, etc.). Para deep dives. Corre en ~60-90 segundos.

### Modo Individual (uno o varios análisis específicos)

El usuario pide un análisis puntual ("armame un RFM", "solo quiero el market basket", "los #7 y #9 nada más"). Esto:

- Es más rápido (segundos en vez de minuto+).
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
- **Individual** — el usuario indica cuáles números (ej: 7 y 9) o nombres (ej: "RFM y cohortes").

Si pidió individual, recibir la lista de IDs o resolver nombres a IDs usando el catálogo de más abajo.

### Paso 3 — Ejecutar el script

**Modo Lite o Full:**

```bash
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --mode lite \
  --output "/tmp/bi_results.json"
```

**Modo Individual (uno o varios):**

```bash
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --analysis 7 \
  --output "/tmp/bi_results.json"

# O varios separados por coma:
python3 scripts/bi_analysis.py \
  --csv "PATH_AL_CSV" \
  --analysis 1,4,7,9 \
  --output "/tmp/bi_results.json"
```

**Listar análisis disponibles (para descubrimiento):**

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

## Catálogo de análisis (ordenado por impacto al negocio)

Los 38 análisis están agrupados en 5 tiers, de **mayor a menor impacto** sobre las decisiones de un eCommerce. Si el usuario tiene poco tiempo o solo puede correr un puñado, priorizar Tier 1 → 2 → 3.

> **Cómo leer cada bloque**:
> - **Qué hace**: la mecánica del análisis.
> - **Para qué sirve**: qué decisión concreta habilita.
> - **Necesita**: columnas mínimas en el CSV.
> - **Modo**: si está en Lite, Full, o solo Full.

---

### TIER 1 — Métricas fundacionales (corré esto sí o sí)

Definen si el negocio funciona y a quién hablarle. Sin estos, todo lo demás es ruido.

#### #7 — Segmentación RFM
- **Qué hace**: clasifica a cada cliente en uno de 11 segmentos según Recency (cuándo compró por última vez), Frequency (cuántas veces) y Monetary (cuánto gastó). Segmentos: Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost.
- **Para qué sirve**: es la base de toda estrategia de CRM y email. Te dice a quién mimar (Champions, Loyal), a quién reactivar urgente (At Risk, About to Sleep), a quién darle la bienvenida (New) y a quién dejar de gastar pauta (Lost). Sin RFM, mandás los mismos mails a todo el mundo y desperdiciás el canal.
- **Necesita**: `email`, `date`, `total`
- **Modo**: Lite + Full

#### #3 — Ranking de productos
- **Qué hace**: ordena los productos por revenue, unidades vendidas y tendencia (últimos 3 meses vs 3 anteriores). Identifica héroes (top absoluto) y estrellas emergentes (alta tendencia).
- **Para qué sirve**: te dice qué *es* tu negocio. De acá salen las decisiones de qué destacar en home, qué pautar, qué reabastecer prioritariamente y dónde concentrar el esfuerzo creativo.
- **Necesita**: `product_name`, `product_price`, `product_qty`, `date`
- **Modo**: Lite + Full

#### #9 — Análisis de cohortes (retención)
- **Qué hace**: matriz mensual de retención (últimas 12 cohortes × 12 meses). Para cada grupo de clientes adquiridos en un mes, qué porcentaje sigue comprando 1, 2, 3... meses después.
- **Para qué sirve**: te dice si el negocio realmente *funciona*. Si la retención cae a cero al M1, cada cliente nuevo es un gasto. Si la cohorte nueva retiene peor que la vieja, algo se está rompiendo. Es la curva que define el modelo.
- **Necesita**: `email`, `date`
- **Modo**: Lite + Full

#### #8 — Customer Lifetime Value (CLV)
- **Qué hace**: calcula el CLV estimado a 3 años por cliente (AOV × frecuencia × lifespan), reporta promedio, mediana y cuartiles. Identifica top 10 por CLV.
- **Para qué sirve**: establece tu techo de CAC. Si un cliente vale $100 en 3 años, no podés pagar $80 para adquirirlo. Define cuánto bid en pauta, cuánto descuento podés regalar y qué inversión en retención tiene sentido.
- **Necesita**: `email`, `date`, `total`
- **Modo**: Lite + Full

#### #11 — Evolución revenue mensual
- **Qué hace**: serie mensual de revenue, órdenes y AOV. Calcula tendencia y detecta meses pico/valle.
- **Para qué sirve**: es la línea de base. Te dice si crecés, si te estancás, si te caés. Toda lectura de las demás métricas se contextualiza contra esta tendencia.
- **Necesita**: `date`, `total`
- **Modo**: Lite + Full

#### #10 — Tasa de recompra
- **Qué hace**: porcentaje de clientes que compraron más de una vez y tiempo medio entre compras (mediana y promedio).
- **Para qué sirve**: health metric esencial. Si la recompra es <20%, sos un negocio de adquisición pura (caro). Si es >40%, tenés base instalada y podés invertir más en retención. La mediana entre compras le da el ritmo a tus automations.
- **Necesita**: `email`, `date`
- **Modo**: Lite + Full

---

### TIER 2 — Decisiones tácticas accionables

Generan acciones concretas: bundles, campañas, recomendaciones, automations.

#### #4 — Productos ancla (cross-sell drivers)
- **Qué hace**: identifica los productos que más aparecen en órdenes multi-producto. Para cada ancla, lista los 5 co-productos más frecuentes.
- **Para qué sirve**: son tus *productos gateway*: los que abren la primera compra y arrastran al carrito otros productos. Exhibirlos primero en home y categorías acelera el AOV. También: invertir pauta en estos productos rinde doble porque traen acompañantes.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Lite + Full

#### #1 — Market Basket Analysis
- **Qué hace**: identifica qué productos se compran juntos. Calcula pares y tríos con support (frecuencia), confidence (probabilidad condicional) y lift (cuánto más probable que por azar).
- **Para qué sirve**: cross-sell directo, bundles, recomendaciones en PDP, módulos "compraron junto" en el checkout, lógica de upsell por email. Cualquier combo con lift &gt; 2 es una oportunidad de revenue incremental.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Lite + Full

#### #19 — Oportunidades de bundling
- **Qué hace**: filtra los combos de #1 con mejor lift y propone bundles concretos con precio combinado.
- **Para qué sirve**: cierra el bucle del market basket en una acción concreta. En vez de "estos se compran juntos", te dice "armá este bundle con 10% off y vas a vender el doble".
- **Necesita**: `order_id`, `product_name`, `product_price`
- **Modo**: Lite + Full

#### #26 — Clientes VIP (top 10%)
- **Qué hace**: identifica el top 10% de clientes por revenue. Reporta su AOV, frecuencia, productos preferidos y mes de adquisición.
- **Para qué sirve**: el VIP suele hacer 40-60% del revenue total. Saber quiénes son, qué compran y cuándo aparecieron habilita programas VIP, ofertas tempranas, acceso anticipado, y "tratamiento aparte" en customer service.
- **Necesita**: `email`, `total`, `product_name`
- **Modo**: Full only

#### #27 — Análisis de churn
- **Qué hace**: identifica clientes que dejaron de comprar (sin actividad por &gt; 2× su intervalo medio de compra). Reporta cuáles, su valor histórico y los últimos productos comprados antes de churn.
- **Para qué sirve**: detección temprana de fuga. Los "últimos productos comprados" muchas veces revelan problemas de calidad o experiencia. Habilita campañas de reactivación con oferta dirigida.
- **Necesita**: `email`, `date`, `total` (idealmente ≥6 meses de histórico)
- **Modo**: Full only

#### #20 — Estacionalidad
- **Qué hace**: detecta picos y valles por mes y por día de la semana. Identifica mes pico, mes valle y día más fuerte.
- **Para qué sirve**: planificación anual de pauta y stock. Cuándo apretar el acelerador, cuándo soltar, cuándo programar lanzamientos. También: rotar contenido orgánico según día de mayor tráfico.
- **Necesita**: `date`, `total`
- **Modo**: Lite + Full

---

### TIER 3 — Optimización de mix, pricing y stock

Decisiones sobre el catálogo, márgenes y composición de revenue.

#### #5 — Long tail 80/20
- **Qué hace**: cuántos SKUs hacen el 80% del revenue. Distribución Pareto del catálogo.
- **Para qué sirve**: decisiones de stock e inversión. Si el 10% de los SKUs hace el 80%, el resto del catálogo puede ser candidato a descatalogar, liquidar o pasar a print-on-demand.
- **Necesita**: `product_name`, `product_price`, `product_qty`
- **Modo**: Lite + Full

#### #12 — Ticket promedio (AOV)
- **Qué hace**: AOV global, AOV mediano, distribución por tramo y evolución mensual. Compara AOV de clientes nuevos vs recurrentes.
- **Para qué sirve**: KPI core de cualquier optimización (bundles, free-shipping threshold, descuentos por volumen). Si AOV mediano &lt;&lt; AOV promedio, hay outliers que distorsionan: limpiar antes de tomar decisiones.
- **Necesita**: `total`
- **Modo**: Lite + Full

#### #13 — Revenue por categoría
- **Qué hace**: mix de revenue por categoría (extraída del nombre del producto). Top N categorías + % de mix.
- **Para qué sirve**: balance del catálogo. Si una categoría concentra 70%, hay riesgo de dependencia. Si todas reparten parejo, oportunidad de empujar una para crecer.
- **Necesita**: `product_name`, `product_price`, `product_qty`
- **Modo**: Lite + Full

#### #14 — Impacto de descuentos
- **Qué hace**: AOV con cupón vs sin cupón, % de órdenes con descuento, top cupones usados, monto total descontado.
- **Para qué sirve**: medir si el descuento *agrega* valor o *canibaliza* margen. Si el AOV con cupón es igual o menor al sin cupón, estás regalando margen sin contrapartida. Si es mayor, el cupón está sirviendo.
- **Necesita**: `total`, `discount` (idealmente `coupon`)
- **Modo**: Lite + Full

#### #2 — Afinidad entre categorías
- **Qué hace**: market basket pero a nivel categoría: qué categorías se combinan en la misma orden.
- **Para qué sirve**: cross-merchandising en home y landings. Si "Remeras" + "Pantalones" tienen alta afinidad, una landing combinada o un carrusel "Outfit completo" puede levantar AOV. También guía la navegación: poner categorías afines visualmente próximas.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Lite + Full

#### #36 — Recomendación de cross-sell
- **Qué hace**: para cada producto top, qué otro recomendar (basado en lift y co-ocurrencia).
- **Para qué sirve**: tabla lista para alimentar el motor de recomendaciones del store. "Si compraste X, te recomendamos Y" directo del dato real, no de heurísticas genéricas.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Full only

#### #37 — Análisis de pricing
- **Qué hace**: identifica productos sobre-precio o sub-precio comparados con su categoría.
- **Para qué sirve**: detecta candidatos a ajuste de precio. Un producto a 50% del promedio de su categoría puede ser "loss leader" intencional o un error. Uno al doble puede estar matando conversión sin que lo veas.
- **Necesita**: `product_name`, `product_price`
- **Modo**: Full only

#### #29 — Análisis de precio
- **Qué hace**: histograma de precios y unidades vendidas por tramo. Identifica price points con mejor performance.
- **Para qué sirve**: encontrar el "sweet spot" de precio del catálogo. A veces el 80% de las ventas se concentra en un rango de $X-$Y muy estrecho; saber esto guía la curaduría de futuras incorporaciones.
- **Necesita**: `product_price`, `product_qty`
- **Modo**: Full only

---

### TIER 4 — Geografía y operativa

Decisiones sobre logística, pauta geo y experiencia post-compra.

#### #15 — Heatmap por provincia
- **Qué hace**: revenue, órdenes y AOV por provincia/estado.
- **Para qué sirve**: decisiones de pauta geo (qué provincias merecen más inversión), de envíos (negociar tarifas en zonas con volumen), de expansión (provincias con AOV alto pero pocos pedidos = ventana de crecimiento).
- **Necesita**: `state`, `total`
- **Modo**: Lite + Full

#### #16 — Costo de envío vs conversión
- **Qué hace**: distribución del costo de envío por tramo y correlación con cancelación.
- **Para qué sirve**: el costo de envío es uno de los principales drivers de abandono. Si la tasa de cancelación se dispara cuando el envío supera $X, ese es tu umbral psicológico — y tu palanca para definir el threshold de envío gratis.
- **Necesita**: `shipping_cost`, `order_status`
- **Modo**: Lite + Full

#### #30 — Penetración por ciudad
- **Qué hace**: top ciudades por revenue, AOV y órdenes (granularidad más fina que provincia).
- **Para qué sirve**: pauta geográfica fina, decisiones de cobertura (¿abrir un punto físico o pickup en X ciudad?), patrones de concentración urbana.
- **Necesita**: `city`, `total`
- **Modo**: Full only

#### #34 — Eficiencia de envío gratis
- **Qué hace**: compara AOV y conversión de órdenes con envío gratis vs con envío pago.
- **Para qué sirve**: evaluar la política de envío gratis. Si el AOV gratis es solo $X mayor que el threshold, el regalo no le está moviendo el AOV — bajar el threshold o eliminar la promo. Si es muy mayor, vale la pena bajarlo más para empujar AOV.
- **Necesita**: `shipping_cost`, `total`
- **Modo**: Full only

#### #32 — Tiempo de fulfillment
- **Qué hace**: días entre orden y despacho. Distribución, mediana y outliers.
- **Para qué sirve**: SLA operativo. Si la mediana sube mes a mes, hay problema de logística que se viene encima. Outliers (órdenes con &gt;10 días de fulfillment) son los que generan tickets de soporte y reviews negativas.
- **Necesita**: `date`, `shipping_date`
- **Modo**: Full only

#### #17 — Tasa de cancelación
- **Qué hace**: % global de canceladas, top motivos de cancelación, evolución mensual, mix por medio de pago.
- **Para qué sirve**: health metric operativo. Tendencia ascendente = problema (stock, pricing, expectativa). Los top motivos te dicen exactamente dónde está la fuga.
- **Necesita**: `order_status`
- **Modo**: Lite + Full

#### #6 — Productos con alta cancelación
- **Qué hace**: identifica productos con tasa de cancelación significativamente sobre la media.
- **Para qué sirve**: detectar productos problemáticos (calidad, stock, expectativa vs realidad). Cada uno es una conversación con catálogo o el proveedor.
- **Necesita**: `product_name`, `order_status`
- **Modo**: Lite + Full

#### #18 — Mix de medios de pago
- **Qué hace**: distribución de órdenes y revenue por medio de pago (MP, tarjeta, transferencia, etc.).
- **Para qué sirve**: optimizar comisiones y checkout. Si el 60% paga por MP y eso te cuesta 6%, negociación pendiente. Si la transferencia tiene AOV mayor, empujarla con descuento.
- **Necesita**: `payment_method`, `total`
- **Modo**: Lite + Full

#### #31 — Medio de envío por zona
- **Qué hace**: mix de shipping methods por provincia.
- **Para qué sirve**: detectar dónde la oferta de envíos está incompleta. Si en una provincia solo hay un courier disponible y la conversión cae, es señal para sumar uno.
- **Necesita**: `state`, `shipping_method`
- **Modo**: Full only

---

### TIER 5 — Avanzados y específicos

Deep dives útiles cuando ya tenés los Tiers 1-4 resueltos.

#### #35 — Forecast de ventas
- **Qué hace**: proyección de revenue a 3 meses con ajuste estacional (mínimo 6 meses de histórico).
- **Para qué sirve**: planificación financiera, presupuestos, cash flow, decisiones de stock para temporada alta.
- **Necesita**: `date`, `total`
- **Modo**: Full only

#### #38 — Identificación de nichos
- **Qué hace**: clusters de productos con alta afinidad interna y bajo overlap entre sí (nichos de catálogo).
- **Para qué sirve**: detectar sub-marcas o líneas implícitas dentro del catálogo. Habilita decisiones de marca paraguas, landings por nicho y curaduría editorial.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Full only

#### #25 — Patrón de upgrade
- **Qué hace**: detecta si los clientes aumentan su AOV en compras sucesivas.
- **Para qué sirve**: si el AOV crece, el storytelling de marca funciona y se puede empujar premium. Si no crece, el techo de cada cliente es el AOV de la primera compra.
- **Necesita**: `email`, `date`, `total`
- **Modo**: Full only

#### #23 — Análisis de SKU/variantes
- **Qué hace**: performance por variante (color, talle, SKU). Detecta variantes muertas y heroínas.
- **Para qué sirve**: stock fino. Discontinuar variantes que no rotan, reforzar las heroínas. Diferencia entre "este producto vende" y "este producto vende solo en talle M negro".
- **Necesita**: `sku`, `product_name`, `product_qty`
- **Modo**: Full only

#### #24 — Ciclo de vida del producto
- **Qué hace**: clasifica productos en emergente, madurez, declive según evolución de unidades.
- **Para qué sirve**: lifecycle management. Promover emergentes, exprimir maduros, liquidar declive antes de que generen stock muerto.
- **Necesita**: `product_name`, `product_qty`, `date`
- **Modo**: Full only

#### #28 — Revenue por canal
- **Qué hace**: distribución de revenue por canal (web, mobile, POS).
- **Para qué sirve**: priorizar inversión en UX por canal. Si mobile concentra órdenes pero AOV baja, hay friction en el checkout mobile.
- **Necesita**: `channel`, `total`
- **Modo**: Full only

#### #33 — Análisis de canal
- **Qué hace**: comparativa profunda por canal — AOV, tasa de cancelación, mix de productos.
- **Para qué sirve**: detectar diferencias de comportamiento que no son obvias. POS puede tener AOV alto pero alta devolución; mobile puede tener bajo AOV pero alta repetición.
- **Necesita**: `channel`, `total`, `order_status`
- **Modo**: Full only

#### #21 — Afinidad entre colores
- **Qué hace**: combos de colores comprados juntos (parsea el nombre del producto buscando colores conocidos).
- **Para qué sirve**: merchandising fino — qué colores se llevan en outfits, qué paletas funcionan, qué nuevos colores agregar al próximo drop.
- **Necesita**: `order_id`, `product_name`
- **Modo**: Full only

#### #22 — Afinidad entre talles
- **Qué hace**: combos de talles en la misma orden.
- **Para qué sirve**: stock por talle, decisiones de curva de producción, detección de "compra para pareja/familia" (talles muy distintos en la misma orden).
- **Necesita**: `order_id`, `product_name`
- **Modo**: Full only

---

## Reglas

- **SIEMPRE** correr `bi_analysis.py` — no calcular análisis manualmente. El script ya maneja todas las plataformas y normaliza columnas.
- Si un análisis falla por columnas faltantes, queda `status: "skipped"` con el motivo. **Mostrarlo en el HTML** como nota al pie de la sección, no ocultarlo.
- **Market Basket**: solo mostrar asociaciones con `support > 1%` y `lift > 1.0`. Por debajo es ruido.
- **RFM**: usar los 11 labels estándar (Champions, Loyal, Potential Loyal, New, Promising, Need Attention, About to Sleep, At Risk, Can't Lose, Hibernating, Lost).
- **Cohortes**: limitar a últimas 12 cohortes × 12 meses para legibilidad.
- **Modo Individual**: si el usuario menciona análisis por nombre ("RFM y cohortes"), resolver a IDs (#7 y #9) usando el catálogo de arriba antes de invocar el script.
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
- "Armame un RFM sobre `ordenes.csv`" → modo Individual #7
- "Quiero el market basket y la afinidad de categorías" → modo Individual #1, #2
