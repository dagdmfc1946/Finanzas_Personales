@echo off
setlocal
cd /d "%~dp0"
title Finanzas DAGD - Vista previa local
if not exist ".venv\Scripts\python.exe" (
  echo No se encontro el entorno de Python del proyecto.
  echo Sigue la preparacion del entorno indicada en README.md.
  pause
  exit /b 1
)
echo.
echo Finanzas DAGD - Fase 1 - Datos ficticios
echo Abre http://127.0.0.1:8765/ en tu navegador.
echo Para detener el aplicativo, presiona Ctrl+C en esta ventana.
echo.
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8765 --insecure --noreload
if errorlevel 1 (
  echo.
  echo No se pudo iniciar. Si el puerto ya esta ocupado, revisa si Finanzas DAGD esta abierto.
  pause
)
