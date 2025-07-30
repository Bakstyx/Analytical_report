#libraries
from click import style
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_daq as daq
import plotly.express as px
import pandas as pd

#Scripts
import dashboard_tables as dt
import dashboard_graphs as dg

folder = r'C:\Users\baks_\Documents\Bakstyx\Repositories\Analytical_report\Results\Test_validation\Test_1\Test_1-2023-02-20\Compiler'



app = Dash(__name__)

colors = {
    'background': '#3a3a3d', 
    'text': '#c3580b' 
}
# Import Dataframes for visualization of data
#General parameters for dataframes
round=2

#Dataframe of descriptive stats general

df_eda = dt.descriptive_stats_arrange(folder=folder, name='descript_stats', 
                        id_vars=['Evaluation', 'Category'], 
                        pivot_columns=['Metric'], round=round)

#Dataframe of eda_diff relative
df_eda_diff = dt.descriptive_stats_arrange(folder=folder, name='descript_stats_diff', 
                        id_vars=['Evaluation', 'Category'], 
                        pivot_columns=['Metric'], round=round)

#Dataframe of eda_diff absolute
df_eda_diff_abs = dt.descriptive_stats_arrange(folder=folder, name='descript_stats_diff_abs', 
                        id_vars=['Evaluation', 'Category'], 
                        pivot_columns=['Metric'], round=round)

#Dataframe of diff relative
df_diff = dt.diff_arrange(folder=folder, name='differences', 
                            id_vars=['Evaluation', 'Differences', 'Sample'], 
                            round=round)

#Dataframe of diff absolute
df_diff_abs = dt.diff_arrange(folder=folder, name='differences_abs', 
                                id_vars=['Evaluation', 'Differences', 'Sample'], 
                                round=round)

#Dataframe of decision analysis
df_limits_analysis = dt.tables_loader(folder=folder, 
                                        name='status_analysis', 
                                        round=round)



#Dataframe of range analysis
df_range_analysis = dt.tables_loader(folder=folder, 
                                        name='status_analysis', 
                                        round=round)


#Functions
#Initially for descriptive stats analysis
def filter_df(dataframe, selected, category):
    df_data = dataframe[dataframe['Evaluation'] == selected]
    if category != 'All':
        df_data = df_data[df_data['Category']==category]
    return df_data

def filter_df_limits(dataframe, selected, category, status):
    df_data = filter_df(dataframe, selected, category)
    if status != 'All':
        df_data = df_data[df_data['Status_rv']==status]
    return df_data

def filter_df_table_viz(dataframe, selected, category):
    df_data = filter_df(dataframe, selected, category)
    df_data.drop(columns=['Results count'], inplace=True)
    return df_data.to_dict("records")

def graph(style, data, x, y, hue, title, order=None, points=None):
    if style == 'bar':
        fig = dg.bar(data, x, y, hue, title, order)
        return fig
    elif style == 'box':
        fig =dg.box(data, x, y, hue, title, points=None)
        return fig

#Grid graps for multiple subplots   
def grid_graph(style, dataframe, rows_grid, cols_grid, labels, values, title):
    if style == 'pie':
        fig = dg.pie_grid_status(dataframe, rows_grid, cols_grid, labels, values, title)
        return fig

#Norm analysis
def filter_df_limits_viz(dataframe, selected, category, decision):
    df_data = filter_df_limits(dataframe, selected, category, decision)
    return df_data.to_dict("records")


#layout config 
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


#layout App
app.layout = html.Div(style={#'backgroundColor': colors['background']
                                }, 
                        children=[
    html.H1(
        children='Dashboard of analytical reports',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Graphical presentation.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    #filters in dashboard
    html.Div(children=[
        html.Label('Select evaluation'),
        dcc.Dropdown(df_eda['Evaluation'].unique().tolist(),
                        id='Selector',
                        style={'display': 'inline-block',
                            'width': '50%',
                            'align-items': 'left',
                            }
                    ),
        dcc.RadioItems(options = df_eda['Category'].unique().tolist()+['All'],
                        value = 'All',
                        id='cat_selector',
                        inline=True,
                        style={'display': 'inline-block',
                                'width': '50%',
                                'align-items': 'center',
                                }
                        ),
        daq.LEDDisplay(
            id='Counter_display',
            label="N muestral",
            style={'display': 'inline-block', 
                    'width': '5%',
                    'align-items': 'right',
                    },
            value=df_eda['Results count'].unique().tolist()[0]
            ),
        ]
    ),
    html.Div([
        dcc.Tabs([
            #Tab of general eda Data + Graphs
            dcc.Tab(
                label='Descriptive statistics', 
                children=[
                    dash_table.DataTable(
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            #'lineHeight': '15px',
                            #'backgroundColor': colors['background']
                                        },
                        style_table={'minWidth': '100%'},
                        data = df_eda.to_dict('records'),
                        editable=False,
                        sort_action="native",
                        id = 'table_eda',
                        page_size=10
                    ),
                    dcc.Graph(
                        id='eda-graph-1',
                        #figure=fig
                        style={
                            'backgroundColor': colors['background']
                        }
                    ),
                ]
            ),
            #Tab of eda diff Data + Graphs. Greaphs using diff dataframe
            dcc.Tab(
                label='Descriptive statistics differences', 
                children=[
                    dash_table.DataTable(
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                #'lineHeight': '15px',
                                #'backgroundColor': colors['background']
                                            },
                            style_table={'minWidth': '100%'},
                            data = df_eda_diff.to_dict('records'),
                            editable=False,
                            sort_action="native",
                            id = 'table_eda_diff',
                            page_size=10
                        ),
                        dcc.Graph(
                            id='eda-diff-graph-1',
                            #figure=fig
                        ),
                ]
            ),
            dcc.Tab(
                label='Descriptive statistics absolute differences', 
                children=[
                    dash_table.DataTable(
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                #'lineHeight': '15px',
                                #'backgroundColor': colors['background']
                                            },
                            style_table={'minWidth': '100%'},
                            data = df_eda_diff_abs.to_dict('records'),
                            editable=False,
                            sort_action="native",
                            id = 'table_eda_diff_abs',
                            page_size=10
                        ),
                        dcc.Graph(
                            id='eda-diff-abs-graph-1',
                            #figure=fig
                        ),
                ]
            ),
            dcc.Tab(label='Limits Analysis',
                children=[
                    dcc.RadioItems(
                        options = df_limits_analysis['Status_rv'].unique().tolist()+['All'],
                        value = 'All',
                        id='norm_selector',
                        inline=True,
                        style={
                            'display': 'inline-block',
                            'width': '50%',
                            'align-items': 'center', 
                        }
                    ),
                    dcc.Tabs(
                        children=[
                            dcc.Tab(
                                label='Limits desicion status', 
                                children=[
                                    dash_table.DataTable(
                                        style_data={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            #'lineHeight': '15px',
                                            #'backgroundColor': colors['background']
                                        },
                                        style_table={'minWidth': '100%'},
                                        data = df_limits_analysis.to_dict('records'),
                                        editable=False,
                                        sort_action="native",
                                        id = 'table_limits_analysis',
                                        page_size=10
                                    ),
                                    dcc.Graph(
                                        id='limits-analysis-graph-1',
                                        #figure=fig
                                    ),
                                ]
                            ),
                        ],
                    ),   
                ],
            ),
        ])
    ]),    
])

#Callback counter
@app.callback(
    Output('Counter_display', 'value'),
    Input("Selector", "value"),
)
def update_output(selected):
    dff = df_eda[df_eda['Evaluation'] == selected]
    value = dff['Results count'].unique().tolist()
    return value

# Callbacks for Tabs


#Callback Eda_tables
@app.callback(
    Output("table_eda", "data"),
    Output("table_eda_diff", "data"),
    Output("table_eda_diff_abs", "data"),
    Input("Selector", "value"),
    Input('cat_selector', 'value'),
)

def display_table(selected, category):
    eda_data = filter_df_table_viz(df_eda, selected, category)
    eda_diff_data = filter_df_table_viz(df_eda_diff, selected, category)
    eda_diff_abs_data = filter_df_table_viz(df_eda_diff_abs, selected, category)
    return eda_data, eda_diff_data, eda_diff_abs_data,

#Callback Eda_graphs
@app.callback(
    Output('eda-graph-1', 'figure'),
    Output('eda-diff-graph-1', 'figure'),
    Output('eda-diff-abs-graph-1', 'figure'),
    Input('Selector', 'value'),
    Input('cat_selector', 'value'),
)
def update_figure(selected, category):
    eda_filtered = filter_df(df_eda, selected, category)
    eda_fig = graph(style='bar', data=eda_filtered, 
                    x="Methodology", y="Results std", hue="Category",
                    title='Standard deviation of Methodologies')
    diff_filtered = filter_df(df_diff, selected, category)
    diff_fig = graph(style='box', data=diff_filtered, 
                    x='Differences', y='Results', hue='Category',
                    title='Difference between Methodologies')
    diff_abs_filtered = filter_df(df_eda_diff_abs, selected, category)
    diff_abs_fig = graph(style='bar', data=diff_abs_filtered, 
                    x="Methodology", y="Results mean", hue="Category",
                    title='Mean absolute difference between Methodologies')
    return eda_fig, diff_fig, diff_abs_fig

#Callback norm_analysis
#Callback norm_analysis table
@app.callback(
    Output("table_limits_analysis", "data"),
    Input("Selector", "value"),
    Input('cat_selector', 'value'),
    Input('norm_selector', 'value'),
)
def display_norm_table(selected, category, status):
    norm_decision = filter_df_limits_viz(df_limits_analysis, selected, category, status)
    return norm_decision

#Callback norm_analysis graphs
@app.callback(
    Output("limits-analysis-graph-1", "figure"),
    Input("Selector", "value"),
    Input('cat_selector', 'value'),
    Input('norm_selector', 'value'),
)
def update_norm_graph(selected, category, status):
    limits_filtered = filter_df_limits(df_limits_analysis, selected, category, status)
    limits_status = grid_graph(style='pie', dataframe=limits_filtered,
                                rows_grid='Methodology', cols_grid='Status_rv',
                                labels="Accuracy", values="Results_parcial",
                                title='Status')
    return limits_status





if __name__ == '__main__':
    app.run_server(debug=True)