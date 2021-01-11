"""RPC Connection, scratch testing script"""
import yaml

# RPC tools
from proto import GoBGPQueryWrapper

# Graphing tools
import graphing


def main():
    """First method called when ran as script"""
    gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
    rpc = GoBGPQueryWrapper(**gobgp_target)

    lsdb = rpc.get_lsdb()
    graph = graphing.build_nx_from_lsdb(lsdb)

    print(yaml.dump(lsdb))  # Print filtered LSDB to stdout, optional dev assistance

    graphing.draw_pyplot_graph(graph)


if __name__ == "__main__":
    main()
