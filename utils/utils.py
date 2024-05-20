from utils.constants import DEFAULT_NETWORK, TOKEN_ROUTE


def get_token_router(network, buy_token, sell_token):
    sell_token = TOKEN_ROUTE[f"{network}:{sell_token.lower()}"]
    buy_token = TOKEN_ROUTE[f"{network}:{buy_token.lower()}"]
    network = DEFAULT_NETWORK
    return network, buy_token, sell_token