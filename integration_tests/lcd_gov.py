from terra_sdk.client.lcd import LCDClient, PaginationOptions


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    pagOpt = PaginationOptions(limit=2, count_total=True)

    # result = terra.gov.proposals()
    # print("whole proposals", result)
    # result = terra.gov.proposals(PaginationOptions(limit=2))
    # print("first 2 params", result)
    # result = terra.gov.proposal(5333)
    # print('just one proposal', result)

    # FIXME: Unclosed client session
    # result = terra.gov.proposer(5333)
    # print('proposer', result)

    # FIXME: Unclosed client session
    # result = terra.gov.deposits(5339)
    # print('deposits', result)
    # result = terra.gov.deposits(5339, params=pagOpt)
    # print('deposits with pagination', result)

    # TODO: test when core/gov/Vote is done
    # result = terra.gov.votes(5333)
    # print('votes', result)
    # result = terra.gov.votes(5333, pagOpt)
    # print('votes with pagination', result)

    # result = terra.gov.tally(5333)
    # print(result)

    # result = terra.gov.deposit_parameters()
    # print(result)
    # result = terra.gov.voting_parameters()
    # print(result)
    # result = terra.gov.tally_parameters()
    # print(result)
    # result = terra.gov.parameters()
    # print(result)


main()
