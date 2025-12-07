from pathlib import Path

from lora_simulation import LoraSimulation, LORA_SIMULATION_ENVIRONMENTS
from lora_configs import lora_configs
from utils import save_results

def main():
  lora_sim = LoraSimulation(env_model=LORA_SIMULATION_ENVIRONMENTS['open_field'])
  output_file = Path("results") / "results.csv"
  config_keys = list(lora_configs[0].keys())
  state_keys = ["BPS", "CHC", "DELAY", "RSSI", "SNR", "TOA", "ATT"]
  rows = []

  for config in enumerate(lora_configs, start=1):
    lora_sim.set_config(config)
    state = lora_sim.ping()

    row = {key: config[key] for key in config_keys}
    row.update({key: state[key] for key in state_keys})

    rows.append(row)

  save_results(rows, output_file)
  print(f"Wrote {len(rows)} rows to {output_file}")

if __name__ == "__main__":
  main()
