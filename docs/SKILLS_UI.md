# Skills UI instaladas para Finanzas DAGD

Instalación realizada después de publicar Fase 1, por solicitud del usuario. No se implementa Fase 2 ni se cambia el diseño en esta intervención. Las skills estarán disponibles automáticamente en el siguiente turno; sus instrucciones también se han leído para preparar el plan.

## Inventario y procedencia fija

Destino de todas las carpetas: `C:\Users\Diego\.codex\skills`. Se utilizó el instalador de skills de Codex, con `--ref` fijado al commit y sin sobrescribir instalaciones existentes.

| Repositorio solicitado | Skill instalada | Ruta fuente | Commit |
|---|---|---|---|
| https://github.com/Leonxlnx/taste-skill | design-taste-frontend | skills/taste-skill | f624f37a8c650b9cc550253104925efe4c8de246 |
| Mismo repositorio Taste | redesign-existing-projects | skills/redesign-skill | f624f37a8c650b9cc550253104925efe4c8de246 |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | ui-ux-pro-max | .claude/skills/ui-ux-pro-max | 56ea9cf174ed86786187daa9de0e6247cb0747e4 |
| https://github.com/pbakaus/impeccable | impeccable | .agents/skills/impeccable | 08d5b470495d242ca0470f4aeae1956c3a074f83 |

Taste contiene varias skills. Se instaló su skill principal y la de rediseño de aplicaciones existentes; no se instalaron los estilos experimentales ni todas sus variantes. La principal declara que no está destinada a dashboards, por lo que no dirigirá el aplicativo financiero.

## Verificaciones

- Cuatro manifiestos SKILL.md presentes; recursos copiados: 29, 1, 76 y 62 archivos respectivamente.
- UI/UX Pro Max: `scripts/search.py` ejecutado con Python existente, sin dependencias extra. La búsqueda de sistema visual sugirió una estructura de marketing no apropiada; se descartó. La búsqueda acotada tampoco ofreció una regla precisa de densidad de dashboard, por lo que no se guardó ese resultado como diseño válido. Se usarán las pautas verificables de accesibilidad y la consulta por componente/stack cuando corresponda.
- Impeccable: lanzador `scripts/impeccable.cmd`, motor 0.1.15 descargado de su release oficial y ejecutado con `context --target preview/templates/preview/page.html`. El contexto encontró la ruta y señaló ausencia de PRODUCT.md/DESIGN.md y de hook automático. Su detección automática no identificó la implementación Django; esto no significa que no exista UI: se conserva la evidencia visual y el código como referencia.
- El primer arranque de Impeccable emitió una advertencia de etiqueta de limpieza del batch. El comando completó con código 0 y produjo contexto. Se verificó el motor independientemente contra el sidecar oficial SHA-256: `981324ea15cc3c107d46b8133b5be77f639dbcd22e671f1eb7d8c69136e9693b`. Se retiró exclusivamente la carpeta temporal vacía que dejó la descarga. No se modificó el código de la skill.
- Motor: `C:\Users\Diego\.impeccable\bin\0.1.15\impeccable.exe`. Fuente de huella: https://github.com/pbakaus/impeccable/releases/download/engine-v0.1.15/impeccable-windows-x64.exe.sha256.
- No se activaron hooks de edición, procesos en segundo plano ni permisos nuevos de Codex. Las skills no son dependencias de ejecución de Finanzas DAGD.

## Criterio para el diseño futuro

Se conserva la identidad oscura azul/turquesa que el usuario revisó. Aplicación de trabajo en modo **Operate** de Impeccable: legibilidad, consistencia, controles familiares y acciones claras. Refinar no equivale a reemplazar la identidad.

- Agent Skills dirige especificación, implementación, pruebas, revisión, documentación y Git durante todo el desarrollo.
- `redesign-existing-projects`: auditar antes de modificar; cambios pequeños sobre Django y CSS existentes. No migrar frameworks por instalar una skill.
- `ui-ux-pro-max`: contraste, foco, etiquetas, validaciones, tamaños de interacción, tablas, estados vacíos y adaptación de pantalla. Priorizar una regla relevante sobre resultados genéricos.
- `impeccable`: jerarquía, consistencia y diseño centrado en tareas; sin animaciones decorativas ni patrones de una landing de ventas.
- Las recomendaciones se subordinan al contexto: no se añadirán fotografías, fuentes remotas, librerías o ruido visual solo porque una variante de skill los proponga. No habrá rediseño antes de aprobar el nuevo plan.

## Actualización y retirada futura

No se configuró actualización automática. Para actualizar, revisar el nuevo commit y sus instrucciones, conservar la versión previa y solicitar la autorización que corresponda al cambio. No sobrescribir personalizaciones sin revisarlas.

Para desinstalar las skills, retirar únicamente sus carpetas nombradas en este inventario cuando ya no se necesiten; no borrar el directorio general `.codex/skills`. Si se quiere eliminar el motor de Impeccable, comprobar primero que ninguna otra skill lo use y retirar exclusivamente su caché de versión. No hay hooks de este proyecto que revertir. Conservar este informe como trazabilidad; no es necesario borrar dependencias de Python del aplicativo.
