import base64
import os
from typing import Optional

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from nova_companion.core.exceptions import TextToImageError
from nova_companion.core.prompts import IMAGE_ENHANCEMENT_PROMPT, IMAGE_SCENARIO_PROMPT
from nova_companion.settings import settings
from pydantic import BaseModel, Field
from together import Together


class ScenarioPrompt(BaseModel):
    """Class for the scenario response"""

    narrative: str = Field(..., description="The AI's narrative response to the question")
    image_prompt: str = Field(..., description="The visual prompt to generate an image representing the scene")


class EnhancedPrompt(BaseModel):
    """Class for the text prompt"""

    content: str = Field(
        ...,
        description="The enhanced text prompt to generate an image",
    )


class TextToImage:
    """A class to handlle to text-to-image generation using Together AI."""

    REQUIRED_ENV_VARS = ["GROQ_API_KEY", "TOGETHER_API_KEY"]

    def __init__(self):
        self.validate_env_vars()
        self._together_client: Optional[Together] = None

    def validate_env_vars(self) -> None:
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def together_client(self) -> Together:
        if self._together_client is None:
            self._together_client = Together(api_key=settings.TOGETHER_API_KEY)
        return self._together_client

    async def generate_image(self, prompt: str, output_path: str = "") -> bytes:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            response = self.together_client.images.generate(
                prompt=prompt,
                model=settings.TTI_MODEL_NAME,
                width=1024,
                height=768,
                steps=4,
                n=1,
                response_format="b64_json",
            )

            image_data = base64.b64decode(response.data[0].b64_json)
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_data)

            return image_data

        except Exception as e:
            raise TextToImageError(f"Failed to generate image: {str(e)}") from e

    async def create_scenario(self, chat_history: list = None) -> ScenarioPrompt:
        try:
            formatted_history = "\n".join([f"{msg.type.title()}: {msg.content}" for msg in chat_history[-5:]])

            llm = ChatGroq(
                model=settings.TEXT_MODEL_NAME,
                api_key=settings.GROQ_API_KEY,
                temperature=0.4,
                max_retries=2,
            )

            structured_llm = llm.with_structured_output(ScenarioPrompt)

            chain = (
                PromptTemplate(
                    input_variables=["chat_history"],
                    template=IMAGE_SCENARIO_PROMPT,
                )
                | structured_llm
            )

            scenario = chain.invoke({"chat_history": formatted_history})

            return scenario

        except Exception as e:
            raise TextToImageError(f"Failed to create scenario: {str(e)}") from e

    async def enhance_prompt(self, prompt: str) -> str:
        try:
            llm = ChatGroq(
                model=settings.TEXT_MODEL_NAME,
                api_key=settings.GROQ_API_KEY,
                temperature=0.25,
                max_retries=2,
            )

            structured_llm = llm.with_structured_output(EnhancedPrompt)

            chain = (
                PromptTemplate(
                    input_variables=["prompt"],
                    template=IMAGE_ENHANCEMENT_PROMPT,
                )
                | structured_llm
            )

            enhanced_prompt = chain.invoke({"prompt": prompt}).content

            return enhanced_prompt

        except Exception as e:
            raise TextToImageError(f"Failed to enhance prompt: {str(e)}") from e
