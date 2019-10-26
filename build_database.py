import os
from config import db, DATABASE_NAME
from models import ArtObject, Coordinate
from PIL import Image


TEST_ARTOBJECTS = [
    {"title": "ArtObject1", "description": "Test1",
     "coordinate": {"latitude": 62.88, "longitude": 63.11, "altitude": 0.1}},
    {"title": "ArtObject2", "description": "Test2",
     "coordinate": {"latitude": 42.88, "longitude": 23.11, "altitude": 0.24314}}
]
TEST_IMAGE = Image.open('test.png')

if os.path.exists(DATABASE_NAME):
    os.remove(DATABASE_NAME)

db.create_all()


# for obj in TEST_ARTOBJECTS:
#     title, description, coord = obj.get("title"), obj.get("description"), obj.get("coordinate")
#     latitude, longitude, altitude = coord.get("latitude"), coord.get("longitude"), coord.get("altitude")
#     p = ArtObject(title=obj.get("title"), description=obj.get("description"),
#                   coordinate=Coordinate(latitude=latitude, longitude=longitude, altitude=altitude))
#     db.session.add(p)

db.session.commit()
