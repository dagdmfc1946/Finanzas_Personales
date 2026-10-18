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
