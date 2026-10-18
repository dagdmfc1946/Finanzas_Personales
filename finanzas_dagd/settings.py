"""Configuración del registro financiero local de Finanzas DAGD."""
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_VERSION = (BASE_DIR / "VERSION").read_text(encoding="utf-8").strip()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "finanzas.sqlite3"
LOCAL_DIR = BASE_DIR / "local"
LOCAL_DIR.mkdir(exist_ok=True)
BACKUP_DIR = BASE_DIR / "backups"
secret_file = LOCAL_DIR / "secret.key"
try:
    with secret_file.open("x", encoding="utf-8") as secret_stream:
        secret_stream.write(secrets.token_urlsafe(64))
except FileExistsError:
    pass
SECRET_KEY = os.environ.get("DAGD_SECRET_KEY") or secret_file.read_text(encoding="utf-8").strip()
if len(SECRET_KEY) < 50:
    raise RuntimeError("El secreto local no es válido; revisa la instalación sin borrar datos.")
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "preview", "ledger"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "preview.middleware.PreviewHeadersMiddleware",
]
ROOT_URLCONF = "finanzas_dagd.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]},
}]
# Persistencia local de la Fase 2; pruebas aisladas por el test runner de Django.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATA_FILE, "OPTIONS": {"timeout": 20}}}
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

LOGIN_URL = "/acceso/"
LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = "/acceso/"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
