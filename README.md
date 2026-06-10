# Maison

Maison is a Django 5.2 LTS rental marketplace scaffold for Kinshasa.

## Local Setup (Windows PowerShell)

Install Python 3.14 and create a local virtual environment:

```powershell
uv --cache-dir .uv-cache venv --python 3.14 .venv
.\\.venv\\Scripts\\Activate.ps1
python --version
uv --cache-dir .uv-cache pip install -r requirements.txt
```

Create the SQLite schema and run checks:

```powershell
python manage.py migrate
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python manage.py check
python manage.py test
python manage.py collectstatic --noinput --dry-run
```

Build Tailwind CSS with the official CLI:

```powershell
npm install
npm run css:build
npm run css:watch
```

Copy `.env.example` to your local environment manager and set real secrets outside git.

## Google OAuth Setup

Maison uses `django-allauth` for Google sign-in with Django sessions. Create a Google OAuth client outside source control and set these local environment variables:

```powershell
GOOGLE_OAUTH_CLIENT_ID=replace-with-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=replace-with-google-client-secret
```

For local development, add this authorized redirect URI in Google Console:

```text
http://localhost:8000/accounts/google/login/callback/
```

Only `profile` and `email` scopes are requested. Do not commit real Google credentials.
