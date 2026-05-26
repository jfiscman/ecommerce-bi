# ecommerce-bi

> Skill de Claude Code para generar informes de Business Intelligence sobre tu tienda eCommerce a partir de un CSV de ventas.

Apuntá la skill a tu export de Tiendanube, Shopify o WooCommerce y obtené un informe con hasta 38 análisis: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded.

Podés correrla en tres modos: **Lite** (20 análisis core), **Full** (38 análisis completos) o **Individual** (uno o varios análisis específicos, ej: solo el RFM, o solo Market Basket + Cohortes).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## ¿Qué hace?

Convierte un CSV de pedidos en un informe accionable. No es un dashboard interactivo: es un **informe estático** pensado para entregar (a cliente, a tu equipo, a vos mismo) con la pregunta ya respondida y la acción concreta encima.

### Ejemplo

```bash
python3 scripts/bi_analysis.py \
  --csv examples/sample_orders.csv \
  --mode lite \
  --output /tmp/bi.json
```

Salida (extracto):

```
Loading CSV: examples/sample_orders.csv
Platform: tiendanube | Encoding: latin-1 | Delimiter: ';' | Rows: 128
Running lite analyses...
  Running #1: Market Basket Analysis...
  Running #2: Afinidad entre categorías...
  ...
Done: 20 ok, 0 skipped
```

Después se renderiza un HTML como [`examples/sample_report.html`](examples/sample_report.html) (abrilo en el browser para ver el output completo).

---

## Análisis disponibles

Los 38 análisis están **rankeados por impacto al negocio** en [`SKILL.md`](SKILL.md). Si recién arrancás, priorizá Tier 1.

### TIER 1 — Métricas fundacionales (corré esto sí o sí)

1. **#7 Segmentación RFM** — base de toda estrategia de CRM/email
2. **#3 Ranking de productos** — qué *es* tu negocio
3. **#9 Cohortes de retención** — define si el negocio funciona
4. **#8 Customer Lifetime Value** — establece tu techo de CAC
5. **#11 Evolución mensual** — la línea de base
6. **#10 Tasa de recompra** — health metric esencial

### TIER 2 — Decisiones tácticas accionables

7. **#4 Productos ancla** (gateway products que abren la primera compra)
8. **#1 Market Basket** (cross-sell directo)
9. **#19 Oportunidades de bundling**
10. **#26 Clientes VIP** (top 10%)
11. **#27 Análisis de churn**
12. **#20 Estacionalidad**

### TIER 3 — Mix, pricing y stock

#5 Long tail 80/20 · #12 Ticket promedio · #13 Revenue por categoría · #14 Impacto de descuentos · #2 Afinidad entre categorías · #36 Cross-sell recomendaciones · #37 Análisis de pricing · #29 Análisis de precio

### TIER 4 — Geografía y operativa

#15 Heatmap provincia · #16 Costo envío vs conversión · #30 Penetración por ciudad · #34 Eficiencia envío gratis · #32 Tiempo fulfillment · #17 Tasa cancelación · #6 Cancelaciones por producto · #18 Mix medios de pago · #31 Medio envío por zona

### TIER 5 — Avanzados y específicos

#35 Forecast · #38 Nichos · #25 Patrón de upgrade · #23 SKU/variantes · #24 Ciclo de vida · #28 Revenue por canal · #33 Análisis de canal · #21 Afinidad colores · #22 Afinidad talles

Detalle de cada uno (qué hace, para qué sirve, columnas requeridas) en [`SKILL.md`](SKILL.md). Metodología técnica en [`references/analysis_catalog.md`](references/analysis_catalog.md).

---

## Modos de ejecución

### Modo Lite (default)

Los 20 análisis core (Tier 1 + Tier 2 base + lo más usado de Tier 3-4). ~30 segundos.

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
# Solo RFM
python3 scripts/bi_analysis.py --csv orders.csv --analysis 7 --output out.json

# RFM + Cohortes + CLV
python3 scripts/bi_analysis.py --csv orders.csv --analysis 7,8,9 --output out.json

# Listar todos los análisis disponibles
python3 scripts/bi_analysis.py --list
```

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
> "Armame un RFM sobre `mi_export_tiendanube.csv`" → modo Individual (#7)
>
> "Quiero solo el market basket y la afinidad de categorías" → modo Individual (#1, #2)

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
- Generar un sample como demo.

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
