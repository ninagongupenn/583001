import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    headers = {
        "Authorization": "Bearer " + os.environ["PINATA_JWT"],
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json={"pinataContent": data},
        timeout=30
    )
    response.raise_for_status()

    cid = response.json()["IpfsHash"]
    return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    gateways = [
        "https://gateway.pinata.cloud/ipfs/",
        "https://ipfs.io/ipfs/",
        "https://dweb.link/ipfs/"
    ]

    for gateway in gateways:
        try:
            response = requests.get(gateway + cid, timeout=30)
            response.raise_for_status()

            data = response.json()
            assert isinstance(data, dict), "get_from_ipfs should return a dict"
            return data

        except (requests.RequestException, ValueError):
            continue

    raise RuntimeError("Unable to retrieve JSON from IPFS")
