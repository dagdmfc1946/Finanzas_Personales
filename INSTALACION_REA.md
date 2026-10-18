# Instalación y desinstalación segura de REA

Fecha: 2026-10-17, America/Bogota. Estado: instalado y verificado para las operaciones descritas. Autorización: el usuario solicitó instalar lo necesario para analizar Moneri. No se inició la Fase 1 del aplicativo.

## Inventario y alcance

| Componente | Versión | Ubicación y finalidad |
|---|---|---|
| Node.js existente de Codex | 24.19.0 | `C:\Users\Diego\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe`. Reutilizado; no instalado ni modificado. |
| npm portátil | 12.2.0 | `C:\Users\Diego\.local\share\rea-finanzas\bootstrap\package`. Usado para adquirir REA y sus dependencias. |
| REA | 6.5.0 | `C:\Users\Diego\.local\share\rea-finanzas\runtime\node_modules\rea-agents`. Instalación local aislada, 173 paquetes añadidos por npm. |
| Eclipse Temurin OpenJDK, JDK completo x64 | 21.0.12.1+1 | `C:\Users\Diego\.local\share\rea-finanzas\android\jdk-21.0.12.1+1`. Java y compilador para el proveedor Android. |
| jadx-headless-mcp | 0.7.1 | `C:\Users\Diego\.local\share\rea-finanzas\android\jadx-headless-mcp-0.7.1-all.jar`. Análisis estático de APK. |
| Skill incluida con REA | metadata.version 42 | Nueva instalación en `C:\Users\Diego\.agents\skills\reverse-engineer-anything`. La skill previa en `.codex\skills` no fue reemplazada. |
| Google Chrome existente | 155.0.8059.82 observado por REA | Reutilizado para capturar la ficha pública. No instalado ni actualizado. |

No se modificaron PATH ni JAVA_HOME globales. No se instalaron Android Studio, emulador, ADB, Hopper, Ghidra, IDA ni extensiones de navegador. No son necesarios para la captura pública y la ruta estática Android seleccionadas. Cada proveedor tiene requisitos propios; esta instalación no garantiza todas las operaciones posibles de REA.

La primera descarga se hizo en `C:\Users\Diego\AppData\Local\REA`. REA detectó virtualización MSIX de Codex y rechazó registrar ese lanzador. Se trasladó la carpeta completa a `.local\share\rea-finanzas`; la configuración usa exclusivamente esta ubicación estable.

## Fuentes y verificaciones de integridad

- REA: https://registry.npmjs.org/rea-agents/6.5.0. npm resolvió y verificó las dependencias; el lockfile queda en `runtime\package-lock.json`.
- npm: https://registry.npmjs.org/npm/-/npm-12.2.0.tgz.
- JDK: API oficial https://api.adoptium.net/v3/assets/latest/21/hotspot?architecture=x64&image_type=jdk&os=windows&vendor=eclipse. Metadatos concretos conservados en `logs\jdk-release.json`.
- SHA-256 del ZIP del JDK, comprobado antes de extraer: `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e`.
- JADX: https://github.com/1013503897/jadx-headless-mcp/releases/download/v0.7.1/jadx-headless-mcp-0.7.1-all.jar.
- SHA-256 de JADX, comprobado contra la referencia publicada por REA: `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75`.
- Requisitos oficiales Android: https://github.com/morluto/rea/blob/main/docs/android-analysis.md.

## Procedimiento realizado

1. Comprobar Node, npm, Java, proveedores y registro existente. Node disponible; npm/npx, Java y registro REA ausentes.
2. Descargar npm portátil e instalar la versión fija de REA mediante `npm-cli.js install --prefix ... --cache ... --ignore-scripts --no-audit --no-fund rea-agents@6.5.0`. Se deshabilitaron scripts de instalación; las operaciones verificadas funcionaron con esa configuración. No se realizó una auditoría completa de dependencias.
3. Descargar y verificar el JDK y el JAR indicados; extraer el JDK sin instalador del sistema.
4. Ejecutar `doctor --client codex --json` y `setup --client codex --dry-run --json`. Resolver el problema de virtualización y repetir el plan desde la ruta estable.
5. Aplicar `setup --client codex --yes --json`, usando JAVA_HOME y REA_JADX_MCP_JAR únicamente en el proceso de configuración. Setup persistió esos valores en el entorno del servidor REA.
6. Comprobar el JDK, el diagnóstico posterior, el arranque MCP y la captura pública de Moneri.

## Configuración y respaldo

Archivo modificado: `C:\Users\Diego\.codex\config.toml`.
Respaldo previo generado por REA: `C:\Users\Diego\.codex\config.toml.rea.backup`.
Se preservó la configuración ajena a REA. Bloques añadidos:

```toml
[mcp_servers.rea]
command = "C:\\Users\\Diego\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\bin\\node.exe"
args = [ "C:\\Users\\Diego\\.local\\share\\rea-finanzas\\runtime\\node_modules\\rea-agents\\scripts\\rea.mjs", "mcp" ]
startup_timeout_sec = 30

[mcp_servers.rea.env]
JAVA_HOME = "C:\\Users\\Diego\\.local\\share\\rea-finanzas\\android\\jdk-21.0.12.1+1"
REA_JADX_MCP_JAR = "C:\\Users\\Diego\\.local\\share\\rea-finanzas\\android\\jadx-headless-mcp-0.7.1-all.jar"
```

El lanzador depende del Node existente de Codex. Si una actualización mueve o elimina ese ejecutable, comprobar su nueva ubicación y actualizar solo `command`; no reinstalar motores por ese motivo.

## Cómo ejecutar y verificar

En PowerShell, usando variables de esta sesión:

```powershell
$reaNode = 'C:\Users\Diego\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$reaRoot = 'C:\Users\Diego\.local\share\rea-finanzas'
$reaCli = Join-Path $reaRoot 'runtime\node_modules\rea-agents\scripts\rea.mjs'
$env:JAVA_HOME = Join-Path $reaRoot 'android\jdk-21.0.12.1+1'
$env:REA_JADX_MCP_JAR = Join-Path $reaRoot 'android\jadx-headless-mcp-0.7.1-all.jar'
& $reaNode $reaCli --version
& $reaNode $reaCli doctor --client codex --json
# Cuando exista un APK real y se conozca su ruta:
# & $reaNode $reaCli inspect-android-package 'D:\ruta\Moneri.apk' --json
```

Resultados observados:

- REA: `6.5.0`; Java y javac: `21.0.12.1`.
- Setup: `status=ready`, acciones `configured_codex` e `installed_skill`.
- Doctor posterior: `healthy=true` para el alcance solicitado; `environment_healthy=false` por proveedores opcionales sin configurar. No implica que Android esté averiado: inspección JADX `configured=true`, `available=true`, JAR validado.
- Conexión de prueba al servidor MCP: inicialización correcta; 207 herramientas anunciadas, incluidas `inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method` y `trace_android_references`. La prueba se cerró al terminar.
- CLI: captura real de Google Play completada, evidencia y limpieza del navegador verificadas. Ver `ANALISIS_REA_MONERI.md`.
- No se comprobó todavía la carga y decompilación de Moneri: falta su APK. Readiness no sustituye esa prueba.

Codex debe reconectar el servidor o reiniciarse para incorporar las herramientas a una sesión que ya estaba abierta. Mientras tanto, la CLI funciona y fue la vía utilizada. La conexión de prueba no añade herramientas al chat actual.

Registros locales: `C:\Users\Diego\.local\share\rea-finanzas\logs`. Incluyen doctor antes/después, planes, aplicación del registro, metadatos JDK, prueba MCP y evidencia de Google Play. No publicar la configuración completa de Codex ni respaldos como parte del proyecto.

## Desinstalación segura futura

Estas instrucciones no se ejecutaron. Preservar primero los informes y las evidencias que se quieran conservar; la evidencia original vive dentro de la carpeta de instalación.

### Retirada limitada a esta instalación (recomendada)

1. Cerrar las sesiones que estén usando REA y salir de Codex. Abrir PowerShell independiente para evitar que la aplicación reescriba su configuración al cerrar.
2. Hacer una copia nueva de `C:\Users\Diego\.codex\config.toml`. Editar ese archivo para retirar exclusivamente los bloques `[mcp_servers.rea]` y `[mcp_servers.rea.env]` añadidos arriba. Conservar las demás secciones. No restaurar íntegramente el respaldo antiguo si hubo cambios posteriores en otras opciones.
3. Revisar la skill nueva en `C:\Users\Diego\.agents\skills\reverse-engineer-anything`; si no tiene cambios propios y no la utiliza otra instalación, retirar únicamente esa carpeta. Conservar la skill preexistente `C:\Users\Diego\.codex\skills\reverse-engineer-anything`.
4. Tras copiar las evidencias necesarias y confirmar que ninguna otra configuración usa esta ruta, borrar solo el directorio aislado. El siguiente bloque comprueba el destino exacto y muestra la operación antes del borrado:

```powershell
$reaRemovalTarget = 'C:\Users\Diego\.local\share\rea-finanzas'
$reaResolvedTarget = (Resolve-Path -LiteralPath $reaRemovalTarget -ErrorAction Stop).Path
if ($reaResolvedTarget -ne 'C:\Users\Diego\.local\share\rea-finanzas') {
    throw 'Destino inesperado; no se elimina nada.'
}
Remove-Item -LiteralPath $reaResolvedTarget -Recurse -WhatIf
# Solo después de revisar la simulación y conservar evidencias:
# Remove-Item -LiteralPath $reaResolvedTarget -Recurse
```

5. Reiniciar Codex y verificar que REA ya no esté registrado. No borrar Node ni Chrome, que existían previamente. El JDK y npm privados desaparecen al retirar `rea-finanzas`; no hay paquetes globales ni cambios de PATH que revertir. Conservar el respaldo de configuración hasta verificar el funcionamiento de Codex.

### Desinstalador oficial: alternativa con alcance más amplio

Antes de borrar la carpeta, `& $reaNode $reaCli uninstall --json` retira registros y skills administrados por REA. En 6.5.0 no ofrece selección `--client` ni `--dry-run`: inspecciona múltiples clientes y destinos de skills, por lo que puede afectar una instalación REA ajena a este proyecto o la skill preexistente. No usarlo sin revisar ese alcance. Omitir `--purge-data` si se quiere conservar el estado. El desinstalador no sustituye la retirada manual de las dependencias portátiles de esta carpeta.
