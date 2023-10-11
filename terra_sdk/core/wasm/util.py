import json
from typing import Union

def parse_msg(msg: Union[dict, str, bytes]) -> dict:
    try:
        return json.loads(msg)
    except:
        return msg
