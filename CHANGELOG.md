# Historial de cambios · Finanzas DAGD

Versión del software: SemVer 2.0.0 (MAYOR.MENOR.PARCHE). Fuente única del número ejecutable: `VERSION`. Este archivo documenta sus cambios. 📌 Abre una versión para ver sus novedades; usa el filtro para buscar una función. ✨ Añadido = función nueva; 🛠️ Corregido = ajuste; 📖 Documentación = guía de uso. No se ha creado una etiqueta ni una publicación estable.

## [0.3.0-alpha.5] - 2026-10-18

🏠 Entrega local para revisión; no publicada.

### ✨ Añadido
- Crear usuario desde Iniciar sesión. Las altas públicas y administrativas son siempre usuarios normales; el administrador solo se crea en la configuración inicial.
- Editar nombre de acceso, nombres, apellidos y estado desde Administrar usuarios, con contraseña y confirmación del administrador.
- Eliminar usuarios normales únicamente desde administración, con copia financiera previa, contraseña, motivo y frase explícita. Administrador inicial protegido; recuperación requiere recrear el acceso y restaurar sus finanzas.

### 🛠️ Corregido
- Barra lateral con desplazamiento vertical y menú de usuario dentro del panel; permite alcanzar historial de cambios y manual en ventanas de poca altura.
- Se retira la asignación de roles posteriores para respetar el administrador único inicial. Se mantiene el aislamiento de finanzas y el reinicio exclusivo del usuario conectado.

### 📖 Documentación
- Registro, permisos y diferencias entre desactivar, eliminar usuario y reiniciar mis datos explicados en el manual.

## [0.3.0-alpha.4] - 2026-10-18

🏠 Entrega local para revisión; pendiente de autorización de publicación.

### ✨ Añadido
- Menú de usuario arriba a la izquierda: perfil, edición, contraseña, salida y reinicio personal; gestión de accesos visible para administradores.
- Administradores y usuarios normales con finanzas aisladas. El titular inicial pasa a administrador sin cambiar su clave. Altas, roles y activación/desactivación por administrador, sin acceso desde su sesión a finanzas ajenas.
- Eliminar movimientos, planes y catálogos no utilizados con contraseña, motivo, texto de confirmación y copia previa. Eliminar un plan conserva los ingresos.
- Reiniciar mis datos vacía únicamente las finanzas del usuario conectado, conservando su acceso y los demás usuarios; copia previa y recuperación documentada.

### 🔒 Protección
- Confirmaciones por POST/CSRF, verificación de pertenencia y revisión, bloqueo de catálogos referenciados y cancelación si falla el respaldo.
- Copias nuevas en carpetas por usuario. Comandos requieren --usuario si hay varias cuentas; ninguna restauración elige implícitamente a otro usuario.
- Administrador no puede quitarse el acceso a sí mismo ni modificar contraseñas ajenas mediante la gestión de accesos.

### 📖 Documentación
- Matriz de permisos en SPEC_USUARIOS_PERMISOS.md y secciones 16/17 del manual con pasos, límites, eliminación/reinicio y recuperación.

## [0.3.0-alpha.3] - 2026-10-18

🏠 Entrega local para revisión. No publicada en GitHub.

### ✨ Añadido
- Grupos opcionales de categorías: Gastos fijos, Gastos variables u otros nombres, con categorías individuales en Sin grupo. Puedes editar cada categoría para cambiarla de grupo.
- Ayuda del formulario según tipo: categorías correspondientes para ingreso/gasto; sin categoría para saldo inicial/transferencia y destinos solo para transferencias.

### 🛠️ Corregido
- El rechazo por categoría incompatible indica el campo y cómo corregirlo. Registrar dinero previo requiere Saldo inicial sin categoría; recibir un sueldo nuevo requiere Ingreso.

### 📖 Documentación
- Manual reescrito con recorrido inicial, tablas de campos, resultados, pasos de sueldo y solución de errores; emojis para ubicar tareas.
- Ejemplos ampliados con campos vacíos, secuencia, alternativas y comprobaciones para evitar duplicados.

### 🔄 Compatibilidad
- Migración conserva categorías existentes sin grupo. Respaldos nuevos de formato 3 incluyen grupos y leen formatos 1/2. Recuperar copias antiguas deja categorías Sin grupo; formato 1 también deja vacía la planificación de sueldo.

## [0.3.0-alpha.2] - 2026-10-18

Entrega local pendiente de revisión y autorización de publicación.

### 🛠️ Corregido
- Consultar mes utiliza ancho según su texto y altura de 46 px, alineado con los filtros; el CSS se actualiza por versión para evitar estilos anteriores en caché.

### ✨ Añadido
- Ejemplos desplegables en cada sección de revisión, con un caso ficticio continuo, pasos y resultados esperados; guía de recorrido en Revisar esta fase y sección 15 del manual. No se insertan datos en la base personal.

## [0.3.0-alpha.1] - 2026-10-18

Entrega local del incremento 3.1, pendiente de revisión y autorización de publicación. Fase 3 continúa en desarrollo.

### ✨ Añadido
- Mi sueldo: previsión neta o cálculo manual de bruto, adicionales y deducciones; actividad, mes trabajado, fecha de cobro esperada y mes presupuestado independientes.
- Cobros parciales mediante vínculos a ingresos existentes, sin duplicar movimientos; pendiente/exceso, correcciones, exclusión de previsiones y desvinculación con motivo.
- Control de versión, pertenencia y trazabilidad. Correcciones/anulaciones de ingresos actualizan el cálculo de cobros.
- Migración de tablas y respaldos de formato 2 con sueldos/vínculos. Lectura del formato 1: restaurarlo deja vacía la planificación que no contiene, con copia previa y reversión ante errores.
- Manual y revisión de fase actualizados. Presupuestos y recurrencias permanecen pendientes en Fase 3.

### 🧪 Verificado
- 61 pruebas Django y 2 JavaScript aprobadas; migraciones sin cambios pendientes y dependencias consistentes.

## [0.2.0-alpha.10] - 2026-10-18

Publicación en dev1 autorizada por el usuario al solicitar iniciar Fase 3.

### 🛠️ Corregido

- Restaurado el ancho de la fila de botones al del buscador. La reducción solicitada corresponde a la altura: botones de 32 px en manual y CHANGELOG.
- Se conserva el formato horizontal y la descripción del filtro a 11 px.

## [0.2.0-alpha.9] - 2026-10-18

Publicación de este ajuste y de los cambios pendientes del lector en dev1 autorizada por el usuario.

### Cambiado

- Fila horizontal de los tres botones más estrecha que el buscador, alineada a su izquierda, en manual y CHANGELOG.
- Se mantiene el tamaño reducido de la descripción y el funcionamiento del filtro y plegado.

## [0.2.0-alpha.8] - 2026-10-18

Ajuste local pendiente de autorización para publicar.

### 🛠️ Corregido

- Los tres botones del índice comparten una sola fila horizontal con el ancho total del buscador, según la aclaración del usuario, en manual e historial.
- Se conserva el tamaño reducido de la descripción del filtro.

## [0.2.0-alpha.7] - 2026-10-18

Ajuste local pendiente de autorización para publicar.

### Cambiado

- Los tres botones del índice ocupan el mismo ancho y altura mínima del buscador, apilados en una columna, en ambos lectores.
- Menor tamaño de letra para la descripción/contador del filtro.
- La hoja de estilos del lector utiliza la versión del aplicativo en su URL para evitar conservar estilos anteriores al recargar después de actualizar.

## [0.2.0-alpha.6] - 2026-10-18

Ajuste local pendiente de autorización para publicar.

### Cambiado

- Buscador, contador y tres botones del lector reubicados dentro del panel En este documento, encima del índice, tanto en el manual como en el historial.
- Controles adaptados al ancho de la columna; la lista de títulos tiene desplazamiento propio para mantenerlos disponibles.

## [0.2.0-alpha.5] - 2026-10-18

Ajuste local pendiente de revisión y autorización para publicar.

### ✨ Añadido

- Versiones del historial y capítulos del manual plegables; grupos de subtítulos del índice también se pueden contraer.
- Filtro por títulos y contenido, sin distinguir mayúsculas ni tildes, con contador de secciones, estado sin coincidencias y limpieza del filtro.
- Acciones Expandir todo y Contraer todo; los enlaces del índice y los fragmentos directos abren la sección de destino.
- Mejora progresiva mediante un script local, sin nuevas dependencias: si JavaScript está deshabilitado, el contenido completo permanece legible. CSP permite scripts propios únicamente en los lectores de documentación.

## [0.2.0-alpha.4] - 2026-10-18

Publicación en dev1 autorizada por el usuario el 2026-10-18.

### ✨ Añadido

- Índice lateral automático en el manual y el historial con enlaces a títulos y subtítulos, destinos únicos para encabezados repetidos y resaltado al navegar.
- Mayor ancho de lectura en ambos documentos, con índice fijo y desplazable en escritorio; en pantallas pequeñas el índice se sitúa encima del contenido.
- Anclas e índice filtrados con las mismas restricciones de HTML seguro. Sin nuevas dependencias ni JavaScript.

## [0.2.0-alpha.3] - 2026-10-18

Publicación de los cambios pendientes de Fase 2 en dev1 autorizada por el usuario. La entrega continúa pendiente de su revisión funcional; no se inicia Fase 3.

### 🛠️ Corregido

- Los lectores del manual e historial convierten Markdown a HTML con títulos jerárquicos, listas, negritas, enlaces, tablas y bloques de código, en lugar de mostrar la sintaxis como texto.
- Estilos de lectura para encabezados, código y tablas; se conserva la apertura en pestañas independientes y la fuente original de cada documento.
- Saneamiento del HTML antes de renderizarlo: se eliminan scripts, atributos de eventos y enlaces con esquemas peligrosos; los ejemplos de HTML dentro de bloques de código siguen escapados.

### 📦 Dependencias

- Markdown 3.11.1 y nh3 0.3.7 instalados únicamente en .venv y fijados en requirements.txt. No se modificaron instalaciones globales.

## [0.2.0-alpha.2] - 2026-10-17

Ajuste local de Fase 2, sin autorización de publicación todavía.

### ✨ Añadido

- Enlaces a CHANGELOG.md y MANUAL_USUARIO.md al pie de la barra lateral, abriendo pestañas nuevas con el manual debajo del historial.
- Lectores locales de los documentos originales, sin nuevas dependencias ni acceso arbitrario a archivos del PC. Contenido escapado y rutas de solo lectura.
- Manual actualizado con el acceso a documentación y aclaración de los módulos de ahorro y obligaciones previstos para Fase 4.

## [0.2.0-alpha.1] - 2026-10-17

Entrega de Fase 2 local, pendiente de revisión visual del usuario y autorización de publicación. Incremento MENOR por nuevas capacidades en desarrollo inicial; no es una versión estable.

### ✨ Añadido

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


### 📖 Documentación

- Manual de usuario ampliado con primera ejecución, requisitos, ausencia de usuarios en Fase 1, solución de problemas y mantenimiento continuo. No cambia la versión ejecutable.

- Pendiente: revisión del usuario sobre la vista previa de Fase 1 y personalizaciones solicitadas.

## [0.1.0-alpha.1] - 2026-10-17

Primera vista previa local; incluida posteriormente en la publicación autorizada de Fase 1.

### ✨ Añadido

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
