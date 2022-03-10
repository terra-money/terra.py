from terra_sdk.core.distribution.proposals import CommunityPoolSpendProposal
from terra_sdk.core.gov.proposals import TextProposal
from terra_sdk.core.params.proposals import ParameterChangeProposal

from terra_proto.cosmos.distribution.v1beta1 import CommunityPoolSpendProposal as CommunityPoolSpendProposal_pb
from terra_proto.cosmos.gov.v1beta1 import TextProposal as TextProposal_pb
from terra_proto.cosmos.params.v1beta1 import ParameterChangeProposal as ParameterChangeProposal_pb
from .base import create_demux, create_demux_proto

parse_content = create_demux(
    [
        CommunityPoolSpendProposal,
        TextProposal,
        ParameterChangeProposal,
    ]
)

parse_content_proto = create_demux_proto(
    [
        [CommunityPoolSpendProposal.type_url, CommunityPoolSpendProposal_pb],
        [TextProposal.type_url, TextProposal_pb],
        [ParameterChangeProposal.type_url, ParameterChangeProposal_pb],
    ]
)
