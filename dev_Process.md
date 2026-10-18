# Proceso de desarrollo · Finanzas DAGD

## Reglas de trazabilidad

Registrar alcance, decisiones, pruebas, límites y estado de aprobación en cada incremento. `VERSION` es la fuente única de versión; `CHANGELOG.md` explica los cambios. Trabajo en `dev1`; commits locales permitidos como trazabilidad, push exclusivamente autorizado por el usuario. Una fase se aprueba después de ejecutarla y revisarla visualmente, por decisión explícita del usuario.

## Antecedentes

- Se verificaron Agent Skills y REA. El repositorio inicial contenía README y commit `36d1070`.
- Se creó y publicó `dev1` por orden del usuario.
- Se instaló REA aislado y se analizó la ficha pública de Moneri; no se analizó un APK. Informes en `Analisis_REA/`, publicados por orden expresa hasta `3a4894a`.
- Se propuso un plan de cinco fases. El usuario autorizó iniciar Fase 1, difirió el APK, fijó el nombre Finanzas DAGD y exigió entregas ejecutables para la aprobación de cada fase.

## Fase 1 · versión local 0.1.0-alpha.1 · 2026-10-17

### Alcance y decisiones

Se añade un prototipo ejecutable a la fase de definición/diseño para permitir la revisión visual solicitada. No se adelanta la persistencia ni el registro de movimientos de Fase 2. Siete secciones de muestra, filtros GET sobre datos sintéticos y una guía de revisión temporal.

Se reutiliza Python 3.12.10 y se crea `.venv` dentro del repositorio. Instalación aislada: Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0 y tzdata 2026.5. Versiones fijadas en `requirements.txt`; no se modificó Python global. Plantillas Django y CSS local, sin framework JavaScript, CDN, fuentes remotas ni servicios financieros.

SQLite se configura en memoria para las comprobaciones de arranque de Django; esta fase no crea archivos de base de datos ni importa el notebook. Los datos son ficticios y los ejemplos de obligaciones se rotulan como independientes del saldo del resumen. La propuesta de almacenar centavos enteros en SQLite evita depender de su aritmética decimal para el dinero real; se validará al definir la persistencia.

Las reglas propuestas y supuestos pendientes están en `SPEC_FASE1.md`. La aprobación del estilo oscuro y de los términos sigue siendo del usuario; los prototipos no deciden por él.

### Skills aplicadas

Agent Skills: especificación, planeación, Git, implementación incremental, interfaz, pruebas, documentación, seguridad y consulta de fuentes. La skill de pruebas de navegador propone Chrome DevTools MCP, que no está configurado en esta sesión; se utilizará un navegador real mediante las herramientas disponibles y se registrará la evidencia. No se instalarán herramientas adicionales de navegador solo para cumplir un proveedor específico.

### Verificación automática realizada

1. Se escribieron ocho pruebas antes de implementar la vista. Tras crear una vista vacía, la ejecución falló con 15 fallos de aserción esperados: identidad, secciones, filtro, validación y restricciones aún ausentes.
2. Tras implementar la vista: `manage.py test preview` pasó las ocho pruebas iniciales. Incluyen navegación por siete rutas, 405 ante escrituras, 404 ante sección desconocida, búsqueda y limpieza, estado vacío, límites de consulta, tipo inválido, escape HTML, cabeceras y rechazo de host ajeno.
3. `manage.py check`: sin incidencias. `pip check`: sin dependencias incompatibles.
4. La prueba real de arranque detectó que `runserver` consulta migraciones y necesitaba abrir la ruta SQLite prevista para otra fase. Se reprodujo con una novena prueba, se cambió a SQLite en memoria y se verificó nuevamente. Así el prototipo no requiere directorios ni archivos financieros persistentes.

### Verificación visual y entrega

Se abrió el aplicativo en el navegador integrado de Codex, mediante CUA, en `http://127.0.0.1:8765/`. Se recorrieron las siete pantallas; se probó búsqueda por arriendo, limpieza del filtro, selección de transferencias, explicación desplegable de recurrencias y casilla temporal de revisión. La marca realizada por la prueba se descarta; no representa aprobación del usuario. Consola observada sin errores ni advertencias en la pestaña del aplicativo.

Se revisó el resumen a 320, 768, 1024 y 1440 px. El ancho del documento coincidió con el ancho disponible (305, 753, 1009 y 1425 px, descontando la barra de desplazamiento); no hubo desbordamiento horizontal global. Se inspeccionaron capturas del resumen y las pantallas de ahorros y revisión. Esto no sustituye una auditoría exhaustiva de accesibilidad ni una prueba de todos los módulos en cada tamaño. CSS e icono respondieron HTTP 200. La comprobación de red se limitó a esos recursos y los registros del servidor; no se obtuvo un perfil completo de rendimiento.

Captura de escritorio conservada como evidencia local fuera de Git: `C:\Users\Diego\.codex\visualizations\2026\10\18\01a14cb2-6722-78a2-8d3a-a2039aa4a5a2\finanzas-dagd-fase1-desktop.jpg`. La captura móvil del navegador integrado no resultó adecuada para juzgar el detalle visual; el control de ancho móvil se corroboró con medidas del DOM. La revisión final del usuario en su pantalla sigue pendiente.

El servidor se dejó ejecutándose en segundo plano, enlazado solo a 127.0.0.1:8765; los registros y el PID inicial se guardan en `local/`, excluido de Git. En Windows, el proceso que escucha puede ser hijo del lanzador del entorno virtual y tener otro PID; no detener procesos ajenos usando solo el número guardado. Para próximas ejecuciones se entrega `Iniciar_Finanzas_DAGD.cmd`.

### Revisión técnica final

Revisión propia de corrección, legibilidad, separación de datos ficticios, límites de entrada y exposición local. Se añade una prueba de que la transferencia se filtra correctamente y no se suma a los gastos consolidados. La batería final tiene diez pruebas, todas aprobadas. Se invirtió temporalmente la condición del filtro; una prueba de regresión detectó el fallo y se restauró el archivo original antes de repetir la batería completa. Registro local: `local/mutation-test.log`. No se afirma que `pip check` sea una auditoría de vulnerabilidades: verifica compatibilidad de dependencias. La demostración no es una entrega de producción y todavía no admite datos reales.

### Estado de aprobación

**Fase 1 pendiente de revisión y aprobación del usuario.** Fase 2 no iniciada. No se autoriza ni ejecuta push de esta entrega. El manual actual es provisional.

## Actualización del manual antes de la primera prueba

Por solicitud del usuario, se amplía MANUAL_USUARIO.md como documentación de uso mantenida durante todo el desarrollo. Incluye inicio desde el entorno ya preparado, acceso sin crear usuario ni superusuario, arranque manual y recuperación del entorno, cierre, recorrido de pantallas, límites, privacidad y solución de problemas. Se contrastó con el iniciador y la configuración actuales. Cada cambio de funcionamiento o acceso deberá actualizar el manual, el proceso y el changelog. No se modificó código ni el número de versión y no se repitieron pruebas de comportamiento por un cambio exclusivamente documental. La Fase 1 sigue pendiente de revisión; no se ejecuta push.

## Publicación autorizada de la Fase 1 y mejora de inicio

El usuario pidió publicar toda la Fase 1, abrir automáticamente el navegador y conservar Revisar esta fase durante el desarrollo. Se añade iniciar.py: confirma identidad del servidor, espera su disponibilidad, abre una pestaña y reutiliza una instancia existente. Cuatro pruebas del iniciador cubren reutilización, espera, fallo de arranque y puerto ocupado por otro servicio. La versión cambia a 0.1.0-alpha.2. Se mantiene la muestra pública ficticia; la referencia exacta de septiembre se documenta exclusivamente en local/REFERENCIA_SEPTIEMBRE.md, ignorada por Git. No se implementan aún las nuevas capacidades propuestas para Fase 2 y posteriores.

## Revisión del plan posterior a publicar Fase 1

Se confirmó origin/dev1 en 7153eb6. Después se instalaron desde commits fijos las skills solicitadas y la variante de Taste para proyectos existentes; se documentaron fuentes, verificación, motor de Impeccable y advertencia de limpieza en docs/SKILLS_UI.md. Se investigaron fuentes oficiales para consulta opcional de saldo; no se confirmó habilitación personal actual de ninguna API y no se accedió a cuentas. El nuevo info_Fases.md incorpora actividades separadas, presupuestos por proyecto/compra y calculadora de financiación, manteniendo cinco fases y Revisar esta fase. Se añade AGENTS.md para conservar las instrucciones del usuario en futuras sesiones. Esta propuesta queda local y pendiente de aprobación; no se inicia Fase 2 ni se publica automáticamente esta revisión.

## Autorización de inicio de Fase 2

El usuario aprobó el alcance revisado, ordenó publicar lo pendiente y canceló la integración bancaria. Solicitó que todos los commits sean en español; se aplica desde esta instrucción y se renombra el commit local aún no publicado, sin reescribir commits ya publicados. Los nuevos incrementos de implementación se conservarán locales hasta su autorización.

## Entrega local de Fase 2 — 2026-10-17

### Autorización y Git

Se publicó la revisión documental autorizada en origin/dev1 mediante `ea0af24`, con mensaje en español. Sustituye al commit local todavía no publicado de la revisión anterior; no se reescribió historia remota. La integración bancaria está cancelada. Los incrementos de implementación posteriores quedan en commits locales en español hasta una nueva autorización para publicarlos.

### Implementación y decisiones

Versión `0.2.0-alpha.1`, incremento MENOR por nuevas capacidades en desarrollo inicial. Definición concreta en SPEC_FASE2.md. Se reutiliza el entorno y las dependencias de Fase 1; no se instala otro paquete del aplicativo.

SQLite persistente en data/finanzas.sqlite3, secreto estable en local/secret.key y respaldos en backups/, todos excluidos de Git. Primer usuario creado por el propio usuario; sin credenciales predeterminadas, administración pública ni recuperación por correo. Sesiones, validadores de contraseña y CSRF de Django. El iniciador aplica migraciones antes de arrancar y reconoce la cabecera del aplicativo al redirigir a configuración o acceso.

Se implementan actividades, cuentas y categorías propias; ingresos, gastos, saldos iniciales y transferencias enlazadas. Importes en centavos enteros y validación de dos decimales. Una cuenta puede tener fondos asignados a varias actividades. Aportes y retiros internos usan transferencia; no incrementan ingresos o gastos consolidados. Resumen de todo el historial vigente con filtro de actividad; fechas y concepto filtran el listado, no los totales generales. Los saldos negativos se muestran sin ocultar movimientos.

Corrección con revisión optimista y motivo; anulación sin eliminación física, con confirmación e historial. Catálogos no se eliminan desde la interfaz; el cambio de tipo de una categoría utilizada se bloquea si deja movimientos incompatibles. El identificador de envío evita duplicar movimientos al reenviar el formulario.

Respaldo JSON de entidades financieras mediante descarga POST o comando, formato permitido explícito, límite de 5 MiB/10.000 registros y SHA-256 para detectar daños. Restauración con validación, copia previa dentro de la transacción y reversión ante errores; no importa contraseñas ni sesiones. Se conserva el historial existente y se incorporan eventos faltantes. Solo copias propias de confianza: el hash no autentica su origen. Los archivos locales no están cifrados.

### Skills y fuentes

Se aplicó using-agent-skills y los flujos de especificación, Git/versionado, implementación incremental, pruebas, seguridad y revisión de código. Para la interfaz se aplicó Impeccable en modo Operate, preservando la identidad oscura/turquesa revisada y los controles conocidos. Se mantuvo la guía Revisar esta fase. La skill Taste orientada a páginas públicas no se aplica a este panel; no se añade un rediseño de marketing.

Impeccable context se ejecutó una vez al comenzar el trabajo UI. Detect se ejecutó una vez sobre las plantillas y CSS modificados: resultado JSON vacío; advirtió que no resuelve enlaces CSS expresados con etiquetas static de Django, por lo que su comprobación de colores es incompleta. Se inspeccionó el renderizado real; este resultado no equivale a una auditoría integral de accesibilidad.

Se contrastaron autenticación, formularios y transacciones con documentación oficial de Django 5.2: https://docs.djangoproject.com/en/5.2/topics/auth/default/ , https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/ y https://docs.djangoproject.com/en/5.2/topics/db/transactions/ .

### Verificación

Primero se ejecutaron pruebas del servicio sin implementar los modelos: fallaron por su ausencia. Los seis casos contables iniciales pasaron tras implementarlos. Las pruebas HTTP se ejecutaron antes de conectar las rutas: fallaron por respuestas 404 y por conservar el inicio de demostración; después pasaron con el flujo de acceso y las rutas nuevas. La prueba histórica de base en memoria se actualizó a la nueva ubicación privada de persistencia; las pruebas de demostración siguen comprobando que esa vista no acepta escrituras.

La batería completa previa a la revisión final pasó 41 pruebas. Incluyó primer registro único, inicio/cierre de sesión, propiedad cruzada, CSRF, precisión, transferencias, edición obsoleta, doble envío, anulaciones, filtros, copias dañadas y recuperación por comando con confirmación. Revisión final: se añadió un caso de rechazo de revisión inválida en respaldos; el resultado final se registra al cerrar la entrega.

manage.py check sin incidencias; makemigrations --check --dry-run sin cambios pendientes; pip check sin incompatibilidades. No se afirma que pip check sea una auditoría de vulnerabilidades. Se invirtió temporalmente el signo del destino de una transferencia; las pruebas detectaron la regresión y se restauró el archivo exacto antes de repetir los casos contables. Registro privado local/mutation-fase2.log. Pruebas financieras en base temporal, sin alterar movimientos personales.

Navegador real mediante CUA: sesión sintética en puerto 8766 y base separada local/revision-fase2.sqlite3. Se comprobó resumen, se registró un gasto ficticio con centavos y se observó su efecto en gastos, saldo total y saldo por cuenta. Se detectó una fecha inicial vacía y se corrigió con prueba de regresión; se verificó nuevamente la fecha de hoy y el formulario. Se mejoró el espaciado de las instrucciones de contraseña. Captura de resumen sintético fuera de Git: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/fase2_resumen_ensayo.png.

La instalación personal del puerto 8765 se migró y se abrió en Configurar mi usuario. No se crearon usuarios ni movimientos personales, ni se importó el notebook. La revisión visual se realizó en el tamaño de escritorio disponible; no se repitió una auditoría completa de anchos móviles, rendimiento o accesibilidad. El usuario debe elegir sus credenciales y revisar en su pantalla.

### Estado

Entrega local de Fase 2 disponible para revisión. Manual, README, tareas, fases y changelog actualizados. No se considera aprobada por pasar las pruebas; no se inicia Fase 3 y no se publica implementación nueva automáticamente.

Cierre de verificación: la batería final pasó **42 pruebas**, sin cambios de migración pendientes ni incompatibilidades de dependencias. La copia de ensayo se mantuvo separada y su servidor se cerró. La instancia personal se recargó con la versión final y permanece en el primer acceso para que el usuario cree sus credenciales. Revisión propia de corrección, propiedad de datos, validación de archivos, transacciones, navegación, legibilidad y paginación: apta para revisión local, sin equivaler a una entrega pública estable. Los registros locales y la captura sintética no se incluyen en Git.

## Documentación accesible desde el aplicativo — 2026-10-17

Por solicitud del usuario, el bloque inferior de la barra lateral convierte CHANGELOG.md en hipervínculo y añade MANUAL_USUARIO.md debajo. Ambos usan target=_blank y rel=noopener noreferrer, con indicación accesible de pestaña nueva. Lectores de solo lectura para dos nombres permitidos explícitamente, disponibles antes del registro para poder consultar el manual inicial; sin rutas arbitrarias ni exposición de datos privados. Se muestra el Markdown original escapado, con ajuste de línea y tamaño de lectura de 16 px. No se añade un procesador de Markdown ni otra dependencia.

Agent Skills aplicado: descubrimiento de flujos, pruebas antes del cambio, Git/versionado y revisión de alcance/UI. Se mantiene la identidad existente y se consulta el piso de calidad de Impeccable. Tres pruebas nuevas produjeron cuatro fallos esperados antes de implementar rutas/enlaces. Verificación final y revisión visual se consignan al cerrar el cambio. Versión local 0.2.0-alpha.2; commit en español y sin push.

Se aclaró al usuario que Ahorros y Préstamos y deudas no se cancelaron: eran pantallas ficticias de Fase 1 y se retiraron del menú del registro real al preparar Fase 2. Siguen disponibles en la demostración; sus capacidades operativas permanecen en Fase 4 según el plan. Esta petición no autoriza adelantar esa fase ni cambia su alcance.

Verificación del cambio: las 45 pruebas de la batería completa pasaron y manage.py check no informó incidencias. Las pruebas nuevas comprueban ambos documentos antes del registro, rechazo de escrituras, lista permitida, escape de HTML y enlaces con pestaña nueva/rel seguro. En navegador real se pulsaron los dos enlaces desde la demostración y se observaron pestañas independientes de Manual de usuario e Historial de cambios, conservando la pantalla de origen; se inspeccionó el lector y la posición de los enlaces. Evidencia local: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/enlaces_documentacion.png. Impeccable detect devolvió lista vacía, con limitación conocida al resolver static de Django para CSS; la revisión visual complementó ese control. Revisión propia: rutas fijas, contenido escapado, lectura de archivos actuales y ausencia de escrituras financieras. No se ejecuta push ni se aprueba otra fase por este ajuste.

## Corrección de formato Markdown y publicación autorizada — 2026-10-18

El usuario señaló que el lector mostraba títulos y código como texto. La causa era presentar el archivo completo en un pre escapado sin procesar Markdown. Solicitó corregirlo y publicar los cambios para cerrar la jornada; se incluye en esa autorización la entrega local de Fase 2 y el ajuste previo de enlaces. No se interpreta como aprobación para iniciar Fase 3 ni se programa un recordatorio para mañana.

Se aplicaron using-agent-skills, pruebas antes del cambio, Git/versionado, seguridad y revisión de código; refinamiento UI limitado al lector, conservando los estilos existentes. Se sustituyó el pre global por un artículo con HTML convertido mediante Python-Markdown y filtrado con nh3. Lista explícita de etiquetas y atributos, protocolos http/https/mailto y contenido activo eliminado; únicamente el resultado saneado se marca como HTML seguro. No se añaden scripts al navegador. Rutas limitadas a los mismos dos documentos públicos, consultados en cada solicitud. Se soportan encabezados, listas, énfasis, enlaces, tablas y código cercado; el código se presenta monoespaciado en bloques desplazables. Se evita duplicar el encabezado principal del documento.

Instalación aislada desde PyPI de ruedas binarias: Markdown==3.11.1 y nh3==0.3.7. Versiones fijadas en requirements.txt; sin actualizar pip ni modificar Python global. Fuentes consultadas: https://python-markdown.github.io/ y https://nh3.readthedocs.io/en/latest/ . No se modifica la base de datos ni se importan datos personales. Para otra copia del proyecto se reinstala requirements.txt; la lectura posterior funciona sin red.

Pruebas de regresión escritas antes de implementar: diez aserciones fallaron al comprobar el formato y la eliminación de HTML peligroso. Se mantienen los controles de documentos permitidos, método HTTP y apertura en pestañas nuevas; se añade cobertura de encabezados/listas/código/tablas/enlaces y de ejemplos de HTML escapados dentro de código. Tras implementar, las cinco pruebas del lector pasaron. Manual y changelog actualizados; versión 0.2.0-alpha.3. Verificación integral, revisión visual y resultado de publicación se registran al cerrar el cambio.

Cierre de verificación: pasaron las **47 pruebas** del proyecto, manage.py check sin incidencias, pip check sin incompatibilidades y migraciones sin cambios pendientes. En el navegador real se recargaron ambos documentos: encabezados semánticos y listas en el historial; listas numeradas, énfasis y bloques de comandos monoespaciados/desplazables en el manual. Captura privada de evidencia: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/markdown_formateado.png. Impeccable detect devolvió lista vacía con la limitación conocida de resolver static de Django; se complementó con inspección visual. Revisión propia de corrección, límites del HTML seguro, ausencia de escrituras financieras y dependencias fijadas: apto para la publicación autorizada en dev1.

La publicación autorizada incluye los commits locales de implementación de Fase 2 (50fd437), enlaces de documentación (b9fd20d) y esta corrección. Datos, usuarios, sesiones, secretos, respaldos y capturas privadas siguen excluidos de Git. Punto de continuación para la próxima jornada: recoger la revisión funcional del usuario sobre Fase 2 antes de iniciar Fase 3. No se adelantan nuevas funciones ni se crea una automatización para mañana.

## Índice lateral y mayor ancho en documentos — 2026-10-18

El usuario solicitó navegación por títulos/subtítulos en el manual y mayor aprovechamiento horizontal también para CHANGELOG. Se aplica el índice a ambos lectores usando la extensión TOC ya incluida en Python-Markdown, sin nuevas dependencias ni scripts. Fuente oficial consultada: https://python-markdown.github.io/extensions/toc/ . Agent Skills aplicado: descubrimiento, pruebas antes del cambio, flujo de Git y refinamiento de la interfaz conforme al piso de calidad de Impeccable.

Se generan identificadores doc- a partir de los encabezados, únicos incluso si se repiten. El contenido y el índice se sanean con nh3; se permite id únicamente en h1–h6. Navegación nativa por fragmentos, resaltado de destino, enlace para saltar al contenido y foco visible. Índice sticky de altura limitada y desplazamiento independiente en escritorio; se coloca encima del artículo hasta 900 px. Contenedor ampliado a un máximo de 1600 px y columnas flexibles; los bloques de código y tablas conservan desplazamiento interno. Manual y changelog actualizados, versión 0.2.0-alpha.4.

Dos pruebas nuevas fallaron antes de implementar el índice. Tras implementar pasaron las siete pruebas del lector: jerarquía, destinos repetidos, enlaces de ambos documentos y filtrado de HTML activo en los encabezados, además de las comprobaciones anteriores de formato y seguridad. La actualización de expectativas con id conserva la exigencia de encabezados semánticos. No se modifican datos financieros ni se inicia otra fase. Este cambio queda local; la autorización previa de publicación correspondía al estado anterior.

Verificación final: **49 pruebas correctas**, manage.py check sin incidencias y git diff --check sin errores. En navegador real se observó el índice a la izquierda y el artículo más ancho en los dos lectores; al pulsar Crear respaldos se verificó la navegación al fragmento doc-9-crear-respaldos, con el encabezado visible y resaltado, manteniendo el índice fijo. Se comprobó la jerarquía de versiones/subtítulos del historial y su desplazamiento independiente. Captura privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/indice_manual.png. No se realizó una auditoría completa de tamaños móviles; el comportamiento adaptable está definido en CSS. Impeccable detect sin hallazgos, con la limitación conocida de enlaces static de Django. Revisión propia de anclas, HTML saneado, estilos y alcance: cambio listo para revisión local. No se ejecuta push ni se modifica el estado de aprobación de Fase 2.

## Autorización de publicación del índice — 2026-10-18

El usuario ordenó subir el ajuste para finalizar la jornada. Se autoriza publicar 4baec13 (índice lateral y mayor ancho del manual/historial) y este registro documental en origin/dev1. La implementación conserva sus 49 pruebas correctas y verificación visual ya registradas; no se cambia comportamiento ni se repiten pruebas por este ajuste documental. Se mantiene la versión 0.2.0-alpha.4. La publicación no autoriza avanzar de fase. Se verificará sincronización con el remoto y árbol de trabajo limpio tras el push.

## Contraer y filtrar documentación — 2026-10-18

El usuario solicitó reducir la extensión del índice y poder filtrar tanto CHANGELOG como el manual. Se implementan dos niveles: capítulos/versiones del contenido plegables y grupos de subtítulos del índice contraíbles. Primera sección abierta por defecto; controles Expandir todo y Contraer todo. Filtro local por texto completo de cada sección, ignorando mayúsculas, tildes y diferencias de espacios, con contador y estado vacío. Se conserva el estado de apertura previo al filtro para recuperarlo al limpiar. Los enlaces a encabezados abren su contenedor aunque estuviera plegado o el fragmento no cambie. La consulta no se guarda ni sale del navegador.

Agent Skills aplicado: descubrimiento, pruebas, Git y revisión de seguridad/UI. Se reutiliza details/summary nativo y JavaScript externo local, sin bibliotecas nuevas. Fuente consultada: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details . La política CSP mantiene default-src none y permite script-src self solo en la ruta de documentos, sin unsafe-inline ni eval. HTML de Markdown sigue saneado antes de usarlo; el script mueve nodos existentes y crea etiquetas con createElement/textContent, sin insertar HTML a partir de búsquedas. Controles ocultos hasta inicializar; si no se ejecuta JavaScript, sigue visible el documento completo con su índice original.

La prueba de controles y alcance de CSP falló antes de implementar. Después pasaron las nueve pruebas Python del lector (incluyendo contenido disponible sin scripts) y dos pruebas de búsqueda con node --test preview/test_document_js.cjs. Se reutilizó Node ya instalado en el PC para esas comprobaciones; el aplicativo no necesita Node al ejecutarse. La interacción completa se verifica en navegador real al cerrar el cambio. Manual y changelog actualizados; versión 0.2.0-alpha.5. Cambios locales, sin orden de push en esta petición y sin avance a otra fase.

Verificación final: 51 pruebas Python y dos de JavaScript correctas; manage.py check y git diff --check sin incidencias. En navegador real: historial filtrado por 0.1.0-alpha.2 (1 de 8 secciones), contraer la coincidencia y su grupo del índice, ausencia de resultados y limpieza con recuperación del listado; abrir un grupo del índice y navegar a una versión cerrada. En el manual, CONTRASENA encontró cuatro capítulos sin exigir tilde/ñ, Contraer todo dejó cero de cuatro abiertos y Expandir todo abrió los cuatro; se comprobó el salto a Crear respaldos. Se restauraron los lectores sin filtros de ensayo. Consola observada sin errores ni advertencias del lector. La instancia anterior del mismo proyecto mantenía plantillas en memoria: se verificaron ruta y relación de procesos antes de reiniciarla, sin modificar datos.

Evidencia privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/documentos_plegar_filtrar.png. Impeccable detect sin hallazgos, con la limitación conocida al resolver static de Django para CSS; revisión visual complementaria en escritorio. No se afirma una auditoría de todos los tamaños móviles ni de todos los navegadores. Revisión propia de alcance, manejo de nodos, permisos de scripts y filtrado: apto para revisión local. Commit en español, sin push y sin aprobación implícita de otra fase.

## Controles de documentos dentro del índice — 2026-10-18

Por corrección del usuario, se mueven buscador, contador y botones Limpiar filtro/Expandir todo/Contraer todo dentro del panel En este documento, encima de sus títulos, en ambos lectores. Se conserva la lógica de búsqueda, anclas y plegado. Controles ajustados a la columna; únicamente la lista de títulos se desplaza dentro del panel fijo en escritorio. En pantallas pequeñas el panel permanece encima del artículo. Agent Skills aplicado para descubrimiento y revisión UI; se conserva la identidad y se consulta el piso de calidad de Impeccable.

Cambio de ubicación/estilos, sin lógica financiera ni dependencias nuevas: no se añaden pruebas que reproduzcan la estructura del CSS. Se ejecutarán las pruebas existentes del lector y búsqueda, además de comprobar el navegador. Manual y changelog actualizados; versión 0.2.0-alpha.6. Commit local en español; sin push ni avance de fase por esta petición.

Verificación: nueve pruebas Python del lector y dos de búsqueda JavaScript correctas, sin errores de whitespace. En navegador real se comprobó la ubicación de los controles dentro del índice en manual y CHANGELOG; en el manual, CONTRASENA devolvió cuatro de trece capítulos y Limpiar filtro recuperó el listado completo. Captura privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/controles_en_indice.png. Se conserva el tamaño de lectura de las listas y el contenido de secciones, evitando heredar el tamaño reducido de details global. Impeccable detect sin hallazgos, con limitación conocida para static de Django; verificación visual complementaria en escritorio. No se repite la batería financiera completa por un cambio limitado a ubicación y estilos. Se conserva la autorización de publicación pendiente; no se ejecuta push.

## Tamaño uniforme de botones y descripción de filtro — 2026-10-18

Por solicitud del usuario, Limpiar filtro, Expandir todo y Contraer todo se apilan individualmente al 100% del ancho del buscador; altura mínima uniforme de 46 px. Descripción del filtro a 11 px, sin reducir el tamaño de lectura del documento. Ajuste común a manual y CHANGELOG. Se añade la versión al URL de document.css para renovar estilos guardados por el navegador al recargar una actualización; la versión procede de VERSION mediante settings. No cambia la lógica de búsqueda ni el almacenamiento financiero.

Agent Skills aplicado para descubrir el flujo y mantener Git/documentación; se conserva el diseño del lector. Cambio visual reversible, sin pruebas nuevas de estructura CSS. Se verifican pruebas existentes del lector y dimensiones visibles en navegador. Manual y changelog actualizados, versión 0.2.0-alpha.7; commit local en español y sin push por esta petición.

Verificación: nueve pruebas existentes del lector correctas. Navegador real en ambos documentos: buscador de 268 px y los tres botones de 268 px, cada botón con 46 px de alto; descripción calculada de 11 px. Se inspeccionó la captura en escritorio y se confirmó carga de los estilos actualizados. Evidencia privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/botones_ancho_buscador.png. Revisión propia del cambio compartido y renovación de caché, sin tocar filtros ni datos. Impeccable detect sin hallazgos, con la limitación conocida de enlaces static de Django. Sin pruebas nuevas para estructura CSS ni repetición de pruebas financieras por este ajuste visual. Se conserva el cambio local, sin push.

## Corrección de disposición horizontal de botones — 2026-10-18

El usuario aclaró que esperaba los tres botones en formato horizontal, manteniendo la letra reducida de la descripción. Se reemplaza la columna por tres columnas iguales dentro del ancho del buscador; textos compactos con ajuste de línea y altura mínima de 44 px. Se mantiene la descripción a 11 px. Ajuste compartido de CSS sin cambiar búsquedas ni datos. Agent Skills aplicado para el flujo y la trazabilidad; cambio visual sin pruebas nuevas que reflejen el CSS. Manual y changelog actualizados, versión 0.2.0-alpha.8. Se verificará en navegador y quedará en commit local en español, sin push.

Verificación: nueve pruebas del lector correctas. En ambos documentos se midió una fila de 268 px, igual al buscador, con tres botones de 86 px y dos separaciones de 5 px; todos tienen la misma posición vertical. La descripción mantiene 11 px. Captura privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/botones_horizontales.png. Revisión visual y detector de estilos completados; sin cambios de lógica ni datos y sin push.

## Botones más estrechos y autorización de publicación — 2026-10-18

El usuario aprobó la disposición horizontal y pidió reducir su ancho respecto al buscador, además de subir los cambios al repositorio. La fila se ajusta al 90% del ancho del campo y se alinea a la izquierda; conserva tres columnas iguales, altura mínima de 44 px y descripción de 11 px. Cambio CSS compartido sin alterar la lógica del lector. Agent Skills aplicado para mantener el flujo de revisión, documentación y Git. No se añaden pruebas que reflejen la estructura de CSS; se verifican pruebas existentes y dimensiones reales. Versión 0.2.0-alpha.9; manual y changelog actualizados.

Autorizado publicar en dev1 los cambios pendientes desde 301fc33: plegado/filtro (92ee0c4), controles en el índice (ad9e1d3), ajustes de botones (4ead57e y 02d9b1b) y este incremento. Todos los commits en español. No se interpreta como aprobación para iniciar Fase 3. Datos, secretos y respaldos permanecen fuera de Git.

Verificación: nueve pruebas Python del lector y dos pruebas JavaScript correctas. En navegador real se midió, tanto en manual como en CHANGELOG, buscador de 268 px y fila de botones de 241,19 px (90%), con tres botones de aproximadamente 77,06 px en la misma posición vertical. Descripción conservada a 11 px. Evidencia privada: C:/Users/Diego/Documents/ChatGPT/Finanzas Personales/botones_compactos.png. Revisión visual y detector de estilos completados. No se añaden pruebas de estructura CSS ni se repite la batería financiera por este ajuste visual. Se publica por la orden expresa del usuario y se verifica sincronización final con origin/dev1; el avance de fase sigue requiriendo su revisión.
