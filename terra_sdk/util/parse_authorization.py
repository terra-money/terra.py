from terra_sdk.core.authz import GenericAuthorization, SendAuthorization, StakeAuthorization
from terra_proto.cosmos.authz.v1beta1 import GenericAuthorization as GenericAuthorization_pb
from terra_proto.cosmos.bank.v1beta1 import SendAuthorization as SendAuthorization_pb
from terra_proto.cosmos.staking.v1beta1 import StakeAuthorization as StakeAuthorization_pb

from .base import create_demux, create_demux_proto, create_demux_amino

parse_authorization = create_demux([GenericAuthorization, SendAuthorization, StakeAuthorization])
parse_authorization_amino = create_demux_amino([GenericAuthorization, SendAuthorization])  # no amino for StakeAuthorization


parse_authorization_proto = create_demux_proto([GenericAuthorization, SendAuthorization, StakeAuthorization])
"""
parse_authorization_proto = create_demux_proto(
    [
        [GenericAuthorization.type_url, GenericAuthorization_pb],
        [SendAuthorization.type_url, SendAuthorization_pb],
        [StakeAuthorization.type_url, StakeAuthorization_pb],
    ]
)
"""