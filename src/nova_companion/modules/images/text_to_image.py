import base64
import base64
import logging
import os
from typing import Optional

from nova_companion.settings import settings
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from together import Together

class ScenarioPrompt(BaseModel):
    """Class for the scenario response"""

    narrative: str = Field(..., description="The AI's narrative response to the question")
    image_prompt: str = Field(..., description="The visual prompt to generate an image representing the scene")


class TextTOImage:
    """A class to handlle to text-to-image generation using Together AI."""

    REQUIRED_ENV_VARS = ["GROQ_API_KEY", "TOGETHER_API_KEY"]