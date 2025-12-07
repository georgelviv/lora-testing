import logging

from lora_simulation import LORA_SIMULATION_ENVIRONMENTS
from src import run_experiment
from src.lora.lora_simulation import LoraSimulation

def main():
  lora = LoraSimulation(
    logger=logging.getLogger("lora"),
    env_model=LORA_SIMULATION_ENVIRONMENTS["open_field"]
  )
  run_experiment(lora, "open_field")

if __name__ == "__main__":
  main()
