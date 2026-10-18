# Manual de usuario — Finanzas DAGD

👋 Esta guía te acompaña desde el primer inicio hasta el registro de tu sueldo. Lee primero **4. Preparar actividades, cuentas y categorías** y **5. Registrar ingresos y gastos** si ya tienes acceso.

Versión del software: consultar `VERSION` (SemVer 2.0.0: MAYOR.MENOR.PARCHE). Historial: `CHANGELOG.md`. Guía para `0.3.0-alpha.3`, entrega local de Fase 3 en revisión.

## 1. 🧭 Qué puedes usar ahora

Puedes guardar cuentas, categorías agrupadas o individuales, ingresos, gastos, saldos iniciales y transferencias. También planear el sueldo, vincular sus cobros, corregir registros y crear respaldos.

**Empieza aquí:** inicia sesión → prepara tus actividades y cuentas → crea categorías si las necesitas → registra movimientos → revisa el resumen. Después usa **Mi sueldo** para relacionar la previsión con un ingreso que ya registraste.

⏳ Presupuestos y recurrencias continúan pendientes dentro de Fase 3. Metas de ahorro, préstamos, deudas y calculadora de cuotas corresponden a Fase 4. La vista `/demo/` contiene pantallas ficticias anteriores; no guarda operaciones. La integración bancaria está cancelada.

## 2. ▶️ Ejecutar en este PC

1. Abre `D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales` en el Explorador.
2. Haz doble clic en **Iniciar_Finanzas_DAGD.cmd**.
3. Espera a que abra el navegador. Si no abre, entra en **http://127.0.0.1:8765/**.
4. Mantén abierta la consola. Para detener el aplicativo, pulsa **Ctrl+C** en ella.

El iniciador prepara las tablas y reutiliza una instancia propia si ya está abierta. Si otro servicio ocupa el puerto, avisa y no lo cierra. Tras actualizar el código, detén la instancia anterior y ejecuta el iniciador de nuevo.

Desde PowerShell también puedes abrirlo así:

```powershell
Set-Location 'D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales'
.\Iniciar_Finanzas_DAGD.cmd
```

En este PC el entorno está preparado. Para otra instalación vacía, con Python 3.12 instalado, copia el código e instala las dependencias una vez:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\Iniciar_Finanzas_DAGD.cmd
```

Después de instalar las dependencias no necesitas Internet para registrar tus datos. El servidor es local de desarrollo; no es un servicio publicado en Internet.

## 3. 🔐 Primera ejecución: crea tu usuario

Solo la primera apertura muestra **Configurar mi usuario**. Escoge nombre y contraseña propia de al menos diez caracteres y sigue las indicaciones del formulario. No existe usuario o contraseña predeterminados ni necesitas un superusuario.

Si ya ves **Iniciar sesión**, introduce el usuario que creaste; no crees otro. Para salir pulsa **Cerrar sesión**. Para actualizar tu clave usa **Cambiar contraseña**.

La instalación empieza sin movimientos y crea la actividad **Personal / trabajo principal**. No se cargan automáticamente los datos del notebook ni los ejemplos de esta guía.

Si olvidas la contraseña, no borres la base. Con acceso autorizado a la carpeta, detén el aplicativo y ejecuta:

```powershell
.\.venv\Scripts\python.exe manage.py changepassword TU_USUARIO
```

Escribe la nueva contraseña solo cuando la consola la pida. No hay recuperación por correo.

## 4. 🗂️ Preparar actividades, cuentas y categorías

Entra en **Actividades y cuentas**. Estas tres cosas tienen funciones distintas:

| Elemento | Pregunta que responde | Ejemplo |
|---|---|---|
| Actividad | ¿A qué ámbito pertenece el dinero? | Personal, Emprendimiento |
| Cuenta | ¿Dónde está el dinero? | Banco, Efectivo |
| Categoría | ¿Qué clase de ingreso o gasto es? | Sueldo, Arriendo, Ventas_Emprendimiento |
| Grupo de categorías | ¿Qué categorías quiero ver juntas? | Gastos fijos, Gastos variables |

### Crear una actividad

Pulsa **Crear actividad**, escribe el nombre y **Guardar**. Usa la actividad personal para tu trabajo principal y crea otra para cada emprendimiento o trabajo secundario que quieras separar. Una misma cuenta puede contener dinero de varias actividades.

### Crear una cuenta y su saldo inicial

Pulsa **Crear cuenta**. Completa nombre y tipo. Si ya tienes dinero en ella, introduce ese importe en **Saldo inicial COP** y elige la actividad a la que pertenece. Si empieza vacía, escribe cero o deja el importe vacío. Guarda.

✅ Un saldo inicial positivo crea su movimiento automáticamente. **No lo registres otra vez en Movimientos.** Si olvidaste indicarlo al crear la cuenta, puedes registrar luego un movimiento de tipo Saldo inicial; consulta la sección 5.

### Crear categorías dentro de un grupo

Pulsa **Crear categoría** y completa:

| Nombre | Tipo | Grupo opcional |
|---|---|---|
| Arriendo | Gasto | Gastos fijos |
| Transporte | Gasto | Gastos fijos |
| Salidas | Gasto | Gastos variables |
| Ventas_Emprendimiento | Ingreso | Dejar vacío |
| Sueldo | Ingreso | Dejar vacío |

Escribe el nombre del grupo o elige uno sugerido al escribir. Repite exactamente el mismo nombre para reunir categorías. Hay un solo nivel de agrupación. El grupo no tiene importe ni tipo propio: cada categoría sigue siendo de Ingreso o Gasto.

Las categorías con grupo vacío aparecen en **Sin grupo**. Las anteriores siguen allí hasta que las edites y les asignes un grupo. Puedes desplegar o contraer cada grupo. Para mover una categoría a otro grupo, pulsa **Editar**, cambia Grupo y guarda. Los movimientos conservan la misma categoría; sus importes no cambian.

El nombre de categoría debe ser único para el mismo tipo dentro de tu usuario, aunque cambies el grupo. Una categoría ya utilizada no puede cambiar a un tipo incompatible con sus movimientos.

## 5. ✍️ Registrar ingresos y gastos

Entra en **Movimientos → Nuevo movimiento**. **Elige primero el Tipo**:

| Si quieres registrar… | Elige | Categoría | Destinos |
|---|---|---|---|
| Dinero que ya tenías al comenzar | Saldo inicial | Sin categoría | Vacíos |
| Dinero que acabas de recibir | Ingreso | Opcional, de Ingreso | Vacíos |
| Dinero que acabas de pagar | Gasto | Opcional, de Gasto | Vacíos |
| Dinero que mueves entre cuentas o actividades propias | Transferencia | Sin categoría | Ambos obligatorios |

El formulario activa los campos que corresponden y filtra las categorías por tipo. Si cambias el tipo, se limpia una categoría incompatible. Sin JavaScript, deja tú mismo los campos que no aplican vacíos; el servidor sigue validándolos.

### Ejemplo A: saldo inicial que aún no registraste

Estos valores son ficticios. Utiliza este ejemplo solo si **no** diste saldo inicial al crear la cuenta:

| Campo | Qué escribir o seleccionar |
|---|---|
| Tipo | Saldo inicial |
| Fecha | La fecha desde la que empiezas el registro |
| Concepto | Saldo inicial de ejemplo |
| Importe COP | `1000000` |
| Actividad de origen | Personal / trabajo principal |
| Cuenta de origen | Banco de ejemplo |
| Categoría | Vacía; con JavaScript aparece desactivada |
| Actividad y cuenta de destino | Vacías; aparecen desactivadas |

Pulsa **Guardar**. Vuelves a Movimientos y ves el registro. En Resumen, el saldo aumenta 1.000.000 COP, pero **Ingresos registrados** no aumenta.

⚠️ El error «La categoría debe corresponder al tipo de ingreso o gasto» de versiones anteriores aparecía si elegías Saldo inicial junto con Sueldo · Ingreso. El saldo inicial va **sin categoría**. Si se trata de un sueldo recibido ahora, elige **Ingreso**, no Saldo inicial.

### Ejemplo B: sueldo recibido

Selecciona **Ingreso**, una fecha real de cobro, concepto **Cobro de sueldo de ejemplo**, importe `2000000`, actividad personal y cuenta Banco de ejemplo. Selecciona la categoría Sueldo · Ingreso o déjala vacía. Los destinos van vacíos. Pulsa **Guardar**.

✅ Ahora sí aumenta **Ingresos registrados**. No vuelvas a crear este ingreso al planear el sueldo: lo vincularás desde Mi sueldo.

### Ejemplo C: gasto de mercado

Selecciona **Gasto**, fecha de compra, concepto **Mercado de ejemplo**, importe `250000`, actividad personal y cuenta Banco de ejemplo. Elige Mercado · Gasto si la creaste; si no, deja categoría vacía. Destinos vacíos. Guarda.

Introduce importes sin separadores de miles y con hasta dos decimales: `25000.50`. Siempre positivos. El tipo determina si entra o sale dinero. Si el formulario muestra un error, corrige el campo indicado: los datos introducidos se conservan y no se guarda un movimiento parcial. Antes de reenviar tras una interrupción, comprueba el listado.

## 6. 🔄 Transferencias y aportes

Ejemplo: retirar 100.000 COP del banco para tener efectivo.

1. Comprueba que existan Banco de ejemplo y Efectivo de ejemplo.
2. En Nuevo movimiento, elige **Transferencia**; fecha de retiro y concepto **Retiro de efectivo de ejemplo**.
3. Importe: `100000`. Origen: actividad personal y Banco de ejemplo.
4. Destino: actividad personal y Efectivo de ejemplo. Categoría desactivada/vacía.
5. Guarda y consulta Resumen.

✅ El banco disminuye 100.000 y el efectivo aumenta 100.000; el total no cambia y no aparece ingreso/gasto externo nuevo. El origen y destino completos deben ser diferentes.

Para aportar dinero propio a tu emprendimiento, cambia la actividad de destino al emprendimiento. Puede usarse la misma cuenta si cambia la actividad. Es una transferencia interna, no una venta. Los gastos compartidos no se reparten automáticamente.

## 7. 📊 Entender el resumen y los filtros

**Resumen** muestra todo el historial vigente. Los filtros de fecha de Movimientos no cambian estos totales:

- **Ingresos registrados:** ingresos reales, sin saldos iniciales ni transferencias.
- **Gastos registrados:** gastos reales vigentes.
- **Saldo calculado:** saldo inicial + ingresos − gastos; las transferencias internas redistribuyen el dinero.

Selecciona una actividad y pulsa **Ver actividad** para ver su dinero asignado. **Consolidado** reúne todas. El saldo se calcula con tus registros; no es una consulta bancaria.

En **Movimientos**, selecciona actividad, tipo, fechas o texto del concepto y pulsa **Aplicar filtros**. **Limpiar** recupera el listado completo. Activa **Incluir anulados** para ver los que ya no afectan saldos.

## 8. 🛠️ Corregir, anular y consultar historial

En la fila de un movimiento vigente:

- **Corregir:** cambia el dato, explica el motivo y guarda. No crees otro movimiento para sustituirlo.
- **Anular:** escribe un motivo, marca la confirmación y pulsa **Confirmar anulación**. Deja de afectar saldos, pero queda conservado.

Si otra ventana modificó el registro, recarga antes de intentarlo de nuevo. No se borra el historial.

En **Historial**, despliega un evento para ver Antes/Después y el motivo. La vista técnica usa `cents`: divide entre 100 para leer COP. Por ejemplo, `25000000` centavos son 250.000 COP. `revision` es el número de edición e identificadores largos relacionan los registros. La bitácora no es inalterable para alguien con acceso directo al archivo del PC.

## 9. 💾 Crear respaldos

Abre **Respaldos → Crear y descargar respaldo**. Se descarga un JSON y se guarda otra copia en `backups/`. Conserva una copia privada fuera del mismo disco.

La copia actual es de **formato 3**: actividades, cuentas, categorías con sus grupos, movimientos, planes de sueldo, vínculos de cobro e historial. No contiene contraseñas, usuarios, sesiones ni claves. Límite básico: 5 MiB o 10.000 registros. No está cifrada.

También puedes crearla desde PowerShell en la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe manage.py respaldo_finanzas
```

## 10. ♻️ Restaurar una copia propia

⚠️ Restaurar **reemplaza los registros financieros actuales**. Para aprender, utiliza otra instalación vacía de ensayo; no pruebes la restauración sobre tus cuentas personales. En esa instalación crea primero tu usuario. Sus credenciales se mantienen al restaurar.

1. Detén el aplicativo receptor y las demás instancias que usen esa misma base.
2. Desde PowerShell en la carpeta receptora, cambia la ruta del ejemplo por tu archivo propio:

```powershell
.\.venv\Scripts\python.exe manage.py restaurar_finanzas 'C:\RUTA\finanzas-respaldo.json' --confirmar
```

3. Lee el resultado: indica dónde guardó la copia previa.
4. Inicia otra vez y comprueba cuentas, movimientos, categorías y Mi sueldo.

El comando crea una copia previa antes de reemplazar datos. Rechaza archivos dañados, campos inesperados y referencias inválidas; ante un error de validación revierte los cambios. Conserva credenciales y eventos existentes del historial, recupera eventos faltantes y añade el evento de restauración. La huella SHA-256 detecta daños accidentales; no certifica al autor. Usa copias propias sin editarlas manualmente. No hay carga desde el navegador.

| Copia que recuperas | Qué ocurre con los datos que esa copia no contiene |
|---|---|
| Formato 3 actual | Recupera grupos, sueldos y vínculos |
| Formato 2 anterior | Recupera sueldos y vínculos; categorías quedan Sin grupo |
| Formato 1 de Fase 2 | Categorías Sin grupo y planificación de sueldo vacía |

Los ingresos de las copias antiguas siguen siendo movimientos. Una versión anterior del aplicativo puede no leer copias de formato 3. Una copia financiera no recupera contraseñas olvidadas.

## 11. 🏠 Archivos privados y cuidado de la instalación

| Carpeta o archivo privado | Para qué sirve |
|---|---|
| `data/finanzas.sqlite3` | Datos y acceso de tu instalación |
| `local/secret.key` | Secreto propio de esta instalación |
| `backups/` | Copias financieras y previas a cambios |

Están excluidos de Git. No los publiques. La contraseña protege la interfaz; los archivos y respaldos **no están cifrados**. Protege el acceso a Windows.

No borres la base ni la clave para arreglar un error. Antes de copiar manualmente una instalación, detén el servidor: copiar SQLite en uso puede producir una copia incompleta. En este equipo se guardan copias consistentes privadas antes de aplicar nuevas migraciones de esta entrega.

## 12. 📖 Consultar documentación en el aplicativo

Los enlaces **CHANGELOG.md** y **MANUAL_USUARIO.md** de la barra lateral abren pestañas nuevas. No pierdes la pantalla original. Pueden leerse antes de iniciar sesión.

En **En este documento**, pulsa un título para saltar a él. Puedes abrir/cerrar capítulos, **Expandir todo**, **Contraer todo** o buscar títulos y contenido sin distinguir tildes ni mayúsculas. **Limpiar filtro** recupera la lectura. Los controles son temporales y funcionan localmente con JavaScript; sin él puedes leer todo y usar la búsqueda del navegador.

El historial usa: ✨ Añadido para funciones nuevas, 🛠️ Corregido para ajustes, 📦 Dependencias y 🧪 Verificado. Las versiones más recientes están arriba. Un estado «local» significa que aún está pendiente de revisión/publicación.

La documentación se lee del Markdown guardado del proyecto; no se conecta a procesadores externos. El lector conserva formato y filtra HTML. Los tres botones del índice siguen en una fila compacta, con altura de 32 px.

## 13. 🆘 Revisión y solución de problemas

| Qué ves | Qué hacer |
|---|---|
| No abre navegador | Visita http://127.0.0.1:8765/ y revisa la consola |
| Versión anterior | Detén la instancia anterior y ejecuta de nuevo el iniciador |
| No deja guardar saldo inicial | No elijas categoría Sueldo; usa Saldo inicial sin categoría ni destinos |
| No deja guardar ingreso/gasto | Revisa tipo de categoría, cuenta, actividad e importe positivo |
| No aparece una categoría | El tipo debe coincidir; créala en Actividades y cuentas o deja el campo vacío |
| No deja transferir | Completa ambos destinos y diferencia origen/destino |
| Sesión caducada | Recarga, inicia sesión y comprueba si ya se guardó antes de reenviar |
| Error al preparar base | Conserva el mensaje y comprueba permisos/espacio; no borres archivos |

En **Revisar esta fase** tienes el recorrido y las casillas temporales. Envíame tus observaciones después de probar. Marcar casillas no guarda una aprobación. Fase 4 y nuevas publicaciones requieren tu autorización; commits en español.

## 14. 💰 Mi sueldo: previsión y cobros

Un **plan de sueldo** describe lo que esperas recibir. Un **movimiento de ingreso** registra el dinero recibido. Se relacionan sin sumar el dinero dos veces.

### Paso 1: planear

En **Mi sueldo → Planear sueldo** completa:

| Campo | Ejemplo ficticio | Significado |
|---|---|---|
| Concepto | Sueldo de ejemplo | Cómo identificarás el plan |
| Actividad | Personal / trabajo principal | A qué trabajo pertenece |
| Modalidad | Neto | Conoces lo que recibirás |
| Mes trabajado | Agosto de 2026 | Cuándo trabajaste |
| Fecha prevista de cobro | 05/09/2026 | Cuándo esperas recibirlo |
| Mes presupuestado | Septiembre de 2026 | A qué mes destinas el sueldo |
| Sueldo neto | `2000000` | Importe previsto |
| Bruto / adicionales / deducciones | Bruto vacío; ajustes vacíos o cero | No aplican en modalidad Neto |
| Incluir en previsión | Marcado | Incluye el plan en previsto/pendiente |

Guarda y consulta **septiembre de 2026**. Antes de vincular cobros: previsto 2.000.000, recibido cero y pendiente 2.000.000 COP. Guardar el plan no modifica tus saldos.

Si prefieres **Bruto y deducciones**, deja el neto vacío y escribe bruto `2200000`, adicionales `100000`, deducciones `300000`. Calcula el mismo neto de 2.000.000 COP. Es un cálculo manual, no liquidación tributaria ni nómina legal.

### Paso 2: registrar el dinero recibido

Si aún no registraste el cobro, ve a Movimientos y crea el **Ingreso** de la sección 5, ejemplo B. Si ya existe, no lo vuelvas a registrar. Usa su fecha y cuenta reales; la fecha puede diferir de la del plan.

### Paso 3: vincular y verificar

Regresa a Mi sueldo, consulta septiembre y pulsa **Vincular ingreso existente** en el plan. Elige Cobro de sueldo de ejemplo y guarda. Solo aparecen ingresos propios vigentes, de la misma actividad y aún sin vínculo.

✅ Recibido 2.000.000, pendiente cero. El saldo de cuentas no cambia al vincular. Si la lista está vacía, revisa que el ingreso exista, no esté anulado, tenga la misma actividad y no pertenezca a otro plan.

### Cobros parciales, correcciones y desvinculación

Para probar cobros parciales, usa **en lugar** del ingreso único dos ingresos de 1.200.000 y 800.000 COP. Vincula el primero: queda pendiente 800.000. Vincula el segundo: queda cero. No uses ambas alternativas a la vez.

Corregir el importe del ingreso actualiza lo recibido. Anularlo lo excluye del cálculo y conserva el vínculo. Si recibes más de lo planeado, se muestra el exceso y el pendiente queda cero.

**Desvincular** pide motivo y confirmación; conserva el ingreso y su saldo. Para cambiar tipo o actividad de un ingreso vinculado, desvincúlalo primero. **Corregir plan** exige motivo y revisión vigente; para cambiar su actividad, no debe conservar cobros incompatibles. No se borran planes. Desmarcar **Incluir en previsión** excluye previsto/pendiente y conserva los cobros reales visibles.

Los totales del módulo pertenecen al mes presupuestado elegido y no representan saldo bancario ni presupuesto mensual completo.

## 15. 🧩 Ejemplo completo y orden de revisión

Cada sección tiene **Ver ejemplo de…**. Pulsa el título para abrir pasos y resultados. Son ejemplos de lectura, **no datos precargados**. Si ya tienes datos personales, no introduzcas el caso completo allí: léelo como guía o usa otra instalación vacía para practicar.

### Recorrido de un caso que empieza vacío

1. **Actividades y cuentas:** usa la actividad personal y crea Emprendimiento de ejemplo. Crea Banco de ejemplo con 1.000.000 COP iniciales personales; crea Efectivo de ejemplo sin saldo. Crea categorías opcionales. No dupliques el saldo inicial.
2. **Movimientos:** registra ingreso personal 2.000.000 COP, ingreso de venta del emprendimiento 300.000 COP y gasto personal de mercado 250.000 COP. Todo en el banco. Después transfiere 100.000 del banco al efectivo, dentro de la actividad personal. Fecha de ejemplo de los cobros: 08/09/2026; mercado: 09/09; transferencia: 10/09.
3. **Mi sueldo:** completa el plan de la sección 14 y vincula el ingreso personal existente. No crees otro ingreso.
4. **Resumen:** compara los resultados de la tabla siguiente; filtra cada actividad y vuelve a Consolidado.
5. **Historial:** corrige Mercado a 260.000 con motivo «Corregir importe de ensayo», revisa antes/después y devuélvelo a 250.000 con otro motivo. El saldo baja 10.000 y después vuelve. Para anulación usa un gasto adicional de ensayo de 10.000 y anúlalo; regresa al saldo anterior.
6. **Respaldos:** descarga una copia al terminar. Solo ensaya la recuperación en otra instalación vacía, como indica la sección 10.
7. **Revisar esta fase:** cierra sesión y vuelve a entrar con tu usuario, comprueba legibilidad/filtros y marca temporalmente lo revisado. Comparte tus observaciones.

| Verificación al completar el caso base | Resultado COP |
|---|---:|
| Ingresos externos | 2.300.000 |
| Gastos | 250.000 |
| Saldo total | 3.050.000 |
| Banco | 2.950.000 |
| Efectivo | 100.000 |
| Saldo asignado personal | 2.750.000 |
| Saldo asignado emprendimiento | 300.000 |
| Sueldo previsto / cobrado / pendiente | 2.000.000 / 2.000.000 / 0 |

Si tus resultados difieren, comprueba que no duplicaste el saldo inicial o el sueldo, que el gasto volvió a 250.000 y que la transferencia no se registró como gasto/ingreso. Estas cifras solo corresponden al caso base, no a tus cuentas reales.
