import random
from .helpers import *

class Control:
    def parse_dates(self, dates={}):
        for d in dates:
            dates[d] = parse_month_string(dates[d])
        return dates

    def build_allocations(self, data={}):
        allocations = {'default': 1}
        if 'default' in data:
            del data['default']
        for key in data:
            value = float(data[key])/100
            allocations[key] = value
            allocations['default'] -= value
        return allocations

    def is_active(self, date):
        active = True
        if 'first' in self.dates and date < self.dates['first']:
            active = False
        if 'last' in self.dates and date > self.dates['last']:
            active = False
        return active

    def get_allocated_amounts(self, date):
        amounts = {a:0 for a in self.allocations}
        if not self.is_active(date):
            return amounts
        total = self.amount
        if self.fluctuate:
            floor = 1 - self.fluctuate
            ceil = 1 + self.fluctuate
            total = self.amount * random.uniform(floor, ceil)
        for a in self.allocations:
            amounts[a] = round(total * self.allocations[a], 2)
        return amounts

class Income(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocations={}, dates={}):
        self.id = str(id)
        self.amount = float(amount)
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocations)
        self.dates = self.parse_dates(dates)

class Expense(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocations={}, dates={}):
        self.id = str(id)
        self.amount = -abs(float(amount))
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocations)
        self.dates = self.parse_dates(dates)
