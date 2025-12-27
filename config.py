import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DB_USER = os.environ.get("root")
DB_PASSWORD = os.environ.get("asblrbgMenWEcOrRblZhObKjgQwdvbNl")
DB_HOST = os.environ.get("mysql.railway.internal")
DB_NAME = os.environ.get("railway")
DB_PORT = os.environ.get("DB_PORT", "3306")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://root:asblrbgMenWEcOrRblZhObKjgQwdvbNl@nozomi.proxy.rlwy.net:23123/railway"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
