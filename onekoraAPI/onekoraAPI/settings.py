
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [
    '10.0.2.2',  
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',        
    'corsheaders',           
    'fcm_django',          
    'api',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onekoraAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'onekoraAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'onekora_db',                   
        'USER': 'root',                         
        'PASSWORD': os.getenv('DB_PASSWORD'),   
        'HOST': 'localhost',                    
        'PORT': '3306',                         
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True 

# Nota de Edson: Voy a dejar esto acá para la
# futura implementación de lo que quiero hacer (incluida la pagina web)
# Los nombres de onekoramobile.com y onekoraweb.com son provisionales no se lo tomen enserio
# No descomentar esto hasta que se haya implementado la web y la app movil, porfis
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://localhost:8081",
#     "http://onekoramobile.com",
#     "http://onekoraweb.com",
# ]


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}













































"""
============================================================================
AVISO DE PROPIEDAD INTELECTUAL
============================================================================
* PROYECTO:        Onekora (Anteriormente "Huánuco Recicla")
* DESARROLLADOR:   Dionicio Orihuela Edson Raul
* AÑO:             2025
* UBICACIÓN:       Huánuco, Perú

----------------------------------------------------------------------------
AUTORÍA
----------------------------------------------------------------------------
Este código fuente, incluyendo la lógica de negocio, arquitectura de software
(Frontend y Backend), diseño de interfaces (UI), experiencia de usuario (UX),
activos gráficos y el rebranding de la identidad visual de la marca "Onekora",
ha sido desarrollado en su totalidad por Dionicio Orihuela Edson Raul.

El autor certifica su autoría exclusiva sobre la obra completa, abarcando:
1. Desarrollo FullStack (React Native / Django).
2. Diseño Gráfico y Creativo.
3. Ingeniería de Software y Base de Datos.

----------------------------------------------------------------------------
MARCO LEGAL
----------------------------------------------------------------------------
Esta obra está protegida por las leyes de propiedad intelectual de la
República del Perú, específicamente bajo el DECRETO LEGISLATIVO Nº 822
(Ley sobre el Derecho de Autor) y sus modificatorias.

Conforme al Artículo 22 de dicha ley, el autor reivindica su DERECHO MORAL
de paternidad sobre la obra, el cual es perpetuo, inalienable e imprescriptible.

Queda terminantemente prohibida la reproducción total o parcial, distribución,
comunicación pública, transformación o ingeniería inversa de este software
sin la autorización previa y por escrito del titular de los derechos.

Cualquier uso no autorizado de este código o de los elementos visuales
asociados constituirá una violación a los derechos de propiedad intelectual
y será sujeto a las acciones civiles y penales correspondientes ante el
INDECOPI y el Poder Judicial del Perú.

============================================================================
"""