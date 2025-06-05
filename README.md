
The app is live at:
[**[https://django-sandwiches-608c09739bab.herokuapp.com/](https://django-sandwiches-608c09739bab.herokuapp.com/)** 


This project began as Code Institute’s “Love Sandwiches” terminal exercise but has been fully rewritten as a Django 4.2 web application with six separate number inputs (one for each sandwich) instead of a single comma-separated field, making it more user-friendly for restaurants to log daily sales. It pushes data to Google Sheets via `gspread` (using service-account credentials loaded either from a `creds.json` file or the `GOOGLE_CREDS_JSON` environment variable), computes surplus and next-day stock using a five-day rolling average +10 %, and displays results in a responsive Bootstrap interface with a persistent dark-mode toggle. The app is deployed on Heroku under Gunicorn with static files served by WhiteNoise, and environment variables are managed via a `.env` file with Python-Decouple.

---

## 🌟 Features at a Glance

| Feature                          | Details                                                                                                                                                                                                                                           | Why It Matters                                                                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Six individual number fields** | Six separate `<input type="number">` fields (one per sandwich) have replaced the original single comma-separated input, eliminating comma-parsing errors and improving form accessibility.     | Prevents user mistakes and speeds data entry, especially on mobile devices.                                                            |
| **Google Sheets backend**        | Uses `gspread` (a Python client for Google Sheets API v4) to authorize with service-account credentials, append sales data, read the last five entries per column, and calculate stock/surplus.  | Leverages a familiar spreadsheet as a zero-infrastructure data store to avoid managing a separate database.            |
| **Stock & surplus logic**        | Surplus = yesterday’s stock − today’s sales; next-day stock = average of the last 5 sales × 1.10 (rounded).                                                                               | Prevents overproduction and waste while ensuring adequate supply.                                                                                                        |
| **Dark-mode toggle**             | TailwindCSS’s `dark:` variant is enabled via a custom `class` strategy, and the user’s preference is stored in `localStorage`.                                                           | Provides comfortable viewing in low-light conditions and persists across sessions.                                |
| **Django 4.2 foundation**        | Built on Django 4.2 (an LTS release with async middleware, improved ASGI, refined model fields, and JSONField support).                                                                  | Ensures long-term support, security patches until 2026, and modern framework features.                           |
| **WhiteNoise for static files**  | `whitenoise` 6.9.0 serves CSS/JS/Images directly from the Django app without an external CDN or storage service.                                                                 | Simplifies static-file handling on Heroku and speeds asset delivery.                                                                                                     |
| **Heroku-ready deployment**      | A one-line `Procfile` (`web: gunicorn django_sandwiches.wsgi`) and pinned dependencies in `requirements.txt` (including Gunicorn 23.0.0, `psycopg2-binary` 2.9.10) allow push-to-deploy.  | Enables fast, reliable deployment; credentials (e.g., `GOOGLE_CREDS_JSON`) live only in Heroku’s Config Vars, not Git.  |

---

## ⚙️ Tech Stack

* **Backend Languages & Frameworks**

  * Python 3.11
  * Django 4.2.21 (LTS, async-ready) 

* **Google Sheets Integration**

  * `gspread` 6.2.1 (Python API for Sheets v4) 
  * `google-auth`, `google-auth-oauthlib`, `oauthlib`, `requests-oauthlib` for OAuth2 service-account flows 

* **Frontend**

  * Bootstrap

* **Static Files & Assets**

  * WhiteNoise 6.9.0 for serving static assets on Heroku 
  * `django-widget-tweaks` 1.5.0 for easier template rendering of form widgets

* **Database & Deployment**

  * PostgreSQL (via `psycopg2-binary` 2.9.10) on Heroku 
  * Gunicorn 23.0.0 as the WSGI server 
  * `dj-database-url` 2.3.0 for parsing Heroku’s `DATABASE_URL` 

* **Environment & Secrets**

  * Python-Decouple 3.8 to load `.env` and Heroku Config Vars (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`). 
  * `django-decouple` pattern ensures secrets are never committed. 

---

## 🚀 Install & Cloning

> **Prerequisites:** Python 3.11+, Git, a Google Cloud service-account JSON key, and a Google Sheets spreadsheet named **`love_sandwiches`** shared with that service account.

```bash
# 1. Clone the repository
git clone https://github.com/fenasti/django-sandwiches.git 
cd django-sandwiches

# 2. Create & activate a virtual environment
python3 -m venv venv 
source venv/bin/activate # (or `.\venv\Scripts\activate` on Windows) :

# 3. Install dependencies
pip install -r requirements.txt 

# 4. Create a `.env` file at the project root (do NOT commit .env)
cat > .env <<EOL
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=django-sandwiches-608c09739bab.herokuapp.com,127.0.0.1,localhost

# 5. Google Sheets credentials (local dev)
#    Save your service-account JSON as "creds.json" at the project root.
#    The code auto-loads creds.json if GOOGLE_CREDS_JSON is not set. 
# 6. Apply migrations & collect static files
python manage.py migrate 
python manage.py collectstatic --noinput 

# 7. Run the development server
python manage.py runserver   

# Visit: http://127.0.0.1:8000/ and start entering daily sandwich sales!
```

---

## ☁️ Deployment on Heroku (Already Live)

The app is live at:
[**[https://django-sandwiches-608c09739bab.herokuapp.com/](https://django-sandwiches-608c09739bab.herokuapp.com/)** 
1. **Provision a Heroku app**

   ```bash
   heroku create django-sandwiches-608c09739bab
   heroku stack:set heroku-22
   ```


2. **Set Heroku Config Vars**
   In the Heroku Dashboard → Settings → Config Vars, add:

   * `SECRET_KEY` → (some random secret key)
   * `DEBUG` → `False`
   * `ALLOWED_HOSTS` → `django-sandwiches-608c09739bab.herokuapp.com`
   * `GOOGLE_CREDS_JSON` → (paste your service-account JSON as a single line)


3. **Procfile**
   The repo’s `Procfile` contains:

   ```
   web: gunicorn django_sandwiches.wsgi
   ```

   This instructs Heroku to use Gunicorn as the WSGI server. 

4. **Push & Deploy**

   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main   # or master, depending on your branch
   ```

   On each push, Heroku will:

   * Install dependencies from `requirements.txt` 
   * Run `python manage.py migrate` automatically 
   * Serve static assets using WhiteNoise 
   * Launch Gunicorn with `django_sandwiches.wsgi` 

---

## 🔄 Data Flow & Google Sheets Logic

1. **Sales Entry** → User enters six integers (one per sandwich).
2. **`update_worksheet(data, "sales")`** → Appends a new row to the `sales` worksheet.
3. **`calculate_surplus_data(sales_row)`** → Fetches the last row of the `stock` worksheet, computes surplus = stock − sales for each item. 
4. **`get_last_5_entries_sales()`** → Grabs the last five entries for each of the six columns from the `sales` worksheet. 
5. **`calculate_stock_data(last_5_entries)`** → Computes the mean of each list, multiplies by 1.10, and rounds to the nearest integer, yielding six new stock values. 
6. **Dashboard** → The calculated surplus (positive = waste, negative = extra demand) and new stock recommendations are displayed inmediatly.

---

## 🎨 UI / UX Touches

* **Bootstrap** is used for styling with custom colors, responsive mobile-first design, and uses the `class` strategy for dark mode
* **Dark-mode toggle** in the navbar applies/toggles a `dark` class on `<html>` and stores the theme in `localStorage` to persist between sessions. 
* **Form errors & validation** are displayed inline using Django’s form-error tags with `django-widget-tweaks`. 


## 🙏 Acknowledgements

* **Code Institute** for the original “Love Sandwiches” CLI exercise.

