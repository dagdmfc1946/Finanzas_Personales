# Decisión vigente: integración bancaria cancelada

El usuario canceló expresamente la integración antes de iniciar Fase 2. No se crearán conectores ni se solicitarán credenciales bancarias. El siguiente estudio es histórico: sus limitaciones no prueban imposibilidad universal de consulta.

# Consulta opcional de saldos bancarios

Estado: investigación preliminar documental; no hay conectores implementados ni acceso a cuentas. Revisión para el plan posterior a Fase 1, 2026-10-17, America/Bogota.

## Alcance pedido

Consultar únicamente saldo de cuentas propias de Nequi y Banco de Bogotá. No pagos, retiros, transferencias ni captura de contraseñas bancarias. La lectura requiere un canal oficial y el consentimiento/habilitación que establezca el proveedor. No se contactó a los bancos ni se crearon cuentas, contratos o credenciales.

## Nequi

El catálogo indexado de su documentación histórica **Nequi Conecta** incluye Open Banking y Consulta de Saldo: https://docs.conecta.nequi.com/. Sin embargo, al revisar el enlace no se pudo abrir desde el navegador de búsqueda y la consulta directa de red no resolvió el host. Esa evidencia histórica no permite confirmar que exista hoy un producto habilitable para este aplicativo personal, ni sus endpoints, scopes, elegibilidad o precio.

La oferta oficial actual para negocios explica registro, validación, credenciales y ambientes de pruebas/producción: https://www.nequi.com.co/negocios/apis. Sus productos comerciales anunciados no prueban por sí mismos que una persona pueda consultar su saldo general desde un aplicativo local. Consulta de pago, reporte comercial y reserva de saldo no equivalen a leer el saldo total de la cuenta.

**Conclusión:** hay una referencia histórica oficial a consulta de saldo; disponibilidad y acceso productivo para Finanzas DAGD todavía no confirmados. Antes de implementarla habría que confirmar con el portal/proveedor vigente el producto exacto de solo lectura y sus requisitos. No se deduce una API personal libre y gratuita de la existencia de APIs de cobro.

## Banco de Bogotá

La página oficial consultada de API de pagos describe integración empresarial, vinculación y contrato bilateral: https://portalst.bancodebogota.com.co/empresas/recaudos-y-pagos/pagos/api-de-pagos. Es evidencia de una oferta de integración, no de un endpoint abierto de saldo personal.

Los canales oficiales documentados permiten consultar saldos y descargar extractos en Banca Virtual/Banca Móvil: https://portalst.bancodebogota.com.co/atencion-al-cliente/canales/transacciones/consultas. Que una función exista en la app bancaria no autoriza ni demuestra una API pública para terceros.

**Conclusión:** no se verificó en las fuentes primarias consultadas una API pública de saldo personal utilizable directamente por Finanzas DAGD. La investigación no demuestra que no exista un servicio privado o una habilitación comercial; quedan pendientes catálogo técnico vigente, acceso para persona natural, autenticación, scopes de lectura, tarifas y condiciones.

## Decisión propuesta para el proyecto

Mantenerlo opcional en Fase 5 y no bloquear la base local. Inicialmente, saldo registrado/conciliación manual y eventual importación revisada de extractos. Una integración se aprobará por separado solo cuando se confirme el producto y el acceso real; no se usará scraping ni ingeniería inversa de la banca para obtener credenciales o invocar endpoints privados.

Si se habilita:

1. Identificar cuenta y actividad sin duplicar el mismo producto bancario.
2. Autorizar solo lectura; no conceder capacidades de pago.
3. Registrar saldo, moneda, fecha/hora, fuente y estado de actualización. No presentar un saldo antiguo como vigente.
4. Ante error, mostrarlo y conservar la última observación fechada; no sustituir por cero.
5. Distinguir saldo observado del banco y saldo calculado por movimientos. La conciliación debe explicar diferencias, no inventar movimientos ni alterar saldos silenciosamente.
6. Gestionar y revocar tokens de forma local apropiada y excluirlos de Git y de registros. El formato y almacenamiento se diseñarán antes de conectar información real.

No se solicita al usuario entregar claves bancarias. No se afirma que un proveedor intermediario tenga cobertura de estas cuentas sin verificar producto, consentimiento, costo y permisos.
