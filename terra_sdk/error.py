from __future__ import annotations

import requests
from fastjsonschema.exceptions import JsonSchemaException

### Base Classes


class terra_sdkException(Exception):
    pass


class terra_sdkWarning(Warning):
    pass


### Validation Errors


class ValidationError(terra_sdkException):
    """Ambiguous validation check failed."""


class DenomIncompatibleError(ValidationError, ValueError):
    """An operation requiring compatible Coins encountered incompatible denoms."""


class InvalidAccAddress(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Account
    address (Bech32-encoded address prefixed with terra-)."""


class InvalidValAddress(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Validator
    (operator) address (Bech32-encoded address prefixed with terravaloper-)."""


class InvalidValConsAddress(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Validator
    (consensus) address (Bech32-encoded pubkey prefixed with terravalcons-)."""


class InvalidAccPubKey(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Account
    public key (Bech32-encoded pubkey prefixed with terrapub-)."""


class InvalidValPubKey(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Validator
    public key (Bech32-encoded pubkey prefixed with terravalpub-)."""


class InvalidValConsPubKey(ValidationError, ValueError):
    """An incorrect value was passed into a method that expects a valid Validator
    Consensus (Tendermint) pubkey (Bech32-encoded pubkey prefixed with terravalconspub-)."""


class InvalidParamChange(ValidationError, ValueError):
    """The parameter change does not adhere to specified schema."""


class JsonSchemaValidationError(ValidationError, JsonSchemaException):
    """Failed attempt to deserialize an object using a :class:`JsonDeserializable`."""

    def __init__(self, cls, data, message, value, name, definition, rule):
        JsonSchemaException.__init__(self, message, value, name, definition, rule)
        self.cls = cls
        self.data = data


### Terra Node IO Errors


class terra_sdkRequestError(terra_sdkException):
    def __init__(
        self, status_code: int, error_msg: str, request: requests.Request = None
    ):
        Exception.__init__(self, f"({status_code}) {error_msg}")
        self.status_code = status_code
        self.message = error_msg
        self.request = request


class UnhandledResponse(terra_sdkRequestError):
    """terra_sdk did not handle the response, but status code 200."""


class BadRequest(terra_sdkRequestError):
    """Malformed request on the part of the user. (4xx errors)"""


class LcdInternalError(terra_sdkRequestError):
    """An error occured on the server while processing the request. (5xx errors)"""


### RPC Errors


class RpcError(terra_sdkRequestError):
    """Error at the RPC node level. Status code is RPC status code, not HTTP."""


class RpcInternalError(RpcError):
    """An internal error occured in the RPC node."""


RPC_ERRORS = {-32603: RpcInternalError}


def get_rpc_error(status_code: int, error_msg: str, request: requests.Request = None):
    try:
        rpc_error = RPC_ERRORS[status_code]
    except KeyError:
        rpc_error = RpcError  # generic fallback
    return rpc_error(status_code, error_msg, request)


### Codespace Errors
class CodespaceError(terra_sdkException):
    """A more specific node error with information about the originating module."""

    def __init__(self, codespace: str, code: int, message: str, **kwargs):
        Exception.__init__(self, f"{codespace} (code {code}) {message}")
        self.codespace = codespace
        self.code = code
        self.message = message
        for k, v in kwargs.items():
            self.__setattr__(k, v)


#### TX Errors


class TxError(terra_sdkException):
    """Broadcasting error due to something wrong with the transaction's content."""

    def __init__(self, message: str, tx, broadcast_result=None):
        Exception.__init__(self, message)
        self.message = message
        self.tx = tx
        self.broadcast_result = broadcast_result


class TxCodespaceError(CodespaceError, TxError):
    """Broadcasting error due to something wrong in the transaction's message content.
    (more specific and due to an error in the message, like denom not existing)."""


class InsufficientFee(TxCodespaceError, ValueError):
    """Transaction was not processed due to insufficient fees."""


class OutOfGasException(TxCodespaceError):
    """Transaction was accepted but validator ran out of gas while processing."""


# tx errors by codespace, error code
CODESPACE_ERRORS = {"sdk": {12: OutOfGasException, 14: InsufficientFee}}


def get_codespace_error(
    codespace: str, code: int, message: str, was_from_tx=False, **kwargs
):
    try:
        error_type = CODESPACE_ERRORS[codespace][code]
    except KeyError:
        error_type = (
            TxCodespaceError if was_from_tx else CodespaceError
        )  # generic fallback
    return error_type(codespace, code, message, **kwargs)


### Misc Errors


class DenomNotFound(terra_sdkException, KeyError):
    """The requested denomination as not found."""


# Warnings


class AccountNotFoundWarning(terra_sdkWarning):
    """Account lookup was performed but ended up with an empty account."""
