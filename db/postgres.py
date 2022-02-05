import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

DB_USER: str = os.getenv("DB_USER")
DB_PASS: str = os.getenv("DB_PASS")
DB_HOST: str = os.getenv("DB_HOST")
DB_NAME: str = os.getenv("DB_NAME")
DB_PORT: int = int(os.getenv("DB_PORT"))


db_url: str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


db = SQLAlchemy()


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app=app)
