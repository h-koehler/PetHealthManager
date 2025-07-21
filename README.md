### Deployed at https://pet-health-manager.onrender.com
This may take a while to load.
## Run locally
### Run server
1. Clone repo
   ```
   git clone https://github.com/h-koehler/PetHealthManager.git
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
5. Run server
   ```
   python manage.py runserver
   ```
### Configure DB:
1. Install PostgreSQL
   ```
   pip install psycopg2-binary
   ```
3. Create database and user. Enter a Password (`[pass]`) when prompted
   ```
   createuser [user] --pwprompt
   createdb [db] --owner=[user]
   ```
4. In `settings.py`, replace DATABASES with:
   ```
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "[db]",
        "USER": "[user]",
        "PASSWORD": "[pass]",
        "HOST": "127.0.0.1", # or 'localhost'
        "PORT": "5432",
     }
   }
   ```
5. Migrate schema
   ```
   python manage.py migrate
   ```
6. Load data
   ```
   python manage.py loaddata demo.json
   ```
