from src import run, ExperimentDescription, logger, load_json

from lora_simulation_model import (LoraSimulation, EnvironmentModel, AreaType)
from lora_hardware_model import LoraHardware

def run_simulation():
  config_suites = load_json("configs-suite.json")
  env_model = EnvironmentModel(
    name="ddd-120-meters",
    path_loss_exponent=2.5,
    shadow_sigma_db=3.0,
    sigma_noise_db=2.0,
    distance_m=120,
    hb_m = 1.2,
    hm_m = 1.0,
    area_type=AreaType.SUBURBAN,
    description="Suburban 120 meters"
  )
  lora = LoraSimulation(
    env_model=env_model
  )
  description: ExperimentDescription = {
    "name": env_model.name,
    "type": "simulation",
    "description": env_model.description
  }
  run(lora, description, configs_suite=config_suites, with_delays=False)

def run_hardware():
  config_suites = load_json("configs-suite.json")
  # port_filter = "/dev/cu.usbserial-59680236201"
  port_filter="/dev/cu.usbserial"
  lora = LoraHardware(logger, port_filter=port_filter)
  description: ExperimentDescription = {
    "type": "hardware",
    "name": "lora-type",
    "description": "Long 1000 meter with wall"
  }
  run(lora, description, configs_suite=config_suites)

def main():
  run_simulation()

if __name__ == "__main__":
  main()
