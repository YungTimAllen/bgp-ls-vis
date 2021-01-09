"""Testing script for prototype

Notes:
    https://www.grpc.io/docs/languages/python/quickstart/
    python3 -m pip install grpcio
    python3 -m pip install grpcio-tools
    - Clone the gobgp repo and prep the rpc protocols to python
    gobgp\api>python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. *.proto
"""
import json

import grpc
import gobgp_pb2 as gobgp
from google.protobuf.json_format import MessageToDict
import gobgp_pb2_grpc
import attribute_pb2


def main():
    """

    Notes:
        Getting all neighbors and attributes
        https://github.com/dbarrosop/gobgp-grpc-demo/blob/master/sample_scripts/get_neighbor.py

    """
    channel = grpc.insecure_channel("172.20.10.2:50051")
    stub = gobgp_pb2_grpc.GobgpApiStub(channel)

    request = gobgp.ListPathRequest(
        table_type=gobgp.LOCAL,
        name="",
        family=gobgp.Family(afi=gobgp.Family.AFI_LS, safi=gobgp.Family.SAFI_LS),
        prefixes=None,
        sort_type=True,
    )

    for response in stub.ListPath(request):
        d = MessageToDict(response, including_default_value_fields=True)
        print(json.dumps(d))

if __name__ == "__main__":
    main()
