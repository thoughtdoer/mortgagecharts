# Christopher Foundas
# IA 690 - Capstone Project
# Dashboard of Mortgage Information - Main Application
# 12/01/2019

import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import flask
import os
import plotly.graph_objs as go


# import data
df = pd.read_csv('mortgagecharts/Borrower_Analysis_cleanup.csv',low_memory=False)

df_table = df[['loan_number','branch_name','loan_purpose','loan_type','loan_amount','official_loan_officer_name', 'closed_date']].copy()

''' Decide if you want these values to be lower case
df_table.branch_name = df_table.branch_name.apply(lambda x: x.lower())
df_table.loan_purpose = df_table.loan_purpose.apply(lambda x: x.lower())
df_table.loan_type = df_table.loan_type.apply(lambda x: x.lower())
'''

#df_table.columns = df_table.columns.str.strip().str.title().str.replace('_', ' ')

# process and aggregate data for display

# generate plots for calling below
# Plot for Loan Purpose (lp)
lp_pv = pd.pivot_table(df_table, index=['closed_date'], columns=["loan_purpose"], values=['loan_amount'], aggfunc=sum, fill_value=0)

lp_trace1 = go.Bar(x=lp_pv.index, y=lp_pv[('loan_amount', 'Purchase')], name='Purchase')
lp_trace2 = go.Bar(x=lp_pv.index, y=lp_pv[('loan_amount', 'Refinance')], name='Refinance')
lp_trace3 = go.Bar(x=lp_pv.index, y=lp_pv[('loan_amount', 'Refinance Cash-out')], name='Refinance Cash-out')

# Plot for Loan Type (lt)
lt_pv = pd.pivot_table(df_table, index=['closed_date'], columns=["loan_type"], values=['loan_amount'], aggfunc=sum, fill_value=0)

lt_trace1 = go.Bar(x=lt_pv.index, y=lt_pv[('loan_amount', 'Conventional')], name='Conventional')
lt_trace2 = go.Bar(x=lt_pv.index, y=lt_pv[('loan_amount', 'FHA')], name='FHA')

# Plot for branch name
b_pv = pd.pivot_table(df_table, index=['closed_date'], columns=["branch_name"], values=['loan_amount'], aggfunc=sum, fill_value=0)

b_trace1 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'Cap Com FCU')], name='CAP COM')
b_trace2 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'Homeowners Advantage')], name='Homeowners Advantage')

b_trace3 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'First Source FCU')], name='First Source FCU')
b_trace4 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'UFirst FCU')], name='UFirst FCU')
b_trace5 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'Stewarts FCU')], name='Stewarts FCU')
b_trace6 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'GHS FCU')], name='GHS FCU')
b_trace7 = go.Bar(x=b_pv.index, y=b_pv[('loan_amount', 'Hudson River Community CU')], name='Hudson River Communiy CU')


# code for the server
server = flask.Flask('main_app')
server.secret_key = os.environ.get('secret_key', 'secret')

PAGE_SIZE = 10

# calling a stylesheet for formatting the dashboard

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash('__name__', server=server, external_stylesheets=external_stylesheets)

# calling the plotly script for using Dash with App
app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'


#children_list = [html.Div(children=[html.H1('Hello World')])]

children_list = [
    html.Div(className='mat-card', style={"display": "block", "margin": "15px", "align": "center"},
             children=[
                 html.Img(src='mortgagecharts/static/logo.jpg', height='50', width='50'),
                 html.H1(children='Mortgage Data Dashboard'),
                 html.P('Data provided from LendingQB MLOS System from 2014 - 2018')
             ] # end children html div 1
             ), #end html div 1

    html.Div(children=[
        html.Div(children=''''''),
        dcc.Graph(
            id='loan-purpose',
            figure={
                'data': [lp_trace1, lp_trace2, lp_trace3],
                'layout':
                go.Layout(title='Loan Amount Closed by Loan Purpose', barmode='stack')
            })
            ] # end children
            ) # end html div
            ,

    html.Div(children=[
        html.Div(children=''''''),
        dcc.Graph(
            id='loan-type',
            figure={
                'data': [lt_trace1, lt_trace2],
                'layout':
                go.Layout(title='Loan Amount Closed by Loan Type', barmode='stack')
            })
            ] # end children
            ), # end html div

        html.Div(children=[
            html.Div(children=''''''),
            dcc.Graph(
                id='branches',
                figure={
                    'data': [b_trace1, b_trace2, b_trace3, b_trace4, b_trace5, b_trace6, b_trace7],
                    'layout':
                    go.Layout(title='Loan Amount Closed by Branch/Channel', barmode='stack')
                })
                ] # end children
                ), # end html div

    html.Div(className='mat-card', style={"display": "block", "margin": "15px"},
            children=[
                 html.H4(children='Details on Loans'),
                 dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_table.columns],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    )

         ] # end children for div 2
         )# end html div 2

                ] # end children list

# This specifies how the app is laid out
app.layout = html.Div(children=children_list)


if __name__ == '__main__':
    app.run_server(debug=False)
