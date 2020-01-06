import os
import yaml
from .factory import Factory
from .helpers import date_x_month_begins, date_x_year_begins

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.BaseLoader)

class Forecast:
    '''
    The core class for Forecast. Define process settings and kick off the process.
    '''
    def __init__(self, config_path, years=1, include_net=False):
        self.data = []
        self.accounts = {}
        self.incomes = {}
        self.expenses = {}
        self.name = os.path.basename(config_path).split('.')[0]
        self.config = read_yaml(config_path)
        self.name = self.config.get('name', 'My forecast')
        self.years = years
        self.include_net = include_net

    def create_objects(self):
        account_factory = Factory('account')
        income_factory = Factory('income')
        expense_factory = Factory('expense')
        self.add_accounts(account_factory.create(self.config['account']))
        if 'income' in self.config:
            self.add_incomes(income_factory.create(self.config['income']))
        if 'expense' in self.config:
            self.add_expenses(expense_factory.create(self.config['expense']))
        return self

    def add_accounts(self, accounts):
        for a in accounts:
            self.accounts[a.name] = a
        return self

    def add_incomes(self, incomes):
        for i in incomes:
            self.incomes[i.name] = i
        return self

    def add_expenses(self, expenses):
        for e in expenses:
            self.expenses[e.name] = e
        return self

    def get_controls(self):
        controls = []
        for i in self.incomes:
            controls.append(self.incomes[i])
        for e in self.expenses:
            controls.append(self.expenses[e])
        return controls

    def get_title(self):
        title = self.name + ' | ' + str(self.years)
        title += ' years' if self.years > 1 else ' year'
        if 'description' in self.config and self.config['description']:
            title += ' (' + self.config['description'] + ')'
        return title

    def get_total_income(self):
        total = 0
        for i in self.incomes:
            total += self.incomes[i].amount
        return round(total)

    def get_total_expense(self):
        total = 0
        for i in self.expenses:
            total += self.expenses[i].amount
        return round(total)

    def get_net_worth(self):
        balances = []
        for a in self.accounts:
            balances.append(self.accounts[a].get_balance())
        return round(sum(balances), 2)

    def get_iterations_per_year(self):
        n = 12 if self.config['mode'] == 'monthly' else 1
        return n

    def get_iteration_count(self):
        return (self.years * self.get_iterations_per_year()) + 1

    def get_iteration_date(self, i):
        if self.config['mode'] == 'monthly':
            return date_x_month_begins(i)
        return date_x_year_begins(i)

    def project(self):
        if self.data:
            return self

        self.create_objects()
        n = self.get_iterations_per_year()
        c = self.get_iteration_count()

        for i in range(0, c):
            item = {}
            date = self.get_iteration_date(i)
            item['date'] = date

            # Add the current balance
            item['balances'] = {}
            for a in self.accounts:
                balance = self.accounts[a].get_balance()
                item['balances'][a] = balance
            if self.include_net:
                item['balances']['net'] = self.get_net_worth()
            self.data.append(item)

            # Compound existing funds
            for a in self.accounts:
                self.accounts[a].compound(n)

            # Debit/credit accounts
            for c in self.get_controls():
                amounts = c.get_allocated_amounts(date)
                for a in amounts:
                    self.accounts[a].add(amounts[a])

        return self
