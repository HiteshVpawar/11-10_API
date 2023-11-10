# app/__init__.py
from flask import Flask
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB Connection Initialization
mongo_client = MongoClient(app.config['MONGO_URI'])
mongo_db = mongo_client[app.config['MONGO_DB_NAME']]


# Importing Modules
from .models import user
from .controllers import user_controller
from .views import user_view

# Exporting Objects for External Use
__all__ = ['app', 'mongo_db', 'user', 'user_controller', 'user_view']
