from flask import Blueprint, request, jsonify
from dtos.request.budget_request import BudgetCreateRequest
from services.budget_service import BudgetService
from exceptions.not_found_exception import NotFoundException
from pydantic import ValidationError

def create_budget_controller(db):
    budget_controller = Blueprint("budget_controller", __name__)
    budget_service = BudgetService(db)

    @budget_controller.route("", methods=["POST"])
    def create_budget():
        try:
            data = request.get_json()
            request_dto = BudgetCreateRequest(**data)
            result = budget_service.create_budget(request_dto)
            return jsonify({"message": "Budget saved", "result": result}), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500

    @budget_controller.route("/<user_id>", methods=["GET"])
    def get_budget_by_user_id(user_id):
        try:
            budget = budget_service.get_budget_by_user_id(user_id)
            return jsonify(budget), 200
        except NotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500

    return budget_controller
