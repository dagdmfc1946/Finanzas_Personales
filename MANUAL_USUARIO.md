# Manual de usuario — Finanzas DAGD

Versión del software: consultar `VERSION` (SemVer 2.0.0: MAYOR.MENOR.PARCHE). Historial: `CHANGELOG.md`. Manual actualizado para Fase 2, entrega local `0.2.0-alpha.10`, pendiente de revisión del usuario.

## 1. Qué puedes usar ahora

Registro persistente de actividades, cuentas, categorías, saldos iniciales, ingresos, gastos y transferencias; resumen por actividad o consolidado; filtros; correcciones y anulaciones con historial; creación y restauración básica de respaldos. Se conserva **Revisar esta fase**.

El detalle de sueldo, recurrencias, presupuestos por proyecto/compra, metas y calculadora de cuotas se desarrollarán en Fases 3 y 4. La integración bancaria está cancelada. Las pantallas anteriores de esos módulos siguen disponibles como demostración ficticia, sin guardar operaciones.

## 2. Ejecutar en este PC

Carpeta: `D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales`.

1. Abre esa carpeta en el Explorador de Windows.
2. Haz doble clic en `Iniciar_Finanzas_DAGD.cmd`.
3. El iniciador prepara las tablas de la base local y abre una pestaña cuando el servidor está listo.
4. Si el navegador no abre automáticamente, visita **http://127.0.0.1:8765/**.
5. Conserva abierta la consola del iniciador. Para detener esa instancia, presiona **Ctrl+C** en ella.

Si ya existe una instancia identificada como Finanzas DAGD, el iniciador la reutiliza. Si el puerto pertenece a otro servicio, muestra un aviso y no lo cierra. Después de actualizar el código, detén la instancia anterior y vuelve a iniciar para cargar los cambios.

Para iniciar desde PowerShell:

```powershell
Set-Location 'D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales'
.\Iniciar_Finanzas_DAGD.cmd
```

El entorno `.venv` ya está preparado en este PC con Python 3.12 y Django 5.2. En otra instalación con Python disponible:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\Iniciar_Finanzas_DAGD.cmd
```

El servidor escucha únicamente en este equipo. No necesitas GitHub ni Internet para registrar movimientos con el entorno ya instalado. Este iniciador de desarrollo local no es un despliegue público.

## 3. Primera ejecución: crea tu usuario

La primera apertura muestra **Configurar mi usuario**. Elige un nombre y una contraseña propia de al menos diez caracteres que cumpla las validaciones indicadas. No hay contraseña predeterminada y no necesitas crear un superusuario ni usar la administración de Django.

Solo se permite este primer registro. Al terminar, entrarás al resumen. Las siguientes visitas pedirán **Iniciar sesión**. Usa **Cerrar sesión** al terminar en un equipo compartido y **Cambiar contraseña** para actualizarla.

Se crea una actividad inicial llamada **Personal / trabajo principal**. Cuentas, categorías y movimientos empiezan vacíos. Los ejemplos del notebook y de las pruebas no se importan automáticamente.

No existe recuperación por correo. Si olvidas la contraseña y tienes acceso autorizado a la carpeta local, detén el aplicativo y ejecuta:

```powershell
.\.venv\Scripts\python.exe manage.py changepassword TU_USUARIO
```

Introduce tú mismo la nueva contraseña cuando lo solicite la consola; no la escribas en comandos, documentos ni en el chat. No borres la base para recuperar el acceso.

## 4. Preparar actividades, cuentas y categorías

En **Actividades y cuentas**:

- **Actividad:** identifica para qué ámbito es el dinero. Puedes crear un emprendimiento y un trabajo secundario, además de tu actividad personal.
- **Cuenta:** identifica dónde está el dinero: banco, billetera, efectivo o ahorros. Una misma cuenta puede servir a varias actividades; no la dupliques por ese motivo.
- **Categoría:** clasifica un ingreso o gasto, por ejemplo trabajo, arriendo o transporte. Su tipo debe coincidir con el movimiento. Es opcional en el registro.

Al crear una cuenta, puedes indicar un saldo inicial y la actividad a la que pertenece. Si introduces un saldo positivo, se crea un movimiento **Saldo inicial** con fecha de hoy. Si es cero o lo dejas vacío, no crea ningún movimiento. Si el dinero inicial pertenece a varias actividades, registra saldos iniciales separados en **Nuevo movimiento**. No vuelvas a registrar como ingresos el dinero que ya incluía ese saldo.

Puedes editar nombres. El saldo inicial no se modifica desde la edición de cuenta: corrige su movimiento con un motivo. Una categoría ya utilizada no puede cambiar a un tipo incompatible con sus movimientos. No se eliminan cuentas o actividades desde esta interfaz.

## 5. Registrar ingresos y gastos

En **Movimientos → Nuevo movimiento**:

1. Selecciona **Ingreso** o **Gasto**.
2. Revisa fecha, concepto e importe en pesos colombianos (COP).
3. Selecciona la actividad y la cuenta de origen.
4. Elige una categoría compatible si deseas usarla.
5. Deja los destinos vacíos y pulsa **Guardar**.

Escribe importes positivos, sin separadores de miles, por ejemplo `25000.50`; se admiten hasta dos decimales. El tipo determina si suma o resta. Los importes se guardan como centavos enteros, evitando redondeos binarios en los cálculos del aplicativo.

El salario recibido es por ahora un ingreso de la actividad personal. Una venta del emprendimiento es un ingreso de su propia actividad; un gasto del emprendimiento debe llevar esa misma actividad. Puedes registrar movimientos con fecha futura; el resumen incluye todo el historial vigente, no solo el mes actual.

## 6. Transferencias y aportes

Usa **Transferencia** para mover dinero propio entre cuentas o actividades. Selecciona cuenta y actividad de origen, además de cuenta y actividad de destino. Deja la categoría vacía.

Puedes aportar dinero personal a tu emprendimiento incluso usando la misma cuenta física: conserva la cuenta y cambia la actividad de destino. Para retirar fondos, invierte origen y destino. Una transferencia entre actividades propias cambia la asignación del dinero, pero no aumenta los ingresos ni gastos externos del consolidado. El origen y el destino completos no pueden ser idénticos.

El reparto de un gasto entre varias actividades se registra manualmente en movimientos separados, cuidando que la suma sea el importe real. No hay reparto automático ni contabilidad empresarial en esta fase.

## 7. Entender el resumen y los filtros

**Resumen** muestra ingresos, gastos y saldo por cuenta para todas las actividades o la seleccionada. Los saldos iniciales y transferencias no aparecen como ingresos externos. El saldo calculado incluye los saldos iniciales y los movimientos vigentes de todo el historial. Un saldo negativo se conserva y se muestra: revisa registros faltantes o errores.

En **Movimientos**, filtra por concepto, actividad, tipo, fechas o inclusión de anulados; **Limpiar** restablece la selección. Las transferencias aparecen al filtrar tanto su actividad de origen como la de destino. Hay paginación de treinta movimientos.

Los filtros de fecha y concepto corresponden al listado de movimientos. Los totales del resumen se filtran por actividad y están rotulados como todo el historial. Ningún saldo representa una consulta al banco.

## 8. Corregir, anular y consultar historial

**Corregir** abre un movimiento vigente. Cambia los campos necesarios e indica el motivo. **Anular** solicita motivo y confirmación; retira su efecto de los saldos, conservando el registro. No hay eliminación definitiva desde la interfaz ni reactivación de anulados en esta fase.

Si otra ventana ya cambió el registro, recarga y revisa antes de volver a editar. Reenviar el mismo formulario de creación no debe duplicar el movimiento. Verifica el listado cuando un navegador o una interrupción deje dudas sobre el resultado.

**Historial** conserva registro, corrección, anulación, edición de catálogos y restauración. Despliega cada evento para ver antes/después. Esta primera vista técnica muestra `cents` en centavos (100 equivalen a 1 COP), identificadores internos y `revision` como número de edición. No constituye una bitácora inalterable frente a quien tenga acceso directo al archivo del PC.

## 9. Crear respaldos

En **Respaldos**, pulsa **Crear y descargar respaldo**. Además de la descarga, se crea una copia en `backups/`. También puedes ejecutar:

```powershell
.\.venv\Scripts\python.exe manage.py respaldo_finanzas
```

La copia JSON incluye actividades, cuentas, categorías, movimientos e historial financiero. No contiene contraseñas, usuarios, sesiones ni claves del sistema. El respaldo básico admite hasta 5 MiB o 10.000 registros. Conserva copias fuera del mismo disco y comprueba su recuperación con datos de ensayo antes de depender de ellas.

## 10. Restaurar una copia propia

La restauración **reemplaza los registros financieros actuales** por los del archivo elegido. Conserva tu usuario y contraseña actuales y los eventos ya existentes del historial; añade un evento de restauración y recupera los eventos faltantes de la copia. Antes de reemplazar datos, genera otra copia en `backups/`.

1. Detén el aplicativo con Ctrl+C y cierra otras instancias que usen la misma base.
2. Confirma la ruta de la copia propia que quieres recuperar.
3. Desde PowerShell en la carpeta del proyecto, ejecuta:

```powershell
.\.venv\Scripts\python.exe manage.py restaurar_finanzas 'C:\RUTA\finanzas-respaldo.json' --confirmar
```

4. Lee el resultado: muestra la ruta del respaldo previo.
5. Inicia nuevamente y revisa cuentas, movimientos y saldos.

El comando rechaza formatos incompatibles, archivos dañados, campos inesperados y referencias inválidas. Si la validación financiera falla, revierte los cambios de la base. La huella SHA-256 detecta alteraciones accidentales; no acredita quién creó el archivo. Restaura únicamente copias propias de confianza, sin editarlas manualmente.

En una instalación nueva, crea primero tu usuario local antes de restaurar la copia financiera. La copia JSON no recupera una contraseña olvidada. No se ofrece carga de archivos desde el navegador.

## 11. Archivos privados y cuidado de la instalación

`data/finanzas.sqlite3` guarda los datos persistentes y el acceso; `local/secret.key` mantiene el secreto de esta instalación; `backups/` contiene copias financieras. Están excluidos de Git, al igual que el notebook y las referencias privadas. No los publiques ni los adjuntes al repositorio.

El aplicativo protege el acceso a las pantallas mediante contraseña, pero **no cifra los archivos locales ni los respaldos**. Conserva el acceso de Windows protegido. Para copiar una instalación completa manualmente, detén el servidor primero y conserva la carpeta privada con sus permisos; copiar una base SQLite mientras está en uso puede producir una copia incompleta.

No borres `data/`, `local/secret.key` ni la base para resolver errores. Una reinstalación de dependencias no exige eliminar datos.

## 12. Consultar documentación en el aplicativo

En la parte inferior de la barra lateral, el enlace **CHANGELOG.md** abre el historial de cambios en una pestaña nueva. Justo debajo está **MANUAL_USUARIO.md**, que abre este manual en otra pestaña. La pantalla original conserva su formulario y filtros. Los lectores presentan títulos, listas, negritas, enlaces, tablas y bloques de código con formato. Consultan el archivo Markdown actual del proyecto cada vez que abres o recargas la página, sin modificarlo. El HTML se filtra antes de mostrarse; los ejemplos de código se conservan como texto dentro de sus bloques.

En ambos lectores encontrarás **En este documento**, un índice con títulos y subtítulos. Pulsa una entrada para ir directamente a esa sección; el encabezado de destino queda resaltado. En escritorio el índice permanece a la izquierda mientras lees y puede desplazarse si es largo. En pantallas pequeñas se sitúa encima del contenido. La lectura utiliza más ancho de pantalla; los comandos largos conservan desplazamiento horizontal dentro de su bloque. El índice se actualiza automáticamente al cambiar los encabezados del archivo.

Cada capítulo del manual y cada versión del historial se pueden abrir o cerrar pulsando su título. Al abrir el lector, la primera sección está desplegada y las demás contraídas; si entras por un enlace a una sección, esta se abre automáticamente. En el índice, las versiones o capítulos con subtítulos también pueden contraerse; **Ver esta sección** lleva a su contenido.

El buscador y los botones **Limpiar filtro**, **Expandir todo** y **Contraer todo** están dentro del panel izquierdo **En este documento**, encima de los títulos. Los tres botones se distribuyen en una única fila horizontal que ocupa el ancho del buscador, con una altura compacta de 32 px; la descripción del filtro conserva su tamaño de letra reducido. Al recorrer un índice largo, se desplaza la lista de títulos mientras los controles permanecen disponibles. En pantallas pequeñas el panel completo se coloca encima del contenido.

Utiliza **Filtrar títulos y contenido** para buscar una palabra, frase o número de versión. La búsqueda ignora mayúsculas y tildes, muestra solo secciones coincidentes y las abre automáticamente, junto con sus entradas del índice. **Limpiar filtro** recupera todas las secciones y el estado anterior a la búsqueda. **Expandir todo** y **Contraer todo** afectan a las secciones visibles y a los grupos del índice. Si no hay coincidencias, cambia la consulta o limpia el filtro. Son controles temporales; no modifican los archivos ni guardan la búsqueda.

Estos controles requieren JavaScript en el navegador y se ejecutan localmente, sin enviar la consulta a servicios externos. Sin JavaScript, el documento completo y sus enlaces siguen disponibles para lectura, y puedes usar la búsqueda del navegador.

Ambos documentos pueden consultarse antes de crear el usuario: `/documentacion/manual/` y `/documentacion/changelog/`. Solo se sirven esos dos archivos públicos; no se exponen archivos financieros privados.

Ahorros y Préstamos y deudas permanecen previstos para Fase 4. Sus pantallas de Fase 1 son demostraciones ficticias, accesibles mediante **Revisar esta fase → Consultar la vista previa ficticia de Fase 1**. El menú de registro real de Fase 2 muestra las funciones ya implementadas. Puedes usar cuentas de tipo Ahorros para registrar dinero guardado, pero las metas y los cálculos de obligaciones siguen pendientes.

Si actualizas una copia anterior del proyecto, instala las dependencias fijadas y reinicia el aplicativo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El lector utiliza Python-Markdown y nh3 dentro del entorno `.venv`. No carga procesadores externos ni necesita Internet para mostrar los documentos una vez instaladas las dependencias. La corrección se publica por autorización del usuario; el avance a Fase 3 sigue pendiente de revisión expresa.

## 13. Revisión y solución de problemas

- **No abre el navegador:** entra en http://127.0.0.1:8765/ y revisa la consola.
- **Aparece la Fase 1 o una versión anterior:** detén la instancia anterior y vuelve a iniciar. La demostración está en `/demo/`; tu registro está en `/app/`.
- **Error al preparar la base:** guarda el mensaje de la consola y revisa espacio/permisos; no borres archivos financieros.
- **Sesión caducada o rechazo de formulario:** recarga, inicia sesión y revisa si el movimiento ya se registró antes de reenviar.
- **Falta una cuenta o actividad:** créala en **Actividades y cuentas** y vuelve al formulario.
- **Dudas de saldos:** comprueba actividad, fechas, anulaciones y posibles saldos iniciales duplicados.

En **Revisar esta fase**, marca temporalmente lo comprobado y envía tus observaciones por el chat. Las casillas no guardan una aprobación. El avance a Fase 3 y la publicación de implementación nueva requieren tu autorización explícita. Todos los commits nuevos se redactan en español.
