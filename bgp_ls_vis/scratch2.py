"""PoC Script for this project, super-alpha code~"""
from proto import GoBGPQueryWrapper

# Graphing tools
import networkx as nx
import matplotlib.pyplot as plt


def main():
    """First method called when ran as script"""
    rpc = GoBGPQueryWrapper("172.20.10.2", "50051")
    lsdb = rpc.get_lsdb()

    graph = build_nx_from_lsdb(lsdb)

    draw_graph(graph)


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


if __name__ == "__main__":
    main()
