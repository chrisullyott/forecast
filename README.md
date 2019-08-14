# forecast

Simulate personal finance projections with Python 3 and [Plotly](https://plot.ly/).

![image](image.png)

### Install dependencies

Install them all with [pip](https://pypi.org/project/pip/). You may need to use `pip3` for Python 3.

```
$ pip install -r requirements.txt
```

### Write configs

Each YAML file in `configs` is a snapshot of a hypothetical, monthly financial profile, and Forecast makes projections on each. See the sample config for details.

### Run

Forecast will build a chart and a CSV for each configuration (except sample.yml) and place these in the `output` directory.

```
$ python main.py <years> --auto-open
```
