import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import data_requests
import os
import dash_bootstrap_components as dbc
import subprocess
import time
from datetime import date

current_day = int(time.strftime('%d', time.gmtime()))
current_month = int(time.strftime('%m', time.gmtime()))
current_year = int(time.strftime('%Y', time.gmtime()))

cities_id = data_requests.json_load('./cities_id.txt')

default_df = pd.read_csv(os.path.join('data',os.listdir('data')[0]))

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

CONTENT_STYLE={
    'color':'#1D2D44',
    'font-family':'system-ui',
    'background-color':'#003580'
}
        
card_bottom_space = {
}  

histogram_card = dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Markdown('''
                                #### Histogram
                                Choose a variable you want to see the distribution of: 
                            ''', className='lead'),
                            dcc.Dropdown(
                                id='variable_selection', 
                                options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.dtypes=='float64') | (default_df.dtypes=='int64')]],
                                value='score',
                                placeholder='Select a variable',
                                clearable=False
                            ),
                            html.Hr(),
                            dcc.Graph('first_graph'),
                        ],
                    ),
                )

barplot_card = dbc.Card(
                dbc.CardBody(
                    [
                        dcc.Markdown('''
                            #### Bar chart
                        '''),
                        html.P(
                            "A bar chart is awesome when you want to show categorical data in a numerical way."
                            " In this example, every column is divided by the free_cancellation variable value.",
                            className='lead'
                        ),
                        dcc.Dropdown(
                                id='variable_selection_barchart', 
                                options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.columns=='category') | (default_df.columns=='neighborhood')]],
                                value='category',
                                placeholder='Select a variable',
                                clearable=False
                            ),
                        dcc.Graph('fifth_graph')
                    ]
                )
            )
scatter_card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "Scatter diagram"
                            ),
                            html.P(
                                'Correlation between variables',
                            ),
                            html.Label(
                                "X variable:"
                            ),
                            dcc.Dropdown(
                                id='variable_selection_corr1', 
                                options=[{'label':column, 'value':column} for column in default_df.columns[1:]],
                                value='score',
                                placeholder='Select a variable'
                            ),
                            html.Label(
                                "Y variable:"
                            ),
                            dcc.Dropdown(
                                id='variable_selection_corr2', 
                                options=[{'label':column, 'value':column} for column in default_df.columns[1:]],
                                value='price_per_night',
                                placeholder='Select a variable'
                            ),
                            html.Label(
                                "Color data in a different way depending on variable:"
                            ),
                            dcc.Dropdown(
                                id='color_variable',
                                options=[{'label':column, 'value':column} for column in default_df.columns[1:]],
                                placeholder='Select a variable'
                            ),
                            html.Hr(),
                            dcc.Graph('second_graph')
                        ],
                    )
                )

boxplots_card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(
                                "Boxplot"
                            ),
                            html.P(
                                'This useful graph provides valuable information regarding descriptive statistics:'
                                ' in particular, what the median, minimum, maximum value is and which is the first and third quartile value per each variable analyzed. ',
                                className='lead',
                            ),
                            html.P(
                                [
                                    "Variable:",
                                    dcc.Dropdown(
                                        id='variable_selection_box', 
                                        options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.dtypes=='float64') | (default_df.dtypes=='int64')]],
                                        value='score',
                                        placeholder='Select a variable',
                                        clearable=False
                                    )
                                ]
                            ),
                            html.Hr(),
                            dcc.Graph('third_graph')
                        ],
                    )
                )

heatmap = dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            "Correlation Heatmap"
                        ),
                        dcc.Graph('fourth_graph')
                    ]
                )
            )
                
sidebar = html.Div(
        dbc.NavbarSimple(
            [
                dbc.NavItem(dbc.NavLink("Webscraping | Data wrangling", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Data Visualization", href="/data-visualization", active="exact"))
            ],
            brand="Booking.com Webscraper",
            brand_href='https://github.com/matteozanatta/booking_webscraper/tree/master',
            color='primary',
            dark=True
        )
)
###-----------------------------------------------------------------
### Visualization webpage
###-----------------------------------------------------------------
header = dbc.Jumbotron(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.H1(
                                        'Data visualization tool',
                                    ),
                                    html.Br(),
                                    html.P(
                                        [
                                            "With this tool can visualize the data previously get from booking.com with my booking-webcraper. "
                                            "See the following link for reference: ",
                                            html.A(
                                                "github.com/booking-webscraper",
                                                href='https://github.com/matteozanatta/booking_webscraper/tree/master',
                                                style={'color':'#748cab'}
                                            ),
                                        ],
                                        className='lead'
                                    ),
                                    html.P(
                                        "Select the database you want to get data from and you will have "
                                        "multiple graphs available to analyze data.",
                                        className='lead'
                                    ),
                                    html.P(
                                        "Can't you find the dataset you were looking for? "
                                        "Webscrape and create a new one one the webscraping page!",
                                        className='lead'
                                    ),
                                    html.Hr(),
                                    html.H4(
                                        "Variables definition"
                                    ),
                                    html.Label(
                                        "Since this visualization page reads a csv file to work properly, it's highly raccomend to take a look and understand the variables involved:",
                                        className='lead'
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'score',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                    " (float): it describes the review point the structure get from customers on booking.com;"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'n_reviews',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                    " (int): as the name suggests, it rapresents the total number of reviews given to a structure by people;"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'total_price',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (float): this is the grand total a person has to pay to access a specific structure in the requested period;"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'category',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (object): right after the booking.com data collection process, structures are grouped in five different categories (hotel, apartments, B&B, Holiday Home and Other);"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'city_center_dist',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (float): this variables containes informations regarding how far the structure is from the city center;"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'neighborhood',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (object): ever wondered what neighborhood a structure is in? This variable contains that info!"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'free_cancellation',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (bool): is a structure listed with free cancellation on booking.com?"
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Span(
                                                        'price_per_night',
                                                        style={'font-weight':'bold'}
                                                    ),
                                                " (float): this is simply the total price for the entire holiday divided by the number of nights you want to find informations for."
                                                ]
                                            )
                                        ],
                                        className='lead'
                                    ),
                                    html.Hr(),
                                ]
                            )
                        ),
                        html.H4(
                            "Database selection",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P(
                                            'To begin with, choose a dataset from the list: ',
                                            className='lead'
                                        ),
                                    ],
                                    width=12,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Select(
                                            id='file_list', 
                                            options=[{'label':filename, 'value':'data/'+filename} for filename in os.listdir('data')],
                                            value=os.path.join('data',os.listdir('data')[0]),
                                            placeholder=os.listdir('data')[0],
                                            style={
                                                'background-color':'#003580',
                                                'color':'white'
                                            }
                                        ),
                                        dcc.Interval(
                                            id='interval_update',
                                            interval = 30*1000,
                                            n_intervals=0
                                        ),
                                        html.Hr(),
                                    ],
                                    width=12
                                )
                            ]
                        ),
                        html.H4(
                            "Info about the selected database"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.P(
                                        'Number of structures in the database:',
                                        className='lead'
                                    ),
                                    width='auto'
                                ),
                                dbc.Col(
                                    html.P(
                                        id='number_of_structures',
                                        className='lead'
                                    ),
                                    width='auto'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
                  
graphs = html.Div(
            [
                dbc.CardGroup(
                    [
                        histogram_card,
                        boxplots_card,
                    ]
                ),
                dbc.CardGroup(
                    [
                        barplot_card,
                        heatmap
                    ]
                ),
                dbc.CardGroup(
                    [
                        scatter_card
                    ]    
                )
            ]
        )

        
        
visualize_data_layout =  html.Div(
                            [
                                sidebar,
                                header,
                                graphs
                                     
                            ],
                            style=CONTENT_STYLE,
                        )
###-----------------------------------------------------------------
### Webscraper webpage
###-----------------------------------------------------------------
webscraper = html.Div(
                [
                    sidebar,
                    dbc.Jumbotron(
                        [
                            dbc.Container(
                                [
                                    dbc.Row(
                                        dbc.Col(
                                            [
                                                html.H1(
                                                    'Webscraping tool',
                                                ),
                                                html.Br(),
                                                html.P(
                                                    [
                                                        "With this tool you can choose some specific parameters and get a csv database containing booking.com listed structures on a city."
                                                        " See the following link for reference: ",
                                                        html.A(
                                                            "github.com/booking-webscraper",
                                                            href='https://github.com/matteozanatta/booking_webscraper/tree/master',
                                                            style={'color':'#748cab'}
                                                        ),
                                                    ],
                                                    className='lead'
                                                ),
                                                html.H6(
                                                    'Check-in and Check-out dates',
                                                ),
                                                html.P(
                                                    "Check-in dates are available only from the moment you watch this website page on because"
                                                    " past data is not accessible through booking.com website, so you would get an error.",
                                                    className='lead'
                                                ),
                                                html.H6(
                                                    'Adults and children number',
                                                ),
                                                html.P(
                                                    " Adults number is limited to 30, children to 10 just like a normal search on booking.com.",
                                                    className='lead'
                                                ),
                                                html.H6(
                                                    'Cycles and threads number',
                                                ),
                                                html.P(
                                                    "What is the 'cycles per page iteration' number? The more the cycles, the more the structures listed in the database."
                                                    " However, increasing this number will significantly enhance the computation time required to get a database from booking.com."
                                                    " To better understand what this number is take a look at the github link.",
                                                    className='lead'
                                                ),
                                                html.P(
                                                    " And what about the number of threads active per search?" 
                                                    " Basically, if you increase this number you can tell the script to send multiple asynchronous request to booking.com." 
                                                    " In other words, you can speed the whole data gathering process up.",
                                                    className='lead'
                                                ),
                                                html.H6(
                                                    'Other useful info'
                                                ),
                                                html.P(
                                                    "If you try to set an invalid number anywhere in the parameters the webscraper won't work.",
                                                    className='lead'
                                                ),
                                                html.P(
                                                    "Once loaded, the dataset will be available for visualization in the 'Data Visualization' part of the website.",
                                                    className='lead'
                                                )
                                            ]
                                        )
                                    ),
                                ]
                            )
                        ]
                    ),
                    dbc.Container(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5(
                                                "Booking.com search parameters"
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.P(
                                                "Select the check-in and check-out date",
                                                className='lead',
                                                style={'font-weight':'400'},

                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.DatePickerRange(
                                                id='input_date',
                                                min_date_allowed=date(current_year, current_month, current_day),
                                                max_date_allowed=date(current_year+3, current_month, current_day),
                                                initial_visible_month=date(current_year, current_month, current_day+1),
                                                start_date=date(current_year, current_month, current_day+1),
                                                end_date=date(current_year, current_month, current_day+7)
                                            ),
                                        ],
                                        width=12,
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Type the number of adults for the search",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                           dbc.Input(
                                                type="number",
                                                min=1,
                                                max=30,
                                                step=1,
                                                id='adult_number',
                                                value='2',
                                                style={
                                                    'background-color':'#febb02'
                                                }
                                            ), 
                                        ],
                                        width=12
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Type the number of children for the search",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                           dbc.Input(
                                                type="number",
                                                min=0,
                                                max=10,
                                                step=1,
                                                id='children-number',
                                                value='0',
                                                style={
                                                    'background-color':'#febb02'
                                                }
                                            ), 
                                        ],
                                        width=12
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Type the city you want to retrieve data of",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                           dbc.Select(
                                                options=[{'label':str(city), 'value':str(city)} for city in list(cities_id)],
                                                id="city_input",
                                                placeholder='Venice',
                                                value='Venice',
                                                style={
                                                    'background-color':'#febb02'
                                                }
                                            ), 
                                        ],
                                        width=12
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            )
                        ],
                        style={
                            'border': 'groove 1px',
                            'margin-bottom':'1em',
                            'padding': '1em',
                            'background-color':'white',
                            '-webkit-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-moz-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-ms-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-o-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)'
                        }
                    ),
                    dbc.Container(
                        [
                          dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5(
                                                "Algorithm parameters"
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Number of cycles per page iteration",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                           dbc.Input(
                                                type="number",
                                                min=1,
                                                max=15,
                                                step=1,
                                                id="iterations_number",
                                                value=3,
                                                style={
                                                    'background-color':'#febb02'
                                                }
                                            ), 
                                        ],
                                        width=12
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Number of thread active for multithreading",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
                                    dbc.Col(
                                        [
                                           dbc.Input(
                                                type="number",
                                                min=1,
                                                max=20,
                                                step=1,
                                                id="threads_number",
                                                value=15,
                                                style={
                                                    'background-color':'#febb02'
                                                }
                                            ), 
                                        ],
                                        width=12
                                    )
                                ],
                                style={
                                    'padding':'0.5em'
                                }
                            )
                        ],
                        style={
                            'margin-bottom':'1em',
                            'border': 'groove 1px',
                            'padding': '1em',
                            'background-color':'white',
                            '-webkit-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-moz-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-ms-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            '-o-box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
                            'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)'
                        }
                    ),
                    dbc.Container(
                        [
                            dbc.Button(
                                "Retrieve data",
                                id='button-scraping',
                                n_clicks=0,
                                block=True,
                                disabled=False,
                                style={
                                    'background-color':'black',
                                    'color':'white',
                                    'box-shadow':'0px 0px 5px 0px black'
                                }
                            ),
                            dbc.Spinner(
                                html.Div(id="loading_spinner"),
                                color='success',
                                fullscreen=True,
                                size='md'
                            ),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader("Result"),
                                    dbc.ModalBody(html.Div(id='modal_content')),
                                    dbc.ModalFooter(
                                        dbc.Button(
                                            "Close", id="close", className="ml-auto", n_clicks=0
                                        )
                                    ),
                                ],
                                id="modal",
                                is_open=False,
                                centered=True
                            ),
                            html.Br(),
                            html.Br(),
                        ],
                        style={
                            'padding':'0'
                        }                        
                    )    
                ],
                style={
                    'background-color':'#003580'
                }
            )                        
                        
app.layout = html.Div(
                [
                    dcc.Location(id='url'),
                    html.Div(id='page-content')
                ],
                style={
                    'font-family':'system-ui',
                }
            )

###-----------------------------------------------------------------
### Callbacks Script
###----------------------------------------------------------------- 
@app.callback(
    Output("file_list", "options"),
    [
        Input('interval_update', 'n_intervals')
    ]
)
def update_file_list(n):
    return [{'label':filename, 'value':os.path.join('data',filename)} for filename in os.listdir('data')]

@app.callback(
    Output('number_of_structures', 'children'),
    [
        Input("file_list", "value"),
    ]
)
def update_info_heading(file):
    return pd.read_csv(file).shape[0]

    
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
        
###-----------------------------------------------------------------
### Callbacks Rendering page
###----------------------------------------------------------------- 
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
###-----------------------------------------------------------------
### Callbacks Graphs section
###-----------------------------------------------------------------            
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
    [    
        Output('second_graph', 'figure'),
        Output('variable_selection_corr1', 'options'),
        Output('variable_selection_corr2', 'options'),
        Output('color_variable','options')
    ],
    [
        Input('variable_selection_corr1', 'value'),
        Input('variable_selection_corr2', 'value'),
        Input('color_variable','value'),
        Input('file_list', 'value')
    ]
)
def update_graph2_and_values_dropdowns(first_var, second_var, third_var, db_sel):
    df = pd.read_csv(db_sel)
    if(first_var==None):
        graph = px.scatter(df, y=second_var, color=third_var)
    elif(second_var==None):
        graph = px.scatter(df, x=first_var, color=third_var)
    elif(third_var==None):
        graph = px.scatter(df, x=first_var, y=second_var)
    else:
        graph = px.scatter(df, x=first_var, y=second_var, color=third_var)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if ('variable_selection_corr1','variable_selection_corr2','color_variable' in changed_id):
        options = disabled_property_dict([second_var, third_var], df.columns[1:])
        options2 = disabled_property_dict([first_var,third_var], df.columns[1:])
        options3 = disabled_property_dict([first_var,second_var], df.columns[1:])
        return(graph, options, options2, options3)
    else:
        return(graph, disabled_property_dict('price_per_night', df.columns[1:]), disabled_property_dict('score', df.columns[1:]), disabled_property_dict(['price_per_night','score'], df.columns[1:]))

def disabled_property_dict(prop_to_disable, df_columns):
    options=[]
    if(prop_to_disable!=None):
        for column in df_columns:
            if(column in prop_to_disable):
                options.append({'label':column, 'value':column, 'disabled':True})
            else:
                options.append({'label':column, 'value':column})
        return options
    else:
        return [{'label':column, 'value':column} for column in df_columns[1:]]
        
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

@app.callback(
    Output('fourth_graph','figure'),
    [
        Input('file_list', 'value')
    ]
)
def update_graph4(db):
    df = pd.read_csv(db)
    return px.imshow(df[df.columns[1:-1]].corr())
    
@app.callback(
    Output('fifth_graph','figure'),
    [
        Input('variable_selection_barchart', 'value'),
        Input('file_list', 'value')
    ]
)
def update_graph5(var, db):
    df = pd.read_csv(db)
    return px.bar(df, x=var, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')

if(__name__=='__main__'):
    app.run_server(debug=False, threaded=True)