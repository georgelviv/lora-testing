from lora_simulation import LoraSimulation, LORA_SIMULATION_ENVIRONMENTS
from lora_configs import lora_configs

def main():
  lora_sim = LoraSimulation(env_model=LORA_SIMULATION_ENVIRONMENTS['open_field'])
  for config in enumerate(lora_configs):
    lora_sim.set_config(config)
    print(f"Config {config}")
    print(f"Result: {lora_sim.ping()}")

if __name__ == "__main__":
  main()
