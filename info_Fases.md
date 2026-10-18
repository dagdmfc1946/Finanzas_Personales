# Finanzas DAGD: fases de desarrollo

## Estado y acuerdos

Fases 1 y 2 publicadas en `dev1`. El usuario autorizó iniciar Fase 3. Primer incremento local con ajustes `0.3.0-alpha.5`: Mi sueldo y cobros vinculados. Presupuestos y recurrencias siguen pendientes dentro de Fase 3. Integración bancaria cancelada.

- Nombre: Finanzas DAGD. Desarrollo local en `D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales`.
- Toda fase tendrá una entrega ejecutable para revisión del usuario. Se conserva **Revisar esta fase** hasta culminar el desarrollo; su contenido reflejará la fase vigente. Sus casillas temporales no son aprobación.
- Agent Skills se aplica durante todo el desarrollo; skills UI instaladas y criterio de uso en `docs/SKILLS_UI.md`.
- Versionado SemVer 2.0.0, número ejecutable en `VERSION`, historial en `CHANGELOG.md`, manual actualizado con cada cambio de uso.
- Publicar o fusionar cambios en GitHub requiere orden o aprobación explícita. La corrección pendiente de los botones y el registro de inicio de Fase 3 se publicaron por orden expresa. La nueva implementación de Fase 3 quedará local hasta otra autorización. Todos los nuevos commits serán en español.
- La referencia principal es el caso de septiembre compartido por el usuario, conservado en `local/REFERENCIA_SEPTIEMBRE.md`, fuera de Git. Los importes reales no se copian a fixtures ni a documentos públicos.
- APK de Moneri diferido. Referencias públicas previas en `Analisis_REA/`.

## Plan revisado de cinco fases

| Fase | Alcance | Entrega ejecutable y criterio de revisión |
|---|---|---|
| **1. Definición y vista previa** | Nombre, arquitectura, reglas propuestas, navegación y pantallas con muestras ficticias. Iniciador con apertura automática del navegador. | Publicada. El usuario puede recorrer las siete secciones. La referencia privada de septiembre se utilizará como caso de aceptación posterior; no se confunde con los ejemplos públicos. |
| **2. Base local y finanzas por actividad** | Persistencia; cuentas, categorías, saldos iniciales, ingresos, gastos y transferencias. Espacios **Personal/trabajo principal**, emprendimientos y trabajos secundarios configurables, identificados tanto en ingresos como en gastos. Respaldo/restauración básica e historial de correcciones. Definir la protección del acceso antes de guardar datos personales. Primer ajuste de legibilidad y componentes con las skills UI, conservando la identidad revisada. | Registrar movimientos en dos actividades, filtrarlos y ver resultados separados; reiniciar sin perder datos; recuperar una copia. Verificar que los fondos movidos entre actividades no generen ingresos duplicados. Revisión visual y aprobación del usuario antes de seguir. |
| **3. Sueldo y presupuestos mensuales o por objetivo** | Sueldo neto o detalle; distinguir devengo, recepción y mes presupuestado. Recurrencias, suscripciones, previsto/realizado. Presupuestos independientes para **proyectos, compras soñadas y otras metas de gasto**, con partidas, tope, plazo opcional y actividad. | Organizar un mes y un proyecto; comparar previsto, comprometido y realizado. Registrar un pago una sola vez aunque esté asociado a un presupuesto. Revisar el saldo proyectado sin presentarlo como saldo bancario confirmado. |
| **4. Ahorros, obligaciones y simulador de compras** | Metas y aportes; préstamos otorgados/recibidos, compras financiadas, cuotas, abonos y vencimientos. **Calculadora de cuotas e intereses**: capital, cuota inicial, plazo, tasa y período explícitos, seguros y cargos; desglose de capital/interés/cargos y tabla de pagos. Modalidad adicional de interés total pactado y reparto, como la referencia privada. | Comparar escenarios sin generar deudas ni gastos automáticamente. Verificar tasa cero, redondeo y última cuota, total pagado e identificación de cada componente. Confirmar por separado la conversión de una simulación en obligación registrada. |
| **5. Validación y entrega** | Reportes por actividad y consolidados, CSV, importación revisable del notebook, restauración completa, revisión del manual y cierre. Integración bancaria excluida por decisión del usuario. | Instalar, iniciar, usar, respaldar y recuperar con el manual. Revisar informes sin mezclar actividades. Se conserva registro/conciliación manual e importación aprobada, sin conectar bancos. |

## Separación de actividades: regla de base

Una **actividad** identifica a qué ámbito pertenece el ingreso o gasto; una **cuenta** identifica dónde está el dinero. Una cuenta bancaria podría servir a varias actividades sin duplicarla artificialmente. Habrá vista por actividad y consolidado, con detalle del origen. Los movimientos internos entre cuentas o actividades propias deberán enlazarse para no contarlos como ingresos externos o gastos nuevos del consolidado.

En Fase 2 los aportes personales y retiros del emprendimiento usan transferencias enlazadas. Cada origen y destino corresponde a una actividad; el reparto automático de un gasto entre varias actividades quedará sujeto a necesidad y aprobación. No se promete contabilidad empresarial, facturación electrónica ni liquidación tributaria.

## Presupuesto, ahorro y simulación son conceptos diferentes

- **Presupuesto:** plan o límite de gasto por mes, proyecto o compra. No crea dinero ni acredita un pago.
- **Meta de ahorro:** objetivo y dinero reservado/aportado. No debe incrementar saldos por duplicado.
- **Simulación:** comparación hipotética de cuotas y costos; no modifica deudas ni movimientos reales.
- **Obligación registrada:** compromiso real con pagos y saldos pendientes.

La calculadora no puede garantizar reproducir cualquier contrato bancario. Se documentarán las modalidades implementadas, tipo de tasa y periodicidad; las tasas anuales efectivas no se dividirán simplemente entre doce. Las condiciones con seguros variables, tasas promocionales o intereses diarios necesitarán datos y reglas expresas.

## Capacidades y dependencias

| Identificador | Responsabilidad | Depende de |
|---|---|---|
| base-local | Inicio, navegación, versión y acceso local | — |
| movimientos | Actividades, cuentas, categorías, movimientos y trazabilidad | base-local |
| plan-mensual | Sueldo, recurrencias y presupuestos mensuales/por proyecto | movimientos |
| compromisos | Metas, préstamos, simulaciones, compras financiadas y pagos | movimientos |
| entrega | Reportes, importación/exportación, recuperación y manual integral | movimientos, plan-mensual, compromisos |

La integración bancaria queda cancelada. El estudio previo en `docs/INTEGRACIONES_BANCARIAS.md` se conserva como antecedente; no representa un servicio disponible ni trabajo pendiente.

## Decisiones de Fase 2 y estado de entrega

- Alcance aprobado por el usuario. Se inicia con acceso local protegido y datos persistentes; todavía no hay aprobación de la entrega resultante.
- Actividad inicial renombrable Personal / trabajo principal; otras actividades creadas por el usuario. Aportes y retiros propios se registran como transferencias entre actividades, incluso dentro de una misma cuenta. Un gasto compartido puede separarse manualmente; sin reparto automático.
- Implementados primer usuario local, sesiones/CSRF y centavos enteros; datos privados en SQLite, sin cifrado del archivo. Especificación y criterios en SPEC_FASE2.md; manual actualizado para el primer acceso.
- Mantener los colores y la navegación como punto de partida; los cambios UI se presentarán ejecutándose para aceptar sugerencias.

Entrega ejecutable de Fase 2 preparada localmente como 0.2.0-alpha.1. Pendientes: revisión del usuario en su PC y autorización de push de esta implementación. No se inicia Fase 3.

## Estado actualizado — inicio autorizado de Fase 3

El usuario autorizó subir la corrección 0.2.0-alpha.10 y comenzar Fase 3. Las restricciones históricas de inicio anteriores quedan superadas por esa instrucción. El plan de cinco fases y la exclusión bancaria siguen vigentes. Primer incremento: sueldo neto/detallado, meses trabajado/presupuestado y cobros reales vinculados sin duplicar movimientos. Siguientes incrementos: presupuestos por mes/proyecto/compra y recurrencias, con previsto/comprometido/realizado. Especificación en SPEC_FASE3.md. Nuevos cambios de implementación permanecen locales hasta orden de publicación; no se inicia Fase 4 automáticamente.
