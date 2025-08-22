import logging

from fastapi import APIRouter
from nova_companion.modules.images.image_to_text import ImageToText
from nova_companion.modules.speech.speech_to_text import SpeechToText
from nova_companion.modules.speech.text_to_speech import TextToSpeech

logger = logging.getLogger(__name__)

speech_to_text = SpeechToText()
text_to_speect = TextToSpeech()
image_to_text = ImageToText()

whatsapp_router = APIRouter()
