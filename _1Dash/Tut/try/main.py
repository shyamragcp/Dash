import pandas as pd
import numpy as np
import datetime
import calendar
from collections import Counter

# Getting Data.
def get_data():
	df = pd.read_csv("full_data.csv")
	return	df

###################
# Data Cleaning ###
###################

def picking_valid_Data(df):
	final = df.loc[df.Status.isna() == False,]
	final = final.loc[df["Application Completion time"].isna() == False,]
	final["Borrower Industry"].fillna("Other",inplace=True)
	final["Residential status"].fillna("Other",inplace=True)
	final["Education Level"].fillna("NotMentioned",inplace=True)
	final["CL Purpose: Name"].fillna("Other",inplace=True)
	return final



########################################
# Deriving Time stamp, Organizing and Sorting ##
########################################

def time_stamp(final,date_column,new_column):
	final[date_column] = pd.to_datetime(final[date_column])
	final[new_column+"Year"]=[x.year for x in final[date_column]]
	final[new_column+"Month"]=[x.month for x in final[date_column]]
	final.sort_values([new_column+"Year",new_column+"Month"],inplace=True)
	final[new_column+"Time"] = [calendar.month_abbr[int(x)] for x in final[new_column+"Month"]]
	final["Time Stamp"] =  final[new_column+"Time"].map(str)+" "+ final[new_column+"Year"].map(str)
	return final

###  Bucketing Numeric Types.
def age_cut(final):
	final["Age_bin"] = pd.cut(final["Age"],[21,26,31,36,41,45,115],right=False,labels=["21-25","26-30","31-35","36-40","41-45","> 45"])
	return final

def income_cut(final):
	final["Net Income"]= pd.cut(final["Salary Income-current month"],[0,15001,20001,25001,30001,40001,50001,60001,70001,80001,90001,100001,110001,120001,130001,140001,150001,10000000000],
		right=False,labels=["Below 15,000","15,001  - 20,000","20,001 - 25,000","25,001 - 30,000","30,001 - 40,000","40,001 - 50,000","50,001 - 60,000","60,001 - 70,000","70,001 - 80,000","80,001 - 90,000","90,001 - 100,000","100,001 - 110,000","110,001 - 120,000","120,001 - 130,000","130,001 - 140,000","140,001 - 150,000",">150,000"])
	return final

def bureau_score(final):
	final.loc[final["CRIF S1 Score"].isna(),"Bureau Score"] = "No-Hit"
	final.loc[(final["CRIF S1 Score"]<300),"Bureau Score"] = "<300"
	final.loc[(final["CRIF S1 Score"]==300),"Bureau Score"] = "300"
	final.loc[(final["CRIF S1 Score"]>=301) & (final["CRIF S1 Score"]<=560),"Bureau Score"] = "301 to 560"
	final.loc[(final["CRIF S1 Score"]>=561) & (final["CRIF S1 Score"]<=600),"Bureau Score"] = "561 to 600"
	final.loc[(final["CRIF S1 Score"]>=601) & (final["CRIF S1 Score"]<=625),"Bureau Score"] = "601 to 625"
	final.loc[(final["CRIF S1 Score"]>=626) & (final["CRIF S1 Score"]<=650),"Bureau Score"] = "626 to 650"
	final.loc[(final["CRIF S1 Score"]>=651) & (final["CRIF S1 Score"]<=675),"Bureau Score"] = "651 to 675"
	final.loc[(final["CRIF S1 Score"]>=676) & (final["CRIF S1 Score"]<=700),"Bureau Score"] = "676 to 700"
	final.loc[(final["CRIF S1 Score"]>=701) & (final["CRIF S1 Score"]<=725),"Bureau Score"] = "701 to 725"
	final.loc[(final["CRIF S1 Score"]>=726) & (final["CRIF S1 Score"]<=750),"Bureau Score"] = "726 to 750"
	final.loc[(final["CRIF S1 Score"]>=751) & (final["CRIF S1 Score"]<=775),"Bureau Score"] = "751 to 775"
	final.loc[(final["CRIF S1 Score"]>=776) & (final["CRIF S1 Score"]<=800),"Bureau Score"] = "776 to 800"
	final.loc[(final["CRIF S1 Score"]>800) ,"Bureau Score"] = ">800"
	return final

def loan_amount(final):
	final["No_App_Loan_Amount"] = pd.cut(final["Requested loan amount"],[50000,75001,100001,125001,150001,200001,250001,300001,350001,400001,450001,500001],right=False,
		labels=["50,000 to 75,000","75,001 to 100,000","100,001 to 125,000","125,001 to 150,000","150,001 to 200,000","200,001 to 250,000","250,001 to 300,000","300,001 to 350,000","350,001 to 400,000","400,001 to 450,000","450,001 to 500,000"]	)
	return	final

# requested 


#######################
# Counter function ####  Main iteration
#######################

# c_var -- variable to be counted

def freq_counter(c_var):
	c=Counter(c_var["Time Stamp"])
	freq_data = pd.DataFrame({"Month":[str(x) for x in c.keys()],
		"Count":[int(x) for x in c.values()]})
	return	freq_data

### Filter Function for filtering Data Frames
def filter_new_df(master_df,col_name,col_val):
	df = master_df.loc[master_df[col_name]==col_val,]
	return df

### Important Variables for analysis
### Use this list for later analysis.
def variable_selection():
	var_list=["Gender","Age_bin","Net Income","Bureau Score","Borrower Industry","No_App_Loan_Amount","Marital status","Residential status",
	"No of dependents","Education Level","CL Purpose: Name","Monexo Rating"]
	return var_list

# Created to get the list of categories available in the variable.
def var_cat_dict(df,col_name,dict_word):
	col_name = list(set(df[col_name]))
	var_dict[dict_word] = col_name

### Printing table
def print_df(df):
	print(df.head())


##############
### Main #####
##############

def main():
	df = get_data()
	final = picking_valid_Data(df)
	final = time_stamp(final,"Application Completion time",new_column="app_")
	final = age_cut(final)
	final = income_cut(final)
	final = bureau_score(final)
	final = loan_amount(final)

# Variable List Calling
	var_list = variable_selection()

# Dictionary preparation for Total Level.
	for x in var_list:
		var_cat_dict(final,x,x)

##########################################
########## Tables Generating #############
##########################################

# Counting for individual variables.
	tot_freq = freq_counter(final)
	# print(tot_freq)
	tot_dict["total"] = tot_freq
	
	# Making Separate Data Frame for Approve and Reject
	approved_final = filter_new_df(final,"Status","LISTED IN MARKETPLACE")
	Rejected_final = filter_new_df(final,"Status","REJECTED")

	tot_freq = freq_counter(approved_final)
	tot_dict["Approved Total"] = tot_freq

	tot_freq = freq_counter(Rejected_final)
	tot_dict["Rejected Total"] = tot_freq

	for x,y in var_dict.items():
		for z in y:
			app_df_dict[str(z).replace("/","")+"final"] = filter_new_df(final,x,z)
			# print(app_df_dict[z+"final"].info())
			app_df_dict_frq[str(z).replace("/","")+"freq"] = freq_counter(app_df_dict[str(z).replace("/","")+"final"])
			# print("\n",app_df_dict_frq[z+"freq"])

# Approved Cases
	for x,y in var_dict.items():
		for z in y:
			Aprvd_app_df_dict[str(z).replace("/","")+"final"] = filter_new_df(approved_final,x,z)
			Aprvd_app_df_dict_frq[str(z).replace("/","")+"freq"] = freq_counter(Aprvd_app_df_dict[str(z).replace("/","")+"final"])

# Rejected Cases
	for x,y in var_dict.items():
		for z in y:
			Reject_app_df_dict[str(z).replace("/","")+"final"] = filter_new_df(Rejected_final,x,z)
			Reject_app_df_dict_frq[str(z).replace("/","")+"freq"] = freq_counter(Reject_app_df_dict[str(z).replace("/","")+"final"])


##################################################################
##################################################################
##################################################################

# Calling Functions.
app_df_dict = dict()  ## -- For collecting DataFrame.
app_df_dict_frq = dict()  ## Frequency count for individual DataFrame.
var_dict = dict() ## -- This dictionary is for Total level.
tot_dict = dict() ## -- Can be used as a bench mark

Aprvd_app_df_dict = dict()  ## -- For collecting DataFrame.
Aprvd_app_df_dict_frq = dict()  ## Frequency count for individual DataFrame.

Reject_app_df_dict = dict()  ## -- For collecting DataFrame.
Reject_app_df_dict_frq = dict()  ## Frequency count for individual DataFrame.

main()



###################################
# App initialisation
###################################

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()

# main()

app.layout = html.Div(children=[
	html.H1("Application MIS (Only for Completed Application)",style={"textAlign":"center"}),
	html.H2(children = "Gender",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_1",
		figure = {
		"data" : [
		# go.Scatter(x=tot_dict["total"].Month,y=tot_dict["total"].Count,mode="lines"),
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		# [go.Scatter(
		# 	x=app_df_dict_frq[str(i)+"freq"].Month,
		# 	y=app_df_dict_frq[str(i)+"freq"].Count,
		# 	mode = "lines",
		# 	name =i) for i in var_dict["Gender"]]
		{"x":app_df_dict_frq["Male"+"freq"].Month,"y": app_df_dict_frq["Male"+"freq"].Count,"type":"line","name":"Male"},
		{"x":app_df_dict_frq["Female"+"freq"].Month,"y": app_df_dict_frq["Female"+"freq"].Count,"type":"line","name":"Female"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Age",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_2",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["21-25"+"freq"].Month,"y": app_df_dict_frq["21-25"+"freq"].Count,"type":"line","name":"21-25"},
		{"x":app_df_dict_frq["26-30"+"freq"].Month,"y": app_df_dict_frq["26-30"+"freq"].Count,"type":"line","name":"26-30"},
		{"x":app_df_dict_frq["31-35"+"freq"].Month,"y": app_df_dict_frq["31-35"+"freq"].Count,"type":"line","name":"31-35"},
		{"x":app_df_dict_frq["36-40"+"freq"].Month,"y": app_df_dict_frq["36-40"+"freq"].Count,"type":"line","name":"36-40"},
		{"x":app_df_dict_frq["41-45"+"freq"].Month,"y": app_df_dict_frq["41-45"+"freq"].Count,"type":"line","name":"41-45"},
		{"x":app_df_dict_frq["> 45"+"freq"].Month,"y": app_df_dict_frq["> 45"+"freq"].Count,"type":"line","name":"> 45"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Net Income",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_3",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["Below 15,000"+"freq"].Month,"y": app_df_dict_frq["Below 15,000"+"freq"].Count,"type":"line","name":"Below 15,000"},
		{"x":app_df_dict_frq["15,001  - 20,000"+"freq"].Month,"y": app_df_dict_frq["15,001  - 20,000"+"freq"].Count,"type":"line","name":"15,001  - 20,000"},
		{"x":app_df_dict_frq["20,001 - 25,000"+"freq"].Month,"y": app_df_dict_frq["20,001 - 25,000"+"freq"].Count,"type":"line","name":"20,001 - 25,000"},
		{"x":app_df_dict_frq["25,001 - 30,000"+"freq"].Month,"y": app_df_dict_frq["25,001 - 30,000"+"freq"].Count,"type":"line","name":"25,001 - 30,000"},
		{"x":app_df_dict_frq["30,001 - 40,000"+"freq"].Month,"y": app_df_dict_frq["30,001 - 40,000"+"freq"].Count,"type":"line","name":"30,001 - 40,000"},
		{"x":app_df_dict_frq["40,001 - 50,000"+"freq"].Month,"y": app_df_dict_frq["40,001 - 50,000"+"freq"].Count,"type":"line","name":"40,001 - 50,000"},
		{"x":app_df_dict_frq["50,001 - 60,000"+"freq"].Month,"y": app_df_dict_frq["50,001 - 60,000"+"freq"].Count,"type":"line","name":"50,001 - 60,000"},
		{"x":app_df_dict_frq["60,001 - 70,000"+"freq"].Month,"y": app_df_dict_frq["60,001 - 70,000"+"freq"].Count,"type":"line","name":"60,001 - 70,000"},
		{"x":app_df_dict_frq["70,001 - 80,000"+"freq"].Month,"y": app_df_dict_frq["70,001 - 80,000"+"freq"].Count,"type":"line","name":"70,001 - 80,000"},
		{"x":app_df_dict_frq["80,001 - 90,000"+"freq"].Month,"y": app_df_dict_frq["80,001 - 90,000"+"freq"].Count,"type":"line","name":"80,001 - 90,000"},
		{"x":app_df_dict_frq["90,001 - 100,000"+"freq"].Month,"y": app_df_dict_frq["90,001 - 100,000"+"freq"].Count,"type":"line","name":"90,001 - 100,000"},
		{"x":app_df_dict_frq["100,001 - 110,000"+"freq"].Month,"y": app_df_dict_frq["100,001 - 110,000"+"freq"].Count,"type":"line","name":"100,001 - 110,000"},
		{"x":app_df_dict_frq["110,001 - 120,000"+"freq"].Month,"y": app_df_dict_frq["110,001 - 120,000"+"freq"].Count,"type":"line","name":"110,001 - 120,000"},
		{"x":app_df_dict_frq["120,001 - 130,000"+"freq"].Month,"y": app_df_dict_frq["120,001 - 130,000"+"freq"].Count,"type":"line","name":"120,001 - 130,000"},
		{"x":app_df_dict_frq["130,001 - 140,000"+"freq"].Month,"y": app_df_dict_frq["130,001 - 140,000"+"freq"].Count,"type":"line","name":"130,001 - 140,000"},
		{"x":app_df_dict_frq["140,001 - 150,000"+"freq"].Month,"y": app_df_dict_frq["140,001 - 150,000"+"freq"].Count,"type":"line","name":"140,001 - 150,000"},
		{"x":app_df_dict_frq[">150,000"+"freq"].Month,"y": app_df_dict_frq[">150,000"+"freq"].Count,"type":"line","name":">150,000"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Bureau Score",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_4",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["No-Hit"+"freq"].Month,"y": app_df_dict_frq["No-Hit"+"freq"].Count,"type":"line","name":"No-Hit"},
		{"x":app_df_dict_frq["<300"+"freq"].Month,"y": app_df_dict_frq["<300"+"freq"].Count,"type":"line","name":"<300"},
		{"x":app_df_dict_frq["300"+"freq"].Month,"y": app_df_dict_frq["300"+"freq"].Count,"type":"line","name":"300"},
		{"x":app_df_dict_frq["301 to 560"+"freq"].Month,"y": app_df_dict_frq["301 to 560"+"freq"].Count,"type":"line","name":"301 to 560"},
		{"x":app_df_dict_frq["561 to 600"+"freq"].Month,"y": app_df_dict_frq["561 to 600"+"freq"].Count,"type":"line","name":"561 to 600"},
		{"x":app_df_dict_frq["601 to 625"+"freq"].Month,"y": app_df_dict_frq["601 to 625"+"freq"].Count,"type":"line","name":"601 to 625"},
		{"x":app_df_dict_frq["626 to 650"+"freq"].Month,"y": app_df_dict_frq["626 to 650"+"freq"].Count,"type":"line","name":"626 to 650"},
		{"x":app_df_dict_frq["651 to 675"+"freq"].Month,"y": app_df_dict_frq["651 to 675"+"freq"].Count,"type":"line","name":"651 to 675"},
		{"x":app_df_dict_frq["676 to 700"+"freq"].Month,"y": app_df_dict_frq["676 to 700"+"freq"].Count,"type":"line","name":"676 to 700"},
		{"x":app_df_dict_frq["701 to 725"+"freq"].Month,"y": app_df_dict_frq["701 to 725"+"freq"].Count,"type":"line","name":"701 to 725"},
		{"x":app_df_dict_frq["726 to 750"+"freq"].Month,"y": app_df_dict_frq["726 to 750"+"freq"].Count,"type":"line","name":"726 to 750"},
		{"x":app_df_dict_frq["751 to 775"+"freq"].Month,"y": app_df_dict_frq["751 to 775"+"freq"].Count,"type":"line","name":"751 to 775"},
		{"x":app_df_dict_frq["776 to 800"+"freq"].Month,"y": app_df_dict_frq["776 to 800"+"freq"].Count,"type":"line","name":"776 to 800"},
		{"x":app_df_dict_frq[">800"+"freq"].Month,"y": app_df_dict_frq[">800"+"freq"].Count,"type":"line","name":">800"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

# Not updated.
	html.H2(children = "Type of Company",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_5",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Marital Status",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_6",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["Married"+"freq"].Month,"y": app_df_dict_frq["Married"+"freq"].Count,"type":"line","name":"Married"},
		{"x":app_df_dict_frq["Single"+"freq"].Month,"y": app_df_dict_frq["Single"+"freq"].Count,"type":"line","name":"Single"},
		{"x":app_df_dict_frq["Divorcee"+"freq"].Month,"y": app_df_dict_frq["Divorcee"+"freq"].Count,"type":"line","name":"Divorcee"},
		{"x":app_df_dict_frq["Widower"+"freq"].Month,"y": app_df_dict_frq["Widower"+"freq"].Count,"type":"line","name":"Widower"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Residential Status",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_7",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["Company Quarters"+"freq"].Month,"y": app_df_dict_frq["Company Quarters"+"freq"].Count,"type":"line","name":"Company Quarters"},
		{"x":app_df_dict_frq["Hostel"+"freq"].Month,"y": app_df_dict_frq["Hostel"+"freq"].Count,"type":"line","name":"Hostel"},
		{"x":app_df_dict_frq["Paying Guest"+"freq"].Month,"y": app_df_dict_frq["Paying Guest"+"freq"].Count,"type":"line","name":"Paying Guest"},
		{"x":app_df_dict_frq["Rented"+"freq"].Month,"y": app_df_dict_frq["Rented"+"freq"].Count,"type":"line","name":"Rented"},
		{"x":app_df_dict_frq["Self or spouse owned"+"freq"].Month,"y": app_df_dict_frq["Self or spouse owned"+"freq"].Count,"type":"line","name":"Self or spouse owned"},
		{"x":app_df_dict_frq["Shared Accommodation"+"freq"].Month,"y": app_df_dict_frq["Shared Accommodation"+"freq"].Count,"type":"line","name":"Shared Accommodation"},
		# {"x":app_df_dict_frq["Paying GuestShared Accomodation"+"freq"].Month,"y": app_df_dict_frq["Paying GuestShared Accomodation"+"freq"].Count,"type":"line","name":"Paying Guest or Shared Accomodation"},
		{"x":app_df_dict_frq["Staying with Parents"+"freq"].Month,"y": app_df_dict_frq["Staying with Parents"+"freq"].Count,"type":"line","name":"Staying with Parents"},
		{"x":app_df_dict_frq["Other"+"freq"].Month,"y": app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "No of dependents",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_8",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["0"+"freq"].Month,"y": app_df_dict_frq["0"+"freq"].Count,"type":"line","name":"0"},
		{"x":app_df_dict_frq["1 to 2"+"freq"].Month,"y": app_df_dict_frq["1 to 2"+"freq"].Count,"type":"line","name":"1 to 2"},
		{"x":app_df_dict_frq["3 to 5"+"freq"].Month,"y": app_df_dict_frq["3 to 5"+"freq"].Count,"type":"line","name":"3 to 5"},
		{"x":app_df_dict_frq["More than 5"+"freq"].Month,"y": app_df_dict_frq["More than 5"+"freq"].Count,"type":"line","name":"More than 5"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Education Level",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_9",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["0"+"freq"].Month,"y": app_df_dict_frq["0"+"freq"].Count,"type":"line","name":"0"},
		{"x":app_df_dict_frq["Diploma"+"freq"].Month,"y": app_df_dict_frq["Diploma"+"freq"].Count,"type":"line","name":"Diploma"},
		{"x":app_df_dict_frq["Graduate"+"freq"].Month,"y": app_df_dict_frq["Graduate"+"freq"].Count,"type":"line","name":"Graduate"},
		{"x":app_df_dict_frq["Post Graduate"+"freq"].Month,"y": app_df_dict_frq["Post Graduate"+"freq"].Count,"type":"line","name":"Post Graduate"},
		{"x":app_df_dict_frq["Professional"+"freq"].Month,"y": app_df_dict_frq["Professional"+"freq"].Count,"type":"line","name":"Professional"},
		{"x":app_df_dict_frq["Upto Hr Secondary"+"freq"].Month,"y": app_df_dict_frq["Upto Hr Secondary"+"freq"].Count,"type":"line","name":"Upto Hr Secondary"},
		{"x":app_df_dict_frq["NotMentioned"+"freq"].Month,"y": app_df_dict_frq["NotMentioned"+"freq"].Count,"type":"line","name":"Not Mentioned"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Number of Application with Applied Loan Amount",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_10",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["50,000 to 75,000"+"freq"].Month,"y": app_df_dict_frq["50,000 to 75,000"+"freq"].Count,"type":"line","name":"50,000 to 75,000"},
		{"x":app_df_dict_frq["75,001 to 100,000"+"freq"].Month,"y": app_df_dict_frq["75,001 to 100,000"+"freq"].Count,"type":"line","name":"75,001 to 100,000"},
		{"x":app_df_dict_frq["100,001 to 125,000"+"freq"].Month,"y": app_df_dict_frq["100,001 to 125,000"+"freq"].Count,"type":"line","name":"100,001 to 125,000"},
		{"x":app_df_dict_frq["125,001 to 150,000"+"freq"].Month,"y": app_df_dict_frq["125,001 to 150,000"+"freq"].Count,"type":"line","name":"125,001 to 150,000"},
		{"x":app_df_dict_frq["150,001 to 200,000"+"freq"].Month,"y": app_df_dict_frq["150,001 to 200,000"+"freq"].Count,"type":"line","name":"150,001 to 200,000"},
		{"x":app_df_dict_frq["200,001 to 250,000"+"freq"].Month,"y": app_df_dict_frq["200,001 to 250,000"+"freq"].Count,"type":"line","name":"200,001 to 250,000"},
		{"x":app_df_dict_frq["250,001 to 300,000"+"freq"].Month,"y": app_df_dict_frq["250,001 to 300,000"+"freq"].Count,"type":"line","name":"250,001 to 300,000"},
		{"x":app_df_dict_frq["300,001 to 350,000"+"freq"].Month,"y": app_df_dict_frq["300,001 to 350,000"+"freq"].Count,"type":"line","name":"300,001 to 350,000"},
		{"x":app_df_dict_frq["350,001 to 400,000"+"freq"].Month,"y": app_df_dict_frq["350,001 to 400,000"+"freq"].Count,"type":"line","name":"350,001 to 400,000"},
		{"x":app_df_dict_frq["400,001 to 450,000"+"freq"].Month,"y": app_df_dict_frq["400,001 to 450,000"+"freq"].Count,"type":"line","name":"400,001 to 450,000"},
		{"x":app_df_dict_frq["450,001 to 500,000"+"freq"].Month,"y": app_df_dict_frq["450,001 to 500,000"+"freq"].Count,"type":"line","name":"450,001 to 500,000"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),


	html.H2(children = "Purpose of Loan",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_11",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["Business"+"freq"].Month,"y": app_df_dict_frq["Business"+"freq"].Count,"type":"line","name":"Business"},
		{"x":app_df_dict_frq["Debt Consolidation"+"freq"].Month,"y": app_df_dict_frq["Debt Consolidation"+"freq"].Count,"type":"line","name":"Debt Consolidation"},
		{"x":app_df_dict_frq["Education"+"freq"].Month,"y": app_df_dict_frq["Education"+"freq"].Count,"type":"line","name":"Education"},
		{"x":app_df_dict_frq["Holiday"+"freq"].Month,"y": app_df_dict_frq["Holiday"+"freq"].Count,"type":"line","name":"Holiday"},
		{"x":app_df_dict_frq["Home renovation"+"freq"].Month,"y": app_df_dict_frq["Home renovation"+"freq"].Count,"type":"line","name":"Home renovation"},
		{"x":app_df_dict_frq["Household General"+"freq"].Month,"y": app_df_dict_frq["Household General"+"freq"].Count,"type":"line","name":"Household General"},
		{"x":app_df_dict_frq["Medical"+"freq"].Month,"y": app_df_dict_frq["Medical"+"freq"].Count,"type":"line","name":"Medical"},
		{"x":app_df_dict_frq["Wedding"+"freq"].Month,"y": app_df_dict_frq["Wedding"+"freq"].Count,"type":"line","name":"Wedding"},
		{"x":app_df_dict_frq["Other"+"freq"].Month,"y": app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Monexo Grading",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_12",
		figure = {
		"data" : [
		{"x":tot_dict["total"].Month,"y": tot_dict["total"].Count,"type":"line","name":"Total"},
		{"x":app_df_dict_frq["Business"+"freq"].Month,"y": app_df_dict_frq["Business"+"freq"].Count,"type":"line","name":"Business"},
		{"x":app_df_dict_frq["Debt Consolidation"+"freq"].Month,"y": app_df_dict_frq["Debt Consolidation"+"freq"].Count,"type":"line","name":"Debt Consolidation"},
		{"x":app_df_dict_frq["Education"+"freq"].Month,"y": app_df_dict_frq["Education"+"freq"].Count,"type":"line","name":"Education"},
		{"x":app_df_dict_frq["Holiday"+"freq"].Month,"y": app_df_dict_frq["Holiday"+"freq"].Count,"type":"line","name":"Holiday"},
		{"x":app_df_dict_frq["Home renovation"+"freq"].Month,"y": app_df_dict_frq["Home renovation"+"freq"].Count,"type":"line","name":"Home renovation"},
		{"x":app_df_dict_frq["Household General"+"freq"].Month,"y": app_df_dict_frq["Household General"+"freq"].Count,"type":"line","name":"Household General"},
		{"x":app_df_dict_frq["Medical"+"freq"].Month,"y": app_df_dict_frq["Medical"+"freq"].Count,"type":"line","name":"Medical"},
		{"x":app_df_dict_frq["Wedding"+"freq"].Month,"y": app_df_dict_frq["Wedding"+"freq"].Count,"type":"line","name":"Wedding"},
		{"x":app_df_dict_frq["Other"+"freq"].Month,"y": app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

######################################
#### Plots for Approved Data Sets ####
######################################

	html.H1("Application MIS (Only for Completed Application) [Filter -- Approved Application]",style={"textAlign":"center"}),
	html.H2(children = "Gender",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_21",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Male"+"freq"].Month,"y": aprvd_app_df_dict_frq["Male"+"freq"].Count,"type":"line","name":"Male"},
		{"x":aprvd_app_df_dict_frq["Female"+"freq"].Month,"y": aprvd_app_df_dict_frq["Female"+"freq"].Count,"type":"line","name":"Female"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Age",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_22",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["21-25"+"freq"].Month,"y": aprvd_app_df_dict_frq["21-25"+"freq"].Count,"type":"line","name":"21-25"},
		{"x":aprvd_app_df_dict_frq["26-30"+"freq"].Month,"y": aprvd_app_df_dict_frq["26-30"+"freq"].Count,"type":"line","name":"26-30"},
		{"x":aprvd_app_df_dict_frq["31-35"+"freq"].Month,"y": aprvd_app_df_dict_frq["31-35"+"freq"].Count,"type":"line","name":"31-35"},
		{"x":aprvd_app_df_dict_frq["36-40"+"freq"].Month,"y": aprvd_app_df_dict_frq["36-40"+"freq"].Count,"type":"line","name":"36-40"},
		{"x":aprvd_app_df_dict_frq["41-45"+"freq"].Month,"y": aprvd_app_df_dict_frq["41-45"+"freq"].Count,"type":"line","name":"41-45"},
		{"x":aprvd_app_df_dict_frq["> 45"+"freq"].Month,"y": aprvd_app_df_dict_frq["> 45"+"freq"].Count,"type":"line","name":"> 45"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Net Income",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_23",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Below 15,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["Below 15,000"+"freq"].Count,"type":"line","name":"Below 15,000"},
		{"x":aprvd_app_df_dict_frq["15,001  - 20,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["15,001  - 20,000"+"freq"].Count,"type":"line","name":"15,001  - 20,000"},
		{"x":aprvd_app_df_dict_frq["20,001 - 25,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["20,001 - 25,000"+"freq"].Count,"type":"line","name":"20,001 - 25,000"},
		{"x":aprvd_app_df_dict_frq["25,001 - 30,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["25,001 - 30,000"+"freq"].Count,"type":"line","name":"25,001 - 30,000"},
		{"x":aprvd_app_df_dict_frq["30,001 - 40,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["30,001 - 40,000"+"freq"].Count,"type":"line","name":"30,001 - 40,000"},
		{"x":aprvd_app_df_dict_frq["40,001 - 50,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["40,001 - 50,000"+"freq"].Count,"type":"line","name":"40,001 - 50,000"},
		{"x":aprvd_app_df_dict_frq["50,001 - 60,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["50,001 - 60,000"+"freq"].Count,"type":"line","name":"50,001 - 60,000"},
		{"x":aprvd_app_df_dict_frq["60,001 - 70,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["60,001 - 70,000"+"freq"].Count,"type":"line","name":"60,001 - 70,000"},
		{"x":aprvd_app_df_dict_frq["70,001 - 80,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["70,001 - 80,000"+"freq"].Count,"type":"line","name":"70,001 - 80,000"},
		{"x":aprvd_app_df_dict_frq["80,001 - 90,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["80,001 - 90,000"+"freq"].Count,"type":"line","name":"80,001 - 90,000"},
		{"x":aprvd_app_df_dict_frq["90,001 - 100,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["90,001 - 100,000"+"freq"].Count,"type":"line","name":"90,001 - 100,000"},
		{"x":aprvd_app_df_dict_frq["100,001 - 110,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["100,001 - 110,000"+"freq"].Count,"type":"line","name":"100,001 - 110,000"},
		{"x":aprvd_app_df_dict_frq["110,001 - 120,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["110,001 - 120,000"+"freq"].Count,"type":"line","name":"110,001 - 120,000"},
		{"x":aprvd_app_df_dict_frq["120,001 - 130,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["120,001 - 130,000"+"freq"].Count,"type":"line","name":"120,001 - 130,000"},
		{"x":aprvd_app_df_dict_frq["130,001 - 140,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["130,001 - 140,000"+"freq"].Count,"type":"line","name":"130,001 - 140,000"},
		{"x":aprvd_app_df_dict_frq["140,001 - 150,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["140,001 - 150,000"+"freq"].Count,"type":"line","name":"140,001 - 150,000"},
		{"x":aprvd_app_df_dict_frq[">150,000"+"freq"].Month,"y": aprvd_app_df_dict_frq[">150,000"+"freq"].Count,"type":"line","name":">150,000"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Bureau Score",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_24",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["No-Hit"+"freq"].Month,"y": aprvd_app_df_dict_frq["No-Hit"+"freq"].Count,"type":"line","name":"No-Hit"},
		{"x":aprvd_app_df_dict_frq["<300"+"freq"].Month,"y": aprvd_app_df_dict_frq["<300"+"freq"].Count,"type":"line","name":"<300"},
		{"x":aprvd_app_df_dict_frq["300"+"freq"].Month,"y": aprvd_app_df_dict_frq["300"+"freq"].Count,"type":"line","name":"300"},
		{"x":aprvd_app_df_dict_frq["301 to 560"+"freq"].Month,"y": aprvd_app_df_dict_frq["301 to 560"+"freq"].Count,"type":"line","name":"301 to 560"},
		{"x":aprvd_app_df_dict_frq["561 to 600"+"freq"].Month,"y": aprvd_app_df_dict_frq["561 to 600"+"freq"].Count,"type":"line","name":"561 to 600"},
		{"x":aprvd_app_df_dict_frq["601 to 625"+"freq"].Month,"y": aprvd_app_df_dict_frq["601 to 625"+"freq"].Count,"type":"line","name":"601 to 625"},
		{"x":aprvd_app_df_dict_frq["626 to 650"+"freq"].Month,"y": aprvd_app_df_dict_frq["626 to 650"+"freq"].Count,"type":"line","name":"626 to 650"},
		{"x":aprvd_app_df_dict_frq["651 to 675"+"freq"].Month,"y": aprvd_app_df_dict_frq["651 to 675"+"freq"].Count,"type":"line","name":"651 to 675"},
		{"x":aprvd_app_df_dict_frq["676 to 700"+"freq"].Month,"y": aprvd_app_df_dict_frq["676 to 700"+"freq"].Count,"type":"line","name":"676 to 700"},
		{"x":aprvd_app_df_dict_frq["701 to 725"+"freq"].Month,"y": aprvd_app_df_dict_frq["701 to 725"+"freq"].Count,"type":"line","name":"701 to 725"},
		{"x":aprvd_app_df_dict_frq["726 to 750"+"freq"].Month,"y": aprvd_app_df_dict_frq["726 to 750"+"freq"].Count,"type":"line","name":"726 to 750"},
		{"x":aprvd_app_df_dict_frq["751 to 775"+"freq"].Month,"y": aprvd_app_df_dict_frq["751 to 775"+"freq"].Count,"type":"line","name":"751 to 775"},
		{"x":aprvd_app_df_dict_frq["776 to 800"+"freq"].Month,"y": aprvd_app_df_dict_frq["776 to 800"+"freq"].Count,"type":"line","name":"776 to 800"},
		{"x":aprvd_app_df_dict_frq[">800"+"freq"].Month,"y": aprvd_app_df_dict_frq[">800"+"freq"].Count,"type":"line","name":">800"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

# Not updated.
	html.H2(children = "Type of Company",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_25",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Marital Status",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_26",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Married"+"freq"].Month,"y": aprvd_app_df_dict_frq["Married"+"freq"].Count,"type":"line","name":"Married"},
		{"x":aprvd_app_df_dict_frq["Single"+"freq"].Month,"y": aprvd_app_df_dict_frq["Single"+"freq"].Count,"type":"line","name":"Single"},
		{"x":aprvd_app_df_dict_frq["Divorcee"+"freq"].Month,"y": aprvd_app_df_dict_frq["Divorcee"+"freq"].Count,"type":"line","name":"Divorcee"},
		{"x":aprvd_app_df_dict_frq["Widower"+"freq"].Month,"y": aprvd_app_df_dict_frq["Widower"+"freq"].Count,"type":"line","name":"Widower"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Residential Status",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_27",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Company Quarters"+"freq"].Month,"y": aprvd_app_df_dict_frq["Company Quarters"+"freq"].Count,"type":"line","name":"Company Quarters"},
		{"x":aprvd_app_df_dict_frq["Hostel"+"freq"].Month,"y": aprvd_app_df_dict_frq["Hostel"+"freq"].Count,"type":"line","name":"Hostel"},
		{"x":aprvd_app_df_dict_frq["Paying Guest"+"freq"].Month,"y": aprvd_app_df_dict_frq["Paying Guest"+"freq"].Count,"type":"line","name":"Paying Guest"},
		{"x":aprvd_app_df_dict_frq["Rented"+"freq"].Month,"y": aprvd_app_df_dict_frq["Rented"+"freq"].Count,"type":"line","name":"Rented"},
		{"x":aprvd_app_df_dict_frq["Self or spouse owned"+"freq"].Month,"y": aprvd_app_df_dict_frq["Self or spouse owned"+"freq"].Count,"type":"line","name":"Self or spouse owned"},
		{"x":aprvd_app_df_dict_frq["Shared Accommodation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Shared Accommodation"+"freq"].Count,"type":"line","name":"Shared Accommodation"},
		# {"x":aprvd_app_df_dict_frq["Paying GuestShared Accomodation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Paying GuestShared Accomodation"+"freq"].Count,"type":"line","name":"Paying Guest or Shared Accomodation"},
		{"x":aprvd_app_df_dict_frq["Staying with Parents"+"freq"].Month,"y": aprvd_app_df_dict_frq["Staying with Parents"+"freq"].Count,"type":"line","name":"Staying with Parents"},
		{"x":aprvd_app_df_dict_frq["Other"+"freq"].Month,"y": aprvd_app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "No of dependents",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_28",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["0"+"freq"].Month,"y": aprvd_app_df_dict_frq["0"+"freq"].Count,"type":"line","name":"0"},
		{"x":aprvd_app_df_dict_frq["1 to 2"+"freq"].Month,"y": aprvd_app_df_dict_frq["1 to 2"+"freq"].Count,"type":"line","name":"1 to 2"},
		{"x":aprvd_app_df_dict_frq["3 to 5"+"freq"].Month,"y": aprvd_app_df_dict_frq["3 to 5"+"freq"].Count,"type":"line","name":"3 to 5"},
		{"x":aprvd_app_df_dict_frq["More than 5"+"freq"].Month,"y": aprvd_app_df_dict_frq["More than 5"+"freq"].Count,"type":"line","name":"More than 5"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Education Level",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_29",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["0"+"freq"].Month,"y": aprvd_app_df_dict_frq["0"+"freq"].Count,"type":"line","name":"0"},
		{"x":aprvd_app_df_dict_frq["Diploma"+"freq"].Month,"y": aprvd_app_df_dict_frq["Diploma"+"freq"].Count,"type":"line","name":"Diploma"},
		{"x":aprvd_app_df_dict_frq["Graduate"+"freq"].Month,"y": aprvd_app_df_dict_frq["Graduate"+"freq"].Count,"type":"line","name":"Graduate"},
		{"x":aprvd_app_df_dict_frq["Post Graduate"+"freq"].Month,"y": aprvd_app_df_dict_frq["Post Graduate"+"freq"].Count,"type":"line","name":"Post Graduate"},
		{"x":aprvd_app_df_dict_frq["Professional"+"freq"].Month,"y": aprvd_app_df_dict_frq["Professional"+"freq"].Count,"type":"line","name":"Professional"},
		{"x":aprvd_app_df_dict_frq["Upto Hr Secondary"+"freq"].Month,"y": aprvd_app_df_dict_frq["Upto Hr Secondary"+"freq"].Count,"type":"line","name":"Upto Hr Secondary"},
		{"x":aprvd_app_df_dict_frq["NotMentioned"+"freq"].Month,"y": aprvd_app_df_dict_frq["NotMentioned"+"freq"].Count,"type":"line","name":"Not Mentioned"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Number of Application with Applied Loan Amount",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_30",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["50,000 to 75,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["50,000 to 75,000"+"freq"].Count,"type":"line","name":"50,000 to 75,000"},
		{"x":aprvd_app_df_dict_frq["75,001 to 100,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["75,001 to 100,000"+"freq"].Count,"type":"line","name":"75,001 to 100,000"},
		{"x":aprvd_app_df_dict_frq["100,001 to 125,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["100,001 to 125,000"+"freq"].Count,"type":"line","name":"100,001 to 125,000"},
		{"x":aprvd_app_df_dict_frq["125,001 to 150,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["125,001 to 150,000"+"freq"].Count,"type":"line","name":"125,001 to 150,000"},
		{"x":aprvd_app_df_dict_frq["150,001 to 200,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["150,001 to 200,000"+"freq"].Count,"type":"line","name":"150,001 to 200,000"},
		{"x":aprvd_app_df_dict_frq["200,001 to 250,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["200,001 to 250,000"+"freq"].Count,"type":"line","name":"200,001 to 250,000"},
		{"x":aprvd_app_df_dict_frq["250,001 to 300,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["250,001 to 300,000"+"freq"].Count,"type":"line","name":"250,001 to 300,000"},
		{"x":aprvd_app_df_dict_frq["300,001 to 350,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["300,001 to 350,000"+"freq"].Count,"type":"line","name":"300,001 to 350,000"},
		{"x":aprvd_app_df_dict_frq["350,001 to 400,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["350,001 to 400,000"+"freq"].Count,"type":"line","name":"350,001 to 400,000"},
		{"x":aprvd_app_df_dict_frq["400,001 to 450,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["400,001 to 450,000"+"freq"].Count,"type":"line","name":"400,001 to 450,000"},
		{"x":aprvd_app_df_dict_frq["450,001 to 500,000"+"freq"].Month,"y": aprvd_app_df_dict_frq["450,001 to 500,000"+"freq"].Count,"type":"line","name":"450,001 to 500,000"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),


	html.H2(children = "Purpose of Loan",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_31",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Business"+"freq"].Month,"y": aprvd_app_df_dict_frq["Business"+"freq"].Count,"type":"line","name":"Business"},
		{"x":aprvd_app_df_dict_frq["Debt Consolidation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Debt Consolidation"+"freq"].Count,"type":"line","name":"Debt Consolidation"},
		{"x":aprvd_app_df_dict_frq["Education"+"freq"].Month,"y": aprvd_app_df_dict_frq["Education"+"freq"].Count,"type":"line","name":"Education"},
		{"x":aprvd_app_df_dict_frq["Holiday"+"freq"].Month,"y": aprvd_app_df_dict_frq["Holiday"+"freq"].Count,"type":"line","name":"Holiday"},
		{"x":aprvd_app_df_dict_frq["Home renovation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Home renovation"+"freq"].Count,"type":"line","name":"Home renovation"},
		{"x":aprvd_app_df_dict_frq["Household General"+"freq"].Month,"y": aprvd_app_df_dict_frq["Household General"+"freq"].Count,"type":"line","name":"Household General"},
		{"x":aprvd_app_df_dict_frq["Medical"+"freq"].Month,"y": aprvd_app_df_dict_frq["Medical"+"freq"].Count,"type":"line","name":"Medical"},
		{"x":aprvd_app_df_dict_frq["Wedding"+"freq"].Month,"y": aprvd_app_df_dict_frq["Wedding"+"freq"].Count,"type":"line","name":"Wedding"},
		{"x":aprvd_app_df_dict_frq["Other"+"freq"].Month,"y": aprvd_app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		),

	html.H2(children = "Monexo Grading",style={"textAlign":"left"}),
	dcc.Graph(
		id = "plot_32",
		figure = {
		"data" : [
		{"x":tot_dict["Approved Total"].Month,"y": tot_dict["Approved Total"].Count,"type":"line","name":"Total"},
		{"x":aprvd_app_df_dict_frq["Business"+"freq"].Month,"y": aprvd_app_df_dict_frq["Business"+"freq"].Count,"type":"line","name":"Business"},
		{"x":aprvd_app_df_dict_frq["Debt Consolidation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Debt Consolidation"+"freq"].Count,"type":"line","name":"Debt Consolidation"},
		{"x":aprvd_app_df_dict_frq["Education"+"freq"].Month,"y": aprvd_app_df_dict_frq["Education"+"freq"].Count,"type":"line","name":"Education"},
		{"x":aprvd_app_df_dict_frq["Holiday"+"freq"].Month,"y": aprvd_app_df_dict_frq["Holiday"+"freq"].Count,"type":"line","name":"Holiday"},
		{"x":aprvd_app_df_dict_frq["Home renovation"+"freq"].Month,"y": aprvd_app_df_dict_frq["Home renovation"+"freq"].Count,"type":"line","name":"Home renovation"},
		{"x":aprvd_app_df_dict_frq["Household General"+"freq"].Month,"y": aprvd_app_df_dict_frq["Household General"+"freq"].Count,"type":"line","name":"Household General"},
		{"x":aprvd_app_df_dict_frq["Medical"+"freq"].Month,"y": aprvd_app_df_dict_frq["Medical"+"freq"].Count,"type":"line","name":"Medical"},
		{"x":aprvd_app_df_dict_frq["Wedding"+"freq"].Month,"y": aprvd_app_df_dict_frq["Wedding"+"freq"].Count,"type":"line","name":"Wedding"},
		{"x":aprvd_app_df_dict_frq["Other"+"freq"].Month,"y": aprvd_app_df_dict_frq["Other"+"freq"].Count,"type":"line","name":"Other"}
		],
		"layout":go.Layout(
			xaxis = {"title":"Time"},
			yaxis = {"title":"Count"},
			hovermode = "closest"
			)
		}
		)

######################################
#### Plots for Rejected Data Sets ####
######################################


	])

app.run_server(debug=True)


