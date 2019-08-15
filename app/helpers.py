import yaml
import random
from datetime import date
from datetime import datetime
from dateutil import relativedelta

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.BaseLoader)

def fluctuate_amount(amount, percent):
    floor = 1 - percent
    ceil = 1 + percent
    return amount * random.uniform(floor, ceil)

def parse_month_string(string):
    return datetime.strptime(string, '%m-%Y').date()

def date_this_month_began():
    return date.today().replace(day=1)

def date_next_month_begins():
    delta = relativedelta.relativedelta(months=+1)
    return (date.today() + delta).replace(day=1)

def date_x_month_begins(months):
    delta = relativedelta.relativedelta(months=months)
    return (date_this_month_began() + delta).replace(day=1)
