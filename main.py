import logging

from lora_simulation import LORA_SIMULATION_ENVIRONMENTS
from src import (
  LoraSimulation, LoraHardware, run, ExperimentDescription,
  EnvironmentModel, AreaType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LORA")

def run_simulation(): 
  env_model = EnvironmentModel(
    name="suburban-260-meters",
    path_loss_exponent=2.5,
    shadow_sigma_db=3.0,
    sigma_noise_db=2.0,
    distance_m=450,
    hb_m = 1.2,
    hm_m = 1.0,
    area_type=AreaType.SUBURBAN,
    description="Suburban 260 meters"
  )
  lora = LoraSimulation(
    logger=logger,
    env_model=env_model
  )
  description: ExperimentDescription = {
    "name": env_model.name,
    "type": "simulation",
    "description": env_model.description
  }
  run(lora, description, logger, with_delays=False)

def run_hardware():
  port_filter = "/dev/cu.usbserial-59680236201"
  # port_filter="/dev/cu.usbserial"
  lora = LoraHardware(logger, port_filter=port_filter)
  description: ExperimentDescription = {
    "type": "hardware",
    "name": "lora-hardware-1000-meters",
    "description": "Long 1000 meter with wall"
  }
  run(lora, description, logger)

def main():
  run_simulation()

if __name__ == "__main__":
  main()
