import unittest
from unittest.mock import MagicMock
from services.expanse_service import ExpenseService
from dtos.request.expense_request import ExpenseUpdateRequest
from exceptions.expense_exception import ExpenseNotFound

class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.repo_mock = MagicMock()
        self.service = ExpenseService(self.repo_mock)

    def test_update_expense_success(self):

        expense_id = "123"
        request = ExpenseUpdateRequest(title="Updated Title", amount=200)
        self.repo_mock.update_expense.return_value = True


        result = self.service.update_expense(expense_id, request)


        self.assertTrue(result)
        self.repo_mock.update_expense.assert_called_once_with(
            expense_id, {"title": "Updated Title", "amount": 200}
        )

    def test_update_expense_with_no_changes(self):

        expense_id = "123"
        request = ExpenseUpdateRequest(title=None, amount=None)


        result = self.service.update_expense(expense_id, request)

        self.assertFalse(result)
        self.repo_mock.update_expense.assert_not_called()

    def test_update_expense_not_found(self):

        expense_id = "Id_not_found"
        request = ExpenseUpdateRequest(title="New Title")
        self.repo_mock.update_expense.return_value = False


        with self.assertRaises(ExpenseNotFound):
            self.service.update_expense(expense_id, request)

if __name__ == '__main__':
    unittest.main()
