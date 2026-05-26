# ecommerce-bi

> Skill de Claude Code para generar informes de Business Intelligence sobre tu tienda eCommerce a partir de un CSV de ventas.

Apuntá la skill a tu export de Tiendanube, Shopify o WooCommerce y obtené un informe con hasta 38 análisis: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded.

Podés correrla en tres modos: **Lite** (20 análisis core), **Full** (38 análisis completos) o **Individual** (un análisis específico o varios, como solo el RFM, o Market Basket + Cohortes).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## Análisis disponibles

Lista completa de los 38 análisis que puede generar esta skill, ordenados de mayor a menor impacto típico al negocio. Cada uno se puede correr individualmente o como parte de los modos Lite / Full.

1. **Segmentación RFM** — Clasifica a cada cliente en 11 segmentos según cuándo compró por última vez (Recency), cuántas veces (Frequency) y cuánto gastó (Monetary). Es la base de toda estrategia de CRM y email: te dice a quién mimar (Champions), a quién reactivar (At Risk), a quién dar bienvenida (New) y a quién dejar de gastarle pauta (Lost).

2. **Ranking de productos** — Ordena el catálogo por revenue, unidades vendidas y tendencia (últimos 3 meses vs 3 anteriores). Identifica héroes (top absoluto) y estrellas emergentes. Te dice qué *es* tu negocio y qué destacar en home, pauta y reabastecimiento.

3. **Análisis de cohortes (retención)** — Matriz mensual de retención: para cada grupo de clientes adquiridos en un mes, qué porcentaje sigue comprando 1, 2, 3 meses después. Define si el negocio funciona: si la retención cae a cero, cada cliente nuevo es solo un gasto.

4. **Customer Lifetime Value (CLV)** — Estima cuánto vale cada cliente a 3 años (AOV × frecuencia × lifespan). Establece tu techo de CAC: si un cliente vale $100, no podés pagar $80 para adquirirlo. Define cuánto invertir en pauta, descuentos y retención.

5. **Evolución mensual de revenue** — Serie mensual de revenue, órdenes y ticket promedio, con tendencia y picos identificados. Es la línea de base contra la que se contextualiza toda otra métrica.

6. **Tasa de recompra** — Porcentaje de clientes que compraron más de una vez y tiempo medio entre compras. Si la recompra es &lt;20% sos un negocio de adquisición pura (caro). Si es &gt;40%, podés invertir en retención. La mediana entre compras le da el ritmo a tus automations.

7. **Productos ancla (gateway products)** — Identifica los productos que más aparecen en órdenes multi-producto y sus mejores co-compras. Son los productos que abren la primera compra y arrastran al carrito otros. Invertir pauta en ellos rinde doble.

8. **Market Basket Analysis** — Detecta qué productos se compran juntos. Calcula pares y tríos con métricas de support, confidence y lift. Insumo directo para cross-sell, bundles, recomendaciones en PDP y módulos "compraron junto".

9. **Oportunidades de bundling** — Toma los combos con mejor lift del Market Basket y propone bundles concretos con precio combinado. Cierra el bucle del análisis en una acción ejecutable: "armá este bundle con 10% off".

10. **Clientes VIP (top 10%)** — Identifica al top 10% de clientes por revenue y reporta su AOV, frecuencia y productos preferidos. Suelen hacer 40-60% del revenue total. Habilita programas VIP, ofertas tempranas y customer service diferenciado.

11. **Análisis de churn** — Detecta clientes que dejaron de comprar (sin actividad por más del doble de su intervalo medio). Reporta su valor histórico y los últimos productos que compraron antes de irse, muchas veces reveladores de problemas de calidad o experiencia.

12. **Estacionalidad** — Detecta picos y valles por mes y por día de la semana. Identifica mes pico, mes valle y día más fuerte. Planificación anual de pauta, stock, lanzamientos y contenido.

13. **Long tail 80/20** — Cuántos SKUs hacen el 80% del revenue. Si pocos SKUs hacen casi todo, el resto del catálogo puede ser candidato a descatalogar, liquidar o pasar a print-on-demand.

14. **Ticket promedio (AOV)** — AOV global, mediano, distribución por tramo y evolución mensual. Compara nuevos vs recurrentes. KPI core de cualquier optimización (bundles, free-shipping threshold, descuentos por volumen).

15. **Revenue por categoría** — Mix del catálogo por categoría con porcentajes. Si una categoría concentra 70%, hay riesgo de dependencia. Si todas reparten parejo, hay oportunidad de empujar una para crecer.

16. **Impacto de descuentos** — Compara AOV con cupón vs sin cupón, % de órdenes con descuento y top cupones. Mide si el descuento *agrega* valor o *canibaliza* margen.

17. **Afinidad entre categorías** — Qué categorías se combinan en la misma orden. Guía cross-merchandising (landings combinadas, carruseles "outfit completo") y la navegación visual del store.

18. **Recomendaciones de cross-sell** — Para cada producto top, qué otro recomendar (basado en lift y co-ocurrencia). Tabla lista para alimentar el motor de recomendaciones del store, derivada del dato real y no de heurísticas genéricas.

19. **Análisis de pricing** — Detecta productos sobre-precio o sub-precio comparados con el promedio de su categoría. Cada uno es candidato a ajuste o conversación con catálogo.

20. **Análisis de precio (distribución)** — Histograma de precios y unidades vendidas por tramo. Identifica el sweet spot del catálogo, útil para curar incorporaciones futuras.

21. **Heatmap por provincia** — Revenue, órdenes y AOV por provincia/estado. Decisiones de pauta geo, negociación de tarifas de envío en zonas con volumen, y detección de provincias con AOV alto pero pocos pedidos (ventana de crecimiento).

22. **Costo de envío vs conversión** — Distribución del costo de envío por tramo y correlación con cancelación. El envío es uno de los principales drivers de abandono: este análisis te da el umbral psicológico de tu base y la palanca para el threshold de envío gratis.

23. **Penetración por ciudad** — Top ciudades por revenue y AOV (granularidad más fina que provincia). Pauta geográfica fina, decisiones de cobertura, patrones de concentración urbana.

24. **Eficiencia de envío gratis** — Compara AOV y conversión de órdenes con envío gratis vs pago. Evalúa si tu política de envío gratis funciona o regalás margen sin contrapartida.

25. **Tiempo de fulfillment** — Días entre orden y despacho: mediana, distribución y outliers. SLA operativo. Si la mediana sube mes a mes, hay un problema de logística por venir.

26. **Tasa de cancelación** — % global de canceladas, top motivos y evolución mensual. Tendencia ascendente = problema (stock, pricing, expectativa). Los motivos te dicen exactamente dónde está la fuga.

27. **Productos con alta cancelación** — Identifica los productos con tasa de cancelación significativamente sobre la media. Cada uno es una conversación con catálogo o con el proveedor.

28. **Mix de medios de pago** — Distribución de órdenes y revenue por medio de pago. Si una procesadora concentra mucho con comisión alta, hay negociación pendiente. Si un medio tiene AOV mayor, empujarlo con descuento.

29. **Medio de envío por zona** — Mix de couriers/métodos por provincia. Detecta dónde la oferta de envíos está incompleta y la conversión cae por falta de opciones.

30. **Forecast de ventas** — Proyección de revenue a 3 meses con ajuste estacional (requiere ≥6 meses de histórico). Planificación financiera, presupuestos, cash flow y stock para temporada alta.

31. **Identificación de nichos** — Clusters de productos con alta afinidad interna y bajo overlap entre sí. Detecta sub-marcas o líneas implícitas dentro del catálogo. Insumo para landings por nicho y curaduría editorial.

32. **Patrón de upgrade** — Detecta si los clientes aumentan su AOV en compras sucesivas. Si crece, el storytelling de marca está funcionando y se puede empujar premium. Si no, el techo de cada cliente es la primera compra.

33. **Análisis de SKU/variantes** — Performance por variante (color, talle, SKU). Detecta variantes muertas y heroínas. Discontinuar lo que no rota, reforzar lo que sí. Diferencia entre "este producto vende" y "vende solo en talle M negro".

34. **Ciclo de vida del producto** — Clasifica productos en emergente, madurez o declive según evolución de unidades. Lifecycle management: promover emergentes, exprimir maduros, liquidar declive antes de que generen stock muerto.

35. **Revenue por canal** — Distribución de revenue por canal (web, mobile, POS). Si mobile concentra órdenes pero el AOV baja, hay friction en el checkout mobile.

36. **Análisis de canal (profundo)** — Comparativa por canal en AOV, tasa de cancelación y mix de productos. Detecta diferencias de comportamiento no obvias entre canales.

37. **Afinidad entre colores** — Combos de colores comprados juntos (parsea el nombre del producto). Merchandising fino: qué paletas funcionan, qué nuevos colores agregar al próximo drop.

38. **Afinidad entre talles** — Combos de talles en la misma orden. Decisiones de curva de stock por talle y detección de "compra para pareja/familia" (talles muy distintos en una misma orden).

---

## Plataformas soportadas

| Plataforma | Detección automática | Encoding | Delimitador |
|---|---|---|---|
| **Tiendanube** | Por headers | `latin-1` | `;` |
| **Shopify** | Por headers | `utf-8` | `,` |
| **WooCommerce** | Por headers | `utf-8` | `,` |
| **Genérico** | Si las columnas matchean los nombres canónicos | autodetectado | autodetectado |

Mapeo completo de columnas en [`references/csv_mapping.md`](references/csv_mapping.md).

---

## Modos de ejecución

### Modo Lite (default)

Los 20 análisis core (los más usados de la lista de arriba). Corre en ~30 segundos.

```bash
python3 scripts/bi_analysis.py --csv orders.csv --mode lite --output out.json
```

### Modo Full

Los 38 análisis completos. ~60-90 segundos.

```bash
python3 scripts/bi_analysis.py --csv orders.csv --mode full --output out.json
```

### Modo Individual

Uno o varios análisis específicos. El script resuelve dependencias automáticamente.

```bash
# Listar todos los análisis con sus IDs internos
python3 scripts/bi_analysis.py --list

# Correr uno solo (RFM)
python3 scripts/bi_analysis.py --csv orders.csv --analysis 7 --output out.json

# Varios (RFM + CLV + Cohortes)
python3 scripts/bi_analysis.py --csv orders.csv --analysis 7,8,9 --output out.json
```

---

## Instalación

### Como skill de Claude Code

```bash
# Opción A: clonar dentro del directorio de skills
git clone https://github.com/mathiaschu/ecommerce-bi.git ~/.claude/skills/ecommerce-bi

# Opción B: clonar en cualquier lado y symlinkear
git clone https://github.com/mathiaschu/ecommerce-bi.git
ln -s "$(pwd)/ecommerce-bi" ~/.claude/skills/ecommerce-bi
```

Reiniciá Claude Code. Después escribí algo como:

> "Hacé un análisis de BI completo sobre `mi_export_tiendanube.csv`" → modo Lite/Full
>
> "Armame un RFM sobre `mi_export_tiendanube.csv`" → modo Individual
>
> "Quiero solo el market basket y la afinidad de categorías" → modo Individual

Claude detecta la skill, te pregunta qué modo y devuelve el informe en HTML.

### Como CLI standalone (sin Claude)

```bash
git clone https://github.com/mathiaschu/ecommerce-bi.git
cd ecommerce-bi
pip3 install pandas numpy

# Análisis Lite
python3 scripts/bi_analysis.py --csv tu_ordenes.csv --mode lite --output resultados.json

# Generar HTML a partir del JSON
python3 examples/generate_sample_html.py resultados.json informe.html
open informe.html
```

---

## Requisitos

- Python 3.9 o superior
- `pandas` y `numpy`

```bash
pip3 install pandas numpy
```

Sin servicios cloud, sin API keys, sin GPU. Todo corre local.

---

## Ejemplo incluido

El repo viene con un CSV sintético en `examples/sample_orders.csv` (~80 órdenes, 12 meses, 20 SKUs, formato Tiendanube). Útil para:

- Verificar que la skill funciona en tu entorno.
- Aprender qué output produce antes de tirarle datos reales.

```bash
python3 scripts/bi_analysis.py \
  --csv examples/sample_orders.csv \
  --mode lite \
  --output examples/sample_results.json

python3 examples/generate_sample_html.py
```

Resultado: [`examples/sample_report.html`](examples/sample_report.html).

---

## Qué columnas necesito en mi CSV

Mínimo para que sirva: `order_id`, `date`, `total`, `product_name`.

Sumá `email` para todos los análisis de cliente. Sumá `state` o `city` para los geográficos.

Tabla completa de qué columnas habilita cada análisis: [`references/required_columns.md`](references/required_columns.md).

---

## Privacidad

- El script no manda datos a ningún servicio externo.
- No requiere API keys ni cuentas.
- Todo el procesamiento es local.
- El `.gitignore` excluye por defecto archivos con sufijo `_real.csv` y `_client.csv` para que no commitees data de clientes por accidente.

---

## Estructura

```
ecommerce-bi/
├── SKILL.md                          ← Skill para Claude Code
├── README.md                         ← Este archivo
├── LICENSE                           ← MIT
├── CONTRIBUTING.md
├── scripts/
│   └── bi_analysis.py                ← Motor (Python + pandas)
├── references/
│   ├── analysis_catalog.md           ← Metodología detallada de los 38 análisis
│   ├── csv_mapping.md                ← Mapeo de columnas por plataforma
│   ├── html_template.md              ← Template HTML del informe
│   └── required_columns.md           ← Qué columnas habilita cada análisis
└── examples/
    ├── generate_sample.py            ← Genera el CSV sintético
    ├── generate_sample_html.py       ← Renderiza JSON → HTML
    ├── sample_orders.csv             ← CSV de prueba
    ├── sample_results.json           ← Output del script sobre el sample
    └── sample_report.html            ← HTML generado a partir del JSON
```

---

## Roadmap

- [ ] Soporte para más plataformas (VTEX, Magento, Amazon Seller).
- [ ] Modo `--diff` para comparar dos rangos de fechas.
- [ ] Export del informe como PDF.
- [ ] Análisis adicionales: previsión de stock, predicción de churn por cliente.

Si te falta algo concreto, [abrí un issue](https://github.com/mathiaschu/ecommerce-bi/issues).

---

## Contribuir

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md). Bugs, plataformas nuevas, análisis adicionales, mejoras al HTML — todo bienvenido.

---

## Licencia

MIT — usá, modificá y compartí libremente. Ver [`LICENSE`](LICENSE).

---

## Autor

Mantenido por [@mathiaschu](https://github.com/mathiaschu). PRs y issues bienvenidos.
