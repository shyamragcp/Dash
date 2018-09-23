import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# Loading Two data sets
iris = pd.read_csv("iris.csv")
mtcars = pd.read_csv("mtcars.csv")

def generate_table(dataframe):
	return html.Table(
		# Header
		[html.Tr([html.Th(col) for col in dataframe.columns])]+
		# Body
		[html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(0,11)],
		style={"border":"1px","color":"black"}
		)

app = dash.Dash()

app.layout=html.Div( children = [
	html.H1(" Drop Down Example", " HI"),
	generate_table(iris)
	])

app.run_server(debug=True)
