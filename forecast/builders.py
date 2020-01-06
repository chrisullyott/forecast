import os
import csv
import plotly.graph_objects as go

class Builder:
    '''
    Generates forecast output. Can take several forms, like a spreadsheet or a graph.

    Variables:
        output_dir {str} -- The directory to place static files.
    '''
    output_dir = 'output'

    def create_file_dir(self, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def format_usd(self, number):
        return '${:,.2f}'.format(number)

class CsvBuilder(Builder):
    def __init__(self, forecast):
        self.forecast = forecast

    def get_rows(self):
        rows = []
        for item in self.forecast.data:
            row = {}
            row['date'] = item['date'].isoformat()
            for balance in item['balances']:
                row[balance] = self.format_usd(item['balances'][balance])
            rows.append(row)
        return rows

    def build(self):
        filename = self.forecast.filename + '.csv'
        filepath = os.path.join('.', self.output_dir, filename)
        self.create_file_dir(filepath)

        rows = self.get_rows()
        with open(filepath, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        return self

class PlotBuilder(Builder):
    def __init__(self, forecast):
        self.forecast = forecast

    def build(self, auto_open=False):
        dates = []
        balances = {}
        for item in self.forecast.data:
            dates.append(item['date'])
            for a in item['balances']:
                if a not in balances:
                    balances[a] = []
                balances[a].append(item['balances'][a])

        fig = go.Figure()
        mode = 'lines+markers' if self.forecast.years < 4 else 'lines'
        for a in balances:
            fig.add_trace(go.Scatter(name=a, mode=mode, x=dates, y=balances[a]))
        fig.update_layout(title=self.forecast.get_title())

        filename = self.forecast.filename + '.html'
        filepath = os.path.join('.', self.output_dir, filename)
        self.create_file_dir(filepath)

        return fig.write_html(filepath, auto_open=auto_open)
