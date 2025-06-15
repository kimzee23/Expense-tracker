from dtos.request.request_report import ReportCreateRequest
from repositories.report_repository import ReportRepository
from utils.mapper.mapper_report import report_model_to_response_dto
from models.report_model import Report
from datetime import datetime, timezone

class ReportService:
    def __init__(self, repo: ReportRepository):
        self.repo = repo

    def create_report(self, request_dto: ReportCreateRequest):
        report_data = request_dto.model_dump()

        report_data["generated_at"] = datetime.now(timezone.utc).isoformat()

        # Leave start_date and end_date as strings (they are valid ISO strings)
        # If you do want datetime objects, parse them first

        new_id = self.repo.save(report_data)
        model = Report(**report_data)

        return report_model_to_response_dto(model, new_id)
