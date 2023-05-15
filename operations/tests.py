from django.test import TestCase
from django.test import Client
from operations.models import Safe, Cost, CostGroup, Transactions


class TestOperations(TestCase):
    fixtures = ['fixture_db.json']

    def setUp(self):
        self.client = Client()
        self.safe_id = 4
        self.group_cost_id = 15
        self.income_group_cost = 1
        self.income_cost = 1
        self.expense_cost = 27
        self.income_id = 1
        self.expense_id = 5

    def test_create_safe(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post('/operations/safe/', {'name': 'A-bank', 'safe_type': 'Card', 'currency': 'UAH'})
        self.assertEqual(response.status_code, 200)
        safe = Safe.objects.filter(name='A-bank')
        self.assertEqual(len(safe), 1)

    def test_delete_safe(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post(f"/operations/safe/{self.safe_id}/", {'id': self.safe_id})
        self.assertEqual(response.status_code, 302)
        safe = Safe.objects.filter(id=self.safe_id)
        self.assertFalse(safe.exists())

    def test_create_group_cost(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post('/operations/group_cost/', {'name': 'Traveling', 'type_group': '0'})
        self.assertEqual(response.status_code, 200)
        group_cost = CostGroup.objects.filter(name='Traveling')
        self.assertEqual(len(group_cost), 1)

    def test_create_cost(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post('/operations/cost/', {'name': 'Tickets',
                                                          'cost_group_id': self.group_cost_id})
        self.assertEqual(response.status_code, 200)
        cost = Cost.objects.filter(name='Tickets', cost_group_id=self.group_cost_id)
        self.assertEqual(len(cost), 1)

    def test_delete_cost(self):
        self.client.login(username='Alex', password='123')
        cost_id = 4
        response = self.client.post(f"/operations/cost/{cost_id}/", {'id': cost_id})
        self.assertEqual(response.status_code, 302)
        cost = Cost.objects.filter(id=cost_id)
        self.assertFalse(cost.exists())

    def test_get_costs(self):
        self.client.login(username='Alex', password='123')
        response = self.client.get('/operations/get_costs/', {'cost_group_id': self.group_cost_id})
        self.assertEqual(response.status_code, 200)
        result = Cost.objects.filter(cost_group_id=self.group_cost_id)
        result_list = [{'id': cost.id, 'name': cost.name, 'cost_group_id': self.group_cost_id} for cost in result]
        expected_result = [{'id': 27, 'name': "Step aerobics", "cost_group_id": 15}]
        self.assertListEqual(result_list, expected_result)

    def test_create_income(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post('/operations/income/', {'date': '2023-05-15', 'safe_id': self.safe_id,
                                                            'group_id': self.income_group_cost,
                                                            'cost_id': self.income_cost,
                                                            'sum': 1000
                                                            })
        self.assertEqual(response.status_code, 200)
        income = Transactions.objects.filter(cost_id=self.income_cost, date='2023-05-15')
        self.assertEqual(len(income), 1)

    def test_delete_income(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post(f"/operations/income/{self.income_id}/", {'id': self.income_id})
        self.assertEqual(response.status_code, 302)
        income = Transactions.objects.filter(id=self.income_id)
        self.assertFalse(income.exists())

    def test_create_expense(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post('/operations/expense/', {'date': '2023-05-15', 'safe_id': self.safe_id,
                                                             'group_id': self.group_cost_id,
                                                             'cost_id': self.expense_cost,
                                                             'sum': 100
                                                             })
        self.assertEqual(response.status_code, 200)
        expense = Transactions.objects.filter(cost_id=self.expense_cost, date='2023-05-15', sum_transactions=100)
        self.assertEqual(len(expense), 1)

    def test_delete_expense(self):
        self.client.login(username='Alex', password='123')
        response = self.client.post(f"/operations/expense/{self.expense_id}/", {'id': self.expense_id})
        self.assertEqual(response.status_code, 302)
        expense = Transactions.objects.filter(id=self.expense_id)
        self.assertFalse(expense.exists())

