from terra_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)


def test_deserializes_msg_exec_authorized_examples(load_json_examples):
    examples = load_json_examples("./MsgExecAuthorized.data.json")
    for example in examples:
        assert MsgExecAuthorized.from_data(example).to_data() == example


def test_deserializes_msg_grant_authorization_examples(load_json_examples):
    examples = load_json_examples("./MsgGrantAuthorization.data.json")
    for example in examples:
        assert MsgGrantAuthorization.from_data(example).to_data() == example


def test_deserializes_msg_revoke_authorization_examples(load_json_examples):
    examples = load_json_examples("./MsgRevokeAuthorization.data.json")
    for example in examples:
        assert MsgRevokeAuthorization.from_data(example).to_data() == example
