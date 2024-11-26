# Litrevu Deployment Guide

## Install App

### Create a Virtual Environment
Create and install a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate # Sur Windows : venv\Scripts\activate
```

Then, install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Setup Environment Variables

Create a `.env` file in the root directory and configure the following environment variables:

```plaintext
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = BASE_DIR / "media"
```

To setup the test database, please add following variable in your environement variables:
```plaintext
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "litrevu_test.db",
    }
}
```
If you want to setup your own database, you need configure that same variable but following [Django guidelines](https://docs.djangoproject.com/en/5.1/ref/databases/) to match your configuration.

You can use [django-environ](https://django-environ.readthedocs.io/) or any similar library to load these variables.

### Setup Database

There is a test database (SQLite) in the repo to test the app. 

However, if you need to create your own database:
* First, setup the database of your chosing.
* Then, apply migrations to configure the database:

```bash
python manage.py migrate
```

## Run the Application Locally

To test the application locally, use the Django development server:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.


## Test data

### Admin logins:

Use following logins to connect as superuser:
- **username** : `root`
- **password** : `root`

Two regular users also exists:
- **username** : `toto`
- **password** : `Tata123*`

And:
- **username** : `tata`
- **password** : `Toto123*`