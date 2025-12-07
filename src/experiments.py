from pathlib import Path
import csv
import asyncio
from typing import Iterable, Dict, Any
import logging
import json

from .lora import LoraBase
from .constants import RESULTS_COLUMNS, lora_configs
from .models import ExperimentDescription


def run_experiment(lora: LoraBase, description: ExperimentDescription, logger: logging.Logger) -> Path:
  config_keys = list(lora_configs[0].keys())

  logger.info(f"Starting experiment: {description["name"]}")

  async def _run():
    await lora.start()
    results = []
    all = len(lora_configs)
    for idx, config in enumerate(lora_configs, start=1):
      logger.info(f"Running {idx}/{all}")
      await lora.config_sync(idx, config)
      state = await lora.ping(idx)


      row = {key: config[key] for key in config_keys}
      row.update({key: state[key] for key in RESULTS_COLUMNS})
      results.append(row)
      await lora.stop()
    return results

  results = asyncio.run(_run())
  output_path = save_results(results, description)
  print(f"Results stored at: {output_path}")
  return output_path

def save_results(experiment_results: Iterable[Dict[str, Any]], description: ExperimentDescription) -> Path:
  rows = list(experiment_results)
  if not rows:
    return Path()

  output_path = Path("results") / description["name"]
  results_path = output_path / "results.csv"
  description_path = output_path / "description.json"
  output_path.parent.mkdir(exist_ok=True, parents=True)
  fieldnames = list(rows[0].keys())

  with results_path.open("w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

  with description_path.open("w") as description_file:
    json.dump(description, description_file, indent=2, sort_keys=True)

  return output_path
