from typing import Optional

from langgraph.graph import MessagesState
from pydantic import Field


class AICompanionState(MessagesState):
    """State class for the AI Companion workflow.

    Extends MessagesState to track conversation history and maintains the last message received.

    Attributes:
        last_message (AnyMessage): The most recent message in the conversation, can be any valid
            LangChain message type (HumanMessage, AIMessage, etc.)
        workflow (str): The current workflow the AI Companion is in. Can be "conversation", "image", or "audio".
        audio_buffer (bytes): The audio buffer to be used for speech-to-text conversion.
        current_activity (str): The current activity of Ava based on the schedule.
        memory_context (str): The context of the memories to be injected into the character card.
    """

    summary: str = Field(default="")
    workflow: str = Field(default="conversation")
    audio_buffer: Optional[bytes] = Field(default=None)
    image_path: Optional[str] = Field(default=None)
    current_activity: str = Field(default="")
    apply_activity: bool = Field(default=False)
    memory_context: str = Field(default="")
