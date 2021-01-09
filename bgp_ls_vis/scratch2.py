"""PoC Script for this project, super-alpha code~"""
import yaml
from proto import GoBGPQueryWrapper

# Graphing tools
import graphing


def main():
    """First method called when ran as script"""
    rpc = GoBGPQueryWrapper("172.20.10.2", "50051")

    lsdb = rpc.get_lsdb()
    graph = graphing.build_nx_from_lsdb(lsdb)

    print(yaml.dump(lsdb))

    # Only works on Linux, pita to get working on Windows
    # graphing.draw_graphviz_graph(graph, "multi.png")

    graphing.draw_pyplot_graph(graph)


if __name__ == "__main__":
    main()
