from app import app
from db import db

db.init_app(app)

# import every resource or model for which we need to create tables automatically
@app.before_first_request
def create_tables():
    db.create_all()