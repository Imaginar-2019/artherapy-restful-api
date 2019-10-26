import os
from config import db, DATABASE_NAME
if os.path.exists(DATABASE_NAME):
    os.remove(DATABASE_NAME)

db.create_all()
