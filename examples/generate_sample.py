#!/usr/bin/env python3
"""
Genera un CSV sintético en formato Tiendanube para usar como ejemplo del repo.

Output: examples/sample_orders.csv (~80 órdenes, 12 meses de histórico, 20 SKUs).
Datos verosímiles pero ficticios. NO usar en producción.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT = Path(__file__).parent / "sample_orders.csv"

PRODUCTS = [
    ("Remera Básica Negra - M",   "REM-NEG-M",   8500),
    ("Remera Básica Negra - L",   "REM-NEG-L",   8500),
    ("Remera Básica Blanca - M",  "REM-BLA-M",   8500),
    ("Remera Básica Blanca - L",  "REM-BLA-L",   8500),
    ("Buzo Oversize Gris - M",    "BUZ-GRI-M",  22000),
    ("Buzo Oversize Gris - L",    "BUZ-GRI-L",  22000),
    ("Buzo Oversize Negro - M",   "BUZ-NEG-M",  22000),
    ("Pantalón Jogger Negro - M", "PAN-NEG-M",  18500),
    ("Pantalón Jogger Negro - L", "PAN-NEG-L",  18500),
    ("Pantalón Jogger Gris - M",  "PAN-GRI-M",  18500),
    ("Gorra Trucker Negra",       "GOR-NEG",     6900),
    ("Gorra Trucker Beige",       "GOR-BEI",     6900),
    ("Riñonera Crossbody Negra",  "RIN-NEG",    12500),
    ("Medias Logo - Pack 3",      "MED-PK3",     4500),
    ("Camisa Lino Blanca - M",    "CAM-BLA-M",  19500),
    ("Camisa Lino Blanca - L",    "CAM-BLA-L",  19500),
    ("Short Surf Verde - M",      "SHO-VER-M",  14500),
    ("Short Surf Negro - M",      "SHO-NEG-M",  14500),
    ("Campera Puffer Negra - M",  "CAM-PUF-M",  45000),
    ("Sticker Pack",              "STK-001",     1500),
]

PROVINCIAS = [
    ("Buenos Aires", 0.42),
    ("Córdoba", 0.13),
    ("Santa Fe", 0.10),
    ("Mendoza", 0.07),
    ("Tucumán", 0.05),
    ("Salta", 0.04),
    ("Entre Ríos", 0.04),
    ("Neuquén", 0.04),
    ("Río Negro", 0.03),
    ("Chubut", 0.03),
    ("Misiones", 0.03),
    ("San Juan", 0.02),
]

CIUDADES = {
    "Buenos Aires": ["CABA", "La Plata", "San Isidro", "Mar del Plata", "Tigre", "Quilmes"],
    "Córdoba": ["Córdoba", "Villa Carlos Paz", "Río Cuarto"],
    "Santa Fe": ["Rosario", "Santa Fe", "Rafaela"],
    "Mendoza": ["Mendoza", "Godoy Cruz", "Maipú"],
    "Tucumán": ["San Miguel de Tucumán", "Yerba Buena"],
    "Salta": ["Salta"],
    "Entre Ríos": ["Paraná", "Concordia"],
    "Neuquén": ["Neuquén"],
    "Río Negro": ["Bariloche", "General Roca"],
    "Chubut": ["Comodoro Rivadavia", "Puerto Madryn"],
    "Misiones": ["Posadas"],
    "San Juan": ["San Juan"],
}

PAYMENT_METHODS = [
    ("Mercado Pago", 0.55),
    ("Transferencia bancaria", 0.20),
    ("Tarjeta de crédito Visa", 0.15),
    ("Tarjeta de crédito Mastercard", 0.08),
    ("Efectivo (Pago Fácil)", 0.02),
]

SHIPPING_METHODS = [
    ("Andreani estándar", 0.40),
    ("Correo Argentino estándar", 0.25),
    ("OCA estándar", 0.20),
    ("Retiro en local", 0.10),
    ("Cadete (CABA y GBA)", 0.05),
]

CHANNELS = [("web", 0.85), ("mobile", 0.13), ("pos", 0.02)]

# Clientes sintéticos. Emails en dominio @example.com (RFC 2606, reservado
# para ejemplos, no enviable). Teléfonos con prefijo +540000... obviamente ficticio.
# Si necesitás más realismo en tu propio sample, cambiá esta lista.
CUSTOMERS = [
    ("Cliente 01", "cliente01@example.com", "+5400011111101"),
    ("Cliente 02", "cliente02@example.com", "+5400011111102"),
    ("Cliente 03", "cliente03@example.com", "+5400011111103"),
    ("Cliente 04", "cliente04@example.com", "+5400011111104"),
    ("Cliente 05", "cliente05@example.com", "+5400011111105"),
    ("Cliente 06", "cliente06@example.com", "+5400011111106"),
    ("Cliente 07", "cliente07@example.com", "+5400011111107"),
    ("Cliente 08", "cliente08@example.com", "+5400011111108"),
    ("Cliente 09", "cliente09@example.com", "+5400011111109"),
    ("Cliente 10", "cliente10@example.com", "+5400011111110"),
    ("Cliente 11", "cliente11@example.com", "+5400011111111"),
    ("Cliente 12", "cliente12@example.com", "+5400011111112"),
    ("Cliente 13", "cliente13@example.com", "+5400011111113"),
    ("Cliente 14", "cliente14@example.com", "+5400011111114"),
    ("Cliente 15", "cliente15@example.com", "+5400011111115"),
    ("Cliente 16", "cliente16@example.com", "+5400011111116"),
    ("Cliente 17", "cliente17@example.com", "+5400011111117"),
    ("Cliente 18", "cliente18@example.com", "+5400011111118"),
    ("Cliente 19", "cliente19@example.com", "+5400011111119"),
    ("Cliente 20", "cliente20@example.com", "+5400011111120"),
    ("Cliente 21", "cliente21@example.com", "+5400011111121"),
    ("Cliente 22", "cliente22@example.com", "+5400011111122"),
    ("Cliente 23", "cliente23@example.com", "+5400011111123"),
    ("Cliente 24", "cliente24@example.com", "+5400011111124"),
    ("Cliente 25", "cliente25@example.com", "+5400011111125"),
]


def weighted_choice(pairs):
    items, weights = zip(*pairs)
    return random.choices(items, weights=weights, k=1)[0]


def random_date_in_range(start, end):
    delta = (end - start).total_seconds()
    return start + timedelta(seconds=random.uniform(0, delta))


def fmt_date(dt):
    return dt.strftime("%d/%m/%Y %H:%M")


COLUMNS = [
    "Número de orden", "Email", "Fecha", "Estado de la orden", "Estado del pago",
    "Estado del envío", "Moneda", "Subtotal de productos", "Descuento",
    "Costo de envío", "Total", "Nombre del comprador", "Teléfono",
    "Dirección", "Ciudad", "Provincia o estado", "País", "Código postal",
    "Medio de envío", "Medio de pago", "Cupón de descuento", "Fecha de pago",
    "Fecha de envío", "Nombre del producto", "Precio del producto",
    "Cantidad del producto", "SKU", "Canal", "Fecha y hora de cancelación",
    "Motivo de cancelación",
]


def generate():
    rows = []
    start_date = datetime(2025, 5, 15)
    end_date = datetime(2026, 5, 15)

    order_seq = 1001
    for _ in range(80):
        order_date = random_date_in_range(start_date, end_date)
        customer = random.choice(CUSTOMERS)
        province = weighted_choice(PROVINCIAS)
        city = random.choice(CIUDADES[province])
        payment_method = weighted_choice(PAYMENT_METHODS)
        shipping_method = weighted_choice(SHIPPING_METHODS)
        channel = weighted_choice(CHANNELS)

        # Decidir cuántos productos tiene la orden
        n_items = random.choices([1, 2, 3, 4], weights=[0.55, 0.27, 0.13, 0.05])[0]
        chosen = random.sample(PRODUCTS, min(n_items, len(PRODUCTS)))

        line_items = []
        subtotal = 0.0
        for prod_name, sku, price in chosen:
            qty = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03])[0]
            line_items.append((prod_name, sku, price, qty))
            subtotal += price * qty

        # Descuento ocasional
        if random.random() < 0.18:
            discount_pct = random.choice([0.10, 0.15, 0.20])
            discount = round(subtotal * discount_pct, 2)
            coupon = random.choice(["WELCOME10", "FREESHIP", "VIP15", "SALE20"])
        else:
            discount = 0.0
            coupon = ""

        # Envío
        if shipping_method == "Retiro en local":
            shipping_cost = 0.0
        elif province == "Buenos Aires":
            shipping_cost = round(random.uniform(2500, 4500), 2)
        else:
            shipping_cost = round(random.uniform(4500, 7500), 2)

        total = subtotal - discount + shipping_cost

        # Estado de la orden
        if random.random() < 0.07:
            status = "Cancelada"
            payment_status = "Reembolsado" if random.random() < 0.5 else "Pendiente"
            shipping_status = "Sin envío"
            cancel_date = fmt_date(order_date + timedelta(hours=random.randint(1, 48)))
            cancel_reason = random.choice([
                "Cambio de opinión", "Error en el pedido", "Stock no disponible",
                "Demora en el envío", "Producto duplicado"
            ])
            payment_date = ""
            shipping_date = ""
        else:
            status = "Cerrada"
            payment_status = "Pagado"
            shipping_status = "Entregado" if random.random() < 0.85 else "Despachado"
            cancel_date = ""
            cancel_reason = ""
            payment_date = fmt_date(order_date + timedelta(hours=random.randint(0, 24)))
            ship_offset = random.randint(1, 6)
            shipping_date = fmt_date(order_date + timedelta(days=ship_offset))

        order_id = f"#{order_seq}"
        order_seq += 1
        name, email, phone = customer
        address = f"Calle Falsa {random.randint(100, 9999)}"
        zip_code = str(random.randint(1000, 9999))

        # Una línea por producto
        for prod_name, sku, price, qty in line_items:
            rows.append({
                "Número de orden": order_id,
                "Email": email,
                "Fecha": fmt_date(order_date),
                "Estado de la orden": status,
                "Estado del pago": payment_status,
                "Estado del envío": shipping_status,
                "Moneda": "ARS",
                "Subtotal de productos": f"{subtotal:.2f}",
                "Descuento": f"{discount:.2f}",
                "Costo de envío": f"{shipping_cost:.2f}",
                "Total": f"{total:.2f}",
                "Nombre del comprador": name,
                "Teléfono": phone,
                "Dirección": address,
                "Ciudad": city,
                "Provincia o estado": province,
                "País": "Argentina",
                "Código postal": zip_code,
                "Medio de envío": shipping_method,
                "Medio de pago": payment_method,
                "Cupón de descuento": coupon,
                "Fecha de pago": payment_date,
                "Fecha de envío": shipping_date,
                "Nombre del producto": prod_name,
                "Precio del producto": f"{price:.2f}",
                "Cantidad del producto": str(qty),
                "SKU": sku,
                "Canal": channel,
                "Fecha y hora de cancelación": cancel_date,
                "Motivo de cancelación": cancel_reason,
            })

    # Clientes repetidos: re-asignar el mismo email a varias órdenes ya generadas
    # para garantizar análisis de cohortes/recompra
    # (ya implícito por random.choice repetido de CUSTOMERS)

    with open(OUTPUT, "w", encoding="latin-1", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, delimiter=";")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Generated {len(rows)} line items across ~80 orders → {OUTPUT}")


if __name__ == "__main__":
    generate()
