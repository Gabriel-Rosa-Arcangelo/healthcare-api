# 🏥 Healthcare API (Django + DRF + JWT + Celery)

Secure REST API to manage **Patients**, **Samples**, **Lab Results**, and generate **clinical PDF reports** in the background — portfolio‑ready with a dark PDF layout.

---

## 🚀 Tech Stack
- **Django** + **Django REST Framework**
- **Auth:** JWT (SimpleJWT)
- **Async:** Celery + Redis
- **DB:** PostgreSQL (SQLite dev-friendly)
- **PDF:** ReportLab + Matplotlib (dark charts)
- **Docs:** OpenAPI/Swagger (drf-spectacular)
- **Docker** (optional)

---

## ✨ Features
- JWT authentication (access/refresh)
- CRUD for Patients, Samples, Results
- Filtering & pagination
- Background report generation (Celery tasks)
- Dark, single‑page PDF (metrics + bar + pie)
- Demo seed with Faker

---

## 🖥️ Quickstart (Local)

```bash
# 1) Create & activate venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt
# recommend: reportlab>=4.0 (avoid md5 usedforsecurity issue)

# 3) Migrate
python manage.py migrate

# 4) Create superuser
python manage.py createsuperuser

# 5) Start Redis (local or Docker)
redis-server
# or
docker run -p 6379:6379 redis:7

# 6) Celery worker (term 1)
celery -A config worker -l info

# 7) Run API (term 2)
python manage.py runserver


### Swagger
<img src="docs/screenshot-swagger.png" width="640"/>

### Reports
<img src="docs/screenshot-report.png" width="640"/>

### Settings & Notes

Use ReportLab ≥ 4.0 (evita erro usedforsecurity em envs antigos).

Para produção: PostgreSQL + S3 (media) + Redis gerenciado.

DEBUG=False e ALLOWED_HOSTS configurados.

📄 License

MIT

👤 Author

Built by Gabriel Rosa Arcangelo (@Gabriel-Rosa-Arcangelo)