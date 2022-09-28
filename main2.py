"""

Created at 2022. 09. 27.
@original_author: Mohammad Ashraf Abdin
@title: 
@description: 

"""
from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash import html, Output, Input, no_update, dcc, State
import marqo
import pprint
import dash_renderjson

mq = marqo.Client(url='http://localhost:8882')

server = Flask(__name__)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MINTY],
    server=server
)

navbar = dbc.NavbarSimple(
    children=[
    ],
    brand="marqo demo",
    brand_href="#",
    color="primary",
    dark=True,
)
tab1 = dbc.Card(
    dbc.CardBody(
        [
            dcc.Input(
                id="title",
                type="text",
                placeholder="title",
            ),
            dcc.Input(
                id="description",
                type="text",
                placeholder="Description",
            ),
            dcc.Input(
                id="_id",
                type="text",
                placeholder="_id",
            ),
            dbc.Button("Add", id="add_doc"),
            html.Div(id='page-content'),

        ],
    ),
    className='t1',
)
tab2 = dbc.Card(
    dbc.CardBody(
        [
            dbc.Container([
                dcc.Input(
                    id="get_document_id",
                    type="text",
                    placeholder="document id",
                ),
            ]),
            dbc.Container([
                dcc.Input(
                    id="get_specific_fields",
                    type="text",
                    placeholder="Search specific fields",
                )]),
            dbc.Container([
                dcc.Input(
                    id="delete_documents",
                    type="text",
                    placeholder="Delete documents",
                )]),
            dbc.Button("go", id="go"),
            html.Div(id="output"),

        ]
    ),
    className='t2',
)
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1, label='Add Documents', tab_id='t1'),
        dbc.Tab(tab2, label='Search', tab_id='t2'),
    ],
    id='tabs',
    active_tab='t1',
)

app.layout = html.Div([
    navbar,
    tabs,
    dcc.Interval(
        id='Update Date'
        , disabled=True
    ),
])


@app.callback(Output('page-content', 'children'),
              Input('add_doc', 'n_clicks'),
              [
                  State('title', 'value'),
                  State('description', 'value'),
                  State('_id', 'value'),
              ])
def first_page(add_button, *values):
    if add_button is not None:
        if values[2] != "":
            mq.index("test_index").add_documents([
                {
                    "Title": values[0],
                    "Description": values[1],
                    "_id": values[2]
                }]
            )
            return "added"
        else:
            mq.index("test_index").add_documents([
                {
                    "Title": values[0],
                    "Description": values[1],
                }]
            )
            return "added"
    return no_update


@app.callback(Output('output', 'children'),
              Input('go', 'n_clicks'),
              [
                  State('get_document_id', 'value'),
                  State('get_specific_fields', 'value'),
                  State('delete_documents', 'value'),
              ])
def second_page(enter_button, *values):
    result = "None"
    if enter_button is not None:
        try:
            if values[0] is not None and values[0] != "":
                result = mq.index("test_index").get_document(values[0])
            elif values[1] is not None and values[1] != "":
                result = mq.index("test_index").search(values[1], searchable_attributes=['Title'])
            elif values[2] is not None and values[2] != "":
                result = mq.index("test_index").delete_documents(ids=[values[2]])
            else:
                return no_update
        except:
            return dash_renderjson.DashRenderjson(id="input", data="Not exist", max_depth=-1,
                                                  invert_theme=True)
        return dash_renderjson.DashRenderjson(id="input", data=result, max_depth=-1,
                                              invert_theme=True)
    else:
        return no_update


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=9000, debug=False)
