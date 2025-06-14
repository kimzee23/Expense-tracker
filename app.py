from flask import Flask
from pymongo import MongoClient

from controllers.expense_controller import create_expense
from controllers.report_controller import create_report_controller
from controllers.user_controller import create_user_controller
from controllers.budget_controller import create_budget_controller

def create_app(db):
    app = Flask(__name__)
    app.register_blueprint(create_user_controller(db), url_prefix="/api/v1/users")
    app.register_blueprint(create_budget_controller(db), url_prefix="/api/v1/budgets")
    app.register_blueprint(create_report_controller(db), url_prefix="/api/v1/reports")
    app.register_blueprint(create_expense(db), url_prefix="/api/v1/expenses")
    return app

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client.expense_tracker_py
    app = create_app(db)
    app.run()
