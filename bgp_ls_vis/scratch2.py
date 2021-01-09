"""PoC Script for this project, super-alpha code~"""
from proto import GoBGPQueryWrapper

# Graphing tools
import graphing


def main():
    """First method called when ran as script"""
    rpc = GoBGPQueryWrapper("172.20.10.2", "50051")

    lsdb = rpc.get_lsdb()
    graph = graphing.build_nx_from_lsdb(lsdb)

    graphing.draw_graph(graph)


if __name__ == "__main__":
    main()
