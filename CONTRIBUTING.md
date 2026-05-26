# Contribuir a ecommerce-bi

Gracias por querer aportar. Esta skill busca ser una herramienta de Business Intelligence simple, robusta y abierta para análisis de eCommerce.

## Cómo contribuir

### Reportar bugs

Abrí un issue describiendo:

1. Qué pasó vs. qué esperabas.
2. Plataforma del CSV (Tiendanube, Shopify, WooCommerce, genérico).
3. Modo (`lite` o `full`) y comando exacto que corriste.
4. Stack trace si hay error (corré con `python3 -u scripts/bi_analysis.py ...` para output sin buffer).
5. Si podés, un CSV mínimo reproducible (3-5 órdenes anonimizadas).

### Pedir un nuevo análisis

Antes de abrir un PR, abrí un issue con la propuesta:

- **Qué responde** el análisis (en una línea).
- **Columnas que necesita** del set canónico.
- **Output esperado** (forma del JSON).
- **Insight accionable**: qué tendría que hacer el merchant con el resultado.

Si la propuesta encaja, podés mandar el PR.

### Agregar soporte para otra plataforma

1. Identificá un "fingerprint" de 3-4 columnas únicas del export.
2. Agregalo a `PLATFORM_FINGERPRINTS` en `scripts/bi_analysis.py`.
3. Agregá el mapeo de columnas en `COLUMN_MAPS` (a los nombres canónicos: ver `references/csv_mapping.md`).
4. Documentá la plataforma nueva en `references/csv_mapping.md` con el mismo formato que las existentes.
5. Pegá un CSV de muestra en `examples/` (mínimo 10 órdenes, datos anonimizados o sintéticos).

### Estilo de código

- Python: idiomatic pandas. Evitar loops cuando hay vectorización.
- Cada función de análisis debe seguir el patrón `analysis_NN_<name>(df, **kwargs) -> dict` y devolver `{"status": "ok"|"skipped"|"error", "data": {...}, "insight": "..."}`.
- Si una columna requerida falta, devolver `{"status": "skipped", "reason": "missing column X"}`. Nunca hacer raise — el script debe terminar siempre con código 0 mientras pueda leer el CSV.
- Los textos del JSON van en español (insights, motivos de skip, etc.) porque el HTML los renderiza directo.

## Pull Requests

- Una feature/fix por PR.
- Incluir descripción de qué cambia y por qué.
- Si tocás `bi_analysis.py`, correr la skill contra `examples/sample_orders.csv` y pegar el output como check.
- Actualizar `SKILL.md`, `references/analysis_catalog.md` y `references/required_columns.md` si agregás o cambiás un análisis.

## Filosofía

- **Privacidad primero**: el script no manda datos a ningún servicio externo.
- **Falla suave**: si falta una columna, skipear el análisis con motivo, no romper todo el informe.
- **Insights, no descripciones**: el HTML no es un dashboard, es un informe. Cada bloque tiene que decir qué hacer con el dato.
- **Sin dependencias mágicas**: solo `pandas` y `numpy`. Nada que requiera GPU, API keys ni servicios cloud.
