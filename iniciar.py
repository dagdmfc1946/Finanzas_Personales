"""Inicia la vista previa y abre una pestaña cuando el servidor está listo."""
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen
import webbrowser

URL = 'http://127.0.0.1:8765/'
ROOT = Path(__file__).resolve().parent


def is_ready():
    try:
        with urlopen(URL, timeout=1) as response:
            page = response.read(131072).decode('utf-8')
        return '<title>Resumen · Finanzas DAGD</title>' in page
    except (OSError, URLError, UnicodeError):
        return False


def port_in_use():
    try:
        with socket.create_connection(('127.0.0.1', 8765), timeout=1):
            return True
    except OSError:
        return False


def wait_until_ready(server):
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if server.poll() is not None:
            return False
        if is_ready():
            return True
        time.sleep(0.2)
    return False


def open_tab():
    if not webbrowser.open(URL, new=2):
        print(f'No se pudo abrir el navegador automaticamente. Abre {URL}')


def main():
    if is_ready():
        print('Finanzas DAGD ya esta ejecutandose. Se abre el navegador.')
        open_tab()
        return 0
    if port_in_use():
        print('El puerto 8765 esta ocupado por un servicio que no se identifico como Finanzas DAGD.')
        return 1
    server = None
    try:
        server = subprocess.Popen([
            sys.executable, str(ROOT / 'manage.py'), 'runserver',
            '127.0.0.1:8765', '--insecure', '--noreload',
        ], cwd=ROOT)
        if not wait_until_ready(server):
            print('No se pudo confirmar el inicio de Finanzas DAGD. Revisa el error de la consola.')
            return 1
        open_tab()
        print('Para detener el aplicativo presiona Ctrl+C en esta ventana.')
        return server.wait()
    except KeyboardInterrupt:
        print('\nCerrando la instancia iniciada desde esta ventana.')
        return 0
    except OSError as error:
        print(f'No se pudo iniciar: {error}')
        return 1
    finally:
        if server is not None and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


if __name__ == '__main__':
    raise SystemExit(main())
