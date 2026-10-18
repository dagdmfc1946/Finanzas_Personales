# Historial de cambios · Finanzas DAGD

Versión del software: SemVer 2.0.0 (MAYOR.MENOR.PARCHE). Fuente única del número ejecutable: `VERSION`. Este archivo documenta sus cambios. No se ha creado una etiqueta ni una publicación estable.

## [0.2.0-alpha.4] - 2026-10-18

Ajuste local posterior a la publicación anterior; pendiente de autorización para subir.

### Añadido

- Índice lateral automático en el manual y el historial con enlaces a títulos y subtítulos, destinos únicos para encabezados repetidos y resaltado al navegar.
- Mayor ancho de lectura en ambos documentos, con índice fijo y desplazable en escritorio; en pantallas pequeñas el índice se sitúa encima del contenido.
- Anclas e índice filtrados con las mismas restricciones de HTML seguro. Sin nuevas dependencias ni JavaScript.

## [0.2.0-alpha.3] - 2026-10-18

Publicación de los cambios pendientes de Fase 2 en dev1 autorizada por el usuario. La entrega continúa pendiente de su revisión funcional; no se inicia Fase 3.

### Corregido

- Los lectores del manual e historial convierten Markdown a HTML con títulos jerárquicos, listas, negritas, enlaces, tablas y bloques de código, en lugar de mostrar la sintaxis como texto.
- Estilos de lectura para encabezados, código y tablas; se conserva la apertura en pestañas independientes y la fuente original de cada documento.
- Saneamiento del HTML antes de renderizarlo: se eliminan scripts, atributos de eventos y enlaces con esquemas peligrosos; los ejemplos de HTML dentro de bloques de código siguen escapados.

### Dependencias

- Markdown 3.11.1 y nh3 0.3.7 instalados únicamente en .venv y fijados en requirements.txt. No se modificaron instalaciones globales.

## [0.2.0-alpha.2] - 2026-10-17

Ajuste local de Fase 2, sin autorización de publicación todavía.

### Añadido

- Enlaces a CHANGELOG.md y MANUAL_USUARIO.md al pie de la barra lateral, abriendo pestañas nuevas con el manual debajo del historial.
- Lectores locales de los documentos originales, sin nuevas dependencias ni acceso arbitrario a archivos del PC. Contenido escapado y rutas de solo lectura.
- Manual actualizado con el acceso a documentación y aclaración de los módulos de ahorro y obligaciones previstos para Fase 4.

## [0.2.0-alpha.1] - 2026-10-17

Entrega de Fase 2 local, pendiente de revisión visual del usuario y autorización de publicación. Incremento MENOR por nuevas capacidades en desarrollo inicial; no es una versión estable.

### Añadido

- Primer usuario local, inicio/cierre de sesión y cambio de contraseña; protección de formularios con CSRF y consultas por propietario.
- Base SQLite persistente y secreto estable, excluidos de Git junto con los respaldos.
- Actividades, cuentas y categorías; saldos iniciales, ingresos, gastos y transferencias por actividad. Centavos enteros y resumen consolidado sin duplicar transferencias.
- Formularios, búsqueda/filtros y paginación; corrección con control de edición, anulación con motivo e historial conservado.
- Respaldo JSON descargable y comandos para crear/restaurar copias con validación, transacción y copia previa; sin exportar credenciales.
- Pantallas de primer uso y estados vacíos, mayor legibilidad y guía Revisar Fase 2. La demostración ficticia permanece separada en /demo/.

### Cambiado

- El iniciador aplica migraciones antes del arranque y reconoce la aplicación también en configuración o acceso.
- Manual actualizado para crear usuario, separar actividades, operar movimientos y recuperar respaldos.
- Plan aprobado por el usuario; integración bancaria cancelada. Commits nuevos en español.
- La revisión documental pendiente se publicó en dev1 mediante ea0af24 por orden expresa. La nueva implementación permanece local.

### Herramientas

- Agent Skills y refinamiento de interfaz con Impeccable; sin nuevas dependencias del aplicativo. Skills UI previamente instaladas documentadas en docs/SKILLS_UI.md.

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
