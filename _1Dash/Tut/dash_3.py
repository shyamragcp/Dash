import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# Loading Two data sets
iris = pd.read_csv("iris.csv")
mtcars = pd.read_csv("mtcars.csv")

test_1 = iris

app = dash.Dash()

app.layout=html.Div(children=[

	html.Label("Dropdown"),
	dcc.Dropdown(
		id="data_list",
		options=[
		{"label":"iris","value":"iris"},
		{"label":"mtcars","value":"mtcars"}
		],
		value="iris"
		),
	dcc.Graph(
		id="plot_1",
		figure={
		"data" : [go.Scatter(
			x=iris.iloc[:,1],
			y=iris.iloc[:,0]
			)]
		}
		),
	dcc.Graph(
		id="plot_2",
		figure={
		"data" : [go.Scatter(
			x=mtcars.iloc[:,1],
			y=mtcars.iloc[:,0]
			)]
		}
		),
	dcc.Graph(
		id="plot_3",
		figure={
		"data" : [go.Scatter(
			x=test_1.iloc[:,1],
			y=test_1.iloc[:,0]
			)]
		}
		)

	])


app.run_server(debug=True)

