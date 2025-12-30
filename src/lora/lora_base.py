from abc import ABC, abstractmethod
from lora_simulation import Config, State

class LoraBase(ABC):
  @abstractmethod
  async def start(self):
    pass

  @abstractmethod
  async def stop(self):
    pass

  @abstractmethod
  async def config_get(self) -> Config:
    pass

  @abstractmethod
  async def ping(self, id: int) -> State:
    pass

  @abstractmethod
  async def config_sync(self, id: int, params) -> bool:
    pass