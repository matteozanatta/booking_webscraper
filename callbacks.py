import pandas as pd
import os
import dash
import subprocess
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(
        external_stylesheets=[dbc.themes.LUX],
        meta_tags=[
            {
                'name':'viewport',
                'content':'width=device-width, initial-scale=1',
                'xmlns':'http://www.w3.org/1999.xhtml',
                'lang':'en',
                'charset':'utf-8'
            }
        ]
    )
    
server = app.server
    
@app.callback(
    Output("file_list", "options"),
    [
        Input('interval_update', 'n_intervals')
    ]
)
def update_file_list(n):
    return [{'label':filename, 'value':os.path.join('data',filename)} for filename in os.listdir('data')]

@app.callback(
    [
        Output('loading_spinner','children'),
        Output('modal','is_open'),
        Output('modal_content','children')
    ],
    [
        Input('button-scraping','n_clicks'),
        Input('close', 'n_clicks'),
        State('input_date', 'start_date'),
        State('input_date', 'end_date'),
        State('adult_number', 'value'),
        State('children-number', 'value'),
        State('iterations_number', 'value'),
        State('threads_number', 'value'),
        State('city_input', 'value')
    ]
)
def run_script(click, modal_close, start_date, end_date, ad_n, ch_n, it_n, th_n, city):
    global im_working
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button-scraping' in changed_id:
        iny, inm, ind = [data for data in start_date.split('-')]
        outy, outm, outd = [data for data in end_date.split('-')]
        for value in [iny, inm, ind, outy, outm, outd, city, ad_n, ch_n, it_n, th_n]:
            if(value==None):
                return("",True,"A parameter value is invalid.")
        output = subprocess.check_output(args=('python db_builder.py '+str(inm)+" "+str(ind)+" "+str(iny)+" "+str(outm)+" "+str(outd)+" "+str(outy)+" "+str(ad_n)+" "+str(ch_n)+" "+str(it_n)+" "+str(th_n)+" "+str(city)), shell=True).decode()
        stripped = output.split()
        info = html.Div(
            [
                html.P(
                    "Number of structures listed on booking.com: "+stripped[5],
                    className='lead'
                ),
                html.P(
                    "Number of structures found by the algorithm: "+stripped[8],
                    className='lead'
                ),
                html.P(
                    "Algorithm efficiency: "+stripped[11]+" %",
                    className='lead'
                ),
                html.P(
                    'Time the algorithm took to run: '+stripped[15]+"s",
                    className='lead'
                ),
                html.Br(),
                html.P(
                    'The data you requested is now available for visualization',
                    style={
                        'color':'green'
                    }
                ),
                
            ]
        )
        return("", True, info)
    elif 'close' in changed_id:
        return("", False, "")
    return dash.no_update, dash.no_update, dash.no_update
        
#----------------------------------------------------------------------
#Page-content render function
@app.callback(
    Output("page-content", "children"), 
    [
        Input("url", "pathname")
    ]
)
def render_page_content(pathname):
    if pathname == "/":
        return webscraper
    elif pathname == "/data-visualization":
        return visualize_data_layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} doesn't exists..."),
        ]
    )
#------------------------------------------------------------------------
#Graphs section            
@app.callback(
        Output('first_graph', 'figure'),
    [
        Input('variable_selection', 'value'),
        Input('file_list', 'value')
    ]
)
def update_graph(column, db_name):
    df = pd.read_csv(db_name)
    return px.histogram(df, x=column).update_xaxes(categoryorder='total descending')
    
@app.callback(
        Output('second_graph', 'figure'),
    [
        Input('variable_selection_corr1', 'value'),
        Input('variable_selection_corr2', 'value'),
        Input('file_list', 'value')
    ]
)
def update_graph2(first_var, second_var, db_sel):
    df = pd.read_csv(db_sel)
    return px.scatter(df, x=first_var, y=second_var, color=df['free_cancellation']) #inserire scelta

@app.callback(
        Output('third_graph', 'figure'),
    [
        Input('variable_selection_box', 'value'),
        Input('file_list', 'value')
    ]
)
def update_graph3(var, db_sel):
    df = pd.read_csv(db_sel)
    return px.box(df, x=var)