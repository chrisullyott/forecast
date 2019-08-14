import random

class Control:
    def build_allocations(self, data={}):
        allocations = {'default': 1}
        if 'default' in data:
            del data['default']
        for key in data:
            value = float(data[key])/100
            allocations[key] = value
            allocations['default'] -= value
        return allocations

    def get_allocated_amounts(self):
        amounts = {}
        total = self.amount
        if self.fluctuate:
            floor = 1 - self.fluctuate
            ceil = 1 + self.fluctuate
            total = self.amount * random.uniform(floor, ceil)
        for a in self.allocations:
            amounts[a] = round(total * self.allocations[a], 2)
        return amounts

class Income(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocate={}):
        self.id = str(id)
        self.amount = float(amount)
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocate)

class Expense(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocate={}):
        self.id = str(id)
        self.amount = -abs(float(amount))
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocate)
