"""Escenario sintético para revisar las pantallas. No contiene datos del notebook."""

NAVIGATION = (
    ("resumen", "Resumen", "01"),
    ("movimientos", "Movimientos", "02"),
    ("sueldo", "Mi sueldo", "03"),
    ("presupuesto", "Presupuesto", "04"),
    ("ahorros", "Ahorros", "05"),
    ("obligaciones", "Préstamos y deudas", "06"),
    ("revision", "Revisar esta fase", "07"),
)

TRANSACTIONS = (
    {"date": "01 oct", "description": "Sueldo de octubre", "category": "Sueldo", "account": "Cuenta principal", "kind": "ingreso", "label": "Ingreso", "amount": 4000000},
    {"date": "02 oct", "description": "Arriendo de octubre", "category": "Vivienda", "account": "Cuenta principal", "kind": "gasto", "label": "Gasto", "amount": 850000},
    {"date": "05 oct", "description": "Compra de mercado", "category": "Alimentación", "account": "Cuenta principal", "kind": "gasto", "label": "Gasto", "amount": 260000},
    {"date": "06 oct", "description": "Transporte del mes", "category": "Transporte", "account": "Billetera", "kind": "gasto", "label": "Gasto", "amount": 120000},
    {"date": "08 oct", "description": "Servicios del mes", "category": "Servicios", "account": "Cuenta principal", "kind": "gasto", "label": "Gasto", "amount": 120000},
    {"date": "09 oct", "description": "Reserva para emergencias", "category": "Ahorro", "account": "Principal → Ahorros", "kind": "transferencia", "label": "Transferencia", "amount": 300000},
)

ACCOUNTS = (
    {"name": "Cuenta principal", "description": "Banco · uso diario", "amount": 1950000, "initial": "CP"},
    {"name": "Billetera", "description": "Pagos pequeños", "amount": 200000, "initial": "BI"},
    {"name": "Efectivo", "description": "Dinero en mano", "amount": 200000, "initial": "EF"},
    {"name": "Ahorros", "description": "Reserva separada", "amount": 300000, "initial": "AH"},
)

BUDGET = (
    {"name": "Vivienda", "spent": 850000, "limit": 900000},
    {"name": "Alimentación", "spent": 260000, "limit": 450000},
    {"name": "Transporte", "spent": 120000, "limit": 250000},
    {"name": "Servicios", "spent": 120000, "limit": 200000},
    {"name": "Otros", "spent": 0, "limit": 200000},
)
