"""Graphing tools for bgp_ls_vis"""
import networkx as nx
import matplotlib.pyplot as plt


def build_nx_from_lsdb(lsdb: list) -> nx.MultiDiGraph:
    """Given list of LSAs (LSDB), builds NetworkX Graph object

    Args:
        lsdb: List<Dict> pulled from GoBGPQueryWrapper.get_lsdb call

    Returns:
        NetworkX MultiDiGraph object

    Requires:
        redhat: graphviz-devel python3-dev graphviz pkg-config
        debian: python3-dev graphviz libgraphviz-dev pkg-config
    """
    graph = nx.MultiDiGraph()

    for lsa in lsdb:
        if lsa["type"] == "Link":
            graph.add_edge(
                lsa["localNode"]["igpRouterId"],
                lsa["remoteNode"]["igpRouterId"],
                color="red",
                cost=lsa["lsattribute"]["link"]["igpMetric"],
            )
        # if lsa['type'] == "Prefix":

    return graph


def draw_pyplot_graph(graph: nx.Graph):
    """Will open a window with the NetworkX graph object drawn

    Given NetworkX graph object, calls matplotlib.pyplot to draw then show the graph object

    Args:
        graph: NetworkX Graph object, or derivative
    """
    for _, _, data in graph.edges(data=True):
        data["label"] = f"Cost: {data.get('cost', '')}"

    nx.draw(graph, with_labels=True, font_weight="bold")
    plt.draw()
    plt.show()


def draw_graphviz_graph(graph: nx.Graph, outfile: str):
    """
    Args:
        graph: NetworkX Graph object, or derivative
    Requires:
        pip3 install pygraphviz
    """

    # Weight labels
    # Edges are returned as tuples with optional data in the order (node, neighbor, data).
    # https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.Graph.edges.html
    for _, _, data in graph.edges(data=True):
        data["label"] = f"Cost: {data.get('cost', '')}"

    graph = nx.drawing.nx_agraph.to_agraph(graph)
    graph.layout("dot")
    graph.draw(outfile)
