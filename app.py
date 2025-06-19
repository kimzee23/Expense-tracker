# app.py
from flask import Flask, render_template
from pymongo import MongoClient

from controllers.auth_controller import create_auth_controller
from controllers.user_controller import create_user_controller
from controllers.budget_controller import create_budget_controller
from controllers.expense_controller import create_expense_controller
from controllers.report_controller import create_report_controller

def create_app(test_db=None):
    app = Flask(__name__)
    app.template_folder = 'templates'
    app.static_folder = 'static'
    app.secret_key = "your_secret_key"

    if test_db is None:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.expense_tracker_py
    else:
        db = test_db

    # Register blueprints
    app.register_blueprint(create_auth_controller(db), url_prefix="")  # No prefix so /dashboard works
    app.register_blueprint(create_user_controller(db), url_prefix="/api/v1/users")
    app.register_blueprint(create_budget_controller(db), url_prefix="/api/v1/budgets")
    app.register_blueprint(create_expense_controller(db), url_prefix="/api/v1/expenses")
    app.register_blueprint(create_report_controller(db), url_prefix="/api/v1/reports")

    @app.route("/")
    def landing():
        return render_template("landing.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
