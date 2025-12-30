import logging

from lora_simulation import LORA_SIMULATION_ENVIRONMENTS
from src import (
  LoraSimulation, LoraHardware, run_experiment, ExperimentDescription
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LORA")

def run_simulation(): 
  env_model = LORA_SIMULATION_ENVIRONMENTS["suburban"]
  lora = LoraSimulation(
    logger=logger,
    env_model=env_model
  )
  description: ExperimentDescription = {
    "name": env_model.name,
    "description": env_model.description
  }
  run_experiment(lora, description, logger)

def run_hardware():
  lora = LoraHardware(logger, port_filter="/dev/cu.usbserial")
  description: ExperimentDescription = {
    "name": "lora-hardware-close",
    "description": "Close"
  }
  run_experiment(lora, description, logger)

def main():
  run_hardware()

if __name__ == "__main__":
  main()
