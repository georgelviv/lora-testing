from pathlib import Path
import asyncio
import time
from typing import Dict, Any
import logging
import json
import pandas as pd

from .lora import LoraBase
from .constants import RESULTS_COLUMNS, lora_configs
from .models import ExperimentDescription

CONFIG_UPDATE_ATTEMPTS = 100

def run_experiment(
  lora: LoraBase,
  description: ExperimentDescription,
  logger: logging.Logger
) -> Path:
  config_keys = list(lora_configs[0].keys())

  logger.info(f"Starting experiment: {description['name']}")

  output_path = Path("results") / description["name"]
  results_path = output_path / "results.csv"
  description_path = output_path / "description.json"
  output_path.mkdir(exist_ok=True, parents=True)

  if not description_path.exists():
    with description_path.open("w") as f:
      json.dump(description, f, indent=2, sort_keys=True)

  async def _run():
    await lora.start()
    total = len(lora_configs)

    for idx, config in enumerate(lora_configs, start=1):
      logger.info(f"Running {idx}/{total}")

      for attempt in range(1, CONFIG_UPDATE_ATTEMPTS + 1):
        logger.info(f"Config update attempt: {attempt}")

        config_is_updated = await lora.config_sync(idx, config)
        logger.info(
          f"Config is {'updated' if config_is_updated else 'not updated'}"
        )

        time.sleep(2)

        if config_is_updated:

          for i in range(1, 5 + 1):
            state = await lora.ping(idx)
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
          time.sleep(attempt ** 2)

    await lora.stop()

  asyncio.run(_run())

  logger.info(f"Results stored at: {output_path}")
  return output_path
