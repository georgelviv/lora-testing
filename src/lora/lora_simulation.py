import logging
from .lora_base import LoraBase
from lora_simulation import (
  LoraSimulation as Simulation, EnvironmentModel,
  Config, State
)

class LoraSimulation(LoraBase):
  def __init__(self, logger: logging.Logger, env_model: EnvironmentModel):
    self.logger = logger
    self.simulation = Simulation(self.logger, env_model)

  async def start(self):
    pass

  async def stop(self):
    pass

  async def config_get(self) -> Config:
    return self.simulation.get_config()

  async def ping(self, id: int) -> State:
    return self.simulation.ping()

  async def config_sync(self, id: int, params: Config) -> None:
    return self.simulation.set_config(params)