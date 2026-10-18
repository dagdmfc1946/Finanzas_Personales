# Finanzas DAGD: manual de la vista previa

Estado: provisional, Fase 1. El manual definitivo se completará en la Fase 5 con funciones verificadas. Versión ejecutable: consultar `VERSION`; historial: `CHANGELOG.md`.

## Iniciar y detener

En `D:\PROYECTOS\Repo_FinanzasPersonales\Finanzas_Personales`, abrir `Iniciar_Finanzas_DAGD.cmd`. Mantener la consola abierta y visitar http://127.0.0.1:8765/. Para detener, Ctrl+C en la consola. Para preparar un entorno nuevo, seguir los comandos del README. REA no es necesario para ejecutar Finanzas DAGD.

Si Codex dejó el servidor abierto para esta revisión, se puede entrar directamente en el enlace. Si el iniciador informa que el puerto está ocupado, comprobar si la vista previa ya responde allí; no cerrar procesos desconocidos. El registro de la ejecución iniciada por Codex queda en `local/`, excluido de Git.

## Qué puedes probar ahora

1. **Resumen:** revisar ingresos y gastos ficticios, saldo, cuentas y recorrido del mes. El saldo incluye la reserva de ahorro.
2. **Movimientos:** buscar por concepto, categoría o cuenta. Por ejemplo, escribir `arriendo` y pulsar Filtrar. Cambiar el tipo entre ingreso, gasto y transferencia; Limpiar muestra nuevamente todos los registros. Si no hay coincidencias se muestra un mensaje.
3. **Mi sueldo:** comparar devengos, deducciones y neto; revisar la separación entre período del sueldo, recepción y mes presupuestado.
4. **Presupuesto:** revisar categorías, importes realizados y compromisos futuros. Desplegar la explicación de recurrencias.
5. **Ahorros:** revisar dos metas de ejemplo y cómo se distingue el ahorro del gasto.
6. **Préstamos y deudas:** comparar lo que se debe con lo que se espera cobrar. Son ejemplos independientes del resumen, aún sin pagos ni cálculos persistidos.
7. **Revisar esta fase:** usar la lista como guía. Las casillas son temporales; enviar las sugerencias y la aprobación al chat.

El mes de octubre de 2026 es fijo y ficticio. No corresponde a una consulta de tus finanzas. No hay botones de registro porque el guardado se implementará desde la Fase 2. No introducir información personal mediante la URL de búsqueda.

## Cómo pedir personalizaciones

Indicar sección, cambio deseado y resultado esperado. Ejemplo: «En Resumen quiero ver primero el dinero disponible después de separar mis ahorros». Puedes comentar colores, tamaño de letra, orden, conceptos, datos faltantes y reglas. Aprobar la Fase 1 no autoriza un push: la publicación se solicita por separado.

## Accesibilidad y pantalla

Se puede navegar con Tab y activar enlaces/botones con el teclado. Hay un enlace para saltar al contenido. En pantallas pequeñas, desplazar horizontalmente las opciones de navegación y, cuando haga falta, la tabla de movimientos. Todo el contenido usa recursos locales y etiquetas en español.

## Datos y respaldos

Esta entrega no guarda movimientos, metas, marcas de revisión ni cambios financieros. Recargar puede reiniciar controles temporales. No se importó el notebook. Las copias de datos personales y su restauración comenzarán en la Fase 2, cuando exista persistencia; no hay respaldo financiero que generar en esta vista previa.
