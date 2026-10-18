# Instrucciones del proyecto Finanzas DAGD

- Usar Agent Skills durante todo el desarrollo: consultar using-agent-skills y aplicar los flujos relevantes. Skills UI instaladas y límites en docs/SKILLS_UI.md.
- Respetar la especificación vigente y el plan de info_Fases.md. El usuario aprobó el alcance revisado y autorizó iniciar Fase 2. No avanzar a Fase 3 sin su revisión de la entrega ejecutable.
- Cada fase necesita una entrega ejecutable y revisión del usuario. Conservar Revisar esta fase hasta culminar el desarrollo; las casillas no otorgan aprobación.
- Trabajar en dev1. Todos los nuevos mensajes de commit deben estar en español. Guardar commits locales para trazabilidad. No hacer push, merge o publicación sin orden o aprobación explícita para ese alcance.
- VERSION es la fuente única del número ejecutable; aplicar SemVer y actualizar CHANGELOG.md. Actualizar MANUAL_USUARIO.md y dev_Process.md con cada cambio de uso o comportamiento.
- Las referencias personales y datos reales permanecen en local/ o almacenamiento local excluido de Git. No copiar sus importes a fixtures/documentos públicos sin autorización específica de publicación. Las actividades y los presupuestos se definen en el plan; no implementar sus reglas por inferencia silenciosa.
- Para cambios de comportamiento: pruebas relevantes, validación local y revisión en navegador cuando corresponda. Comandos: .venv\Scripts\python.exe manage.py test; .venv\Scripts\python.exe -m unittest discover -s . -p test_iniciar.py; .venv\Scripts\python.exe manage.py check.
- El servidor de la vista previa es solo local, 127.0.0.1:8765. No conectar bancos, habilitar pagos ni recolectar claves. La integración bancaria fue cancelada por el usuario y queda fuera del alcance; no implementarla.
