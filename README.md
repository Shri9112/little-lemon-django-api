# Little Lemon — Minimal Django REST Framework Project

A compact educational implementation for the Coursera Little Lemon peer-graded assignment.

## Features
- Django serves a static HTML home page at `/`.
- REST API for menu items and table bookings.
- MySQL configuration (PyMySQL) controlled by environment variables.
- SQLite fallback for a quick local smoke test only.
- Registration returns a DRF token; login returns a token; logout invalidates it.
- Public menu reads; authenticated menu writes.
- Authenticated users can manage their own bookings; staff can see all bookings.
- Automated API tests.

## 1. Set up on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For a quick smoke test without MySQL, use SQLite (the default):

```bash
python manage.py migrate
python manage.py test
python manage.py runserver
```

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/api/.

## 2. Configure MySQL for the assignment

Install/start MySQL locally if it is not already installed. Log in as a MySQL administrator and run:

```sql
CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'littlelemon_user'@'localhost' IDENTIFIED BY 'change-this-password';
GRANT ALL PRIVILEGES ON littlelemon.* TO 'littlelemon_user'@'localhost';
FLUSH PRIVILEGES;
```

Copy `.env.example` to `.env` and set `DB_ENGINE=mysql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` to match your MySQL setup.

**Note:** Django does not load `.env` automatically in this minimal project. Export the variables in your terminal before running Django. Example:

```bash
export DB_ENGINE=mysql
export DB_NAME=littlelemon
export DB_USER=littlelemon_user
export DB_PASSWORD='change-this-password'
export DB_HOST=127.0.0.1
export DB_PORT=3306
python manage.py migrate
python manage.py test
python manage.py runserver
```

Use the same environment variables in each new terminal. Never commit real passwords or secret keys.

## 3. Create an admin user (optional)

```bash
python manage.py createsuperuser
```

## 4. API endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/api/menu/` | Public | List menu items |
| GET | `/api/menu/<id>/` | Public | Retrieve one item |
| POST | `/api/menu/` | Token | Create item |
| PUT/PATCH | `/api/menu/<id>/` | Token | Update item |
| DELETE | `/api/menu/<id>/` | Token | Delete item |
| GET | `/api/bookings/` | Token | List own bookings (staff see all) |
| POST | `/api/bookings/` | Token | Create booking |
| GET | `/api/bookings/<id>/` | Token | Retrieve own booking |
| PUT/PATCH | `/api/bookings/<id>/` | Token | Update own booking |
| DELETE | `/api/bookings/<id>/` | Token | Delete own booking |
| POST | `/api/registration/` | Public | Register and receive token |
| POST | `/api/login/` | Public | Obtain token |
| POST | `/api/logout/` | Token | Invalidate current token |
| GET | `/` | Public | Static HTML home page |

### Example requests

Register:
```json
{"username":"demo","email":"demo@example.com","password":"StrongPass456!"}
```

Login:
```json
{"username":"demo","password":"StrongPass456!"}
```

Create menu item (send header `Authorization: Token YOUR_TOKEN`):
```json
{"title":"Lemon Cake","price":"5.50","inventory":10}
```

Create booking (send header `Authorization: Token YOUR_TOKEN`):
```json
{"name":"Demo Guest","no_of_guests":2,"booking_date":"2027-01-15T19:00:00+05:30"}
```

## 5. Insomnia testing
Create a request for each endpoint. For protected routes, add header:
`Authorization: Token YOUR_TOKEN`

For POST/PUT requests choose JSON body. Run registration first and copy its `token` value.

## 6. Tests

```bash
python manage.py test
```

The included tests cover the HTML page, public menu reads, permissions, registration and booking creation.

## 7. GitHub submission

Create an empty public GitHub repository named `little-lemon-django-api`, then run from this project directory:

```bash
git init
git add .
git commit -m "Build Little Lemon Django REST API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/little-lemon-django-api.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not push `.env`, passwords, or database files.

On Coursera, open **My submission**, enter a project title such as `Little Lemon Django REST API`, paste your repository URL (not the `.git` URL is also fine), preview, and submit. Then complete two peer reviews.

## Important
This is a minimal learning project, not production-ready software. Use a strong secret key, `DEBUG=False`, proper HTTPS, secure secret management and stronger validation before deployment.
