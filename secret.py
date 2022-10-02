from dotenv import load_dotenv
import os 

load_dotenv()

ENV = os.getenv("MYENV")

API_KEY = os.getenv('MOVIEAPIKEY')
BASE_URL = os.getenv('BASEURL')

DB_SECRET = os.getenv('DBSECRET')
DB_URI = os.getenv('DBURI')

ADMIN_USER = os.getenv('ADMINUSER')
ADMIN_PASS = os.getenv('ADMINPASS')