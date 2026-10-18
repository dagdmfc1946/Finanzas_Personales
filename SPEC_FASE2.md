# Fase 2: base local y movimientos por actividad

Alcance autorizado por el usuario tras aprobar el plan. Esta especificación concreta el incremento; la entrega seguirá pendiente de su revisión ejecutable. La integración bancaria está cancelada. No se importará la referencia privada sin una instrucción expresa.

## Decisiones

- Un usuario local creado por el propio usuario en el primer acceso; contraseña validada y almacenada por Django como hash, sesiones del servidor y CSRF. La configuración inicial se cierra tras crear el primer usuario. Sin panel de administración público, recuperación por correo ni registro de terceros.
- SQLite persistente en `data/finanzas.sqlite3`; secreto local estable en `local/secret.key`. Datos, secretos y respaldos excluidos de Git. El acceso protege la interfaz; los archivos locales no están cifrados por esta entrega y dependen de la protección de Windows.
- Actividades configurables, cuentas y categorías pertenecen al usuario. Una actividad por origen y destino del movimiento; no se reparten gastos entre varias actividades en este incremento.
- Importes exactos en centavos enteros. Entradas positivas con máximo de dos decimales; ingresos, gastos, saldos iniciales y transferencias tienen efectos explícitos. Saldo inicial no se cuenta como ingreso del período. No se prohíben saldos negativos: se muestran para no ocultar movimientos históricos ni prometer conciliación bancaria.
- Una transferencia enlaza cuenta/actividad de origen y cuenta/actividad de destino. Puede mover asignación entre actividades de una misma cuenta, pero no puede ser idéntica en ambos extremos. Consolidado sin ingreso/gasto ficticio; vista filtrada muestra saldo asignado, no un nuevo saldo bancario.
- Corrección con control de versión del registro; dos ediciones concurrentes no se sobrescriben silenciosamente. Anulación mediante POST, confirmación y motivo; se conserva historial y no se elimina desde la interfaz.
- Copia JSON con versión de formato, huella SHA-256 y entidades financieras. Restaura por transacción con validaciones y copia previa; conserva el usuario y la contraseña actuales. No se utiliza pickle, SQL aportado por archivos ni deserialización de modelos arbitrarios. La huella detecta daños, no acredita el origen: solo restaurar copias propias de confianza.
- Mantener la demostración ficticia separada de los datos personales. Las secciones de sueldo, presupuesto, ahorro y obligaciones siguen siendo referencia de fases futuras. Revisar esta fase permanece disponible.

## Entregas verificables

1. Acceso protegido y almacenamiento local: primer usuario, inicio/cierre de sesión, aislamiento por propietario y migraciones.
2. Actividades, cuentas y categorías; movimientos, transferencias, filtros y resumen. Datos vacíos al instalar; ningún importe real o ficticio se mezcla automáticamente.
3. Correcciones, anulaciones, historial y respaldo/restauración básica. Formularios y estados vacíos ejecutables, usando la identidad oscura/turquesa existente y mayor legibilidad.

## Verificación

Pruebas de permisos, CSRF, primer acceso cerrado, propiedad cruzada, precisión, transferencias entre actividades/cuentas, saldos iniciales, ediciones obsoletas, anulación, filtros y restauración íntegra/dañada. Ejecución en navegador con atención al primer acceso y a los límites de revisión automatizada; el usuario creará sus credenciales reales.

Comandos: `.venv\Scripts\python.exe manage.py test`, `.venv\Scripts\python.exe -m unittest test_iniciar`, `.venv\Scripts\python.exe manage.py check`, `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`.

La restauración y las migraciones se prueban con bases de ensayo. No se reducirán pruebas para ocultar regresiones. Manual y proceso se actualizan con el flujo real. Commits locales en español; nuevos cambios de implementación sin push hasta autorización del usuario.

Fuentes: documentación Django 5.2 sobre autenticación, formularios y transacciones; biblioteca estándar Python para JSON y SHA-256. Bibliotecas ya instaladas; no se añade otro framework ni motor.
