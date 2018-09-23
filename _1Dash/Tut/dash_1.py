import dash
import dash_core_components as dcc
import dash_html_components as html


# App Initialisation
app = dash.Dash()

colors = {
	"background":"#008000",
	"text" : "#7FDBFF"
}

app.layout = html.Div(style={"backgroundColor":colors["background"]},children = [
	html.H1("Hello First child property",style={"textAlign":"center","color":colors["text"]}),
	html.Div(children=[
		html.H2("Division Inside a division",style={"textAlign":"center"})
		]),

	dcc.Graph(
		id = "Example.graph",
		figure = {
		"data":[
		{"x":[1,2,3],"y":[4,1,2],"type":"bar","name":"First"},
		{"x":[1,2,3],"y":[3,2,4],"type":"bar","name":"Second"}
		],
		"layout":{
		"title":"Data Visualisation"
		}
		}
		)

	])

app.run_server(debug=True)


# Why Debug is using -- So that we can change the script live. It is going to exctract



