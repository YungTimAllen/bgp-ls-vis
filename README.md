[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Docstrings: Google](https://img.shields.io/badge/Docstrings-Google-green)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)
[![Discord](https://img.shields.io/discord/245189311681527808.svg?label=Networking&logo=discord)](https://discord.me/networking)
# BGP Link-State AFI Visualiser (bgp-ls-vis)

PoC collection of scripts and modules that perform the following

1. Connects via gRPC to a running GoBGP instance and submits a query for the contents of the BGP-LS table
   * or, loads from file a cached BGP-LS table (To dump, `proto.GoBGPQueryWrapper.debug()`)
2. Filters the returned structured data for only those values which are useful and required
3. Builds a NetworkX graph object representative of the NLRI extracted
4. Draws visual representation of said NetworkX graph object to screen or file

## Minimal Example

```python
# RPC tools
from proto import GoBGPQueryWrapper
# Graphing tools
import graphing

gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
rpc = GoBGPQueryWrapper(**gobgp_target)

lsdb = rpc.get_lsdb()
graph = graphing.build_nx_from_lsdb(lsdb)

graphing.draw_pyplot_graph(graph)
```

## Requirements and Resources

`pip install -r requirements.txt`

---

* [NetworkX](https://networkx.org/) + matplotlib (`graphing.draw_pyplot_graph`)

```buildoutcfg
   pip3 install networkx matplotlib
```

To get pygraphviz working ...

```buildoutcfg
    Requires:
        redhat: graphviz-devel python3-dev graphviz pkg-config
        debian: python3-dev graphviz libgraphviz-dev pkg-config
```

* [GoBGP](https://github.com/osrg/gobgp)
* [gRPCio](https://pypi.org/project/grpcio/)

You may need to prepare your own gRPC python interfaces if ours dont work. This process is described in the GoBGP guide 
on [interfacing from your favourite language](https://github.com/osrg/gobgp/blob/master/docs/sources/grpc-client.md#python).

```buildoutcfg
    - https://www.grpc.io/docs/languages/python/quickstart/
    python3 -m pip install grpcio
    python3 -m pip install grpcio-tools
    - Clone the gobgp repo and prep the rpc interface to python
    gobgp\api> python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. *.proto
```

## Why?

Because we can, and it's fun

## Lab & Testing Topology

### Networking

Testing topologies are running ISIS, and 1 node peers with BGP-LS to the Ubuntu guest running GoBGP.

* Clouds are a breakout for the virtual environment, allowing RPC calls from the real-world.
* All nodes must support ISIS, but only the node peering to the GoBGP systems needs to support and peer BGP-LS
  * e.g Only R2 has an iBGP peering for `address-family link-state link-state` (BGP-LS) to the GoBGP instance.

![Lab Topology 1](https://i.imgur.com/H9x8ash.png)

*This topology is described under `tests/lab_topology_definitions/lab_topology.yaml`*

![Lab Topology 2](https://i.imgur.com/Zh4pD1R.png)

*This topology is described under `tests/lab_topology_definitions/18-node-topology.yaml`*

### GoBGP 

GoBGP configuration file is defined by the following YAML

```yaml
global:
  config:
    as: 65001
    router-id: 10.2.9.9
neighbors:
- config:
    neighbor-address: 10.2.9.2
    peer-as: 65001
  transport:
    config:
      local-address: 10.2.9.9
  afi-safis:
  - config:
      afi-safi-name: ls
```

---

## Progress so far:

- Supports loading BGP-LS table dumps from file, an alternative to RPC connections
- Resolves ISIS TLV 137 for actual hostnames
- Supports Psuedonodes

`graphing.draw_pyplot_graph` for BGP-LS table dump `tests/junos_bgpls_nopsn.yml` draws the following

![](https://i.imgur.com/ctltjR8.png)

`graphing.draw_pyplot_graph` for BGP-LS table dump `tests/18-node-isis-w-bcast-segment.yaml` draws the following

![](https://i.imgur.com/GBv0tN9.png)

## Contributors

* YungTimAllen
* FlyingScotsman