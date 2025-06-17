from flask import Blueprint, request, jsonify
from services.expanse_service import ExpenseService
from dtos.request.expense_request import ExpenseCreateRequest
from pydantic import ValidationError
from repositories.expanse_repository import  ExpenseRepository

def create_expense_controller(db):
    expense_bp = Blueprint("expense_controller", __name__)
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)

    @expense_bp.route("/", methods=["POST"])
    def create_expense_handler():
        try:
            data = request.get_json()
            expense_req = ExpenseCreateRequest(**data)
            result = service.create_expense(expense_req)
            return jsonify({"id": result}), 201
        except ValidationError as e:
            print("Validation error:", e.errors())
            return jsonify({"error": e.errors()}), 400
        except Exception as e:
            print("Unexpected error:", str(e))
            return jsonify({"error": str(e)}), 500

    return expense_bp
