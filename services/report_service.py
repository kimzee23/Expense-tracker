from _pydatetime import timezone
from datetime import datetime
from collections import defaultdict

from dtos.request.request_report import ReportCreateRequest
from models.report_model import Report
from repositories.report_repository import ReportRepository
from utils.mapper.mapper_report import report_model_to_response_dto


class ReportService:
    def __init__(self, repo: ReportRepository):
        self.repo = repo

    def create_report(self, request_dto: ReportCreateRequest):
        report_data = request_dto.model_dump()
        report_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        new_id = self.repo.save(report_data)
        model = Report(**report_data)
        return report_model_to_response_dto(model, new_id)

    def generate_report(self, user_id: str):
        expenses = self.repo.get_expenses_by_user_id(user_id)

        total_expense = sum(e["amount"] for e in expenses)
        recent_expenses = sorted(expenses, key=lambda e: e["date"], reverse=True)[:5]

        expenses_by_date = defaultdict(float)
        expenses_by_category = defaultdict(float)
        expenses_by_hour = defaultdict(float)

        for e in expenses:
            date_val = e.get("date")


            if isinstance(date_val, str):
                dt = datetime.fromisoformat(date_val)
            elif isinstance(date_val, datetime):
                dt = date_val
            else:
                continue
            date_str = dt.strftime("%Y-%m-%d")
            hour = dt.hour

            amount = e.get("amount", 0)
            category = e.get("category", "Uncategorized")

            expenses_by_date[date_str] += amount
            expenses_by_hour[hour] += amount
            expenses_by_category[category] += amount

        return {
            "total_expense": total_expense,
            "recent_expenses": [
                {
                    **e,
                    "_id": str(e["_id"]) if "_id" in e else None
                } for e in recent_expenses
            ],

            "expenses_by_date": [{"date": k, "total": v} for k, v in expenses_by_date.items()],
            "expenses_by_category": dict(expenses_by_category),
            "expenses_by_hour": [{"hour": k, "total": v} for k, v in expenses_by_hour.items()],
        }
