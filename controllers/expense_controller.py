# controllers/expense_controller.py

from flask import Blueprint, request, jsonify
from services.expanse_service import ExpenseService
from dtos.request.expense_request import ExpenseCreateRequest
from exceptions.invaild_input_exception import InvaidInputException
from bson.errors import InvalidId

expense_controller = Blueprint("expense_controller", __name__)
service = ExpenseService()

@expense_controller.route("/expenses", methods=["POST"])
def create_expense():
    try:
        payload = request.get_json()
        req = ExpenseCreateRequest(**payload)
        expense_id = service.create_expense(req)
        return jsonify({"expense_id": expense_id}), 201
    except InvaidInputException as e:
        return jsonify({"error": e.message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expense_controller.route("/expenses/<expense_id>", methods=["GET"])
def get_expense(expense_id):
    try:
        expense = service.get_expense_by_id(expense_id)
        return jsonify(expense.model_dump()), 200
    except InvaidInputException as e:
        return jsonify({"error": e.message}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expense_controller.route("/expenses/user/<user_id>", methods=["GET"])
def get_user_expenses(user_id):
    try:
        expenses = service.get_expenses_by_user(user_id)
        return jsonify([e.model_dump() for e in expenses]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expense_controller.route("/expenses/<expense_id>", methods=["PUT"])
def update_expense(expense_id):
    try:
        updated_data = request.get_json()
        service.update_expense(expense_id, updated_data)
        return jsonify({"message": "Expense updated successfully"}), 200
    except InvaidInputException as e:
        return jsonify({"error": e.message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@expense_controller.route("/expenses/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    try:
        service.delete_expense(expense_id)
        return jsonify({"message": "Expense deleted successfully"}), 200
    except InvaidInputException as e:
        return jsonify({"error": e.message}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Don't forget to return it for app use
def get_expense_controller():
    return expense_controller
