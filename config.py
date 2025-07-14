import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ORS_API_KEY = os.getenv("ORS_API_KEY")

LVIV_CENTER = (49.8419, 24.0315)  # Центр Львова
LVIV_RADIUS_KM = 10  # Межа міста — 10 км