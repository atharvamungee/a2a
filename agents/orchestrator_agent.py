import uvicorn
from uuid import uuid4

import httpx
from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.utils import get_message_text, new_agent_text_message

TIME_AGENT_URL = "http://localhost:8001"
LOCATION_AGENT_URL = "http://localhost:8002"


class OrchestratorAgentExecutor(AgentExecutor):
    def __init__(self) -> None:
        self.httpx_client = httpx.AsyncClient()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input().lower()
        responses: list[str] = []

        if "time" in query:
            time_client = await A2AClient.get_client_from_agent_card_url(
                self.httpx_client, TIME_AGENT_URL
            )
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(message=context.message),
            )
            resp = await time_client.send_message(request)
            result = resp.root.result
            if hasattr(result, "parts"):
                responses.append(get_message_text(result))

        if "location" in query:
            location_client = await A2AClient.get_client_from_agent_card_url(
                self.httpx_client, LOCATION_AGENT_URL
            )
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(message=context.message),
            )
            resp = await location_client.send_message(request)
            result = resp.root.result
            if hasattr(result, "parts"):
                responses.append(get_message_text(result))

        if responses:
            final_text = "\n".join(responses)
        else:
            final_text = "No suitable agent found"

        event_queue.enqueue_event(new_agent_text_message(final_text))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        await self.httpx_client.aclose()


def build_app() -> A2AStarletteApplication:
    skill = AgentSkill(
        id="orchestrate",
        name="Orchestrate requests",
        description="Routes user queries to other agents",
        tags=["orchestrator"],
        examples=["what time is it", "where are you"],
    )

    agent_card = AgentCard(
        name="Orchestrator Agent",
        description="Routes queries to specialized agents",
        url="http://localhost:9000/",
        version="1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=OrchestratorAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )


if __name__ == "__main__":
    server = build_app()
    uvicorn.run(server.build(), host="0.0.0.0", port=9000)
