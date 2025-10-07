# SongStories - AI Short Songs (Prototype)

## Quick start (Windows)
1. Unzip the project and open terminal in project folder.
2. Create virtual env:
   python -m venv .venv
   .venv\Scripts\activate
3. Install requirements:
   pip install -r requirements.txt
4. Set environment variable (PowerShell):
   setx MUSICGPT_API_KEY "your_key_here"
   (or in current session: $env:MUSICGPT_API_KEY='your_key_here')
5. Run migrations and start:
   python manage.py migrate
   python manage.py runserver
6. Open http://127.0.0.1:8000

## Deploy (Render)
- Push repo to GitHub.
- Create Web Service on Render and connect repo.
- Build command: pip install -r requirements.txt
- Start command: gunicorn songstories.wsgi
- Add ENV var MUSICGPT_API_KEY in Render dashboard.
# SongStories
