import uvicorn

from tools import format_pacific_time

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from a2a.utils import new_agent_text_message


class TimeAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        current_time = format_pacific_time()
        event_queue.enqueue_event(new_agent_text_message(current_time))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


def build_app() -> A2AStarletteApplication:
    skill = AgentSkill(
        id='get_time',
        name='Get current time',
        description='Returns the current Pacific Time',
        tags=['time'],
        examples=['what time is it'],
    )

    agent_card = AgentCard(
        name='Time Agent',
        description='Returns the current Pacific time',
        url='http://localhost:8001/',
        version='1.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=TimeAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )


if __name__ == '__main__':
    server = build_app()
    uvicorn.run(server.build(), host='0.0.0.0', port=8001)
