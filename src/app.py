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
import datetime
import numpy as np

current_day = int(time.strftime('%d', time.gmtime()))
current_month = int(time.strftime('%m', time.gmtime()))
current_year = int(time.strftime('%Y', time.gmtime()))

cities_id = data_requests.json_load('./cities_id.txt')

default_df = pd.read_csv(os.path.join('data',os.listdir('data')[0]))

app = dash.Dash(
        __name__,
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
       
histogram_card = dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Markdown('''
                                #### Histogram
                                An histogram let you see the distribution of a numerical variable.
                            ''', className='lead'),
                            html.P(
                                [
                                    'Variable:',
                                    dcc.Dropdown(
                                    id='variable_selection', 
                                    options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.dtypes=='float64') | (default_df.dtypes=='int64')]],
                                    value='score',
                                    placeholder='Select a variable',
                                    clearable=False
                                    ),
                                ]
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
                            " In this example, every column is divided by the free_cancellation variable value."
                            " Values are ordered by ascending order, so columns on the left have more values compared to the right ones.",
                            className='lead'
                        ),
                        dcc.Dropdown(
                                id='variable_selection_barchart', 
                                options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.columns=='category') | (default_df.columns=='neighborhood')]],
                                value='category',
                                placeholder='Select a variable',
                                clearable=False
                            ),
                        html.Hr(),
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
                                "A scatter plot is really useful to plot variables against each other and (maybe) find curious relations while visualizing data. "
                                " With this graph you're also able to differentiate color between data values following a given variable.",
                                className='lead'
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
                                ' in particular, what the median, minimum, maximum value is and which is the first and third quartile value per each variable analyzed.',
                                className='lead',
                            ),
                            html.P(
                                [
                                    "Variable:",
                                    dcc.Dropdown(
                                        id='variable_selection_box', 
                                        options=[{'label':column, 'value':column} for column in default_df.columns[(default_df.dtypes=='float64') | (default_df.dtypes=='int64')]],
                                        value='city_center_dist',
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
                        html.P(
                            'With this correlation heatmap you can visually identify correlation between numerical variables in an easy way. '
                            "The higher the correlation value between two variables, the more they're related.",
                            className='lead',
                        ),
                        html.Hr(),
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

general_filter = dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Markdown('''
                            #### General filter
                            Here you can set a main filter that's going to affect all database visualized data.
                            
                            Firstly select the variable, then the value you want to filter to correctly visualize the dataset. 
                            ''', className='lead'),
                            dcc.Dropdown(
                                id='filter_dropdown_var',
                                options=[{'label':column, 'value':column} for column in default_df.columns[1:]],
                                
                            ),
                            html.Div(
                                id='div_filter_dropdown_values',
                            ),
                        ]
                    ),
                    id='general_filter_card'
                )
               
info_card = dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            "Info about the selected database",
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
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.P(
                                        'After filtering (if you are), the structures you are visualizing are:',
                                        className='lead'
                                    ),
                                    width='auto'
                                ),
                                dbc.Col(
                                    html.P(
                                        id='number_of_structures2',
                                        className='lead'
                                    ),
                                    width='auto'
                                )
                            ]
                        )
                    ]
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
                                    html.Hr(),
                                    html.H4(
                                        "Variables definition"
                                    ),
                                    html.Label(
                                        "Since this visualization page reads a csv file to work properly, it's highly raccomended to understand and take a look at the variables involved:",
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
                                        html.P(
                                            "Can't you find the dataset you were looking for? "
                                            "Webscrape and create a new one one the webscraping page!",
                                            className='lead',
                                            style={
                                                'padding-top':'1em'
                                            }
                                        ),
                                        dcc.Interval(
                                            id='interval_update',
                                            interval = 30*1000,
                                            n_intervals=0
                                        ),
                                    ],
                                    width=12
                                )
                            ]
                        ),
                    ]
                )
            ],
            style={
                'margin-bottom':0
            }
        )
                  
graphs = html.Div(
            [
                dbc.CardDeck(
                    [
                        general_filter,
                    ],
                    style={
                        'margin':'1.5em 0'
                    }
                ),
                dbc.CardDeck(
                    [
                        info_card
                    ],
                    style={
                        'margin':'1.5em 0'
                    }
                ),
                dbc.CardDeck(
                    [
                        histogram_card,
                        heatmap,
                    ],
                    style={
                        'margin':'1.5em 0'
                    }
                ),
                dbc.CardDeck(
                    [
                        barplot_card,
                        boxplots_card,
                    ],
                    style={
                        'margin':'1.5em 0'
                    }
                ),
                dbc.CardDeck(
                    [
                        scatter_card
                    ],
                    style={
                        'margin':'1.5em 0'
                    }
                ),
            ]
        )

visualize_data_layout =  html.Div(
                            [
                                sidebar,
                                header,
                                graphs
                                     
                            ],
                            style={
                                'color':'#1D2D44',
                                'font-family':'system-ui',
                                'background-color':'#003580'
                            },
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
                                                "Booking.com search parameters",
                                                style={
                                                    'background-color':'lightsteelblue',
                                                    'width':'fit-content'
                                                }
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
                                                min_date_allowed=datetime.date(current_year, current_month, current_day),
                                                max_date_allowed=datetime.date(current_year, current_month, current_day)+datetime.timedelta(days=365*3),
                                                initial_visible_month=datetime.date(current_year, current_month, current_day)+datetime.timedelta(days=1),
                                                start_date=datetime.date(current_year, current_month, current_day)+datetime.timedelta(days=1),
                                                end_date=datetime.date(current_year, current_month, current_day)+datetime.timedelta(days=7)
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
                                                    'background-color':'lightgrey'
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
                                                    'background-color':'lightgrey'
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
                                                "Algorithm parameters",
                                                style={
                                                    'background-color':'lightsteelblue',
                                                    'width':'fit-content'
                                                }
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
                                                    'background-color':'lightgrey'
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
                                                    'background-color':'lightgrey'
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
                                            html.P(
                                                "You don't know what these numbers are? Leave them like that to do a standard search on booking.com.",
                                                className='lead',
                                                style={'font-weight':'400'}
                                            ),
                                            html.P(
                                                "Don't reload the webpage while retrieving data: the whole process could take up to 120 seconds to finish.",
                                                className='lead',
                                                style={'color':'red'}
                                            ),
                                            
                                        ],
                                        width=12
                                    ),
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
    Output('div_filter_dropdown_values','children'),
    [
        Input("file_list", "value"),
        Input('filter_dropdown_var','value')
    ]
)
def main_filter(db, var):
    if(var==None):
        return html.Div(id='filter_range_selector')
    df = pd.read_csv(db)
    if(var=='score'):
        min = df[var].min()
        max = df[var].max()
        return dcc.RangeSlider(
            id='filter_range_selector',
            min = min,
            max = max,
            step = None,
            value = [df[var].quantile(0.4),df[var].quantile(0.8)],
            marks = data_requests.marks_creator(df, var, 1),
            allowCross = False,
        )
    elif((var=='total_price') | (var=='price_per_night') | (var=='n_reviews')):
        if(df[var].min()==0):
            min = 0.1
        else:
            min = df[var].min()
        max = df[var].max()
        return dcc.RangeSlider(
            id='filter_range_selector',
            min = np.log10(min),
            max = np.log10(max),
            step = None,
            value = [np.log10(df[var].quantile(0.4)),np.log10(df[var].quantile(0.8))],
            marks = data_requests.log_marks_creator(df, var, 0),
            allowCross = False,
        )
    elif(var=='city_center_dist'):
        if(df[var].min()==0):
            min = 0.1
        else:
            min = df[var].min()
        max = df[var].max()
        return dcc.RangeSlider(
            id='filter_range_selector',
            min = np.log10(min),
            max = np.log10(max),
            step = None,
            value = [np.log10(df[var].quantile(0.4)),np.log10(df[var].quantile(0.8))],
            marks = data_requests.log_marks_creator(df, var, 1),
            allowCross = False
        )
    elif(df[var].dtypes=='object'):
        return dcc.Dropdown(
            id='filter_range_selector',
            options=[{'label':value, 'value':value} for value in df[var].unique()],
            placeholder='Select a value',
            multi=True,
        )
    elif(df[var].dtypes=='bool'):
        return dcc.Dropdown(
            id='filter_range_selector',
            options=[{'label':str(value), 'value':str(value)} for value in df[var].unique()],
            placeholder='Select a value',
        )    
    else:
        return dash.no_update
    
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
        State('iterations_number', 'value'),
        State('threads_number', 'value'),
        State('city_input', 'value')
    ]
)
def run_script(click, modal_close, start_date, end_date, ad_n, it_n, th_n, city):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button-scraping' in changed_id:
        iny, inm, ind = [data for data in start_date.split('-')]
        outy, outm, outd = [data for data in end_date.split('-')]
        for value in [iny, inm, ind, outy, outm, outd, city, ad_n, it_n, th_n]:
            if(value==None):
                return("",True,"A parameter value is invalid.")
        output = subprocess.check_output(args=('python db_builder.py '+str(inm)+" "+str(ind)+" "+str(iny)+" "+str(outm)+" "+str(outd)+" "+str(outy)+" "+str(ad_n)+" "+str(it_n)+" "+str(th_n)+" "+str(city)), shell=True).decode()
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
    
@app.callback(
    Output('number_of_structures2', 'children'),
    [
        Input("file_list", "value"),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def n_structure_now_visualizing(db_name, var, values):
    df = pd.read_csv(db_name)
    if(values!=None and values):
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            return df[df[var].between(int(10**values[0]),int(10**values[1]))].shape[0]
        elif(var=='city_center_dist'):
            return df[df[var].between(10**values[0],10**values[1])].shape[0]
        elif(df[var].dtype=='object'):
            return df[df[var].isin(values)].shape[0]
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            return df[df[var]==is_true].shape[0]
        else:
            return df[df[var].between(values[0],values[1])].shape[0]
    return df.shape[0]
    
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
        Input('file_list', 'value'),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def update_graph(column, db_name, var, values):
    df = pd.read_csv(db_name)
    #If values array exists and has values
    if(values!=None and values):
        #If number is shown in the filter in a logarithmic scale, we have to use its exponent
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            return px.histogram(df[df[var].between(int(10**values[0]),int(10**values[1]))], x=column)
        #This variable has a different treatment because it's in a log scale and it's float. Results cannot be filtered by an integer cast
        elif(var=='city_center_dist'):
            return px.histogram(df[df[var].between(10**values[0],10**values[1])], x=column)
        #if categorical data
        elif(df[var].dtype=='object'):
            return px.histogram(df[df[var].isin(values)], x=column)
        #if we are checking the free cancellation variable
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            return px.histogram(df[df[var]==is_true], x=column)
        #This is valid for the score variable
        else:
            return px.histogram(df[df[var].between(values[0],values[1])], x=column)
    return px.histogram(df, x=column)
    
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
        Input('file_list', 'value'),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def update_graph2_and_values_dropdowns(first_var, second_var, third_var, db_sel, var, values):
    df = pd.read_csv(db_sel)
    #If values array exists and has values and filter the df according to user input
    if(values!=None and values):
        #If number is shown in the filter in a logarithmic scale, we have to use its exponent
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            df = df[df[var].between(int(10**values[0]),int(10**values[1]))]
        #This variable has a different treatment because it's in a log scale and it's float. Results cannot be filtered by an integer cast
        elif(var=='city_center_dist'):
            df = df[df[var].between(10**values[0],10**values[1])]
        #if categorical data
        elif(df[var].dtype=='object'):
            df = df[df[var].isin(values)]
        #if we are checking the free cancellation variable
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            df = df[df[var]==is_true]
        #This is valid for the score variable
        else:
            df = df[df[var].between(values[0],values[1])]
    if(first_var==None):
        graph = px.scatter(df, y=second_var, color=third_var)
    elif(second_var==None):
        graph = px.scatter(df, x=first_var, color=third_var)
    elif(third_var==None):
        graph = px.scatter(df, x=first_var, y=second_var)
    else:
        graph = px.scatter(df, x=first_var, y=second_var, color=third_var)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if ('variable_selection_corr1' 'variable_selection_corr2' 'color_variable' in changed_id):
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
        Input('file_list', 'value'),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def update_graph3(column, db_sel, var, values):
    df = pd.read_csv(db_sel)
    #If values array exists and has values
    if(values!=None and values):
        #If number is shown in the filter in a logarithmic scale, we have to use its exponent
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            return px.box(df[df[var].between(int(10**values[0]),int(10**values[1]))], x=column)
        #This variable has a different treatment because it's in a log scale and it's float. Results cannot be filtered by an integer cast
        elif(var=='city_center_dist'):
            return px.box(df[df[var].between(10**values[0],10**values[1])], x=column)
        #if categorical data
        elif(df[var].dtype=='object'):
            return px.box(df[df[var].isin(values)], x=column)
        #if we are checking the free cancellation variable
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            return px.box(df[df[var]==is_true], x=column)
        #This is valid for the score variable
        else:
            return px.box(df[df[var].between(values[0],values[1])], x=column)
    return px.box(df, x=column)

@app.callback(
    Output('fourth_graph','figure'),
    [
        Input('file_list', 'value'),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def update_graph4(db, var, values):
    df = pd.read_csv(db)
    df = df[df.columns[1:-1]]
    #If values array exists and has values
    if(values!=None and values):
        #If number is shown in the filter in a logarithmic scale, we have to use its exponent
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            return px.imshow(df[df[var].between(int(10**values[0]),int(10**values[1]))].corr())
        #This variable has a different treatment because it's in a log scale and it's float. Results cannot be filtered by an integer cast
        elif(var=='city_center_dist'):
            return px.imshow(df[df[var].between(10**values[0],10**values[1])].corr())
        #if categorical data
        elif(df[var].dtype=='object'):
            return px.imshow(df[df[var].isin(values)].corr())
        #if we are checking the free cancellation variable
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            return px.imshow(df[df[var]==is_true].corr())
        #This is valid for the score variable
        else:
            return px.imshow(df[df[var].between(values[0],values[1])].corr())
    return px.imshow(df.corr())
    
@app.callback(
    Output('fifth_graph','figure'),
    [
        Input('variable_selection_barchart', 'value'),
        Input('file_list', 'value'),
        State('filter_dropdown_var','value'),
        Input('filter_range_selector', 'value')
    ]
)
def update_graph5(column, db, var, values):
    df = pd.read_csv(db)
    #If values array exists and has values
    if(values!=None and values):
        #If number is shown in the filter in a logarithmic scale, we have to use its exponent
        if(((df[var].dtype=='int64') | (df[var].dtype=='float64')) & (var!='score') & (var!='city_center_dist')):
            return px.bar(df[df[var].between(int(10**values[0]),int(10**values[1]))], x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')
        #This variable has a different treatment because it's in a log scale and it's float. Results cannot be filtered by an integer cast
        elif(var=='city_center_dist'):
            return px.bar(df[df[var].between(10**values[0],10**values[1])], x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')
        #if categorical data
        elif(df[var].dtype=='object'):
            return px.bar(df[df[var].isin(values)], x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')
        #if we are checking the free cancellation variable
        elif(df[var].dtype=='bool'):
            is_true = values=='True'
            return px.bar(df[df[var]==is_true], x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')
        #This is valid for the score variable
        else:
            return px.bar(df[df[var].between(values[0],values[1])], x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')
    return px.bar(df, x=column, color='free_cancellation', barmode='group').update_xaxes(categoryorder='total descending')

if(__name__=='__main__'):
    app.run_server(debug=False, threaded=True)
