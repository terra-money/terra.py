Usage with Pagination
=====================

You can query information with Pagination to get information partially.

PaginationOption
----------------

.. autoclass:: terra_sdk.client.lcd.params.APIParams
    :members:

.. autoclass:: terra_sdk.client.lcd.params.PaginationOptions
    :members:

You can use PaginationOptions as APIParams for params of query functions.

.. code-block:: python
    :emphasize-lines: 5,8

    from terra_sdk.client.lcd import LCDClient, PaginationOptions

    terra = LCDClient(
        url="https://lcd.terra.dev/",
        chain_id="columbus-5",
    )


    result, pagination  = terra.gov.proposals()

    while pagination["next_key"] is not None:
        pagOpt = PaginationOptions(key=pagination["next_key"])
        result, pagination = terra.gov.proposals(params=pagOpt)
        pagOpt.key = pagination["next_key"]
        print(result)

