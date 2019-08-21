import os
import argparse
from app import *

# Parse arguments
parser = argparse.ArgumentParser(description='Forecast command line')
parser.add_argument('years', help='Number of years to project', type=int)
parser.add_argument('--auto-open', help='Whether to open the HTML', action='store_true')
parser.add_argument('--include-net', help='Whether to include net worth', action='store_true')
args = parser.parse_args()

# Build forecasts
directory = os.path.join('.', 'configs')
for filename in os.listdir(directory):
    extension = os.path.splitext(filename)[1][1:]
    if extension != 'yml' or filename == 'sample.yml': continue
    filepath = os.path.join(directory, filename)
    forecast = Forecast(filepath, args.years, args.include_net).project()
    PlotBuilder(forecast).build(args.auto_open)
    CsvBuilder(forecast).build()
