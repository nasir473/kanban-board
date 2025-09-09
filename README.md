Kanban Board (Django)
======================

Project overview
----------------
A lightweight Kanban board built with Django and SQLite. It supports multiple "Spaces" (workspaces) such as Office and Home, drag-and-drop task status updates, task detail editing with comments, and an admin module to manage spaces and tasks. The UI uses a brown/cream theme and serves static assets from the app `board/static` folder.

Tech stack
----------
- Python 3.13
- Django 5.2.5
- SQLite (default development DB)
- Templates + vanilla JS for drag-and-drop

Quick setup (development)
-------------------------
Open a PowerShell terminal in the project root and run:

```powershell
# create & activate virtualenv (example)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install deps if you keep requirements.txt
pip install -r requirements.txt   # optional

# create migrations and migrate
python manage.py makemigrations
python manage.py migrate

# create admin user
python manage.py createsuperuser

# run server
python manage.py runserver
```

Static files
------------
Static files live under `board/static/`. The project is configured to include `board/static` in `STATICFILES_DIRS` so during development Django serves these automatically when `DEBUG = True`.

Favicon
-------
Place a favicon file in `board/static/` (example `new_favicon.ico`). The base template references it using the `{% static %}` tag.

Key features
------------
- Workspaces (Spaces): created/managed via Django admin (`/admin/board/space/`). Any space created is listed in the site navbar dropdown and presents an independent, initially-empty Kanban board.
- Tasks: Task model with fields: short_description, description, status, workspace (ForeignKey to `Space`), comments.
- Drag-and-drop: move tasks between columns (status) using drag-and-drop. Status updates call the `update_task_status` view.
- Task detail: edit task fields and comments from a dedicated page; comments persist on the model and show on task cards.
- Admin: custom admin styling (placed under `board/static/admin/css/custom_admin.css`) and `Space` management.

Important file locations
------------------------
- Models: `board/models.py` (Task, Space)
- Views: `board/views.py` (board_view, create_task, task_detail, update_task_status, delete_task)
- Templates: `board/templates/` (base.html, board/board.html, board/create.html, board/task_detail.html)
- Admin: `board/admin.py`
- Static: `board/static/` (CSS, favicon, custom admin CSS)
- Context processor: `board/context_processors.py` (exposes `spaces` and `current_workspace` to templates)
- Settings: `kanban/settings.py` (STATICFILES_DIRS and context processor registered)

Database and migrations
-----------------------
Migrations are used to evolve the schema. After pulling changes, always run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

If you add fields that require data migration (for example, converting a string field to a ForeignKey), add a `RunPython` data migration and test locally.

How spaces (workspaces) work
---------------------------
- Spaces are stored in the `Space` model (`board.Space`).
- The navbar dropdown is populated from `Space` entries. Selecting a space sets `request.session['current_workspace']` and reloads the board for that space.
- Tasks reference a `Space` via `Task.workspace` (a ForeignKey). Tasks shown on the board are filtered by `workspace__name`.

Admin guidance
--------------
- Create/delete `Space` records in `/admin/board/space/`.
- Tasks are visible in `/admin/board/task/`; `comments` field is searchable and editable in admin.

Developer notes & conventions
-----------------------------
- Templates use `{% load static %}` and the custom `get_item` filter (where used) for dictionary lookups in templates.
- Avoid hardcoding workspace names in templates and views; rely on the `Space` table and the `spaces` context processor.
- Keep CSS variables in `base.html` to preserve the theme; reuse the variables in custom admin CSS.

Changelog (how to update)
-------------------------
When you add a new feature, append a new entry here with date, author, and a short description. Use this template:

- YYYY-MM-DD — <Your Name> — Short description of change. Files changed: `path/to/file1`, `path/to/file2`.

Current entries:
- 2025-09-02 — Initial project and features added (Tasks, Spaces, drag-and-drop, admin, comments persisted to model).

Suggested small tasks to keep documentation updated
--------------------------------------------------
- When you add or rename a model field, update the "Key features" and "Important file locations" sections.
- Add migration notes to "Database and migrations" when creating data migrations.

Testing and linting
-------------------
- Quick system check:

```powershell
python manage.py check
```

- Run tests (if you add tests):

```powershell
python manage.py test
```

Future improvements (ideas)
--------------------------
- Make `Task` comments into a separate `Comment` model (timestamp + author) for a full audit trail.
- Inline board editing for comments with AJAX/modal.
- Add unit tests for views and model migrations.
- Convert admin custom CSS into a small static app for reuse.

Contact and contributors
------------------------
Keep a short note here about who to contact for questions and where to record contribution notes.


---
Generated on 2025-09-02. Update this doc with new features as you add them.
