import base64
import os
from typing import Optional, Union

from groq import Groq
from nova_companion.core.exceptions import ImageToTextError
from nova_companion.settings import settings
from utils.logger import logging

logging.info("Loaded image_to_text.py")


class ImageToText:
    """A class to handle image-to-text conversion using Groq's vision capabilities."""

    REQUIRED_ENV_VARS = ["GROQ_API_KEY"]

    def __init__(self):
        logging.info("Initializing ImageToText")
        self._validate_env_vars()
        self._client: Optional[Groq] = None
        self.logger = logging

    def _validate_env_vars(self) -> None:
        logging.info("Called _validate_env_vars")
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> Groq:
        logging.info("Accessed client property")
        if self._client is None:
            self._client = Groq(api_key=settings.GROQ_API_KEY)
        return self._client

    async def analyze_image(self, image_data: Union[str, bytes], prompt: str = "") -> str:
        logging.info(f"Called analyze_image with prompt: {prompt}")
        try:
            # Handle file path
            if isinstance(image_data, str):
                if not os.path.exists(image_data):
                    raise ValueError(f"Image file not found: {image_data}")
                with open(image_data, "rb") as f:
                    image_bytes = f.read()
            else:
                image_bytes = image_data

            if not image_bytes:
                raise ValueError("Image data cannot be empty")

            # Convert image to base64
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            # Default prompt if none provided
            if not prompt:
                prompt = "Please describe what you see in this image in detail."

            # Create the messages for the vision API
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ]

            # Make the API call
            response = self.client.chat.completions.create(
                model=settings.ITT_MODEL_NAME,
                messages=messages,
                max_tokens=1000,
            )

            if not response.choices:
                raise ImageToTextError("No response received from the vision model")

            description = response.choices[0].message.content
            self.logging.info(f"Generated image description: {description}")

            return description

        except Exception as e:
            raise ImageToTextError(f"Failed to analyze image: {str(e)}") from e
