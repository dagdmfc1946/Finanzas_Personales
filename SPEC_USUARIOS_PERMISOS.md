# Usuarios, perfiles y eliminación — contrato de implementación

Solicitud autorizada por el usuario durante Fase 3. Agent Skills: especificación, TDD, seguridad, interfaz y Git. No cambia la secuencia de presupuestos/recurrencias ni autoriza publicación.

## Roles

| Capacidad | Normal | Administrador |
|---|---|---|
| Registro, sueldo, catálogos, historial, copias | Solo propios | Solo propios |
| Perfil y contraseña | Solo propio | Solo propio |
| Eliminar registros / reiniciar finanzas | Solo propios, confirmación y copia previa | Solo propios, mismas condiciones |
| Listar accesos; crear usuarios; asignar roles; activar/desactivar | No | Sí, con contraseña del administrador para cambios |
| Ver o modificar finanzas de otro usuario / reiniciarlo | No | No |

Administrador se identifica por is_staff en este aplicativo, sin habilitar Django admin ni conceder superusuario. La migración promueve al titular de Installation; el primer registro nuevo también será administrador. No cambia contraseñas existentes. No hay registro público adicional: solo alta por administrador. Cada alta crea actividad personal vacía. No se permite al administrador desactivarse ni quitarse su rol; no se editan cuentas superusuario mediante esta interfaz. Desactivar conserva datos e invalida acceso normal a nuevas solicitudes.

## Perfil y menú

Icono desplegable en barra lateral superior izquierda, con nombre y rol, perfil, editar, cambiar contraseña, usuarios (solo administrador), reiniciar mis datos y cerrar sesión por POST. Perfil editable: nombre de acceso, nombres y apellidos, con contraseña actual; no expone roles editables ni crea credenciales predeterminadas. Cambiar contraseña valida la anterior con formularios Django y mantiene la sesión propia.

## Eliminación y reinicio

- Rutas autenticadas, GET solo muestra confirmación; POST con CSRF, contraseña actual, motivo, casilla y frase explícita. Acceso a registros ajenos responde 404. No se recibe propietario objetivo desde formulario.
- Eliminar movimiento retira su efecto monetario y vínculos de cobro propios. Eliminar sueldo retira plan y vínculos; conserva ingresos. Catálogos solo se eliminan si no están referenciados. Se verifica revisión para movimientos/sueldos y se conserva evento de auditoría, sin contraseñas.
- Antes de cambiar datos se crea copia JSON recuperable; fallo al crearla impide borrar. No se elimina la base SQLite ni archivos. Copias nuevas se guardan por usuario. Recuperación mediante comando documentado y usuario explícito si hay varios.
- Reiniciar mis datos borra únicamente registros financieros e historial del conectado, recrea su actividad personal y un evento de reinicio. Conserva credenciales, perfil, rol, otros usuarios, sus finanzas, sesiones y copias. No hay botón global ni reinicio ajeno, tampoco para administrador.
- Confirmación advierte qué conserva y copia previa; no se ejecuta sobre datos reales durante pruebas. CLI de copia/restauración exige --usuario cuando hay varios para evitar apuntar al titular por error.

## Aceptación

Pruebas de pertenencia, rol, CSRF, contraseña/frase incorrectas, GET sin borrado, fallo de copia, referencias protegidas, eliminación de cobros/sueldos, reinicio aislado y recuperación, perfil sin escalada, administrador sin autodesactivación, normal sin listado de accesos y usuarios desactivados sin sesión válida. Revisión visual en base separada, manual actualizado, sin push.

## Estado de entrega

Implementado localmente en 0.3.0-alpha.4. Diez casos específicos de permisos/operaciones y suite total de 76 pruebas Django aprobados, además de 2 de JavaScript. Migración con copia previa y credenciales conservadas; revisión visual en base separada. Pendiente revisión del usuario y autorización de publicación.
