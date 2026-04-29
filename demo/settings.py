from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "django-material-demo"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "material",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    }
]

STATIC_URL = "static/"
