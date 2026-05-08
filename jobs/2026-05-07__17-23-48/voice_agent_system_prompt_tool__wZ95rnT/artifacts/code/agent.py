from livekit import agents
from livekit.agents import Agent, JobContext
from datetime import datetime


@agents.function_tool()
def get_current_time() -> str:
    """
    Get the current time in a human-readable format.
    
    Returns:
        str: The current time in HH:MM:SS format
    """
    now = datetime.now()
    return now.strftime("%H:%M:%S")


@agents.function_tool()
def get_current_date() -> str:
    """
    Get the current date in a human-readable format.
    
    Returns:
        str: The current date in YYYY-MM-DD format with the day name
    """
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y")


class Assistant(Agent):
    """
    A voice assistant agent that can provide current time and date information.
    
    This agent uses a custom system prompt to guide its behavior and has access
    to function tools for retrieving current time and date information.
    """
    
    def __init__(self):
        super().__init__(
            name="assistant-agent",
            instructions=(
                "You are a helpful voice assistant. You can provide current time and date information "
                "when requested by the user. Be friendly, concise, and accurate in your responses. "
                "When asked about the time or date, use the available tools to fetch the current "
                "information and present it in a natural, conversational way."
            )
        )
    
    async def enter(self, job: JobContext):
        """Called when the agent joins a conversation."""
        await super().enter(job)
        print(f"Assistant agent joined conversation: {job.room.name}")
    
    async def exit(self, job: JobContext):
        """Called when the agent leaves a conversation."""
        await super().exit(job)
        print(f"Assistant agent left conversation: {job.room.name}")