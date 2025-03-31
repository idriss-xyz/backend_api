import requests


def get_farcaster_verified_addresses_from_api(fid):
    url = f"https://api.warpcast.com//fc/primary-address?fid={fid}&protocol=ethereum"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_fid(fc_name):
    """
    Fetches fid for the given fcname.

    Args:
        identity (str): The wallet identity to query.

    Returns:
        int: fid of user.
    """
    transferResponse = requests.get(
        f"https://fnames.farcaster.xyz/transfers/current?name={fc_name}", timeout=10
    )

    if not transferResponse.ok:
        transferResponse.raise_for_status()
    transferData = transferResponse.json()
    print("transferdata", transferData)
    return {"fid": transferData["transfer"]["to"], "username": fc_name}
