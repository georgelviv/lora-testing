from src import run, ExperimentDescription, logger, load_json

from lora_simulation_model import (LoraSimulationModel, EnvironmentModel, AreaType)
from lora_hardware_model import LoraHardwareModel
from lora_math_model import LoraMathModel

def run_math_simulation():
  config_suites = load_json("configs-suite.json")

  for distance in [120, 260, 450]:
    env_model = EnvironmentModel(
      name=f"math-{distance}-meters",
      path_loss_exponent=2.5,
      shadow_sigma_db=3.0,
      sigma_noise_db=2.0,
      distance_m=distance,
      hb_m = 1.2,
      hm_m = 1.0,
      area_type=AreaType.SUBURBAN,
      description=f"Suburban {distance} meters"
    )
    lora = LoraMathModel(
      env_model=env_model
    )
    description: ExperimentDescription = {
      "name": env_model.name,
      "type": "math",
      "avg_result_file_name": f"math-{distance}",
      "description": env_model.description
    }
    run(lora, description, configs_suite=config_suites, with_delays=False)

def run_simulation():
  config_suites = load_json("configs-suite.json")
  for distance in [120, 260, 450]:
    env_model = EnvironmentModel(
      name=f"suburban-{distance}-meters",
      path_loss_exponent=2,
      shadow_sigma_db=3,
      sigma_noise_db=2.5,
      distance_m=distance,
      hb_m = 15,
      hm_m = 10,
      area_type=AreaType.URBAN,
      description=f"Suburban {distance} meters."
    )
    lora = LoraSimulationModel(
      env_model=env_model
    )
    description: ExperimentDescription = {
      "name": env_model.name,
      "type": "simulation",
      "avg_result_file_name": f"simulation-{distance}",
      "description": env_model.description
    }
    run(lora, description, configs_suite=config_suites, with_delays=False)

def run_hardware():
  config_suites = load_json("configs-suite.json")
  # port_filter = "/dev/cu.usbserial-59680236201"
  port_filter="/dev/cu.usbserial"
  lora = LoraHardwareModel(logger, port_filter=port_filter)
  description: ExperimentDescription = {
    "type": "hardware",
    "name": "lora-type",
    "description": "Long 1000 meter with wall"
  }
  run(lora, description, configs_suite=config_suites)

def main():
  run_simulation()
  # run_math_simulation()

if __name__ == "__main__":
  main()
