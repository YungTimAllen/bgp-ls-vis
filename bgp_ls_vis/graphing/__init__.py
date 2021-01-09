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
            )
        # if lsa['type'] == "Prefix":

    return graph


def draw_graph(graph: nx.Graph):
    """Will open a window with the NetworkX graph object drawn

    Given NetworkX graph object, calls matplotlib.pyplot to draw then show the graph object

    Args:
        graph: NetworkX Graph object, or derivative
    """
    nx.draw(graph, with_labels=True, font_weight="bold")
    plt.draw()
    plt.show()
