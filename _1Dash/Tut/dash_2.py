# Scatter Plot.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

app = dash.Dash()

app.layout = html.Div(children = [
	html.H1("IRIS Dataset",style = {"textAlign":"center"}),

	dcc.Graph(
		id="plot_1",
		figure = {
		"data" : [
		go.Scatter(
			x=df[df['continent'] == i]['gdp per capita'],
			y=df[df['continent'] == i]['life expectancy'],
			text=df[df['continent'] == i]['country'],
			mode='markers',
			opacity=0.7,
			marker={"size":15},
			name=i
			) for i in df.continent.unique()
		],
		"layout":go.Layout(
			xaxis={"title":"GDP Per Capita"},
			yaxis={"title":"Life Expectancy"}
			)
		}

		)
	])



app.run_server(debug=True)

