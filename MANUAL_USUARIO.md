# Manual de usuario · Finanzas DAGD

Este manual explica cómo ejecutar y revisar las funciones disponibles. Se actualizará con cada cambio que afecte el inicio, acceso, pantallas, registro de información, respaldos o uso del aplicativo, sin esperar al cierre del proyecto.

Estado actual: **Fase 1, vista previa con datos ficticios, pendiente de tu aprobación**. Versión cubierta: `0.1.0-alpha.2`. La fuente única de versión del software es `VERSION`; el historial está en `CHANGELOG.md`.

## 1. Lo que debes saber antes de comenzar

| Pregunta | Respuesta para esta versión |
|---|---|
| ¿Debo crear un usuario? | **No.** Todavía no hay registro, inicio de sesión ni usuarios del aplicativo. |
| ¿Debo crear un superusuario de Django? | **No.** No hay un panel de administración habilitado ni debes ejecutar `createsuperuser`. |
| ¿Necesito contraseña? | No para esta vista previa. La protección del acceso se definirá antes de trabajar con información personal. |
| ¿Debo preparar la base de datos? | No. No debes ejecutar migraciones para esta fase. SQLite funciona en memoria para las comprobaciones internas de arranque. |
| ¿Puedo ingresar ya mis cuentas reales? | Todavía no. Las pantallas son de demostración y no permiten guardar movimientos financieros. |
| ¿Se importó mi notebook? | No. Todos los importes y nombres del escenario se crearon como ejemplos ficticios. |
| ¿Necesito Internet? | Solo para instalar dependencias si el entorno no está preparado. La vista previa ya instalada funciona sin Internet. |
| ¿Necesito REA o el APK de Moneri? | No. REA fue una herramienta de referencia; no es requisito para ejecutar Finanzas DAGD. |
| ¿Es un programa Android? | No. Actualmente se ejecuta en tu PC y se utiliza desde el navegador. |
| ¿Debo abrir puertos o usar permisos de administrador? | No. La aplicación se inicia con tu sesión habitual de Windows y escucha únicamente en tu propio PC. |

El período **octubre de 2026** es un escenario fijo de ejemplo, no una consulta de tus finanzas ni un selector de mes funcional. La Fase 1 sirve para personalizar la estructura antes de implementar el registro real.

## 2. Ubicación y requisitos

Carpeta del proyecto:

```text
D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales
```

Requisitos del entorno preparado:

- Windows y un navegador, como Chrome o Edge.
- Python 3.12; en la preparación inicial se utilizó Python 3.12.10.
- Entorno virtual `.venv` dentro del proyecto, con las dependencias de `requirements.txt`.
- Puerto local 8765 disponible, salvo que Finanzas DAGD ya esté ejecutándose allí.

**El entorno ya se preparó en este PC.** Para la primera prueba, comienza por el apartado siguiente; no necesitas reinstalar Python, Django ni las dependencias.

## 3. Primera ejecución en tu PC

### Si el aplicativo ya quedó abierto por Codex

1. Abre [Finanzas DAGD](http://127.0.0.1:8765/) en el navegador.
2. Comprueba que aparezcan el nombre Finanzas DAGD y el aviso de datos ficticios.
3. Si carga correctamente, ya puedes recorrerlo. Si ejecutas el iniciador, reconocerá la instancia existente y abrirá una pestaña sin crear otro servidor.
4. Si aparece un error de conexión, utiliza el iniciador descrito a continuación.

El servidor que abre Codex puede estar funcionando en segundo plano, sin una consola visible. Si necesitas detener esa instancia y no tienes su consola, solicítalo en el chat para identificar el proceso correspondiente; no cierres indiscriminadamente procesos Python.

### Inicio habitual con doble clic

1. Abre el Explorador de archivos y entra en la carpeta del proyecto.
2. Haz doble clic en **`Iniciar_Finanzas_DAGD.cmd`**.
3. Se abrirá una ventana de consola. Déjala abierta mientras uses el aplicativo.
4. Espera a que la consola indique que el servidor está escuchando en `http://127.0.0.1:8765/`. La salida de Django puede mostrar `Starting development server at ...`.
5. El iniciador abrirá automáticamente una pestaña en tu navegador predeterminado cuando confirme que Finanzas DAGD está listo. Si el navegador no se abre, entra manualmente en [http://127.0.0.1:8765/](http://127.0.0.1:8765/).

El iniciador espera hasta 20 segundos al servidor antes de abrir la pestaña. Si Finanzas DAGD ya está abierto, reutiliza ese servidor; si el puerto pertenece a otro servicio, informa del conflicto y no lo detiene. Al reutilizar una instancia, el iniciador termina: esa ventana no controla el servidor existente. La ruta del proyecto no se introduce en la barra del navegador: se utiliza la dirección HTTP indicada.

El aviso de Django sobre servidor de desarrollo es esperado en esta entrega local. No cambies la dirección a `0.0.0.0`, no configures acceso desde Internet y no abras puertos del router para esta fase.

### Inicio alternativo desde PowerShell

```powershell
Set-Location -LiteralPath 'D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales'
.\Iniciar_Finanzas_DAGD.cmd
```

También puedes ejecutar directamente:

```powershell
Set-Location -LiteralPath 'D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales'
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765 --insecure --noreload
```

No es necesario activar el entorno virtual: estos comandos invocan su Python directamente. El parámetro `--insecure` permite servir los estilos e icono con `DEBUG=False` en esta configuración de desarrollo; no debe interpretarse como una instrucción para desactivar la seguridad del equipo.

## 4. Cerrar, detener y volver a abrir

- Cerrar la pestaña **no detiene** el servidor.
- Si lo iniciaste con el archivo `.cmd` o desde PowerShell, vuelve a esa consola y pulsa **Ctrl+C**. Si Windows pregunta si deseas terminar el trabajo por lotes, confirma.
- Con el servidor detenido, la dirección local dejará de responder. Para volver a utilizarlo, ejecuta de nuevo el iniciador y abre la misma dirección.
- Al reiniciar o apagar el PC, será necesario iniciar otra vez el aplicativo. No se configuró inicio automático con Windows.
- Esta vista previa no tiene datos financieros guardados que puedas perder al detenerla. Las casillas de revisión son temporales.

Si el servidor fue iniciado en segundo plano por Codex, aplica la indicación del apartado 3 para identificarlo antes de detenerlo.

## 5. Recorrido recomendado para tu primera revisión

### Resumen

Revisa las tarjetas de ingresos, gastos realizados y saldo en cuentas. En el ejemplo:

- Ingresos: $ 4.000.000.
- Gastos realizados: $ 1.350.000.
- Saldo consolidado: $ 2.650.000, que incluye $ 300.000 en Ahorros.

La transferencia a Ahorros no se suma a los gastos, porque mueve dinero entre cuentas propias. La gráfica muestra el recorrido del escenario y no consulta información bancaria. Las cuentas, metas y compromisos visibles sirven para juzgar la distribución y la claridad de la pantalla.

### Movimientos

1. Entra en **Movimientos** desde la navegación.
2. En Buscar movimiento escribe `arriendo` y pulsa **Filtrar**: debe quedar el gasto de arriendo.
3. Pulsa **Limpiar** para recuperar los seis movimientos de ejemplo.
4. Selecciona **Transferencias** en el tipo y pulsa **Filtrar**: debe quedar la reserva para emergencias.
5. Prueba una búsqueda sin coincidencias para revisar el mensaje de estado vacío.

La búsqueda también reconoce categoría y cuenta. El tipo y la búsqueda se combinan. El máximo de búsqueda es de 80 caracteres. Los filtros aparecen en la dirección del navegador; no introduzcas información personal en ellos.

No encontrarás un botón para crear o guardar movimientos en esta fase. Los formularios financieros y su persistencia se desarrollarán desde la Fase 2.

### Mi sueldo

Compara el desglose de devengos, deducciones y neto. Revisa si te resulta clara la separación entre período del sueldo, fecha de recepción y mes presupuestado. Los importes de ejemplo no representan una liquidación laboral ni tasas legales.

La idea propuesta es registrar el neto una sola vez, aunque se muestre su desglose. El registro real se desarrollará en la Fase 3.

### Presupuesto

Revisa la distribución por categoría, el gasto realizado y el margen del presupuesto. Ese margen no es lo mismo que el saldo bancario. Los compromisos futuros aparecen como previstos y sin pagar; todavía no se suman a los gastos realizados.

Despliega la explicación **¿Cómo funcionarán las recurrencias?** para revisar la regla propuesta. Las categorías y límites visibles todavía no se pueden editar.

### Ahorros

Revisa las metas de fondo de emergencia y renovación del computador. Las barras muestran el progreso de ejemplo. Crear una meta no debería aumentar el saldo propio y reservar dinero no debería generar un gasto ficticio. El registro de metas y aportes llegará en la Fase 4.

### Préstamos y deudas

Compara la compra financiada por pagar con el préstamo otorgado por cobrar. Despliega los componentes de la cuota.

Estos son **ejemplos independientes**: sus saldos y fechas no están integrados al resumen ni al historial de movimientos. La gestión real de préstamos, cuotas, capital, intereses y cargos se desarrollará en la Fase 4.

### Revisar esta fase

Utiliza la lista como guía para comprobar nombre, estilo, secciones, claridad del resumen, filtros y comodidad en tu pantalla. Marcar casillas no envía mensajes ni guarda una aprobación y puede reiniciarse al recargar o cerrar.

Envía tus sugerencias o aprobación **por el chat**. No hace falta aprobar la fase antes de proponer ajustes.

## 6. Qué funciona y qué sigue pendiente

| Disponible para probar ahora | Pendiente de desarrollo |
|---|---|
| Navegación por siete secciones. | Crear, editar o anular movimientos reales. |
| Filtros sobre registros ficticios. | Guardar cuentas, categorías y saldos propios. |
| Vistas propuestas de sueldo y presupuesto. | Configurar sueldo, recurrencias y presupuestos reales. |
| Ejemplos de metas y obligaciones. | Registrar aportes, cuotas, pagos y cobros. |
| Guía temporal de revisión. | Persistencia, respaldos y restauración de datos financieros. |
| Interfaz local con recursos incluidos. | Importación del notebook, exportaciones y reportes definitivos. |

No hay conexión con bancos, ejecución de pagos, sincronización en nube ni acceso móvil configurado. No debes interpretar los importes de demostración como tu situación financiera.

## 7. Preparar el entorno si falta o en otra instalación

Este apartado es de recuperación o instalación nueva; no es un paso obligatorio en cada inicio. Desde PowerShell:

```powershell
Set-Location -LiteralPath 'D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales'
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test preview
.\Iniciar_Finanzas_DAGD.cmd
```

`pip install` necesita Internet para descargar dependencias si no están disponibles en caché. No ejecutes la preparación sobre un servidor que esté utilizando ese entorno: detén primero la instancia que iniciaste. Si `py -3.12` no se reconoce, comprueba la instalación de Python 3.12 antes de continuar; no sustituyas versiones sin revisar su compatibilidad.

No ejecutes `migrate`, `createsuperuser` ni instales servidores de bases de datos para esta fase. No necesitas modificar la política de ejecución de PowerShell para utilizar el `.cmd` o invocar directamente `python.exe`.

## 8. Problemas frecuentes

| Situación | Qué revisar |
|---|---|
| El navegador indica que no puede conectarse. | Confirma que la consola siga abierta y que el servidor haya iniciado. Usa exactamente `http://127.0.0.1:8765/`, con HTTP y el puerto 8765. |
| El puerto ya está ocupado. | Comprueba si Finanzas DAGD ya carga en esa dirección. Si muestra otro programa, no lo detengas sin identificarlo; comunica el mensaje en el chat. |
| No se encuentra `.venv\Scripts\python.exe`. | Comprueba la carpeta del proyecto y sigue el apartado 7 si el entorno está ausente. No borres carpetas para resolverlo sin identificar la causa. |
| Aparece `No module named django`. | Asegúrate de usar el Python de `.venv` y de que estén instaladas las dependencias del apartado 7. |
| La consola se cierra o muestra un error al iniciar. | Ejecuta el iniciador desde una ventana de PowerShell ya abierta para poder leer el mensaje. Comunica el texto del error. |
| La página aparece sin estilos. | Inicia con el `.cmd` o con el comando completo que incluye `--insecure`. Después recarga el navegador. |
| Una búsqueda no muestra nada. | Revisa tanto el texto como el tipo seleccionado, o pulsa Limpiar. |
| No puedo editar importes o registrar mi sueldo. | Es el límite previsto de la vista previa, no un error de permisos ni falta de usuario. |
| Las casillas no recuerdan mi revisión. | Son controles temporales; tus comentarios y aprobación se registran mediante el chat. |
| Se modificó el proyecto pero sigo viendo la versión anterior. | El servidor se inicia con `--noreload`: después de cambios de código, detén y reinicia tu instancia; luego recarga la página. |

Los registros de la instancia iniciada por Codex se encuentran en `local/server.stdout.log` y `local/server.stderr.log`; no se suben a Git. El número de `local/server.pid` identifica el lanzador inicial y no debe usarse a ciegas para cerrar procesos. Cuando inicias desde tu consola, consulta su salida.

## 9. Datos, privacidad y respaldos

No se guardan movimientos, metas, cambios de importes ni casillas de revisión. Las búsquedas son parámetros de la dirección y pueden quedar en el historial del navegador o en la salida del servidor; utiliza solo términos de ejemplo.

Esta entrega no genera un archivo de base de datos financiero. Por tanto, no hay un respaldo de cuentas reales que debas crear antes de probarla. Las copias y restauración se implementarán desde que exista persistencia, en la Fase 2.

El entorno `.venv`, los registros `local/`, las futuras bases y respaldos están excluidos de Git. No copies información privada del notebook a los archivos de demostración ni a GitHub. Los archivos fuente se conservan mediante commits locales; una publicación remota requiere tu orden o aprobación explícita.

## 10. Accesibilidad y personalización

Puedes navegar con Tab y activar enlaces y botones mediante teclado. El enlace Saltar al contenido permite evitar recorrer toda la navegación. En pantallas pequeñas, las opciones del menú y las tablas se desplazan horizontalmente dentro de su zona.

Para pedir un cambio, indica **sección, cambio deseado y resultado esperado**. Por ejemplo: «En Resumen quiero ver primero el dinero disponible después de separar mis ahorros». Puedes sugerir otro tema visual, tamaño de letra, orden de secciones, nombres o reglas.

Cada fase se revisará ejecutando el aplicativo. Su aprobación se registra expresamente en el chat; no equivale a autorizar que se suba a GitHub.

## 11. Mantenimiento de este manual

En cada incremento que modifique el uso se actualizarán las instrucciones pertinentes y se registrará el cambio en `dev_Process.md` y `CHANGELOG.md`. Cuando se incorpore autenticación, este manual explicará la creación del primer usuario y su acceso; cuando exista persistencia, incluirá ubicación y tratamiento de los datos y procedimientos probados de respaldo/restauración.

Las funciones futuras permanecerán identificadas como pendientes hasta que se implementen y verifiquen. En la Fase 5 se realizará la revisión integral del manual; eso no aplaza sus actualizaciones durante el desarrollo.
