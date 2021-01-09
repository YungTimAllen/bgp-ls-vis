"""t"""
# Standard Imports
from collections import defaultdict
from google.protobuf.json_format import MessageToDict

# RPC & GoBGP imports
import grpc
from . import gobgp_pb2 as gobgp
from . import gobgp_pb2_grpc
from . import attribute_pb2


class GoBGPQueryWrapper:
    """x"""

    def __init__(self, target_ipv4_address, target_rpc_port):
        channel = grpc.insecure_channel(f"{target_ipv4_address}:{target_rpc_port}")
        self.stub = gobgp_pb2_grpc.GobgpApiStub(channel)

    @staticmethod
    def __build_rpc_request() -> gobgp.ListPathRequest:
        """x"""
        request = gobgp.ListPathRequest(
            table_type=gobgp.LOCAL,
            name="",
            family=gobgp.Family(afi=gobgp.Family.AFI_LS, safi=gobgp.Family.SAFI_LS),
            prefixes=None,
            sort_type=True,
        )
        return request

    def __get_bgp_ls_lsdb(self) -> list:
        """

        Returns:

        """
        request = self.__build_rpc_request()
        response = self.stub.ListPath(request)
        rtn = [MessageToDict(nlri) for nlri in response]
        return rtn

    def get_lsdb(self) -> list:
        """

        Returns:

        """
        brib = self.__get_bgp_ls_lsdb()

        filtered_lsdb = []

        for lsa in brib:

            nlri = dict(lsa["destination"]["paths"][0]["nlri"]["nlri"])

            if nlri["@type"] == "type.googleapis.com/gobgpapi.LsLinkNLRI":
                filtered_lsdb.append(
                    {
                        "type": "Link",
                        "localNode": nlri["localNode"],
                        "remoteNode": nlri["remoteNode"],
                        "linkDescriptor": nlri["linkDescriptor"],
                    }
                )
            elif nlri["@type"] == "type.googleapis.com/gobgpapi.LsPrefixV4NLRI":
                filtered_lsdb.append(
                    {
                        "type": "Prefix",
                        "localNode": nlri["localNode"],
                        "prefixDescriptor": nlri["prefixDescriptor"],
                    }
                )

            # print(nlri)

        return filtered_lsdb

        # return brib
