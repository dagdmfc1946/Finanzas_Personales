# Finanzas DAGD

Aplicativo de finanzas personales para ejecutar localmente en Windows. Fase 1: vista previa navegable con datos ficticios, pendiente de revisión del usuario. No registra ni importa aún datos financieros.

## Abrir la entrega preparada

1. Ejecutar `Iniciar_Finanzas_DAGD.cmd` en esta carpeta y mantener la ventana abierta.
2. Abrir http://127.0.0.1:8765/ en el navegador.
3. Recorrer las secciones y la página **Revisar esta fase**. Enviar sugerencias o aprobación por el chat.
4. Para detener el servidor, pulsar Ctrl+C en su ventana.

Si ya existe un servidor de Finanzas DAGD en ese puerto, basta con abrir la dirección. No ejecutar otro servidor en el mismo puerto ni detener procesos ajenos.

## Preparar el entorno en otra instalación

Requisitos: Python 3.12 y acceso a PyPI para instalar dependencias una vez. Desde PowerShell, en la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test preview
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765 --insecure --noreload
```

El servidor de desarrollo y el parámetro `--insecure` sirven esta demostración y sus estáticos con DEBUG desactivado; el enlace permanece en la interfaz de loopback. No se requiere `migrate` ni crear una base de datos para la Fase 1. Tras instalar las dependencias, la vista previa funciona sin conexión a Internet y no carga fuentes ni bibliotecas desde servicios externos.

## Documentación y reglas

- [Fases](info_Fases.md), [especificación de Fase 1](SPEC_FASE1.md), [tareas](tasks/todo.md).
- [Proceso](dev_Process.md), [cambios](CHANGELOG.md), [manual de usuario](MANUAL_USUARIO.md).
- [Instalación REA](Analisis_REA/INSTALACION_REA.md) y [análisis público de Moneri](Analisis_REA/ANALISIS_REA_MONERI.md).
- Número de versión en `VERSION`, sin duplicarlo en código. Cada fase requiere revisión ejecutable y aprobación del usuario. Subir a GitHub únicamente por orden o aprobación explícita.
- `.venv/`, bases, respaldos, secretos, registros locales y datos reales quedan fuera de Git.
