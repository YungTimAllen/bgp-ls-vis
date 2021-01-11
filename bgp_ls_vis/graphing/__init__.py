"""Graphing tools for bgp_ls_vis"""
import networkx as nx
import matplotlib.pyplot as plt


def lsa_cost(lsa: dict) -> int:
    """Checks a given LSA to see if the igpMetric attribute is present in the lsattr

    Args:
        lsa: lsa dict object from lsdb (See: GoBGPQueryWrapper.build_nx_from_lsdb)

    Returns:
        Integer value for cost inside lsattr if present, else zero
    """
    if "igpMetric" not in lsa["lsattribute"]["link"].keys():
        lsa["lsattribute"]["link"]["igpMetric"] = 0
    return lsa["lsattribute"]["link"]["igpMetric"]


def build_nx_from_lsdb(lsdb: list) -> nx.MultiDiGraph:
    """Given list of LSAs (LSDB), builds NetworkX Graph object

    Args:
        lsdb: List<Dict> pulled from GoBGPQueryWrapper.get_lsdb call

    Returns:
        NetworkX MultiDiGraph object
    """
    graph = nx.MultiDiGraph()

    for lsa in lsdb:
        if lsa["type"] == "Node":
            b_pseudonode = False
            if "pseudonode" in list(lsa["localNode"].keys()):
                b_pseudonode = lsa["localNode"]["pseudonode"]
            graph.add_node(lsa["localNode"]["igpRouterId"], pseudonode=b_pseudonode)

    for lsa in lsdb:
        if lsa["type"] == "Link":
            graph.add_edge(
                lsa["localNode"]["igpRouterId"],
                lsa["remoteNode"]["igpRouterId"],
                cost=lsa_cost(lsa),
                pseudonode="pseudonode" in lsa["remoteNode"].keys(),
            )

    return graph


def draw_pyplot_graph(graph: nx.Graph):
    """Will open a window with the NetworkX graph object drawn

    Given NetworkX graph object, calls matplotlib.pyplot to draw then show the graph object

    Args:
        graph: NetworkX Graph object, or derivative

    Requires:
        import matplotlib.pyplot as plt
    """
    # Create dict of key=node, value=pseudonode status (bool)
    pns = {v: d["pseudonode"] for _, v, d in graph.edges(data=True)}
    # color_map is an ordered list, where order is for `node in graph`
    # This is the same order nx.draw encounters nodes
    color_map = []
    for node in graph:
        if node in list(pns.keys()):
            if pns[node]:
                # If node is a pseudonode ...
                color_map.append("blue")
            else:
                color_map.append("green")
        else:
            color_map.append("green")

    edge_labels = {
        (u, v): d["cost"] if d["cost"] > 0 else "" for u, v, d in graph.edges(data=True)
    }

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, node_color=color_map, with_labels=True, font_size=7)
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7
    )
    plt.show()


def draw_graphviz_graph(graph: nx.Graph, outfile: str):
    """Draws NetworkX graph object to file using Graphviz

    Args:
        graph: NetworkX Graph object, or derivative

    Requires:
        pip3 install pygraphviz
        redhat: graphviz-devel python3-dev graphviz pkg-config
        debian: python3-dev graphviz libgraphviz-dev pkg-config
    """

    # Weight labels
    # Edges are returned as tuples with optional data in the order (node, neighbor, data).
    # https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.Graph.edges.html
    for _, _, data in graph.edges(data=True):
        data["label"] = f"Cost: {data.get('cost', '')}"

    graph = nx.drawing.nx_agraph.to_agraph(graph)
    graph.layout("dot")
    graph.draw(outfile)
