from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key_here'

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mysql@localhost/ecom_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
