from terra_sdk.core.msgauth import SendAuthorization, GenericAuthorization
from .base import create_demux

parse_authorization = create_demux([SendAuthorization, GenericAuthorization])