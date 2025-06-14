from flask import Blueprint, request, jsonify
from services.expanse_service import ExpenseService
from repositories.expanse_repository import ExpenseRepository
from dtos.request.expense_request import ExpenseCreateRequest
from utils.mapper.expense_mapper import expense_model_to_response_dto
from pydantic import ValidationError

def create_expense(db):
    expense_bp = Blueprint('expense_controller', __name__)
    repo = ExpenseRepository(db)
    service = ExpenseService(repo)

    @expense_bp.route("/", methods=["POST"])
    def create_expense_handler():
        try:
            data = request.get_json()
            expense_req = ExpenseCreateRequest(**data)
            response_dto = service.create_expense(expense_req)
            return jsonify(response_dto.model_dump()), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return expense_bp
