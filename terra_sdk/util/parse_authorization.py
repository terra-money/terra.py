from terra_sdk.core.authz import GenericAuthorization, SendAuthorization

from .base import create_demux

parse_authorization = create_demux([GenericAuthorization, SendAuthorization])
