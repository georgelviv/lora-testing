from pathlib import Path
import csv
import asyncio
from typing import Iterable, Dict, Any

from .lora import LoraBase
from .constants import RESULTS_COLUMNS, lora_configs


def run_experiment(lora: LoraBase, experiment_name: str) -> Path:
  config_keys = list(lora_configs[0].keys())

  print(f"Starting experiment: {experiment_name}")

  async def _collect_rows():
    rows = []
    for idx, config in enumerate(lora_configs, start=1):
      await lora.config_sync(idx, config)
      state = await lora.ping(idx)

      row = {key: config[key] for key in config_keys}
      row.update({key: state[key] for key in RESULTS_COLUMNS})
      rows.append(row)
    return rows

  rows = asyncio.run(_collect_rows())
  output_path = save_results(rows, experiment_name)
  print(f"Results stored at: {output_path}")
  return output_path

def save_results(experiment_results: Iterable[Dict[str, Any]], experiment_name: str) -> Path:
  rows = list(experiment_results)
  if not rows:
    return Path()

  output_path = Path("results") / experiment_name / "results.csv"
  output_path.parent.mkdir(exist_ok=True, parents=True)
  fieldnames = list(rows[0].keys())

  with output_path.open("w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

  return output_path
