# Tareas de la Fase 1

- [x] Registrar nombre, plan de cinco fases y condición de aprobación visual.
  - Aceptación: Finanzas DAGD, APK diferido, separación entre revisión local y push.
  - Verificación: `info_Fases.md` y `SPEC_FASE1.md`.
- [x] Preparar entorno Django local y versión única.
  - Aceptación: entorno aislado, dependencias fijadas y `VERSION` leído por las pantallas.
  - Verificación: `manage.py check`, `pip check` y prueba de versión.
- [x] Entregar navegación y pantallas con datos ficticios.
  - Aceptación: siete rutas accesibles, sin escrituras financieras y con rótulo de demostración.
  - Verificación: `manage.py test preview`.
- [x] Añadir búsqueda y filtrado de muestra.
  - Aceptación: filtrar y limpiar sin alterar datos; consultas inválidas rechazadas y HTML escapado.
  - Verificación: pruebas de filtro, vacío, validación y escape.
- [x] Comprobar navegador, presentación adaptable y arranque en Windows.
  - Aceptación: pantalla visible, recursos locales correctos y sin errores de consola; revisar anchos acordados.
  - Verificación: evidencia registrada en `dev_Process.md`.
- [x] Obtener revisión del usuario y registrar sus sugerencias.
  - Aceptación: aprobación explícita de esta fase o lista de ajustes.
  - Verificación: conversación y actualización de `dev_Process.md`.

Las tareas técnicas terminadas no marcan por sí mismas la fase como aprobada. La persistencia y los formularios financieros son trabajo de Fase 2.

## Siguiente decisión

- [x] Aprobar la revisión de info_Fases.md posterior a publicar Fase 1.
  - Aceptación: confirmar el alcance por actividades, presupuestos por proyecto/compra y simulador, con la integración bancaria cancelada.
  - Verificación: instrucción explícita del usuario en el chat antes de iniciar Fase 2.

La revisión visual recibida y la orden de publicar Fase 1 no aprueban automáticamente el nuevo alcance de Fase 2.

El usuario aprobó el alcance, canceló la integración bancaria y autorizó iniciar Fase 2. Las tareas de ejecución se detallan en SPEC_FASE2.md.

## Fase 2: entrega local

- [x] Acceso local y persistencia: primer usuario, sesiones/CSRF y migraciones; ver pruebas AccessTests y de arranque.
- [x] Catálogos y movimientos por actividad con centavos exactos; ver MoneyTests y LedgerViewsTests.
- [x] Transferencias, filtros y resumen consolidado sin duplicación; correcciones/anulación con historial y versiones.
- [x] Respaldo y restauración básica, copia previa y validación; ver BackupTests y comandos documentados.
- [x] Primer uso, estados vacíos, manual y revisión visual en navegador con base sintética aislada.
- [x] Revisión del usuario en su pantalla y observaciones de personalización.
- [x] Publicación de Fase 2 e inicio de Fase 3 autorizados expresamente en el chat.
- [x] Inicio de Fase 3 autorizado expresamente por el usuario.

## Fase 3: incrementos ejecutables

- [x] 3.1 Sueldo neto/detallado, meses independientes, cobros parciales sin duplicación, correcciones y respaldo compatible; pruebas automatizadas aprobadas.
- [ ] Revisión del usuario del incremento 3.1 y observaciones.
- [ ] 3.2 Presupuestos mensuales y por proyecto/compra con partidas, tope, plazo y actividad.
- [ ] 3.3 Recurrencias, suscripciones y comparación previsto/comprometido/realizado.
- [ ] Revisión de la Fase 3 completa y autorización para Fase 4.

La orden de publicar el ajuste previo no publica automáticamente la implementación nueva de Fase 3.
