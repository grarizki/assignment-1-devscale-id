# config.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
ALEMBIC_CONFIG_FILE = "alembic.ini"