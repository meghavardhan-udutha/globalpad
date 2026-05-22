# GlobalPad — Secure File Sharing

A code-based file sharing web app built with Python, Django, and MySQL.
No authentication required — a code is all you need.

---

## Features

- **Upload Pad** — Create a pad with a custom code, add text and/or files
- **Access Pad** — Enter any code to view text content and download files
- **No Login Required** — Access and upload with just a code
- **REST API** — Clean endpoints for upload and retrieval
- **File Types** — Any file type supported (images, PDFs, documents, etc.)

---

## Quick Start (SQLite — development)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install Django Pillow

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## MySQL Setup (production)

1. Install mysqlclient:
```bash
pip install mysqlclient
```

2. Create the database:
```sql
CREATE DATABASE globalpad_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'globalpad'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON globalpad_db.* TO 'globalpad'@'localhost';
FLUSH PRIVILEGES;
```

3. Update `globalpad/settings.py` — replace the DATABASES block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'globalpad_db',
        'USER': 'globalpad',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Run migrations:
```bash
pip install -r requirements.txt
python manage.py migrate
```

---

## REST API

### Upload / Create a Pad
```
POST /api/upload/
Content-Type: multipart/form-data

Fields:
  code    (required) — 3-20 chars, letters/numbers/hyphens/underscores
  text    (optional) — plain text content
  files   (optional) — one or more files (repeat key for multiple)
```

**Response:**
```json
{
  "success": true,
  "code": "MY-CODE",
  "created": true,
  "files_uploaded": 2,
  "message": "Pad created successfully."
}
```

---

### Retrieve a Pad
```
GET /api/pad/<code>/
```

**Response:**
```json
{
  "code": "MY-CODE",
  "text": "Your text here",
  "files": [
    {
      "id": 1,
      "name": "document.pdf",
      "size": "1.2 MB",
      "type": "pdf",
      "url": "/media/uploads/MY-CODE/document.pdf"
    }
  ],
  "created_at": "2025-01-01 12:00",
  "updated_at": "2025-01-01 12:00"
}
```

---

### Download a File
```
GET /api/file/<file_id>/download/
```

Returns the file as a downloadable attachment.

---

## Project Structure

```
globalpad/
├── globalpad/
│   ├── settings.py       — Django settings (DB, media, etc.)
│   ├── urls.py           — Root URL config
│   └── wsgi.py
├── pad/
│   ├── models.py         — Pad and PadFile models
│   ├── views.py          — REST API views
│   ├── urls.py           — App URL routes
│   ├── migrations/       — DB migrations
│   └── templates/pad/
│       ├── index.html    — Landing page
│       ├── access.html   — Access files page
│       └── upload.html   — Upload/create pad page
├── media/                — Uploaded files stored here
├── static/               — Static assets
├── requirements.txt
└── manage.py
```

---

## Notes

- Uploaded files are stored in `media/uploads/<code>/`
- Max upload size: 50MB per request (configurable in settings.py)
- Codes are case-insensitive on input (normalized to uppercase)
- If a code already exists, uploading to it **appends** new files and **updates** text
