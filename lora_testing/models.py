from enum import StrEnum
from typing import TypedDict
from abc import ABC, abstractmethod
from lora_common import State, Action

class ExperimentDescription(TypedDict):
  name: str
  description: str
  type: str
  avg_result_file_name: str


class LoraBase(ABC):
  @property
  @abstractmethod
  def name(self) -> str:
      pass

  @abstractmethod
  async def start(self):
    pass

  @abstractmethod
  async def stop(self):
    pass

  @abstractmethod
  async def config_get(self) -> Action:
    pass

  @abstractmethod
  async def ping(self, id: int) -> State:
    pass

  @abstractmethod
  async def config_sync(self, id: int, params) -> bool:
    pass

class ArgEnv(StrEnum):
  SIMULATION = 'simulation'
  HARDWARE = 'hardware',
  MATH = 'math'

class Args(TypedDict):
  env: ArgEnv
  distance: int
  with_delays: bool
  port: str