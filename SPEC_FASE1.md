# Finanzas DAGD: especificación de la Fase 1

## Objetivo y aprobación

Entregar una base local ejecutable para revisar identidad, navegación, distribución de información y requisitos antes de construir la gestión financiera persistente. El usuario autorizó esta fase y exige ejecutar el aplicativo para aprobar cada entrega. Estado: implementada como vista previa, **pendiente de aprobación visual y funcional del usuario**.

## Alcance de esta vista previa

- Siete pantallas: Resumen, Movimientos, Mi sueldo, Presupuesto, Ahorros, Préstamos y deudas, y Revisar esta fase.
- Datos sintéticos de octubre de 2026, rotulados en todas las páginas. Este período es un escenario fijo, no un filtro que consulte datos reales ni una fecha actual calculada.
- Navegación funcional, búsqueda por concepto/categoría/cuenta, filtro por tipo, limpieza de filtros, estado sin coincidencias y validación de entradas.
- Casillas temporales para orientar la revisión; no guardan respuestas ni constituyen aprobación.
- Ningún formulario de creación financiera, importación de notebook, conexión bancaria o escritura de datos personales.

## Arquitectura y decisión técnica

Python 3.12 existente y Django 5.2 LTS, con parche fijado en `requirements.txt`, plantillas de servidor y CSS local. SQLite funciona en memoria para las comprobaciones de arranque de Django; esta demostración no crea archivos de base de datos ni guarda información financiera. Solo GET/HEAD; otros métodos reciben 405.

Django permite aprovechar la experiencia previa del usuario y usar la misma base en fases posteriores. Las plantillas evitan añadir un framework JavaScript y una cadena de compilación para la revisión inicial. Se eligió 5.2 LTS para una base con soporte prolongado, en lugar de perseguir una versión mayor por novedad. Una futura aplicación Android requerirá diseñar su cliente y acceso a los datos; no es una conversión automática.

La configuración escucha únicamente en `127.0.0.1:8765`, acepta hosts locales y mantiene `DEBUG=False`. El servidor de desarrollo usa `--insecure` exclusivamente para servir CSS y el icono con DEBUG desactivado; no es una autorización para exponer el servidor en red. No hay autenticación porque esta fase solo ofrece muestras públicas ficticias. Antes de admitir datos reales se revisará la protección del acceso local y del equipo.

## Contrato visual inicial, sujeto a tus sugerencias

Interfaz oscura azul profundo, acento turquesa y tipografía del sistema. El resumen prioriza ingresos, gastos y saldo; las cuentas quedan visibles junto al recorrido del mes. Color acompañado por etiquetas y signos, navegación con sección activa y foco visible. En pantallas pequeñas, navegación horizontal desplazable y contenido en una columna. Las tablas se desplazan dentro de su contenedor.

La referencia aportada muestra consolidación y pantallas oscuras, pero no permite estudiar todas las interacciones: la densidad, tipografía y distribución son propuestas propias. No se reproduce la marca Moneri. No hay botones de guardar que aparenten una funcionalidad inexistente.

## Reglas financieras propuestas para las fases siguientes

1. Separar cuentas y categorías. Un saldo pertenece a una cuenta; una categoría explica el propósito del movimiento.
2. Transferir entre cuentas propias no crea un ingreso ni un gasto consolidado. La reserva de ahorro sigue formando parte del dinero propio.
3. El sueldo puede registrarse como neto o mediante conceptos; su detalle no debe volver a sumar el neto como un segundo ingreso. Separar período devengado, recepción y mes presupuestado.
4. Diferenciar previsto de realizado. Un compromiso y su pago no son dos gastos. Las recurrencias deben evitar duplicados.
5. Distinguir deuda recibida, préstamo otorgado y compra financiada. El préstamo recibido no debe confundirse con sueldo; devolver capital no debe duplicar el costo de la compra. Separar capital, interés y cargos antes de implementarlo.
6. Dinero con representación exacta: para SQLite se propone almacenar centavos enteros y realizar cálculos con enteros/Decimal, con redondeo explícito. El ejemplo visual solo usa pesos enteros. La política de intereses y redondeo de cuotas se confirmará antes de la Fase 4.
7. Correcciones y anulaciones con historial, conciliación de saldos y migraciones probadas; no borrar un movimiento sin trazabilidad.
8. Respaldar desde que haya datos persistidos. No versionar bases, copias, credenciales ni datos personales del notebook.

Estos puntos son requisitos propuestos, no un motor financiero terminado. Los saldos del resumen de demostración son coherentes entre sí; las obligaciones son ejemplos independientes, explícitamente no integrados al resumen.

## Supuestos por confirmar durante la revisión

- Uso individual, moneda principal COP e interfaz en español.
- Preferencia por diseño oscuro; decidir si necesitas también tema claro.
- Orden de navegación y términos preferidos: ingresos/sueldo, cuentas, ahorro y obligaciones.
- Necesidad de una clave de acceso local cuando existan datos personales.
- Saldo inicial, calendario de pago, conceptos de sueldo y categorías reales se recogerán antes de implementarlos.

## Estructura y comandos

`finanzas_dagd/`: configuración y rutas. `preview/`: datos ficticios, vista, filtros, plantillas, estilos y pruebas. `VERSION`: fuente única de versión ejecutable. `Analisis_REA/`: informes previos. `.venv/`, `data/`, `backups/`, `local/`: excluidos de Git.

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe manage.py test preview
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765 --insecure --noreload
```

Estilo: Python con nombres `snake_case`, vistas pequeñas, datos de ejemplo separados de la presentación, escape automático de plantillas y validación mediante Django Forms. No se usa float para importes ni se desactiva el escape de HTML.

## Criterios de aceptación y límites

- Todas las pantallas identifican Finanzas DAGD, versión y naturaleza ficticia de los datos.
- Búsqueda/filtros reproducibles, entradas inválidas rechazadas y consultas escapadas.
- Navegación por teclado, etiquetas de formulario, foco visible, texto legible y revisión de presentación a 320, 768, 1024 y 1440 px.
- Pruebas automáticas sin acceso a base de datos; comprobación en navegador real y entrega abierta localmente para el usuario.
- Siempre: documentar decisiones, verificar antes de commitear y mantener cada fase pendiente hasta su aprobación explícita. Consultar antes de publicar o modificar el alcance acordado. Nunca: subir datos privados, eliminar pruebas para ocultar fallos o atribuir al análisis REA comportamientos no observados.

## Fuentes

- Django en Windows: https://docs.djangoproject.com/en/5.2/howto/windows/.
- Ejecución local: https://docs.djangoproject.com/en/5.2/ref/django-admin/#runserver.
- Política y versiones: https://www.djangoproject.com/download/.
- Precisión SQLite: https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes.
- SemVer: https://semver.org/lang/es/.
- Referencia funcional: `Analisis_REA/ANALISIS_REA_MONERI.md`.
