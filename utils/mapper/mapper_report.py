from datetime import datetime

from models.report_model import Report
from dtos.response.response_report import ReportResponse

def document_to_report_model_dto(doc):
    return Report(**doc)

def report_model_to_response_dto(model: Report, report_id: str) -> dict:
    def to_iso(value):
        return value.isoformat() if isinstance(value, datetime) else value

    return {
        "id": report_id,
        "user_id": model.user_id,
        "title": model.title,
        "description": model.description,
        "start_date": to_iso(model.start_date),
        "end_date": to_iso(model.end_date),
        "total_budget": model.total_budget,
        "total_expense": model.total_expense,
        "total_income": model.total_income,
        "generated_at": to_iso(model.generated_at),
    }
