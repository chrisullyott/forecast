import os
import argparse
from app import *

# Parse arguments
parser = argparse.ArgumentParser(description='Forecast command line')
parser.add_argument('years', help='Number of years to project', type=int)
parser.add_argument('--auto-open', help='Whether to open the HTML', action='store_true')
args = parser.parse_args()

# Build forecasts
directory = os.path.join('.', 'configs')
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    forecast = Forecast(filepath, args.years, args.auto_open)
    forecast.project()
