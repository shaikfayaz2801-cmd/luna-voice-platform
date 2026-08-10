from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseAIProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict], stream: bool = True) -> AsyncGenerator[str, None]:
        pass
        
    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        pass
