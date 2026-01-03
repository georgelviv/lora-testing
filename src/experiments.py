from pathlib import Path
import asyncio
import time
from typing import Dict, Any, List
import json
import pandas as pd

from .constants import RESULTS_COLUMNS
from .models import ExperimentDescription, LoraModelBase, Config
from .utils import avg_results, logger

CONFIG_UPDATE_ATTEMPTS = 100

def run_experiment(
  lora_model: LoraModelBase,
  configs_suite: list[Config],
  results_path: str,
  with_delays: bool = True,
) -> Path:
  config_keys = list(configs_suite[0].keys())

  async def _run():
    await lora_model.start()
    total = len(configs_suite)

    for idx, config in enumerate(configs_suite, start=1):
      logger.info(f"------------Running {idx}/{total}-------------- ")

      for attempt in range(1, CONFIG_UPDATE_ATTEMPTS + 1):
        logger.info(f"Config update attempt: {attempt}")

        config_is_updated = await lora_model.config_sync(idx, config)
        logger.info(
          f"Config is {'updated' if config_is_updated else 'not updated'}"
        )

        if with_delays:
          time.sleep(2)

        if config_is_updated:

          for i in range(1, 5 + 1):
            state = await lora_model.ping(idx)
            if with_delays:
              time.sleep(2)

            row: Dict[str, Any] = {key: config[key] for key in config_keys}
            row.update({key: state[key] for key in RESULTS_COLUMNS})
            df = pd.DataFrame([row])
            df.to_csv(
              results_path,
              mode="a",
              index=False,
              header=not results_path.exists()
            )
          break
        else:
          if with_delays:
            time.sleep(attempt ** 2)

    await lora_model.stop()

  asyncio.run(_run())

def run(
  lora_model: LoraModelBase,
  description: ExperimentDescription,
  configs_suite: list[Config],
  with_delays: bool = True
):
  
  output_path = Path("results") / description["type"] / description["name"]
  results_path = output_path / "results.csv"
  description_path = output_path / "description.json"
  output_path.mkdir(exist_ok=True, parents=True)

  if not description_path.exists():
    with description_path.open("w") as f:
      json.dump(description, f, indent=2, sort_keys=True)

  logger.info(f"Starting experiment: {description['name']}")

  run_experiment(lora_model, configs_suite, results_path, with_delays)
  logger.info(f"Results stored at: {output_path}")

  avg_results(results_path)