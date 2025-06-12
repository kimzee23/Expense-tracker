from flask import Flask
from pymongo import MongoClient

from controllers.user_controller import create_user_controller

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.expense_tracker_py
app.register_blueprint(create_user_controller(db), url_prefix="/api/v1/users")

if __name__ == "__main__":
    app.run()
