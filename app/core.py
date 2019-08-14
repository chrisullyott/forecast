import os
import yaml
import plotly.graph_objects as go
from .factory import *
from .helpers import *

class Forecast:
    config = {}
    accounts = {}
    incomes = {}
    expenses = {}

    def __init__(self, config_path, years=1, auto_open=False):
        self.config_path = config_path
        with open(config_path, 'r') as file:
            self.config = yaml.load(file, Loader=yaml.BaseLoader)
        self.years = years
        self.auto_open = auto_open
        self.id = os.path.basename(config_path).split('.')[0]
        self.name = self.config.get('name', 'My forecast')
        self.create_objects()

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

    def run_control(self, control, iteration):
        amounts = control.get_allocated_amounts()
        for a in amounts:
            self.accounts[a].add(amounts[a])

    def get_title(self):
        title = self.name + ' | ' + str(self.years) + ' years '
        title += '(' + self.get_description() + ')'
        return title

    def get_description(self):
        income = '$' + str(self.get_total_income())
        expense = '$' + str(abs(self.get_total_expense()))
        return income + ' in income, ' + expense + ' in expenses monthly'

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

    def build_data(self):
        data = {'dates':[], 'net_balance':[], 'balances':{}}

        for i in range(0, self.years * 12):
            date = date_x_month_begins(i)
            data['dates'].append(date)
            for a in self.accounts:
                self.accounts[a].compound()
            for c in self.get_controls():
                self.run_control(c, i)
            for a in self.accounts:
                balance = self.accounts[a].get_balance()
                if a not in data['balances']:
                    data['balances'][a] = []
                data['balances'][a].append(balance)

        return data

    def build_plot(self, data):
        output_dir = os.path.join('.', 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            name='net_balance',
            x=data['dates'],
            y=data['net_balance']
        ))

        for a in data['balances']:
            fig.add_trace(go.Scatter(
                name=a,
                x=data['dates'],
                y=data['balances'][a]
            ))

        fig.update_layout(title=self.get_title())

        return fig.write_html(
            os.path.join(output_dir, self.id + '.html'),
            auto_open=self.auto_open
        )

    def project(self):
        return self.build_plot(self.build_data())
