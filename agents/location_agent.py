import uvicorn

from tools import random_nyc_location

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from a2a.utils import new_agent_text_message


class LocationAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        location = random_nyc_location()
        event_queue.enqueue_event(new_agent_text_message(f"New York - {location}"))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


def build_app() -> A2AStarletteApplication:
    skill = AgentSkill(
        id='get_location',
        name='Get location',
        description='Returns a random NYC location',
        tags=['location'],
        examples=['where are you'],
    )

    agent_card = AgentCard(
        name='Location Agent',
        description='Returns a random NYC location',
        url='http://localhost:8002/',
        version='1.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=LocationAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )


if __name__ == '__main__':
    server = build_app()
    uvicorn.run(server.build(), host='0.0.0.0', port=8002)
