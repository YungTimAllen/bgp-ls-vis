import yaml
from proto import GoBGPQueryWrapper
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
from pprint import pprint
import graphing
import plotly.graph_objects as go


def main():
    """First method called when ran as script"""
    rpc = GoBGPQueryWrapper("192.168.242.132", "50051")

    elements = [
        # The nodes elements
        {'data': {'id': 'one', 'label': 'Node 1'}, },
        {'data': {'id': 'two', 'label': 'Node 2'}, },

        # The edge elements
        {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
    ]

    lsdb = rpc.get_lsdb()

    print(yaml.dump(rpc.debug()))

    mad_shit = graphing.build_nx_from_lsdb(lsdb)

    even_madder_shit = []

    for node in mad_shit.nodes():
        even_madder_shit.append(
            {'data': {'id': node, 'label': node}, },
        )

    for edge in mad_shit.edges():
        even_madder_shit.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': f"{edge[0]} to {edge[1]}"}}
        )

    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            html.P("Mad topology:"),
            cyto.Cytoscape(
                id="cytoscape",
                elements=even_madder_shit,
                layout={'name': 'breadthfirst'},
                style={'width': '1024px', 'height': '768px'}
            ),
        ]
    )

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
