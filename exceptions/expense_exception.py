class ExpenseNotFound(Exception):
    def __init__(self, expense_id: str):
        self.message = f"Expense with id {expense_id} was not found"
        super().__init__(self.message)


class InvalidExpenseException(Exception):
    def __init__(self, reason: str = "Invalid Expense data"):
        self.message = reason
        super().__init__(self.message)