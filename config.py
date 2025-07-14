import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7976646211:AAGdsEcpvDl1-pzoyXEFc0lkmbm6tlUCKck")

ADMINS = [
    1364324881,  # Admin 1
    591264759,   # Admin 2
]

Lviv_Center_Coords = (49.8419, 24.0315)
Lviv_Boundary_km = 10  # умовна відстань від центру до межі Львова
BASE_OUTSIDE_CITY_COST = 900
