import asyncio
from uuid import uuid4

import httpx
from a2a.client import A2AClient
from a2a.types import Message, MessageSendParams, Part, Role, SendMessageRequest, TextPart


async def main(query: str) -> None:
    async with httpx.AsyncClient() as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(httpx_client, "http://localhost:9000")

        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=query))],
            messageId=str(uuid4()),
        )
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(message=message),
        )

        response = await client.send_message(request)
        print(response.model_dump_json(indent=2, exclude_none=True))


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Can you tell me the time and the location?"
    asyncio.run(main(query))
