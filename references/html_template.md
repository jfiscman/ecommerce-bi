# HTML Template — Business Intelligence Report

Guía para que Claude arme el HTML del informe a partir del JSON producido por `bi_analysis.py`.

## Principios

Esta guía es **deliberadamente neutra y permisiva**. No impone una identidad visual concreta. La razón es simple: el informe es del usuario final (el dueño de la tienda), no de la skill. Por defecto se entrega con un diseño profesional, sobrio y agnóstico. Si el usuario lo pide, Claude puede adaptarlo al branding del negocio (colores, logo, tipografía propia).

Reglas:

1. **Sin marca propia en el HTML generado**. No mencionar la skill, ni el autor, ni ninguna agencia. La única referencia permitida es una línea sutil al final del footer atribuyendo la herramienta — y nada más.
2. **Diseño neutro por default**. Sistema de fuentes nativo, paleta de grises + un acento neutro, bordes sutiles. Nada estridente.
3. **Si el usuario provee branding** (logo, colores, tipografía), Claude debe respetarlo y adaptar.
4. **Legible primero, bonito segundo**. Es un informe de negocio para leer y tomar decisiones, no un poster.

---

## Estructura del informe (en este orden)

1. **Header**
   - Nombre del negocio (si el usuario lo dio; si no, "Informe de Business Intelligence")
   - Rango de fechas del dataset
   - Plataforma detectada (Tiendanube / Shopify / WooCommerce / Genérico)
   - Badge de modo: `LITE` / `FULL` / `INDIVIDUAL`

2. **Métricas hero** (4 tarjetas)
   - Revenue total
   - Órdenes totales
   - Clientes únicos
   - Ticket promedio
   - Cada tarjeta con tendencia vs 3 meses anteriores (si está disponible)

3. **Secciones por categoría** — en este orden:
   1. Producto
   2. Cliente
   3. Revenue
   4. Geográfico
   5. Operativo
   6. Estratégico

   Si el modo es Individual, solo incluir las categorías que tienen al menos un análisis pedido.

4. **Cada análisis dentro de su sección**:
   - Título (sin el ID interno; usar solo el nombre)
   - Tabla / lista / chart con los datos del JSON
   - Insight accionable (1-2 líneas; qué hacer con el dato, no qué dice el dato)

5. **Análisis "skipped"**: incluir un placeholder breve "Análisis no disponible: {reason}". No ocultar.

6. **Footer**
   - Atribución mínima: "Reporte generado con ecommerce-bi · creado por [@mathiaschu](https://twitter.com/mathiaschu)"
   - Nada más.

---

## CSS base sugerido (neutro)

Lo siguiente es un punto de partida razonable. Claude puede ajustar dimensiones, espaciados, etc. **No usar paletas con marca personal**. Si el usuario provee colores propios, sustituir los valores `--accent`, `--bg-card-emphasis`, etc.

```css
:root {
  --bg: #ffffff;
  --bg-subtle: #fafafa;
  --bg-card: #ffffff;
  --bg-card-emphasis: #f4f6f8;
  --border: #e5e7eb;
  --border-strong: #d1d5db;
  --text: #111827;
  --text-secondary: #4b5563;
  --text-muted: #6b7280;
  --accent: #1e40af;          /* azul sobrio — sustituible */
  --accent-soft: #eff6ff;
  --positive: #047857;
  --negative: #b91c1c;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: ui-monospace, 'SF Mono', Menlo, monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.55;
  padding: 56px 24px;
}

.container { max-width: 1100px; margin: 0 auto; }

/* Header */
header { margin-bottom: 56px; padding-bottom: 28px; border-bottom: 1px solid var(--border); }
h1 { font-size: 32px; font-weight: 600; letter-spacing: -0.01em; margin: 4px 0 6px; }
.subtitle { color: var(--text-secondary); font-size: 14px; }
.mode-badge {
  display: inline-block;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  padding: 3px 9px;
  border-radius: 4px;
  margin-left: 8px;
  vertical-align: middle;
  text-transform: uppercase;
}

/* Hero metrics */
.hero-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 28px;
}
.hero {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 18px;
}
.hero-num { font-size: 26px; font-weight: 600; color: var(--text); }
.hero-lbl {
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}
.hero-trend { font-size: 12px; margin-top: 8px; color: var(--text-secondary); }

/* Section / Category */
section.category { margin: 56px 0 24px; }
section.category h2 {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-secondary);
  margin-bottom: 20px;
  border-top: 1px solid var(--border);
  padding-top: 24px;
}

/* Analysis card */
.analysis {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 14px;
}
.analysis h3 { font-size: 18px; font-weight: 600; margin-bottom: 14px; color: var(--text); }

/* Stats / KPIs inside an analysis */
.kpi-row { color: var(--text-secondary); font-size: 14px; margin-bottom: 10px; }
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 10px;
  margin: 14px 0;
}
.stat {
  background: var(--bg-card-emphasis);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px;
}
.stat-num { font-size: 20px; font-weight: 600; color: var(--text); }
.stat-lbl {
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}

/* Tables */
table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 14px; }
th, td {
  text-align: left;
  padding: 9px 12px;
  border-bottom: 1px solid var(--border);
}
th {
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.08em;
}

/* Insight block */
.insight {
  background: var(--bg-card-emphasis);
  border-left: 3px solid var(--accent);
  padding: 12px 16px;
  margin-top: 14px;
  color: var(--text);
  font-size: 14px;
  line-height: 1.55;
}

/* Skipped analysis */
.skipped {
  color: var(--text-muted);
  font-style: italic;
  font-size: 13px;
}

/* Footer */
footer {
  text-align: center;
  color: var(--text-muted);
  font-size: 12px;
  padding: 36px 0 0;
  border-top: 1px solid var(--border);
  margin-top: 56px;
}
footer a { color: var(--text-secondary); text-decoration: none; }
footer a:hover { color: var(--accent); text-decoration: underline; }
```

---

## Template HTML mínimo

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{business_name}} — Business Intelligence Report</title>
  <style>
    /* CSS base de arriba (o el que defina el branding del usuario si lo dio) */
  </style>
</head>
<body>
  <div class="container">

    <header>
      <h1>{{business_name}} <span class="mode-badge">{{mode}}</span></h1>
      <p class="subtitle">{{date_min}} → {{date_max}} · Plataforma: {{platform}}</p>

      <div class="hero-grid">
        <div class="hero">
          <div class="hero-num">{{total_revenue}}</div>
          <div class="hero-lbl">Revenue</div>
          <div class="hero-trend">{{revenue_trend}} vs 3M anteriores</div>
        </div>
        <div class="hero">
          <div class="hero-num">{{total_orders}}</div>
          <div class="hero-lbl">Órdenes</div>
          <div class="hero-trend">{{orders_trend}} vs 3M anteriores</div>
        </div>
        <div class="hero">
          <div class="hero-num">{{unique_customers}}</div>
          <div class="hero-lbl">Clientes únicos</div>
          <div class="hero-trend">{{customers_trend}} vs 3M anteriores</div>
        </div>
        <div class="hero">
          <div class="hero-num">{{avg_ticket}}</div>
          <div class="hero-lbl">Ticket promedio</div>
          <div class="hero-trend">{{ticket_trend}} vs 3M anteriores</div>
        </div>
      </div>
    </header>

    <!-- Para cada categoría que tenga análisis ok: -->
    <section class="category">
      <h2>{{category_name}}</h2>

      <!-- Para cada análisis dentro de la categoría: -->
      <div class="analysis">
        <h3>{{analysis_name}}</h3>
        <!-- KPIs, tabla, chart según el análisis -->
        <p class="insight">{{actionable_insight}}</p>
      </div>

    </section>

    <footer>
      Reporte generado con
      <a href="https://github.com/mathiaschu/ecommerce-bi">ecommerce-bi</a>
      · creado por
      <a href="https://twitter.com/mathiaschu">@mathiaschu</a>
    </footer>

  </div>
</body>
</html>
```

---

## Adaptación al branding del usuario

Si el usuario provee uno o más de los siguientes, Claude debe respetarlo:

- **Colores corporativos** → sustituir `--accent` y los background emphasis.
- **Tipografía propia** → reemplazar `--font` por la family del usuario y agregar el `<link>` correspondiente.
- **Logo** → insertar como `<img>` en el header, arriba del título.
- **Modo dark** → adaptar `--bg`, `--text`, etc. invirtiendo la escala. Mantener contraste WCAG AA mínimo.

Si el usuario no da nada, **usar el default neutro de esta guía sin agregar identidad propia**.
