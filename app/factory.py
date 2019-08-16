from .accounts import *
from .controls import *

class Factory:
    def __init__(self, type):
        self.type = type

    def create_account(self, item):
        return Account(
            item.get('id'),
            item.get('initial_balance', 0),
            item.get('annual_return', 0))

    def create_income(self, item):
        return Income(
            item.get('id'),
            item.get('amount', 0),
            item.get('fluctuate', 0),
            item.get('allocations', {}),
            item.get('dates', {}))

    def create_expense(self, item):
        return Expense(
            item.get('id'),
            item.get('amount', 0),
            item.get('fluctuate', 0),
            item.get('allocations', {}),
            item.get('dates', {}))

    def create_instance(self, item):
        return getattr(self, 'create_' + self.type)(item)

    def create(self, data):
        objects = []
        for item in data:
            obj = self.create_instance(item)
            objects.append(obj)
        return objects
