import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7976646211:AAGdsEcpvDl1-pzoyXEFc0lkmbm6tlUCKck")
ORS_API_KEY = os.getenv("5b3ce3597851110001cf6248aa59ec61e83c41059f923ebaff9a9868")

LVIV_CENTER = (49.8419, 24.0315)  # Центр Львова
LVIV_RADIUS_KM = 10  # Межа міста — 10 км
