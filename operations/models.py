import datetime
from django.db import models


class Safe(models.Model):
    SAFE_TYPE = (
        ('Cash', 'C1'),
        ('Card', 'C2'),
        ('Cryptocurrency', 'C3')
    )
    CURRENCY = (
        ('UAH', 980),
        ('USD', 840),
        ('EUR', 978),
        ('GBP', 826),
        ('PLN', 985),
        ('CNY', 156),
        ('JPY', 392),
        ('CHF', 756),
        ('CZK', 203)
    )
    name = models.CharField(max_length=100)
    safe_type = models.CharField(choices=SAFE_TYPE, max_length=15)
    currency = models.CharField(choices=CURRENCY, max_length=3)
    user_id = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.safe_type} {self.currency}'


class CostGroup(models.Model):
    TYPE_GROUP = [(0, 'expense'), (1, 'income')]
    name = models.CharField(max_length=100)
    type_group = models.IntegerField(choices=TYPE_GROUP, default=0)
    user_id = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.type_group}'


class Cost(models.Model):
    name = models.CharField(max_length=100)
    cost_group_id = models.ForeignKey(CostGroup, on_delete=models.CASCADE)
    user_id = models.IntegerField()

    def __str__(self):
        return f'{self.cost_group_id.name} {self.name}'


class Transactions(models.Model):
    date = models.DateField(default=datetime.date.today)
    safe_id = models.ForeignKey(Safe, on_delete=models.CASCADE)
    group_id = models.ForeignKey(CostGroup, on_delete=models.CASCADE)
    cost_id = models.ForeignKey(Cost, on_delete=models.CASCADE)
    sum_transactions = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return f'{self.date} {self.safe_id.name} {self.group_id.name} {self.cost_id.name} {self.sum_transactions}'
