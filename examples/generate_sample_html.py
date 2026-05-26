#!/usr/bin/env python3
"""
Renderiza el JSON de bi_analysis.py como un HTML standalone.

Útil para:
- Generar el sample_report.html del repo.
- Tener una vista rápida si no usás Claude Code para armar el HTML branded.

Uso: python3 examples/generate_sample_html.py [json_input] [html_output]
Defaults: examples/sample_results.json → examples/sample_report.html
"""

import json
import sys
from pathlib import Path

JSON_IN = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "sample_results.json"
HTML_OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "sample_report.html"


def money(v):
    if v is None:
        return "—"
    return f"${v:,.0f}".replace(",", ".")


def pct(v, digits=1):
    if v is None:
        return "—"
    return f"{v:.{digits}f}%"


def num(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:,.1f}".replace(",", ".")
    return f"{v:,}".replace(",", ".")


def trend_badge(v):
    if v is None:
        return ""
    arrow = "↑" if v > 0 else "↓" if v < 0 else "→"
    color = "var(--green)" if v > 0 else "var(--red)" if v < 0 else "var(--text-muted)"
    return f'<span style="color:{color};font-weight:600;">{arrow} {abs(v):.1f}%</span>'


# ──────────────────────────────────────────────────────────────────────────────
# Renderers — uno por análisis
# ──────────────────────────────────────────────────────────────────────────────

def render_1_market_basket(d):
    rows = "".join(
        f"<tr><td>{' + '.join(p['items'])}</td><td>{p['count']}</td>"
        f"<td>{p['support']:.1f}%</td><td>{p['confidence']:.1f}%</td>"
        f"<td><b>{p['lift']:.2f}×</b></td></tr>"
        for p in d.get("pairs", [])[:10]
    )
    return f"""
    <p class="kpi-row">
      <span><b>{d.get('multi_product_orders', 0)}</b> órdenes multi-producto ({d.get('multi_product_pct', 0):.1f}% del total)</span>
    </p>
    <table>
      <thead><tr><th>Combo</th><th>Veces</th><th>Support</th><th>Confidence</th><th>Lift</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="5">Sin pares con lift > 1.0</td></tr>'}</tbody>
    </table>
    <p class="insight">Bundles con lift &gt; 2 son candidatos naturales a packs o cross-sell en PDP.</p>
    """


def render_2_category_affinity(d):
    rows = "".join(
        f"<tr><td>{' + '.join(p['items'])}</td><td>{p['support']:.1f}%</td><td>{p['lift']:.2f}×</td></tr>"
        for p in d.get("pairs", [])[:8]
    )
    return f"""<table>
      <thead><tr><th>Categorías combinadas</th><th>Support</th><th>Lift</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="3">Sin afinidad significativa</td></tr>'}</tbody>
    </table>
    <p class="insight">Categorías que se combinan son material para landings y colecciones cruzadas.</p>"""


def render_3_ranking(d):
    rows = "".join(
        f"<tr><td>{p['product_name']}</td><td>{money(p['revenue'])}</td>"
        f"<td>{num(p['units'])}</td><td>{money(p.get('avg_price'))}</td>"
        f"<td>{trend_badge(p.get('trend_pct'))}</td></tr>"
        for p in d.get("products", [])[:10]
    )
    return f"""<table>
      <thead><tr><th>Producto</th><th>Revenue</th><th>Unidades</th><th>Precio prom.</th><th>Tendencia</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="insight">Detectar héroes (top revenue) y estrellas emergentes (top tendencia) — push diferenciado.</p>"""


def render_4_anchors(d):
    rows = "".join(
        f"<tr><td>{a['product_name']}</td><td>{a['multi_order_count']}</td>"
        f"<td>Top co-producto: {a['top_co_products'][0]['name']} ({a['top_co_products'][0]['count']}×)</td></tr>"
        for a in d.get("anchors", [])[:10] if a.get("top_co_products")
    )
    return f"""<table>
      <thead><tr><th>Producto ancla</th><th>Apariciones en multi-orden</th><th>Mejor co-compra</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="3">Datos insuficientes</td></tr>'}</tbody>
    </table>
    <p class="insight">Productos ancla son drivers de cross-sell — exhibirlos primero acelera el AOV.</p>"""


def render_5_long_tail(d):
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{d['products_80_pct']}</div><div class="stat-lbl">SKUs hacen el 80% del revenue</div></div>
      <div class="stat"><div class="stat-num">{d['pct_products_80']:.1f}%</div><div class="stat-lbl">del catálogo</div></div>
      <div class="stat"><div class="stat-num">{d['total_products']}</div><div class="stat-lbl">SKUs totales</div></div>
    </div>
    <p class="insight">Concentración Pareto. Si pocos SKUs hacen casi todo el revenue, revisar inversión de stock en el long tail.</p>"""


def render_6_cancellation_product(d):
    rows = "".join(
        f"<tr><td>{p['product_name']}</td><td>{num(p['total_orders'])}</td>"
        f"<td>{p['cancel_rate']:.1f}%</td><td>{trend_badge(p['cancel_rate'] - d['overall_cancel_rate'])}</td></tr>"
        for p in d.get("flagged_products", [])[:10]
    )
    return f"""<p>Tasa global de cancelación: <b>{d['overall_cancel_rate']:.1f}%</b></p>
    <table>
      <thead><tr><th>Producto</th><th>Órdenes</th><th>Tasa cancel.</th><th>vs media</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="4">Sin productos con cancelación anómala</td></tr>'}</tbody>
    </table>"""


def render_7_rfm(d):
    rows = "".join(
        f"<tr><td>{s['segment']}</td><td>{s['count']}</td><td>{s['pct']:.1f}%</td>"
        f"<td>{money(s.get('avg_monetary'))}</td></tr>"
        for s in d.get("segments", [])
    )
    return f"""<p>Total clientes segmentados: <b>{d['total_customers']}</b></p>
    <table>
      <thead><tr><th>Segmento</th><th>Clientes</th><th>%</th><th>Revenue prom.</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="insight">Champions y Loyal sostienen el negocio. At Risk y About to Sleep son ventana de reactivación.</p>"""


def render_8_clv(d):
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{money(d['avg_clv'])}</div><div class="stat-lbl">CLV promedio (3 años)</div></div>
      <div class="stat"><div class="stat-num">{money(d['median_clv'])}</div><div class="stat-lbl">CLV mediano</div></div>
      <div class="stat"><div class="stat-num">{num(d['avg_orders'])}</div><div class="stat-lbl">Órdenes prom. por cliente</div></div>
    </div>
    <p class="insight">El gap entre promedio y mediana indica concentración. Top 10% suele 3-5× la mediana.</p>"""


def render_9_cohorts(d):
    months_shown = 6
    rows = []
    for cohort in d.get("cohort_matrix", [])[-8:]:
        cells = "".join(
            f'<td style="background:rgba(228,255,90,{(cohort.get(f"m{i}", 0) or 0) / 100 * 0.5});">{(cohort.get(f"m{i}") or 0):.0f}%</td>'
            for i in range(months_shown)
        )
        rows.append(f"<tr><td><b>{cohort['cohort']}</b></td>{cells}</tr>")
    headers = "".join(f"<th>M{i}</th>" for i in range(months_shown))
    return f"""<table>
      <thead><tr><th>Cohorte</th>{headers}</tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <p>Retención promedio: <b>{d.get('avg_retention', 0):.1f}%</b></p>
    <p class="insight">Comparar la curva de cohortes nuevas vs viejas — caída en M1 es síntoma de onboarding débil.</p>"""


def render_10_repurchase(d):
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{d['repurchase_rate']:.1f}%</div><div class="stat-lbl">Tasa de recompra</div></div>
      <div class="stat"><div class="stat-num">{num(d['time_between_purchases'].get('median'))}</div><div class="stat-lbl">Días entre compras (mediana)</div></div>
      <div class="stat"><div class="stat-num">{num(d['repeat_customers'])}</div><div class="stat-lbl">Clientes recurrentes</div></div>
    </div>
    <p class="insight">Si la mediana entre compras &gt; 90 días, las automations de retención no se están disparando bien.</p>"""


def render_11_monthly(d):
    rows = "".join(
        f"<tr><td>{m['month']}</td><td>{money(m['revenue'])}</td>"
        f"<td>{num(m['orders'])}</td><td>{money(m['aov'])}</td></tr>"
        for m in d.get("monthly", [])
    )
    return f"""<p>Total: <b>{money(d['total_revenue'])}</b> en <b>{num(d['total_orders'])}</b> órdenes</p>
    <table>
      <thead><tr><th>Mes</th><th>Revenue</th><th>Órdenes</th><th>AOV</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def render_12_aov(d):
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{money(d['overall_aov'])}</div><div class="stat-lbl">AOV global</div></div>
      <div class="stat"><div class="stat-num">{money(d['median_aov'])}</div><div class="stat-lbl">AOV mediano</div></div>
    </div>
    <p class="insight">Si AOV mediano &lt;&lt; AOV promedio hay órdenes outlier que distorsionan: limpiar antes de tomar decisiones de pricing.</p>"""


def render_13_revenue_category(d):
    rows = "".join(
        f"<tr><td>{c['category']}</td><td>{money(c['revenue'])}</td>"
        f"<td>{c['pct']:.1f}%</td><td>{num(c['units'])}</td></tr>"
        for c in d.get("categories", [])[:10]
    )
    return f"""<table>
      <thead><tr><th>Categoría</th><th>Revenue</th><th>% Mix</th><th>Unidades</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def render_14_discounts(d):
    comp = d.get("comparison", {})
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{pct(comp.get('with_discount_pct', 0))}</div><div class="stat-lbl">Órdenes con descuento</div></div>
      <div class="stat"><div class="stat-num">{money(comp.get('aov_with', 0))}</div><div class="stat-lbl">AOV con cupón</div></div>
      <div class="stat"><div class="stat-num">{money(comp.get('aov_without', 0))}</div><div class="stat-lbl">AOV sin cupón</div></div>
    </div>
    <p class="insight">Si AOV con cupón &lt; AOV sin cupón, el descuento canibaliza margen sin aumentar valor.</p>"""


def render_15_provinces(d):
    rows = "".join(
        f"<tr><td>{p['state']}</td><td>{money(p['revenue'])}</td>"
        f"<td>{num(p['orders'])}</td><td>{money(p['aov'])}</td></tr>"
        for p in d.get("provinces", [])[:12]
    )
    return f"""<table>
      <thead><tr><th>Provincia</th><th>Revenue</th><th>Órdenes</th><th>AOV</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="insight">Top provincias absorben pauta. Provincias con AOV alto y volumen bajo son targets a escalar.</p>"""


def render_16_shipping(d):
    return f"""<p>Costo medio de envío: <b>{money(d['overall_avg_shipping'])}</b></p>
    <p>% órdenes con envío gratis: <b>{pct(d['overall_free_pct'])}</b></p>
    <p class="insight">Costos de envío altos por provincia explican abandono geográfico.</p>"""


def render_17_cancellation(d):
    rows = "".join(f"<tr><td>{r['reason']}</td><td>{num(r['count'])}</td><td>{pct(r['pct'])}</td></tr>"
                   for r in d.get("reasons", [])[:8])
    return f"""<div class="stat-grid">
      <div class="stat"><div class="stat-num">{pct(d['cancel_rate'])}</div><div class="stat-lbl">Tasa cancelación</div></div>
      <div class="stat"><div class="stat-num">{num(d['cancelled_orders'])}</div><div class="stat-lbl">Órdenes canceladas</div></div>
      <div class="stat"><div class="stat-num">{num(d['total_orders'])}</div><div class="stat-lbl">Órdenes totales</div></div>
    </div>
    <table>
      <thead><tr><th>Motivo</th><th>Cuenta</th><th>%</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def render_18_payment(d):
    rows = "".join(
        f"<tr><td>{p['method']}</td><td>{num(p['orders'])}</td>"
        f"<td>{pct(p['orders_pct'])}</td><td>{money(p['revenue'])}</td></tr>"
        for p in d.get("payment_methods", [])
    )
    return f"""<table>
      <thead><tr><th>Medio</th><th>Órdenes</th><th>% Mix</th><th>Revenue</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def render_19_bundling(d):
    rows = "".join(
        f"<tr><td>{' + '.join(b['items'])}</td><td>{money(b.get('avg_combined_price', 0))}</td>"
        f"<td>{b['lift']:.2f}×</td></tr>"
        for b in d.get("bundles", [])[:8]
    )
    return f"""<table>
      <thead><tr><th>Bundle propuesto</th><th>Precio combinado</th><th>Lift</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="3">Sin bundles candidatos</td></tr>'}</tbody>
    </table>
    <p class="insight">Lift &gt; 2 + precio combinado interesante = pack con descuento moderado.</p>"""


def render_20_seasonality(d):
    rows_dow = "".join(f"<tr><td>{x['day']}</td><td>{money(x['revenue'])}</td></tr>"
                       for x in d.get("by_day_of_week", []))
    return f"""<p>Mes pico: <b>{d.get('peak_month', '—')}</b> · Mes valle: <b>{d.get('low_month', '—')}</b></p>
    <p>Día pico: <b>{d.get('peak_day', '—')}</b></p>
    <table>
      <thead><tr><th>Día semana</th><th>Revenue</th></tr></thead>
      <tbody>{rows_dow}</tbody>
    </table>
    <p class="insight">Programar campañas en valles y pauta agresiva en picos.</p>"""


def render_39_retention_gateway(d):
    baseline = d.get("global_repurchase_rate", 0)
    rows = "".join(
        f"<tr><td>{p['product_name']}</td><td>{num(p['first_purchase_customers'])}</td>"
        f"<td>{num(p['repeaters'])}</td><td><b>{p['retention_rate']:.1f}%</b></td>"
        f"<td>{p['lift_vs_baseline']:.2f}×</td></tr>"
        for p in d.get("products", [])[:12]
    )
    top = d.get("top_product")
    top_line = (
        f"Mejor gateway: <b>{top['product_name']}</b> — "
        f"{top['retention_rate']:.1f}% de retención vs {baseline:.1f}% global "
        f"(lift {top['lift_vs_baseline']:.2f}×)."
        if top else "Sin productos calificados."
    )
    return f"""<p class="kpi-row">Baseline global de recompra: <b>{baseline:.1f}%</b> · Muestra mínima por producto: {d.get('min_sample_size', 0)} clientes · Productos calificados: {d.get('qualified_products', 0)}</p>
    <table>
      <thead><tr><th>Producto</th><th>Clientes 1ra compra</th><th>Volvieron</th><th>Tasa retención</th><th>Lift vs baseline</th></tr></thead>
      <tbody>{rows or '<tr><td colspan="5">Sin productos con muestra suficiente</td></tr>'}</tbody>
    </table>
    <p class="insight">{top_line} Empujar los productos con lift &gt; 1.3 en pauta de adquisición rinde más que el best-seller absoluto: capturan clientes que vuelven, no solo ventas one-shot.</p>"""


RENDERERS = {
    1: render_1_market_basket,
    2: render_2_category_affinity,
    3: render_3_ranking,
    4: render_4_anchors,
    5: render_5_long_tail,
    6: render_6_cancellation_product,
    7: render_7_rfm,
    8: render_8_clv,
    9: render_9_cohorts,
    10: render_10_repurchase,
    11: render_11_monthly,
    12: render_12_aov,
    13: render_13_revenue_category,
    14: render_14_discounts,
    15: render_15_provinces,
    16: render_16_shipping,
    17: render_17_cancellation,
    18: render_18_payment,
    19: render_19_bundling,
    20: render_20_seasonality,
    39: render_39_retention_gateway,
}


# ──────────────────────────────────────────────────────────────────────────────
# Layout
# ──────────────────────────────────────────────────────────────────────────────

CSS = """
:root {
  --bg: #0a0a0a;
  --bg-card: #141414;
  --border: #262626;
  --text: #f5f5f5;
  --text-muted: #a3a3a3;
  --text-dim: #737373;
  --lime: #E4FF5A;
  --blue: #3346FF;
  --green: #22c55e;
  --red: #ef4444;
  --font: 'Geist', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-weight: 400;
  line-height: 1.5;
  padding: 48px 24px;
  background-image:
    radial-gradient(circle at 20% 10%, rgba(228,255,90,0.04), transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(51,70,255,0.04), transparent 50%);
}
.container { max-width: 1100px; margin: 0 auto; }
header { margin-bottom: 64px; padding-bottom: 32px; border-bottom: 1px solid var(--border); }
.brand { color: var(--lime); font-size: 14px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; }
h1 { font-size: 48px; font-weight: 700; margin: 12px 0 8px; letter-spacing: -0.02em; }
.subtitle { color: var(--text-muted); font-size: 16px; }
.mode-badge {
  display: inline-block; background: var(--lime); color: #000;
  font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
  padding: 4px 10px; border-radius: 4px; margin-left: 8px; vertical-align: middle;
}
.hero-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 32px;
}
.hero {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 8px; padding: 20px;
}
.hero-num { font-size: 32px; font-weight: 700; color: var(--lime); }
.hero-lbl { color: var(--text-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
.hero-trend { font-size: 12px; margin-top: 8px; }
section.category { margin: 72px 0 32px; }
section.category h2 {
  font-size: 12px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.2em; color: var(--lime); margin-bottom: 24px;
  border-top: 1px solid var(--border); padding-top: 32px;
}
.analysis { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 28px; margin-bottom: 16px; }
.analysis h3 { font-size: 20px; font-weight: 600; margin-bottom: 16px; }
.analysis h3 .num { color: var(--text-dim); margin-right: 8px; font-weight: 400; }
.kpi-row { color: var(--text-muted); font-size: 14px; margin-bottom: 12px; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 16px 0; }
.stat { background: rgba(228,255,90,0.04); border: 1px solid rgba(228,255,90,0.15); border-radius: 6px; padding: 14px; }
.stat-num { font-size: 22px; font-weight: 700; color: var(--lime); }
.stat-lbl { color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }
table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
th { color: var(--text-dim); font-weight: 500; text-transform: uppercase; font-size: 11px; letter-spacing: 0.08em; }
td b { color: var(--lime); }
.insight {
  background: rgba(228,255,90,0.06); border-left: 2px solid var(--lime);
  padding: 12px 16px; margin-top: 16px; color: var(--text); font-size: 14px; line-height: 1.5;
}
footer { text-align: center; color: var(--text-dim); font-size: 12px; padding: 48px 0 0; border-top: 1px solid var(--border); margin-top: 64px; }
footer a { color: var(--lime); text-decoration: none; }
"""

CATEGORY_ORDER = ["Producto", "Cliente", "Revenue", "Geográfico", "Operativo", "Estratégico"]


def main():
    with open(JSON_IN, encoding="utf-8") as f:
        data = json.load(f)

    summary = data["summary"]
    analyses = data["analyses"]

    # Hero block
    hero_cards = f"""
      <div class="hero"><div class="hero-num">{money(summary['total_revenue'])}</div>
        <div class="hero-lbl">Revenue</div>
        <div class="hero-trend">{trend_badge(summary['trends'].get('revenue'))} vs 3M anteriores</div></div>
      <div class="hero"><div class="hero-num">{num(summary['total_orders'])}</div>
        <div class="hero-lbl">Órdenes</div>
        <div class="hero-trend">{trend_badge(summary['trends'].get('orders'))} vs 3M anteriores</div></div>
      <div class="hero"><div class="hero-num">{num(summary['unique_customers'])}</div>
        <div class="hero-lbl">Clientes únicos</div>
        <div class="hero-trend">{trend_badge(summary['trends'].get('customers'))} vs 3M anteriores</div></div>
      <div class="hero"><div class="hero-num">{money(summary['avg_ticket'])}</div>
        <div class="hero-lbl">Ticket promedio</div>
        <div class="hero-trend">{trend_badge(summary['trends'].get('ticket'))} vs 3M anteriores</div></div>
    """

    # Group analyses by category
    by_cat = {cat: [] for cat in CATEGORY_ORDER}
    for k, v in analyses.items():
        cat = v.get("category", "Otros")
        if cat in by_cat:
            by_cat[cat].append((int(k), v))

    sections = []
    for cat in CATEGORY_ORDER:
        items = sorted(by_cat[cat], key=lambda x: x[0])
        if not items:
            continue
        blocks = []
        for num_id, a in items:
            d = a.get("data", {})
            if d.get("status") == "skipped":
                blocks.append(
                    f'<div class="analysis"><h3><span class="num">#{num_id}</span>{a["name"]}</h3>'
                    f'<p class="kpi-row">Análisis omitido: {d.get("reason", "datos insuficientes")}</p></div>'
                )
                continue
            try:
                body = RENDERERS[num_id](d)
            except Exception as e:
                body = f'<p class="kpi-row">Error al renderizar: {e}</p>'
            blocks.append(
                f'<div class="analysis"><h3><span class="num">#{num_id}</span>{a["name"]}</h3>{body}</div>'
            )
        sections.append(f'<section class="category"><h2>{cat}</h2>{"".join(blocks)}</section>')

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BI Report — Sample · ecommerce-bi</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">ecommerce-bi · sample</div>
      <h1>Business Intelligence Report <span class="mode-badge">{data['mode'].upper()}</span></h1>
      <p class="subtitle">Tienda sintética · {summary['date_min']} → {summary['date_max']} · Plataforma: {summary['platform']}</p>
      <div class="hero-grid">{hero_cards}</div>
    </header>
    {"".join(sections)}
    <footer>
      Generado por <a href="https://github.com/mathiaschu/ecommerce-bi">ecommerce-bi</a> ·
      Datos sintéticos (sample del repo) · Datos no representan ninguna tienda real
    </footer>
  </div>
</body>
</html>
"""
    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"HTML generated: {HTML_OUT}")


if __name__ == "__main__":
    main()
