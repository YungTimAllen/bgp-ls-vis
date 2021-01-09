import gobgp_pb2
import attribute_pb2
from google.protobuf.json_format import MessageToJson, Parse


class PathHandler:
    def __init__(self, stub, table_type, family, vrf_id=None):
        self.__stub = stub
        self.table_type = table_type
        self.family = family
        self.vrf_id = vrf_id

    def get_path(self, neighbor_ip=None, prefixes=None, sort=True, json_format=True):
        request = gobgp_pb2.ListPathRequest(
            table_type=self.table_type,
            name=neighbor_ip,
            family=self.family,
            prefixes=prefixes,
            sort_type=sort,
        )

        for response in self.__stub.ListPath(request):
            if json_format:
                yield MessageToJson(response, including_default_value_fields=True)
            else:
                yield response

    def add_path(
        self,
        nlri,
        path_attributes=None,
        is_nexthop_invalid=False,
        source_asn=None,
        source_id=None,
    ):
        request = gobgp_pb2.AddPathRequest(
            table_type=self.table_type,
            vrf_id=self.vrf_id,
            path=gobgp_pb2.Path(
                nlri=nlri,
                pattrs=path_attributes,
                family=self.family,
                is_nexthop_invalid=is_nexthop_invalid,
                source_asn=source_asn,
                source_id=source_id,
            ),
        )

        if self.__stub.AddPath(request):
            return True
        else:
            return False
