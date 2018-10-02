import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
	html.Label("Drop Down",style={"textAlign":"left"}),
	dcc.Dropdown(
		options=[
		{"label":"Kannur","value":"KNR"},
		{"label":"Calicut","value":"CLT"},
		{"label":"Bangaluru","value":"BGLR"}
		],value="KNR",style={"width":"48%","float":"left"}
		),

	html.Label("Multi Select Drop Down",style={"textAlign":"left"}),
	dcc.Dropdown(
		options=[
		{"label":"Kannur","value":"KNR"},
		{"label":"Calicut","value":"CLT"},
		{"label":"Bangaluru","value":"BGLR"}
		],value="KNR",style={"width":"48%","float":"right"},
		multi=True
		),
	html.Label("Radio Buttons"),
	dcc.RadioItems(
		options=[{"label":"Kannur","value":"KNR"},
		{"label":"Calicut","value":"CLT"},
		{"label":"Bangaluru","value":"BGLR"}], value="KNR"
		),
	html.Label("Check Boxes"),
	dcc.Checklist(
		options=[{"label":"Kannur","value":"KNR"},
		{"label":"Calicut","value":"CLT"},
		{"label":"Bangaluru","value":"BGLR"}], values=["KNR","CLT"]
		),
	html.Label("Text Input"),
	dcc.Input(id="my-id",value="MTL",type="text"),
	html.Div(id="my-div"),
	html.Label("Slider"),
	dcc.Slider(min=0,max=10,value=5,marks=list(range(0,10)))

	])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

app.run_server(debug=True)

print("It worked")

