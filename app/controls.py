from .helpers import fluctuate_amount, parse_date

class Control:
    def build_allocations(self, data=None):
        if data is None:
            data = {}
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
        if 'start' in self.dates and date < self.dates['start']:
            active = False
        if 'end' in self.dates and date >= self.dates['end']:
            active = False
        return active

    def get_allocated_amounts(self, date):
        amounts = {a:0 for a in self.allocations}
        if not self.is_active(date):
            return amounts
        total = fluctuate_amount(self.amount, self.fluctuate)
        for a in self.allocations:
            amounts[a] = round(total * self.allocations[a], 2)
        return amounts

class Income(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocations=None, dates=None):
        if allocations is None:
            allocations = {}
        if dates is None:
            dates = {}
        self.id = str(id)
        self.amount = float(amount)
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocations)
        self.dates = {d: parse_date(dates[d]) for d in dates}

class Expense(Control):
    def __init__(self, id, amount=0, fluctuate=0, allocations=None, dates=None):
        if allocations is None:
            allocations = {}
        if dates is None:
            dates = {}
        self.id = str(id)
        self.amount = -abs(float(amount))
        self.fluctuate = float(fluctuate)/100
        self.allocations = self.build_allocations(allocations)
        self.dates = {d: parse_date(dates[d]) for d in dates}
