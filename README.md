# mini-django-app — Notes

A small Django app for creating, viewing, and deleting short text notes.
Built to be simple enough to use as the base project for a DevSecOps
exercise (branch protection, PR workflow, CODEOWNERS, etc.).

## Features
- List all notes
- Create a new note (title + content)
- View a single note
- Delete a note
- Notes manageable from the Django admin

## Project structure
```
mini-django-app/
├── manage.py
├── requirements.txt
├── notes_project/      # Django project (settings, urls, wsgi)
└── notes/               # The notes app (models, views, forms, admin)
    └── migrations/
templates/notes/         # HTML templates
```

## Setup
```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.
Admin panel: http://127.0.0.1:8000/admin/

## Contributing
All changes should go through a Pull Request into `main`.
