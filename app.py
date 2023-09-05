from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://ravi:ravi1234@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize SQLAlchemy with the app instance
from flask_login import LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)



