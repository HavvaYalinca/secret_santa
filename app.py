from random import Random, shuffle
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

participants = ["A", "B", "G", "H", "O"]
participant_order = participants.copy()


def get_target_for_person(participants, buyer):
    b_index = participants.index(buyer)
    return participants[(b_index + 1) % len(participants)]


# ----------------------------------------------------

part_1 = html.Div(
    [
        html.H1(children="Secret Santa Generator"),
        # TODO: interactive participant name list
        # html.H6('Enter names of the participants'),
        dbc.Row(
            [
                dbc.Col(html.P("Participants: " + ", ".join(participants))),
                dbc.Col(
                    dbc.Input(id="seed", placeholder="Random number", type="number")
                ),
            ]
        ),
        html.Div(
            dbc.Button("Shuffle!", id="shuffle_button", n_clicks=0),
            className="d-grid gap-2",
        ),
        html.Div(
            html.Img(id="shuffle_gif", src=None, style={"width": "50%"}),
            style={"textAlign": "center"},
        ),
    ]
)
part_2 = html.Div(
    id="div_pt2",
    children=[
        # Choose your name
        html.H2("Find out your match!"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="person_dropdown",
                        options=participants,
                        placeholder="Choose your name",
                        disabled=False,
                    ),
                    width=10,
                ),
                dbc.Col(dbc.Button("Submit", id="fetch_match_button"), width=2),
            ]
        ),
        html.Div(
            [
                html.P("Your match is   .", style={"display": "inline-block"}),
                html.H6(
                    id="result_name",
                    style={"display": "inline-block", "color": "blue", "fontSize": 18},
                ),
            ],
            style={"display": "inline-block"},
        ),
    ],
    style={"display": "none"},
)

app.layout = dbc.Col(
    [part_1, part_2],
    width={"size": 8, "offset": 2},
)

# ----------------------------------------------------

# Enter participant names
# TODO

# Shuffle the names
@app.callback(
    [Output("shuffle_gif", "src"), Output("div_pt2", "style")],
    Input("shuffle_button", "n_clicks"),
    State("seed", "value"),
)
def show_shuffling_gif(n_clicks, seed):
    if n_clicks:
        Random(seed).shuffle(participant_order)
        return "https://media.giphy.com/media/bG5rDPx76wHMZtsXmr/giphy.gif", {
            "display": "block"
        }
    else:
        return None, {"display": "none"}


# Find out your person's name
@app.callback(
    Output("result_name", "children"),
    Input("fetch_match_button", "n_clicks"),
    [
        State("person_dropdown", "value"),
        State("result_name", "children"),
    ],
)
def find_your_match(n_clicks, chooser, existing):
    if n_clicks == 1:  # you can have only one look!
        return get_target_for_person(participant_order, chooser)
    else:
        return existing


# Disable dropdown, shuffle and submit buttons after a name is shown
# TODO: use browser data storage so refreshing the page doesnt give you another chance to have a peek.
@app.callback(
    [
        Output("person_dropdown", "disabled"),
        Output("fetch_match_button", "disabled"),
        Output("shuffle_button", "disabled"),
    ],
    Input("result_name", "children"),
)
def disable_dd(name):
    return bool(name), bool(name), bool(name)


# ----------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=False)
