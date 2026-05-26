# ecommerce-bi

> Skill de Claude Code para generar informes de Business Intelligence sobre tu tienda eCommerce a partir de un CSV de ventas.

Apuntá la skill a tu export de Tiendanube, Shopify o WooCommerce y obtené un informe con hasta 38 análisis: Market Basket, RFM, cohortes, CLV, cross-sell, churn, estacionalidad, forecast y más. Output: JSON estructurado + informe HTML branded.

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

**Modo Lite (20)** — los más accionables, ~30 segundos:

- **Producto**: Market Basket, afinidad de categorías, ranking, productos ancla, long tail 80/20, cancelaciones por producto.
- **Cliente**: segmentación RFM (11 segmentos), CLV, cohortes, recompra.
- **Revenue**: evolución mensual, ticket promedio, mix por categoría, impacto de descuentos.
- **Geográfico**: heatmap por provincia, costo de envío vs conversión.
- **Operativo**: cancelaciones, mix de medios de pago.
- **Estratégico**: bundling, estacionalidad.

**Modo Full (38)** — agrega 18 análisis más:

- Afinidad de colores, talles, SKU/variantes, ciclo de vida de producto.
- Patrón de upgrade, clientes VIP (top 10%), churn.
- Revenue por canal, análisis de precio.
- Penetración por ciudad, medio de envío por zona.
- Tiempo de fulfillment, análisis de canal, eficiencia de envío gratis.
- Forecast de ventas, recomendaciones de cross-sell, pricing, identificación de nichos.

Detalle de cada uno (qué responde, qué necesita, output esperado): [`SKILL.md`](SKILL.md) y [`references/analysis_catalog.md`](references/analysis_catalog.md).

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

> "Hacé un análisis de BI sobre `mi_export_tiendanube.csv`"

Claude detecta la skill, te pregunta el modo (Lite/Full) y devuelve el informe en HTML.

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

Hecho por [Mathias Schusterman](https://github.com/mathiaschu), CEO de [Clica](https://clica.agency), agencia de Growth para eCommerce. Esta skill es lo que usamos puertas adentro para analizar tiendas de clientes — la abrimos para que cualquiera pueda usarla.
