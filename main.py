import logging

from lora_simulation import LORA_SIMULATION_ENVIRONMENTS
from src import (
  LoraSimulation, LoraHardware, run_experiment
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lora")

def main():
  # lora = LoraSimulation(
  #   logger=logger,
  #   env_model=LORA_SIMULATION_ENVIRONMENTS["open_field"]
  # )
  lora = LoraHardware(logger, port_filter="/dev/cu.usbserial")
  run_experiment(lora, "hardware_close", logger)

if __name__ == "__main__":
  main()
