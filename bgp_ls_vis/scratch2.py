"""x"""
import yaml
from proto import GoBGPQueryWrapper
# Graphing tools
import networkx as nx
import matplotlib.pyplot as plt


def main():
    rpc = GoBGPQueryWrapper("172.20.10.2", "50051")
    lsdb = rpc.get_lsdb()

    print(yaml.dump(lsdb, sort_keys=False))

    build_nx_from_lsdb(lsdb)

def build_nx_from_lsdb(lsdb:list):
    """

    Args:
        lsdb:

    Returns:

    Requires:
        redhat: graphviz-devel python3-dev graphviz pkg-config
        debian: python3-dev graphviz libgraphviz-dev pkg-config

    """
    graph = nx.MultiDiGraph()

    for lsa in lsdb:
        if lsa['type'] == "Link":
            graph.add_edge(lsa['localNode']['igpRouterId'], lsa['remoteNode']['igpRouterId'], color="red")
        # if lsa['type'] == "Prefix":

    nx.draw(graph, with_labels=True, font_weight="bold")
    plt.draw()
    plt.show()


if __name__ == "__main__":
    main()
