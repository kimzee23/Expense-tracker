
from flask import request, render_template, redirect, url_for, session, Flask
from pymongo import MongoClient
from controllers.auth_controller import create_auth_controller
from controllers.dashboard_controller import dashboard_bp
from controllers.user_controller import create_user_controller
from controllers.budget_controller import create_budget_controller
from controllers.expense_controller import create_expense
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

    auth_bp = create_auth_controller(db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(create_user_controller(db), url_prefix="/api/v1/users")
    app.register_blueprint(create_budget_controller(db), url_prefix="/api/v1/budgets")
    app.register_blueprint(create_report_controller(db), url_prefix="/api/v1/reports")
    app.register_blueprint(create_expense(db), url_prefix="/api/v1/expenses")

    # Root route
    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            return redirect("/login")
        return render_template("dashboard.html")

    @auth_bp.route('/register', methods=['GET'])
    def register_page():
        return render_template('register.html')

    @auth_bp.route('/login', methods=['GET'])
    def login_page():
        return render_template('login.html')

    return app




    import pprint
    print("\n--- Registered URL Map ---")
    pprint.pprint([str(rule) for rule in app.url_map.iter_rules()])
    print("--------------------------\n")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)