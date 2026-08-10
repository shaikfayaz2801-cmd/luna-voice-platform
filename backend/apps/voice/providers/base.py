from abc import ABC, abstractmethod

class BaseTTS(ABC):
    @abstractmethod
    async def stream_tts(self, text: str, voice_id: str): pass

class BaseSTT(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str: pass
