"""Web-frontend dashboard for Dash/Flask graphing"""
from pprint import pprint

import networkx
import yaml
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Project internal imports
from ..proto import GoBGPQueryWrapper
from ..graphing import *


def main(
    rpc: GoBGPQueryWrapper = None,
    nx_graph: networkx.Graph = None,
    host="127.0.0.1",
    port=8050,
):
    """Builds dash frontend and runs

    Args:
        rpc: proto.GoBGPQueryWrapper object - used for callback when eventually implemented
        nx_graph: NetworkX Graph object, given by graphing.build_nx_from_lsdb
        host: Local IPv4 address on which to serve the Dash service
        port: Local TCP port on which to serve the Dash service
    """
    elements = []

    for node in nx_graph.nodes():
        elements.append(
            {
                "data": {"id": node, "label": node},
            },
        )
    for source_edge, target_edge in nx_graph.edges():
        elements.append(
            {
                "data": {
                    "source": source_edge,
                    "target": target_edge,
                    "cost": nx_graph[source_edge][target_edge][0]["cost"],
                }
            }
        )

    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            html.P("Mad topology:"),
            cyto.Cytoscape(
                id="cytoscape",
                elements=elements,
                layout={
                    "name": "cose",
                    "componentSpacing": 20,
                },
                style={
                    "width": "100%",
                    "height": "100%",
                    "position": "absolute",
                    "left": 0,
                    "top": 0,
                    "z-index": 999,
                },
                stylesheet=[
                    {
                        "selector": "node",
                        "style": {
                            "label": "data(label)",
                            "text-halign": "center",
                            "text-valign": "center",
                            "background-color": "#4272f5",
                            "padding": 20,
                        },
                    },
                    {
                        "selector": "edge",
                        "style": {
                            "source-label": "data(cost)",
                            "source-text-offset": 45,
                            "width": "2%",
                        },
                    },
                ],
            ),
        ]
    )

    app.run_server(debug=True, host=host, port=port)
