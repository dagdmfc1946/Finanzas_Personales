# Análisis REA de Moneri para Finanzas Personales

Fecha: 2026-10-17, America/Bogota.
Estado: análisis preliminar de la ficha pública terminado; análisis estático y funcional de la aplicación Android pendiente de disponer de su paquete. Fase 1 del aplicativo personalizado no iniciada.

## Objetivo y límite

Seleccionar las capacidades útiles para la gestión local de sueldo, gastos y compromisos del usuario. La aplicación personalizada tendrá implementación propia y diseño adaptado; no se requiere reconstruir todo Moneri.

Paquete identificado por la URL: `co.moneri.app`.
Referencia solicitada: https://play.google.com/store/apps/details?id=co.moneri.app&pli=1.
Captura REA: https://play.google.com/store/apps/details?id=co.moneri.app&hl=es_CO. Se cambió el parámetro de idioma para obtener la ficha en español de Colombia; el identificador de aplicación se conserva.

## Método y evidencia REA real

Se utilizó la skill `reverse-engineer-anything` y REA 6.5.0, operación `capture_browser_scenario`, mediante CLI. REA abrió Chrome existente en modo headless con un perfil temporal, navegó a la ficha y esperó 2500 ms. Capturó URL, DOM y árbol de accesibilidad; no se inició sesión, instaló Moneri, pulsó Instalar ni interactuó con cuentas financieras.

- Evidence ID: `ev_0ae67fa5ebf119bdce6629226d417ee4a24ed6dc1ce9207c58bf42051bba4f4c`.
- Archivo completo: `C:\Users\Diego\.local\share\rea-finanzas\logs\moneri-play-evidence.json`.
- Entrada reproducible: `C:\Users\Diego\.local\share\rea-finanzas\logs\moneri-scenario.json`.
- Proveedor: `rea-playwright-browser-scenario`, versión `1`.
- Navegador observado: Chromium `155.0.8059.82`.
- Captura normalizada: `completeness.status=complete`; sin secciones solicitadas faltantes ni truncadas. Esta integridad se refiere a la captura de la página, no a una investigación completa de Moneri.
- Limpieza: `terminated-owned-process`.
- DOM: SHA-256 `45a115cccf3d527c9eb76f31b77b19e5e6e8c95d3c60b30707c5b275f6f535e0`.
- Accesibilidad: SHA-256 `aa9a285679b064bac16d6f483dd905c60e61d0a6d91cff3ee50d34e3b301998c`.

Los archivos completos permanecen locales y no se han subido a GitHub. La evidencia original contiene la página pública; este informe usa resúmenes propios, sin reproducir su texto completo.

Para repetir la captura, definir `$reaNode` y `$reaCli` como en `INSTALACION_REA.md` y ejecutar:

```powershell
& $reaNode $reaCli capture-browser-scenario 'C:\Users\Diego\.local\share\rea-finanzas\logs\moneri-scenario.json' --json
```

Una nueva captura reflejará la página existente en esa fecha y puede generar identificadores y huellas diferentes.

## Observaciones de la ficha y selección propuesta

Todas las observaciones de esta tabla proceden del árbol de accesibilidad del paso `wait-public-listing` de la evidencia citada. Son funcionalidades declaradas públicamente por el desarrollador, no comportamiento probado dentro de la aplicación. Las decisiones son propuestas para revisar en la Fase 1.

| Capacidad anunciada | Selección para el aplicativo personalizado | Prioridad propuesta |
|---|---|---|
| Registro de ingresos, gastos y ahorros | Formularios breves, fecha, importe, cuenta, categoría y observación. | Esencial |
| Agrupación por bancos, brókeres y billeteras | Cuentas configurables: efectivo, bancos y billeteras; saldo por cuenta. | Esencial |
| Consolidación del patrimonio | Resumen personal con cuentas y obligaciones claramente diferenciadas. | Alta |
| Presentación en COP y USD | Empezar en COP; dejar multimoneda para una necesidad confirmada. | Diferida |
| Seguimiento de activos e inversiones | Evaluar más adelante; no es necesario para controlar sueldo y gastos. | Diferida |
| Cotizaciones, búsqueda bursátil y métricas de rentabilidad | Suponen proveedores externos y reglas adicionales; fuera del alcance inicial propuesto. | Diferida |
| Comunidad y conversación sobre inversiones | No contribuye al uso personal local solicitado. | Excluida inicialmente |

La ficha identifica a PlusMedia360 como desarrollador y declara actualización del 1 de agosto de 2026. La fecha de la ficha no identifica una versión binaria exacta ni acredita qué APK se distribuiría a un dispositivo concreto.

## Necesidades propias que no quedan demostradas por esta evidencia

El usuario solicitó sueldo detallado, ahorros, préstamos, deudas, compras y gastos fijos. El notebook aporta además el uso de presupuestos mensuales y pagos en cuotas. La ficha capturada no permite establecer cómo Moneri implementa cada uno de esos casos ni si los cubre completamente.

Se propone definir estas capacidades como requisitos propios, aunque Moneri no las documente:

- Sueldo: distinguir período devengado, recepción y presupuesto; permitir importe neto o desglose de conceptos sin contabilizar ambos como ingresos separados.
- Gastos fijos: separar plantilla recurrente, compromiso previsto y pago realizado; evitar crear pagos duplicados.
- Compras y deudas: diferenciar valor de compra, financiación y abonos; distinguir capital, interés y cargos.
- Préstamos: distinguir dinero prestado a terceros de obligaciones recibidas; registrar los cobros y pagos sobre sus saldos.
- Ahorros: distinguir transferencias entre cuentas propias de gastos; las metas no deben crear dinero adicional.
- Fiabilidad: importes exactos, reglas explícitas de redondeo, historial de correcciones, copia de seguridad y restauración.

Estas son propuestas de ingeniería derivadas de la necesidad del usuario; no se atribuyen a Moneri ni son reglas ya aprobadas.

## ¿Basta el enlace de Google Play?

**Sí para analizar la descripción pública y elegir ideas; no para analizar técnicamente la aplicación Android ni verificar su funcionamiento.** REA recibe una ruta local de APK para `inspect_android_package`; una URL de la tienda no proporciona ese artefacto.

Para continuar con análisis estático hace falta un APK de Moneri obtenido de su distribución o instalación legítima. Si se distribuye mediante APK divididos, debe preservarse el conjunto instalado; el primer comando documentado espera un APK independiente, por lo que habrá que revisar la compatibilidad de la operación con el formato recibido antes de afirmar cobertura completa. Un AAB tampoco se debe tratar como si fuera un APK.

Para verificar comportamientos visibles también sirven grabaciones o capturas de los recorridos de interés. Estas muestran flujos, pero no sustituyen el análisis estático. No se descargó un APK de sitios de terceros ni se adquirió acceso a cuentas o servidores de Moneri.

## Siguiente análisis cuando exista el artefacto

1. Identificar origen, versión, formato y SHA-256 del paquete; conservar la identidad analizada.
2. Ejecutar `inspect_android_package` con esa ruta. La instalación actual pasa readiness de JADX; la prueba real con Moneri todavía no se ha ejecutado.
3. Buscar clases o recursos relacionados con ingresos, gastos, cuentas, ahorro y deudas. Si se necesitan métodos, seleccionar las clases y sobrecargas observadas; no adivinar nombres ni mecanismos internos.
4. Registrar observaciones, inferencias y desconocidos con Evidence IDs. Tener en cuenta ofuscación, cargas dinámicas, implementación Flutter/nativa o lógica remota; JADX no garantiza reconstruir todo tipo de APK.
5. Contrastar únicamente los flujos necesarios y convertir los hallazgos útiles en requisitos propios revisables. El análisis estático no prueba ejecución, fórmulas remotas ni cumplimiento de las declaraciones de privacidad.

## Lista de cobertura

| Pregunta | Estado | Evidencia o limitación |
|---|---|---|
| ¿REA está instalado y registra herramientas? | Respondida | Setup listo, handshake MCP correcto con 207 herramientas; ver instalación. |
| ¿Está preparado el proveedor Android? | Respondida en readiness | JDK completo y JADX verificados, `available=true`; falta prueba con APK. |
| ¿Qué anuncia Moneri y qué es pertinente? | Respondida a nivel de ficha | Captura REA y selección propuesta de este documento. |
| ¿Cómo funcionan sus pantallas y validaciones? | Pendiente | La ficha no equivale al aplicativo en ejecución. |
| ¿Qué reglas y fórmulas implementa Moneri? | Pendiente | Falta APK y evidencia suficiente del comportamiento; parte podría ser remota. |
| ¿Puede comenzar la Fase 1 con estos hallazgos? | Pendiente de decisión del usuario | No se ha iniciado; las limitaciones quedan explícitas para evitar atribuir funciones no comprobadas. |

## Trazabilidad

- Rama de trabajo: `dev1`, creada y publicada previamente por orden del usuario.
- Esta intervención instala herramientas y prepara los dos informes solicitados. No crea aún `info_Fases.md`, `dev_Process.md`, `CHANGELOG.md` ni `MANUAL_USUARIO.md` y no implementa el aplicativo.
- La autorización de instalación no se interpreta como permiso para publicar estos cambios. No se realiza push.
