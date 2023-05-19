from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from operations.models import Safe, Cost, CostGroup, Transactions
from datetime import date


class TestReports(TestCase):

    def setUp(self):
        self.client = Client()

    # get_cash_balance_report
    # if user doesn't have a safe
    def test_get_cash_balance_report(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        expected_balance_list = []
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has one safe without any transactions
    def test_get_cash_balance_report2(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        expected_balance_list = []
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has one safe with 1 transaction income
    def test_get_cash_balance_report3(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)

        create_cost = Cost.objects.create(name='Salary', cost_group_id=CostGroup.objects.get(name="Income"), user_id=user.pk)
        create_income = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'), group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 1000}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has one safe with 1 transaction expense
    def test_get_cash_balance_report4(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)

        create_cost = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_expense = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'), group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): (-100)}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has one safe with transactions expense and income
    def test_get_cash_balance_report5(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs_expense = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)
        create_group_costs_income = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)
        create_cost_expense = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_cost_income = Cost.objects.create(
            name='Salary', cost_group_id=CostGroup.objects.get(name="Income"), user_id=user.pk)
        create_income = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        create_expense = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 900}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has one safe with transactions 2 expense and income
    def test_get_cash_balance_report6(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs_expense = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)
        create_group_costs_income = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)
        create_cost_expense = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_cost_income = Cost.objects.create(
            name='Salary', cost_group_id=CostGroup.objects.get(name="Income"), user_id=user.pk)
        create_income = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        create_expense = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        create_expense2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=300, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 600}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

        # If user has 2 safe without any transactions

    def test_get_cash_balance_report7(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe1 = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_safe2 = Safe.objects.create(name='Privat', safe_type='Card', currency='UAH', user_id=user.pk)
        expected_balance_list = []
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

        # If user has 2 safe with 1 transaction income

    def test_get_cash_balance_report8(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe1 = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_safe2 = Safe.objects.create(name='Privat', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)

        create_cost = Cost.objects.create(name='Salary', cost_group_id=CostGroup.objects.get(name="Income"),
                                          user_id=user.pk)
        create_income = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 1000}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has 2 safe with 1 transaction expense
    def test_get_cash_balance_report9(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe1 = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_safe2 = Safe.objects.create(name='Privat', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)

        create_cost = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_expense1 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        create_expense = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=50, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): (-100)},
                                 {Safe.objects.get(name='Privat'): (-50)}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has 2 safe with  transaction expense and income
    def test_get_cash_balance_report10(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe1 = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_safe2 = Safe.objects.create(name='Privat', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs_expense = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)
        create_cost_expense = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_group_costs_income = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)
        create_cost_income = Cost.objects.create(
            name='Salary', cost_group_id=CostGroup.objects.get(name="Income"), user_id=user.pk)
        create_income1 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        create_income2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=10000, user_id=user.pk)
        create_expense1 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        create_expense2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=50, user_id=user.pk)
        create_expense2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=500, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 900},
                                 {Safe.objects.get(name='Privat'): 9450}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)

    # If user has 2 safe with  transaction expense and income different period
    def test_get_cash_balance_report11(self):
        user = User.objects.create_user(username='Alex', password='123')
        self.client.login(username='Alex', password='123')
        create_safe1 = Safe.objects.create(name='Monobank', safe_type='Card', currency='UAH', user_id=user.pk)
        create_safe2 = Safe.objects.create(name='Privat', safe_type='Card', currency='UAH', user_id=user.pk)
        create_group_costs_expense = CostGroup.objects.create(name='Food', type_group=0, user_id=user.pk)
        create_cost_expense = Cost.objects.create(
            name='Fruits', cost_group_id=CostGroup.objects.get(name="Food"), user_id=user.pk)
        create_group_costs_income = CostGroup.objects.create(name='Income', type_group=1, user_id=user.pk)
        create_cost_income = Cost.objects.create(
            name='Salary', cost_group_id=CostGroup.objects.get(name="Income"), user_id=user.pk)
        create_income1 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=1000, user_id=user.pk)
        create_income2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Income"),
            cost_id=Cost.objects.get(name='Salary'), sum_transactions=10000, user_id=user.pk)
        create_expense1 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Monobank'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=100, user_id=user.pk)
        create_expense2 = Transactions.objects.create(
            date=date(2023, 5, 15), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=50, user_id=user.pk)
        create_expense2 = Transactions.objects.create(
            date=date(2023, 5, 19), safe_id=Safe.objects.get(name='Privat'),
            group_id=CostGroup.objects.get(name="Food"),
            cost_id=Cost.objects.get(name='Fruits'), sum_transactions=500, user_id=user.pk)
        expected_balance_list = [{Safe.objects.get(name='Monobank'): 900},
                                 {Safe.objects.get(name='Privat'): 9450}]
        response = self.client.get('/reports/balance/')
        self.assertListEqual(response.context['total_balance_list'], expected_balance_list)
