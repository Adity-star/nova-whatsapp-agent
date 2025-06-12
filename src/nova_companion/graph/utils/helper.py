import re

from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from nova_companion.settings import Settings

def get_chat_model(temperature: float=0.5):
    return ChatGroq(
        api_key=Settings.GROQ_API_KEY,
        model_name=Settings.TEXT_MODEL_NAME,
        temperature=temperature,
    )


def remove_asterisk_content(text: str) -> str:
    """Remove content between asterisks from the text."""
    return re.sub(r"\*.*?\*", "", text).strip()


class AsteriskRemovalParser(StrOutputParser):
    def parse(self, text):
        return remove_asterisk_content(super().parse(text))
    
def get_text_to_image_module():
    