# Fase 3 — sueldo y planificación

Inicio expresamente autorizado por el usuario. Se conserva el alcance del plan de cinco fases. Implementación incremental con entrega ejecutable y revisión, sin publicación de código nuevo automática.

## Capacidades y orden

| Incremento | Capacidad | Depende de |
|---|---|---|
| 3.1 | Sueldo previsto y cobros vinculados | Movimientos de Fase 2 |
| 3.2 | Presupuestos mensuales, proyectos y compras con partidas/tope/plazo/actividad | 3.1 y movimientos |
| 3.3 | Recurrencias y suscripciones; comparar previsto, comprometido y realizado | 3.2 |

## Contrato del incremento 3.1

- El usuario registra un sueldo previsto por actividad. Modalidad neta o detalle manual: bruto + adicionales − deducciones = neto positivo, con centavos exactos. No se calculan retenciones fiscales ni nómina legal.
- Mes trabajado, fecha esperada de cobro y mes presupuestado son independientes. Los meses se almacenan por su primer día. No se impone que el cobro ocurra en el mismo mes trabajado o presupuestado.
- Un sueldo previsto no crea movimientos ni modifica saldos. Se muestran previsto, cobros vinculados vigentes, pendiente y exceso; no se presenta la proyección como saldo bancario.
- El cobro se registra como ingreso en Movimientos y se vincula después. Varios ingresos pueden representar pagos parciales de un sueldo; cada ingreso se vincula a un único sueldo. Vincular no crea ni copia el ingreso. Cuenta, importe y fecha reales proceden del movimiento existente.
- Solo ingresos propios de la misma actividad. No se vinculan anulados; si un ingreso ya vinculado se anula, deja de contar como recibido sin borrar su historial. Corregirlo mantiene el cálculo al día; no puede cambiar a gasto/transferencia ni a otra actividad mientras exista vínculo.
- Se permite desvincular con motivo para corregir una clasificación; esto no anula el ingreso. No hay borrado de sueldos: pueden excluirse de previsiones, conservando sus cobros. Ediciones requieren motivo y control de versión; trazabilidad en el historial existente.
- Resumen mensual por mes presupuestado y actividad, con los cobros vinculados independientemente de su fecha real, que siempre se muestra para evitar confundir períodos.
- Formularios protegidos por acceso local/CSRF y propiedad. Sin credenciales predeterminadas ni importación del notebook o sus valores privados.
- Respaldos incluyen sueldos y vínculos. Formato nuevo con compatibilidad de lectura para copias de Fase 2; restaurar una copia antigua sustituye los datos financieros e incluye dejar vacía la planificación ausente. Se crea copia previa y la restauración es transaccional.

## Verificación y entrega

Pruebas de detalle neto, importes, meses, pertenencia, vínculos repetidos/parciales, anulación/corrección de ingresos, ediciones obsoletas, desvinculación, protección de acceso y restauración nueva/antigua. Revisión visual en base de ensayo aislada; nunca crear credenciales personales del usuario. Manual actualizado y Revisar esta fase refleja el incremento vigente y sus límites.

Este primer incremento inicia Fase 3, sin afirmar que estén implementados todavía los presupuestos, recurrencias o el saldo proyectado de un plan mensual completo. Sus contratos se concretarán en incrementos siguientes antes de codificarlos. No anticipar ahorro/deudas/simulador de Fase 4.

## Estado del primer incremento

3.1 implementado localmente en `0.3.0-alpha.1`: 10 pruebas específicas; suite completa de 61 pruebas Django y 2 JavaScript aprobada. Migración aplicada con copia privada previa. Pendiente revisión personal del usuario; 3.2 y 3.3 aún no implementados.
