import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine
from app import models

def create_tables():
    models.Base.metadata.create_all(bind=engine)