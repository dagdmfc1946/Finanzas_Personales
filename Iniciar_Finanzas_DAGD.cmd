@echo off
setlocal
cd /d "%~dp0"
title Finanzas DAGD - Registro local
if not exist ".venv\Scripts\python.exe" (
  echo No se encontro el entorno de Python del proyecto.
  echo Sigue la preparacion del entorno indicada en README.md.
  pause
  exit /b 1
)
echo.
echo Finanzas DAGD - Fase 3 - Sueldo y registro local
echo Se abrira una pestana en el navegador cuando el servidor este listo.
echo Para detener el aplicativo, presiona Ctrl+C en esta ventana.
echo.
".venv\Scripts\python.exe" iniciar.py
if errorlevel 1 (
  echo.
  echo No se pudo iniciar. Si el puerto ya esta ocupado, revisa si Finanzas DAGD esta abierto.
  pause
)
