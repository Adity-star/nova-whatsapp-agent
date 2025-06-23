import uuid
from datetime import datetime
from typing import List, Optional

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from nova_companion.core.prompts import MEMORY_ANALYSIS_PROMPT
from nova_companion.modules.memory.long_term.vector_store import get_vector_store
from nova_companion.settings import settings
from pydantic import BaseModel, Field
from utils.logger import logging

logging.info("Loaded memory_manager.py")


class MemoryAnalysis(BaseModel):
    """Result of analyzing a message for memory-worthy content."""

    is_important: bool = Field(
        ...,
        description="Whether the message is important enough to be stored as a memory",
    )
    formatted_memory: Optional[str] = Field(..., description="The formatted memory to be stored")


class MemoryManager:
    """Manager class for handling long-term memory operations."""

    def __init__(self):
        logging.info("Initializing MemoryManager")
        self.vector_store = get_vector_store()
        self.logger = logging
        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0.1,
            max_retries=2,
        ).with_structured_output(MemoryAnalysis)

    async def _analyze_memory(self, message: str) -> MemoryAnalysis:
        logging.info(f"Called _analyze_memory with message: {message}")
        prompt = MEMORY_ANALYSIS_PROMPT.format(message=message)
        return await self.llm.ainvoke(prompt)

    async def extract_and_store_memories(self, message: BaseMessage) -> None:
        logging.info(f"Called extract_and_store_memories with message: {message}")
        if message.type != "human":
            return

        # Analyze the message for importance and formatting
        analysis = await self._analyze_memory(message.content)
        if analysis.is_important and analysis.formatted_memory:
            # Check if similar memory exists
            similar = self.vector_store.find_similar_memory(analysis.formatted_memory)
            if similar:
                # Skip storage if we already have a similar memory
                self.logger.info(f"Similar memory already exists: '{analysis.formatted_memory}'")
                return

            # Store new memory
            self.logger.info(f"Storing new memory: '{analysis.formatted_memory}'")
            self.vector_store.store_memory(
                text=analysis.formatted_memory,
                metadata={
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                },
            )

    def get_relevant_memories(self, context: str) -> List[str]:
        logging.info(f"Called get_relevant_memories with context: {context}")
        memories = self.vector_store.search_memories(context, k=settings.MEMORY_TOP_K)
        if memories:
            for memory in memories:
                self.logger.debug(f"Memory: '{memory.text}' (score: {memory.score:.2f})")
        return [memory.text for memory in memories]

    def format_memories_for_prompt(self, memories: List[str]) -> str:
        logging.info(f"Called format_memories_for_prompt with {len(memories)} memories")
        if not memories:
            return ""
        return "\n".join(f"- {memory}" for memory in memories)


def get_memory_manager() -> MemoryManager:
    logging.info("Called get_memory_manager")
    return MemoryManager()
