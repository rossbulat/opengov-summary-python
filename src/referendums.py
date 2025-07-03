from typing import Optional

import httpx
import openai

# Base URL for PolkAssembly API to fetch referendum data
POLKASSEMBLY_BASE_URL = "https://api.polkassembly.io/api/v1"


def get_referendum(ref_id: int):
    """Fetches referendum data from PolkAssembly API and returns relevant metadata"""
    url = "/posts/on-chain-post"
    params = {"postId": ref_id, "proposalType": "referendums_v2"}
    headers = {"x-network": "polkadot"}

    with httpx.Client(base_url=POLKASSEMBLY_BASE_URL, timeout=None) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


def summarise_referendum(content: str) -> Optional[str]:
    """Generates a summary of the referendum content using OpenAI's GPT model"""
    response = openai.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a neutral Polkadot governance analyst.\n"
                            "Summarise the referendum in 150-200 words.\n"
                            "• Purpose\n• Funding/mechanics\n"
                            "• Potential impact\n• Controversial points (if any)\n\n"
                            "The output of this summary is for the command line, so it is "
                            "imperative that plain text is output - not markdown, not HTML, etc. "
                            "Just plain text."
                        ),
                    }
                ],
            },
            {"role": "user", "content": content},
        ],
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True,
    )

    return response.output_text
