from flask import Blueprint, request, jsonify
from dtos.request.request_report import ReportCreateRequest
from services.report_service import ReportService
from repositories.report_repository import ReportRepository
from utils.mapper.mapper_report import document_to_report_model_dto, report_model_to_response_dto
from pydantic import ValidationError

def create_report_controller(db):
    report_bp = Blueprint('report_controller', __name__)
    repo = ReportRepository(db)
    service = ReportService(repo)

    @report_bp.route("/", methods=["POST"])
    def create_report():
        try:
            data = request.get_json()
            report_req = ReportCreateRequest(**data)
            response_dto = service.create_report(report_req)
            return jsonify(response_dto.model_dump()), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return report_bp
