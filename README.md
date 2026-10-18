# Finanzas DAGD

Aplicativo de finanzas personales para ejecutar localmente en Windows. Fase 3 iniciada: primer incremento local revisable con sueldo neto/detallado, meses independientes y cobros vinculados sin duplicar ingresos. Conserva actividades, cuentas, movimientos, correcciones y respaldos. Presupuestos y recurrencias son los siguientes incrementos de esta fase. La integración bancaria está cancelada.

## Ejecutar

1. Lee [MANUAL_USUARIO.md](MANUAL_USUARIO.md).
2. Ejecuta `Iniciar_Finanzas_DAGD.cmd`; prepara las tablas y abre el navegador.
3. En el primer inicio crea tu usuario local administrador. Después podrás crear usuarios adicionales desde el menú de perfil, con finanzas separadas. No hay credenciales predeterminadas ni necesitas un superusuario. Los registros empiezan vacíos.
4. Abre http://127.0.0.1:8765/ si no se abre automáticamente. Conserva la consola del iniciador; Ctrl+C detiene su instancia.

Tras actualizar, reinicia el servidor para cargar los cambios. La demostración ficticia anterior está en `/demo/` y no guarda datos personales.

## Preparar otra instalación

Python 3.12 y acceso a PyPI una vez para instalar dependencias. En la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\Iniciar_Finanzas_DAGD.cmd
```

El servidor de desarrollo escucha solo en loopback y sirve los estáticos locales con `--insecure` y DEBUG desactivado. No es un despliegue público. Después de preparar el entorno, no necesita conexión a Internet para registrar movimientos.

## Verificar

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
```

Las pruebas financieras usan una base aislada; no escriben en tus movimientos personales. Los respaldos y la restauración se explican en el manual.

## Documentación y reglas

- [Fases](info_Fases.md), [especificación de Fase 3](SPEC_FASE3.md), [especificación de Fase 2](SPEC_FASE2.md), [tareas](tasks/todo.md), [especificación histórica de Fase 1](SPEC_FASE1.md).
- [Proceso](dev_Process.md), [cambios](CHANGELOG.md), [manual](MANUAL_USUARIO.md), [reglas](AGENTS.md).
- [Instalación REA](Analisis_REA/INSTALACION_REA.md), [análisis público de Moneri](Analisis_REA/ANALISIS_REA_MONERI.md), [skills UI](docs/SKILLS_UI.md).
- Versión única en `VERSION` según SemVer. Commits nuevos en español. Cada fase requiere revisión ejecutable; publicar únicamente con autorización explícita.
- `.venv/`, `data/`, `local/`, `backups/`, bases, secretos y datos reales quedan fuera de Git. Los archivos financieros locales no están cifrados por el aplicativo.
