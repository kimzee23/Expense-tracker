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


        report_data["generated_at"] = datetime.now(timezone.utc)
        report_data["start_date"] = report_data["start_date"].isoformat()
        report_data["end_date"] = report_data["end_date"].isoformat()
        print("Debug report_data", report_data)


        report_data["total_expense"] = 0
        report_data["total_budget"] = 0

        new_id = self.repo.save(report_data)
        model = Report(**report_data)

        return report_model_to_response_dto(model, new_id)
