import os
import yaml
from .factory import *
from .helpers import *

class Forecast:
    config = {}
    accounts = {}
    incomes = {}
    expenses = {}

    def __init__(self, config_path, years=1, include_net=False):
        self.data = []
        self.config_path = config_path
        with open(config_path, 'r') as file:
            self.config = yaml.load(file, Loader=yaml.BaseLoader)
        self.years = years
        self.id = os.path.basename(config_path).split('.')[0]
        self.name = self.config.get('name', 'My forecast')
        self.include_net = include_net

    def create_objects(self):
        account_factory = Factory('account')
        income_factory = Factory('income')
        expense_factory = Factory('expense')
        self.add_accounts(account_factory.create(self.config['account']))
        self.add_incomes(income_factory.create(self.config['income']))
        self.add_expenses(expense_factory.create(self.config['expense']))
        return self

    def add_accounts(self, accounts):
        for a in accounts:
            self.accounts[a.id] = a
        return self

    def add_incomes(self, incomes):
        for i in incomes:
            self.incomes[i.id] = i
        return self

    def add_expenses(self, expenses):
        for e in expenses:
            self.expenses[e.id] = e
        return self

    def get_controls(self):
        controls = []
        for i in self.incomes:
            controls.append(self.incomes[i])
        for e in self.expenses:
            controls.append(self.expenses[e])
        return controls

    def get_title(self):
        title = self.name + ' | ' + str(self.years) + ' years '
        if 'description' in self.config and self.config['description']:
            title += '(' + self.config['description'] + ')'
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
        return round(sum(balances),2)

    def project(self):
        if self.data:
            return self

        self.create_objects()

        for i in range(0, self.years * 12):
            # Get date
            item = {}
            date = date_x_month_begins(i)
            item['date'] = date

            # Run controls
            for a in self.accounts:
                self.accounts[a].compound()
            for c in self.get_controls():
                amounts = c.get_allocated_amounts(date)
                for a in amounts:
                    self.accounts[a].add(amounts[a])

            # Get balances
            item['balances'] = {}
            for a in self.accounts:
                balance = self.accounts[a].get_balance()
                item['balances'][a] = balance
            if self.include_net:
                item['balances']['net'] = self.get_net_worth()
            self.data.append(item)

        return self

