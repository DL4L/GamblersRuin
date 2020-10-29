import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
import gr2

pio.templates.default = 'gridon'

# Initiate app
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server
colors = {
    'background': 'white',
    'header': 'black',
    'text1': 'black',
    'text2': '#3C85CC'
}
markdown_text1 = '''

'''


markdown_text2 = '''

'''
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        # accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)

app.layout = html.Div(

    [
        dcc.Store(id='aggregate_data'),
        html.Div([html.H1("Gambler's Ruin & Kelly Criterion")],
                 className="row header_row"),
        html.Div(
            [
                html.Div(
                    [html.Div([
                        html.H6("Parameters", className="param_title"),
                        html.P(
                            'Enter your starting money',
                            className="control_label"
                        ),
                        dcc.Input(
                            id="input_start", type="number", placeholder="Enter your starting amount of money",
                            min=0, max=10000000, step='any', value=10
                        ),
                        html.P(
                            "Select the bet amount. % of your total money",
                            className="control_label"
                        ),
                        dcc.Slider(
                            id='bet-p-slider',
                            min=0,
                            max=100,
                            step=5,
                            value=80,
                            marks={0: '0', 50: '50%', 100: '100%'}
                        ),
                        html.Div(id='bet-p-slider-output-container',
                                 className="control_label control_output_label"),
                        html.P(
                            'Select the odds of winning the bet',
                            className="control_label"
                        ),
                        dcc.Slider(
                            id='p-slider',
                            min=0,
                            max=100,
                            step=5,
                            value=70,
                            marks={0: '0', 50: '50%', 100: '100%'}
                        ),
                        html.P(id='p-slider-output-container',
                               className="control_label control_output_label"),

                        html.Br(),




                        html.P(
                            'Enter number of rounds to play',
                            className="control_label"
                        ),
                        dcc.Input(
                            id="input_rounds", type="number", placeholder="Enter number of rounds to play",
                            min=0, max=1000000, step='any', value=200
                        ),

                        html.P(
                            'Number of simulations/players',
                            className="control_label"
                        ),
                        dcc.Input(
                            id="input_trials", type="number", placeholder="Enter number of trials",
                            min=3, max=500, step='any', value=200
                        ),
                    ], className="param_section"),


                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [html.Div(id="loader-wrapper", children=[dcc.Loading(
                        className="loading-1-full",
                        id="loading-1",
                        type="graph",
                        fullscreen=True,
                        style={"opacity": "50%"},
                        children=html.Div(id="loading-output-1",
                                          )
                    )]),

                        html.Div(
                            [
                                dcc.Graph(
                                    id='count_graph',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                    )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [

                html.Div(
                    [html.Button("Description", id="toggle-hide", type="button", className="collapsible"),
                     html.Div([
                         html.Div(
                             [

                                 html.H6(
                                     id="experiment_desc",
                                     className="info_text"
                                 ),
                                 html.H6(
                                     "Try adjusting the parameters, can you find the best outcome?",
                                     id="static_experiment_desc",
                                     className="info_text",

                                 ),
                                 html.Ul(
                                     [html.Li("What is the optimal bet percentage for the given odds? Can you ensure that most simulations/players finish with more than they started?"), html.Li("What happens as you increase number of rounds?")])

                             ],
                             id="tripleContainer",
                             className="pretty_container"

                         ),
                     ],
                        id="content",
                        style={'display': 'none'}
                    ),

                    ],
                    id="infoContainer",
                    className="row description_div"
                ),
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        html.H1('Breakdown', id='breakdown_title'),
                        html.Div([
                            html.P(id='breakdown_stats')
                        ]),
                        html.Div([
                            html.P(id='breakdown_stats_1')
                        ]),
                        html.Div([
                            html.P(id='breakdown_stats_2')
                        ]),
                        html.Div([
                            html.P(id='breakdown_stats_3')
                        ]),
                        html.Div([
                            html.P(id='breakdown_stats_4')
                        ])
                    ],
                    className='pretty_container four columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [

                html.Div(
                    [
                        html.Div(
                            [


                                html.H2(
                                    "How to find the best bet percentage",
                                    id="",
                                    className="info_text",

                                ),
                                html.Br(),
                                html.H4(
                                    "The Kelly Criterion"),
                                html.H6(
                                    "The Kelly Criterion is a mathematical formula that helps investors and gamblers calculate what percentage of their money they should allocate to each investment or bet."),
                                html.A(
                                    'Investopedia', href='https://www.investopedia.com/articles/trading/04/091504.asp#:~:text=The%20Kelly%20Criterion%20is%20a,to%20each%20investment%20or%20bet.'),
                                html.A(
                                    'Wikipedia', href='https://en.wikipedia.org/wiki/Kelly_criterion'),
                                html.H6(
                                    id="kelly_optimal")

                            ],
                            id="",
                            className="pretty_container kelly_container"
                        ),



                    ],
                    id="",
                    className="row description_div kelly_container"
                ),
            ],

            className='row',
        ),

    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


@app.callback([Output('content', 'style')],
              [Input('toggle-hide', 'n_clicks')],
              [State('content', 'style')]
              )
def callback(n_clicks, style):
    if n_clicks:
        if style is None or 'display' not in style:
            style = {'display': 'none'}
        else:
            style['display'] = 'block' if style['display'] == 'none' else 'none'
        return [style]
    return [style]


@app.callback(
    [dash.dependencies.Output(
        'p-slider-output-container', 'children'), Output('kelly_optimal', 'children')],
    [dash.dependencies.Input('p-slider', 'value')])
def update_p_slider_output(value):
    kelly_p = round(((value)-(100-value)), 2)
    if kelly_p <= 0:
        kelly_p = 0
    kelly = "The optimal bet percentage, for the current selected odds, is %s%%." % (
        str(int(kelly_p)))
    return 'You have selected {}%'.format(value), kelly


@app.callback(
    dash.dependencies.Output('bet-p-slider-output-container', 'children'),
    [dash.dependencies.Input('bet-p-slider', 'value')])
def update_bet_p_slider_output(value):
    return 'You have selected {}%'.format(value)


@app.callback(
    dash.dependencies.Output('experiment_desc', 'children'),
    [dash.dependencies.Input('input_trials', 'value'), dash.dependencies.Input('input_rounds', 'value'),
     dash.dependencies.Input('p-slider', 'value'), dash.dependencies.Input('input_start', 'value'), dash.dependencies.Input('bet-p-slider', 'value')])
def update_exp_desc(v1, v2, v3, v4, v5):
    # return "Imagine %s people independently playing %s rounds of a game with %s%% chance of winning each round. They start with £%s and bet %s%%  of their money each round." % (v1, v2, v3, v4, v5)
    return html.Ul([html.Li("Starting Money: %s" % (v4)), html.Li("Bet Amount : %s%%" % (v5)), html.Li("Odds of Winning Each Round: %s%%" % (v3)),
                    html.Li("Number of Rounds: %s" % (v2)), html.Li("Number of Simulations: %s" % (v1))])


"""
@app.callback(
    [
        Output('count_graph', 'figure'), Output('main_graph', 'figure'),
        Output('breakdown_stats', 'children'), Output(
            'breakdown_stats_1', 'children'), Output('breakdown_stats_2', 'children'),
        Output('breakdown_stats_3', 'children'), Output('breakdown_stats_4', 'children'), Output("loading-output-1", "children")],
    [dash.dependencies.Input('input_trials', 'value'), dash.dependencies.Input('input_rounds', 'value'),
     dash.dependencies.Input('p-slider', 'value'), dash.dependencies.Input('input_start', 'value'), dash.dependencies.Input('bet-p-slider', 'value')])
def update_after_go(trials, rounds, p, start, bet_p):
    if trials and rounds and start:
        p = p/100
        bet_p = bet_p/100
        loading = True

        gr = gr2.GR2(num_trials=trials, games_per_trial=rounds,
                     win_prob=p, start_amount=start, bet_percent=bet_p)
        out = gr.simulate()
        loading = False

        
        median_per_round = gr.median_per_round(out)
        lower_q = gr.lower_quartile(out)
        upper_q = gr.upper_quartile(out)
        df_median = pd.DataFrame(
            [median_per_round.keys(), pd.Series(upper_q), pd.Series(median_per_round),  pd.Series(lower_q)]).T
        df_median.columns = ["Round", "Upper Quartile", "Median",
                             "Lower Quartile"]
        fig1 = px.line(df_median, x="Round",
                       y=["Upper Quartile", "Median", "Lower Quartile"], title="Log Median Winnings by Round")
        fig1.update_yaxes(title_text="Log Winnings")

        winnings = gr.get_winnings_for_each_trial(np.log(out[-1]))
        fig2 = px.scatter(
            winnings, title="Log Winnings After %s Rounds" % (rounds))
        fig2.update_layout(showlegend=False)
        fig2.update_xaxes(title_text='Person / Trial')
        fig2.update_yaxes(title_text='Log Winnings'.format(rounds))

        top = gr.max_result_formatted(out[-1])
        first, second, third = '1st place: £' + \
            top[0], '2nd place: £' + top[1], '3rd place: £' + top[2]
        # max_result = 'Highest Earner: £' + gr.max_result_formatted(out[-1])
        median = gr.median_result(out[-1]).round(2)
        median = gr.format_price(median)
        median_ret = 'Median Earnings: £' + median
        lost = gr.percent_lost(out[-1])
        lost_ret = '%s out of %s players finished with less than they started' % (
            lost, trials)

        return fig1, fig2, first, second, third, median_ret, lost_ret, ''
    else:
        return {}, {}, '', '', '', '', '', ''
"""


@app.callback(
    [
        Output('count_graph', 'figure'), Output('main_graph', 'figure'),
        Output('breakdown_stats', 'children'), Output(
            'breakdown_stats_1', 'children'), Output('breakdown_stats_2', 'children'),
        Output('breakdown_stats_3', 'children'), Output('breakdown_stats_4', 'children'), Output("loading-output-1", "children")],
    [dash.dependencies.Input('input_trials', 'value'), dash.dependencies.Input('input_rounds', 'value'),
     dash.dependencies.Input('p-slider', 'value'), dash.dependencies.Input('input_start', 'value'), dash.dependencies.Input('bet-p-slider', 'value')])
def update_after_go(trials, rounds, p, start, bet_p):
    if trials and rounds and start:
        p = p/100
        bet_p = bet_p/100
        loading = True

        gr = gr2.GR2(num_trials=trials, games_per_trial=rounds,
                     win_prob=p, start_amount=start, bet_percent=bet_p)
        out = gr.simulate_quick()
        loading = False

        end_results = [i[-1] for i in out]
        results_by_round = [[i[j] for i in out] for j in range(len(out[0]))]
        median_per_round = gr.quick_median_per_round(results_by_round)
        lower_q = gr.quick_lower_quartile(results_by_round)
        upper_q = gr.quick_upper_quartile(results_by_round)
        df_median = pd.DataFrame(
            [median_per_round.keys(), pd.Series(upper_q), pd.Series(median_per_round),  pd.Series(lower_q)]).T
        df_median.columns = ["Round", "Upper Quartile", "Median",
                             "Lower Quartile"]
        fig1 = px.line(df_median, x="Round",
                       y=["Upper Quartile", "Median", "Lower Quartile"], title="Log Median Winnings by Round")
        fig1.update_yaxes(title_text="Log Winnings")

        winnings = gr.get_winnings_for_each_trial(np.log(end_results))
        fig2 = px.scatter(
            winnings, title="Log Winnings After %s Rounds" % (rounds))
        fig2.update_layout(showlegend=False)
        fig2.update_xaxes(title_text='Person / Trial')
        fig2.update_yaxes(title_text='Log Winnings'.format(rounds))

        top = gr.max_result_formatted(end_results)
        first, second, third = '1st place: £' + \
            top[0], '2nd place: £' + top[1], '3rd place: £' + top[2]
        # max_result = 'Highest Earner: £' + gr.max_result_formatted(out[-1])
        median = gr.median_result(end_results).round(2)
        median = gr.format_price(median)
        median_ret = 'Median Earnings: £' + median
        lost = gr.percent_lost(end_results)
        lost_ret = '%s out of %s players finished with less than they started' % (
            lost, trials)

        return fig1, fig2, first, second, third, median_ret, lost_ret, ''
    else:
        return {}, {}, '', '', '', '', '', ''


if __name__ == '__main__':
    app.run_server(debug=True)
