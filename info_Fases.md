# Finanzas DAGD: fases de desarrollo

## Acuerdos vigentes

- Nombre del aplicativo: **Finanzas DAGD**.
- Ruta: `D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales`.
- Rama: `dev1`. Cada subida a GitHub requiere una orden o aprobación explícita; aprobar una fase no autoriza automáticamente su publicación.
- El usuario autorizó iniciar la Fase 1 después de revisar el plan de cinco fases. El APK de Moneri no es necesario y su análisis queda diferido.
- **Todas las fases necesitan una entrega ejecutable local y revisión visual del usuario antes de aprobarse.** Las pruebas técnicas no sustituyen esa aprobación.
- La versión se lee de `VERSION`; el historial se registra en `CHANGELOG.md`. Se aplica SemVer 2.0.0, incluyendo identificadores de prelanzamiento durante las revisiones.

## Fases

| Fase | Alcance | Entrega que puede ejecutar el usuario | Condición para aprobar |
|---|---|---|---|
| 1. Definición y diseño | Requisitos, módulos, reglas propuestas, arquitectura y diseño inicial. | Vista previa Django navegable, con nombre Finanzas DAGD y datos ficticios, búsqueda y filtros de ejemplo. | Revisar pantallas y documentación; resolver o aceptar expresamente los supuestos pendientes. |
| 2. Movimientos locales | Cuentas, categorías, saldos iniciales, ingresos, gastos, transferencias, persistencia y respaldo básico. | Registrar y corregir movimientos reales localmente; reiniciar y recuperar una copia de prueba. | Verificar saldos y datos persistidos, respaldos, validaciones y facilidad de uso. |
| 3. Sueldo y planificación | Neto o detalle del sueldo, fechas y períodos, gastos fijos, suscripciones, presupuestos. | Organizar un mes y comparar importes previstos y realizados con datos propios. | Comprobar que el mes se explica sin duplicar sueldo, recurrencias ni pagos. |
| 4. Ahorros y obligaciones | Metas, aportes, préstamos otorgados y recibidos, compras financiadas, cuotas, abonos y vencimientos. | Gestionar metas y pagos con separación de capital, intereses y cargos. | Verificar movimientos, saldos de obligaciones y reglas de ahorro con casos acordados. |
| 5. Entrega local | Reportes, CSV, importación revisable del notebook, restauración completa y manual final. | Iniciar, utilizar, respaldar y recuperar el aplicativo siguiendo el manual. | Aceptación de los flujos completos y de la documentación de entrega. |

Estado actual: **Fase 1 en revisión; aún no aprobada**. Fases 2–5 pendientes. El incremento ejecutable de la Fase 1 anticipa la base mínima de Django para satisfacer la revisión visual; no implementa aún el registro financiero de la Fase 2.

## Mapa de capacidades y dependencias

| Identificador | Responsabilidad | Depende de |
|---|---|---|
| base-local | Inicio, navegación, configuración y versión | — |
| movimientos | Cuentas, categorías, ingresos, gastos, transferencias y trazabilidad | base-local |
| plan-mensual | Sueldo y presupuesto, previsiones y recurrencias | movimientos |
| compromisos | Metas, préstamos, compras financiadas y pagos | movimientos |
| entrega | Importación, exportación, reportes, respaldo y manual definitivo | movimientos, plan-mensual, compromisos |

Este mapa describe el orden propuesto; no implica que los módulos financieros estén implementados. Cada capacidad futura tendrá reglas y criterios de aceptación revisables antes de su desarrollo.

## Límites iniciales

Uso personal local, español y COP. Sin integración bancaria, cotizaciones, comunidad, nube ni Android en el alcance inicial. Las propuestas sobre el funcionamiento financiero se detallan en `SPEC_FASE1.md`; los datos de demostración no provienen del notebook personal. El análisis público de Moneri es una referencia, no una especificación de sus reglas internas.

Las instrucciones de inicio y recorrido están en `MANUAL_USUARIO.md`. Tareas y evidencia de verificación: `tasks/todo.md` y `dev_Process.md`.
