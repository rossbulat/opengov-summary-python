import httpx

# Base URL for PolkAssembly API to fetch referendum data
POLKASSEMBLY_BASE_URL = "https://api.polkassembly.io/api/v1"


def get_referendum(ref_id: int):
    url = "/posts/on-chain-post"
    params = {"postId": ref_id, "proposalType": "referendums_v2"}
    headers = {"x-network": "polkadot"}

    with httpx.Client(base_url=POLKASSEMBLY_BASE_URL, timeout=None) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
