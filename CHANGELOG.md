# Historial de cambios · Finanzas DAGD

Versión del software: SemVer 2.0.0 (MAYOR.MENOR.PARCHE). Fuente única del número ejecutable: `VERSION`. Este archivo documenta sus cambios. No se ha creado una etiqueta ni una publicación estable.

## [Sin publicar]

### Planeación y herramientas

- Plan propuesto revisado: separación por actividades desde Fase 2, presupuestos por proyecto/compra, simulador de financiación y consulta bancaria opcional. Pendiente de aprobación; sin implementar Fase 2.
- Skills de UI instaladas y verificadas en el entorno personal; fuentes e instrucciones en docs/SKILLS_UI.md.
- Reglas duraderas del usuario en AGENTS.md y estudio preliminar de saldos en docs/INTEGRACIONES_BANCARIAS.md.

- Nuevas propuestas posteriores a la publicación de Fase 1 se revisarán antes de iniciar la Fase 2.

## [0.1.0-alpha.2] - 2026-10-17

Publicación en dev1 autorizada por el usuario; no es una versión estable ni el inicio de Fase 2.

### Cambiado

- El iniciador espera al servidor y abre automáticamente una pestaña del navegador predeterminado.
- Si ya existe una instancia de Finanzas DAGD la reutiliza; ante otro servicio en el puerto no lo detiene.
- Pruebas del iniciador y manual de primera ejecución actualizados.
- La referencia financiera de septiembre proporcionada por el usuario se conserva en local/, excluida de Git. Los ejemplos públicos siguen siendo ficticios.


### Documentación

- Manual de usuario ampliado con primera ejecución, requisitos, ausencia de usuarios en Fase 1, solución de problemas y mantenimiento continuo. No cambia la versión ejecutable.

- Pendiente: revisión del usuario sobre la vista previa de Fase 1 y personalizaciones solicitadas.

## [0.1.0-alpha.1] - 2026-10-17

Primera vista previa local; incluida posteriormente en la publicación autorizada de Fase 1.

### Añadido

- Nombre Finanzas DAGD, navegación local y siete pantallas de demostración con datos ficticios.
- Resumen, cuentas de ejemplo, movimientos con búsqueda/filtros y vistas propuestas de sueldo, presupuesto, ahorros y obligaciones.
- Guía de revisión de fase, instrucciones de inicio en Windows y manual provisional.
- Documentación de fases, decisiones, reglas propuestas y trazabilidad.
- Pruebas de acceso, filtros, validación, escape de consultas y bloqueo de escrituras.

### Límites

- Sin registro, importación ni persistencia de datos financieros. Las obligaciones ilustran escenarios independientes.
- El APK de Moneri queda fuera del trabajo inicial por decisión del usuario.
- Los informes REA se publicaron previamente en `dev1` y permanecen en `Analisis_REA/`.

## Política de versiones

Desarrollo inicial en `0.y.z`, con sufijos `alpha`/`beta` cuando corresponda. Se acordará el contrato de compatibilidad de los datos y las interfaces antes de `1.0.0`. Desde la versión estable, cambios incompatibles incrementan MAYOR, funcionalidad compatible MENOR y correcciones compatibles PARCHE. No se usa `2.0.0` como versión del producto por ser el número de la especificación SemVer. Etiquetas y subidas requieren autorización explícita.
