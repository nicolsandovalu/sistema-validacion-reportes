"""
Configuración de Django para el sistema de validación de reportes.
Ajustado para cumplir con los estándares de seguridad y requerimientos de la Evaluación 2.
"""

from pathlib import Path
from decouple import config

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 1. SEGURIDAD Y CONFIGURACIÓN PRINCIPAL
# ==========================================
# La clave secreta y el modo debug se leen desde el archivo .env para externalizar credenciales
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*'] # Ajustar con los dominios reales en producción

# ==========================================
# 2. APLICACIONES Y MIDDLEWARES
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 
        'APP_DIRS': True,  # Permite que Django encuentre las plantillas en core/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto.wsgi.application'

# ==========================================
# 3. BASE DE DATOS (Criterio 2.1.1)
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración del campo ID por defecto para evitar advertencias de Django
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# 4. VALIDACIÓN DE CONTRASEÑAS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================
# 5. INTERNACIONALIZACIÓN Y ZONA HORARIA
# ==========================================
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ==========================================
# 6. ARCHIVOS ESTÁTICOS
# ==========================================
STATIC_URL = 'static/'

# ==========================================
# 7. CONFIGURACIÓN DE CORREOS AUTOMÁTICOS
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Se unifica el uso de 'decouple' para leer credenciales, eliminando el módulo 'os'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ==========================================
# 8. RUTAS DE AUTENTICACIÓN (Criterio 2.1.4)
# ==========================================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'gestion_reportes'
LOGOUT_REDIRECT_URL = 'login'