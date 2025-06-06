import uvicorn

from tools import format_pacific_time, random_nyc_location

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from a2a.utils import new_agent_text_message


class InfoAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        time_str = format_pacific_time()
        location = random_nyc_location()
        text = f"Pacific time: {time_str}\nLocation: New York - {location}"
        event_queue.enqueue_event(new_agent_text_message(text))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


def build_app() -> A2AStarletteApplication:
    skill = AgentSkill(
        id='get_info',
        name='Get time and location',
        description='Returns pacific time and a random NYC location',
        tags=['info'],
        examples=['info'],
    )

    agent_card = AgentCard(
        name='Info Agent',
        description='Returns time and location info',
        url='http://localhost:8003/',
        version='1.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=InfoAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )


if __name__ == '__main__':
    server = build_app()
    uvicorn.run(server.build(), host='0.0.0.0', port=8003)
