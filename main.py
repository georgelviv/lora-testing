from lora_simulation import LoraSimulation, LORA_SIMULATION_ENVIRONMENTS

def main():
  lora_sim = LoraSimulation(env_model=LORA_SIMULATION_ENVIRONMENTS['open_field'])
  print(lora_sim)

if __name__ == "__main__":
  main()