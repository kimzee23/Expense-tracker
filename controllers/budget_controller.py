from flask import Blueprint, request, jsonify
from dtos.request.budget_request import BudgetCreateRequest
from services.budget_service import BudgetService
from exceptions.not_found_exception import NotFoundException
from pydantic import ValidationError

def create_budget_controller(db):
    budget_controller = Blueprint("budget_controller", __name__)
    budget_service = BudgetService(db)

    @budget_controller.route("/", methods=["POST"])
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
            print("Requesting budget for user_id:", user_id)  # Debug log
            budget = budget_service.get_budget_by_user_id(user_id)
            print("Fetched budget:", budget)  # Debug log

            if not budget:
                return jsonify({"amount": 0}), 200  # Default empty budget

            return jsonify(budget), 200
        except NotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500

    @budget_controller.route("/<user_id>", methods=["DELETE"])
    def delete_budget(user_id):
        try:
            deleted = budget_service.delete_budget_by_user_id(user_id)
            if deleted:
                return jsonify({"message": "Budget deleted"}), 200
            else:
                return jsonify({"error": "No budget found for this user"}), 404
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500

    return budget_controller


