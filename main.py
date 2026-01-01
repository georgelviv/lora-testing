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
  port_filter = "/dev/cu.usbserial-59680236201"
  # port_filter="/dev/cu.usbserial"
  lora = LoraHardware(logger, port_filter=port_filter)
  description: ExperimentDescription = {
    "name": "lora-hardware-500-meters",
    "description": "Long 500 meter with wall"
  }
  run_experiment(lora, description, logger)

def main():
  run_hardware()

if __name__ == "__main__":
  main()
