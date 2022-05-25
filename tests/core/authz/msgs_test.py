from math import expm1
from terra_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)


def test_deserializes_msg_exec_authorized_examples(load_json_examples):
    examples = load_json_examples("./MsgExecAuthorized.data.json")
    for example in examples:
        target = MsgExecAuthorized.from_data(example).to_data()
        assert target["@type"] == "/cosmos.authz.v1beta1.MsgExec"
        assert target["grantee"] == example["grantee"]


def test_deserializes_msg_grant_authorization_examples(load_json_examples):
    examples = load_json_examples("./MsgGrantAuthorization.data.json")
    for example in examples:
        target = MsgGrantAuthorization.from_data(example).to_data()

        assert target["@type"] == "/cosmos.authz.v1beta1.MsgGrant"
        assert target["grant"] == example["grant"]
        assert target["granter"] == example["granter"]
        assert target["grantee"] == example["grantee"]


def test_deserializes_msg_revoke_authorization_examples(load_json_examples):
    examples = load_json_examples("./MsgRevokeAuthorization.data.json")
   
    for example in examples:
        target = MsgRevokeAuthorization.from_data(example).to_data()

        assert target["@type"] == "/cosmos.authz.v1beta1.MsgRevoke"
        assert target["granter"] == example["granter"]
        assert target["grantee"] == example["grantee"]
        assert target["msg_type_url"] == example["msg_type_url"]