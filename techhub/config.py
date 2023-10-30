from sqlalchemy import create_engine

import mysql.connector

config = {
    'user': 'root',
    'password':'',
    'host': '127.0.0.1',
    'database': 'techhub',
    'charset': 'utf8mb4'
}

connection = mysql.connector.connect(**config)

SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
ADMIN_EMAIL="admin@personal.com"
USER_PROFILE_PATH="techhub/static/images/profile/"
POST_IMAGE_PATH = "techhub/static/images/post/"
ADMIN_PROFILE_PATH="techhub/static/images/profile/"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root@127.0.0.1/techhub?charset=utf8mb4"
engine = create_engine('mysql+mysqlconnector://root@127.0.0.1/techhub?charset=utf8mb4')

