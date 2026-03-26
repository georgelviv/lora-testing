import argparse
from pathlib import Path
import sys
import pandas as pd
import logging
import json
from .models import ArgEnv, Args, ExperimentDescription, LoraBase
from lora_simulation_model import (LoraSimulationModel, EnvironmentModel, AreaType)
from lora_hardware_model import LoraHardwareModel
from lora_math_model import LoraMathModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LORA TESTING")

def avg_results(csv_path, description: ExperimentDescription):
  df = pd.read_csv(csv_path)

  GROUP_COLS = ["SF", "FQ", "BW", "CR", "TP", "IH", "HS", "PL", "CL", "RT"]

  df_avg = (
    df.groupby(GROUP_COLS, as_index=False).mean(numeric_only=True).round(3)
  )

  avg_file_name = "avg.csv"
  if "avg_result_file_name" in description:
    avg_file_name = f"{description['avg_result_file_name']}.csv"

  out_path = csv_path.with_name(avg_file_name)
  df_avg.to_csv(
    out_path,
    index=False
  )
  df_avg.to_csv(out_path, index=False)
  print(f"Saved: {out_path}")

  
def load_json(json_path: str):
  path = Path(json_path)

  with path.open("r", encoding="utf-8") as f:
    data = json.load(f)

  return data

def read_args() -> Args:
  parser = argparse.ArgumentParser()
  parser.add_argument("--env", type=str, default='simulation')
  parser.add_argument("--distance", type=int, default=100)
  parser.add_argument("--no_delays", action="store_false", dest="with_delays")
  parser.add_argument("--port", type=str, default='/dev/cu.usbserial') 

  args = parser.parse_args()

  print(args.with_delays)

  return {
    'env': ArgEnv(args.env),
    'port': args.port,
    'distance': int(args.distance),
    'with_delays': args.with_delays
  }

def get_backend(logger: logging.Logger, args: Args) -> LoraBase:
  env: ArgEnv = args['env']
  distance: str = args['distance']

  if env == ArgEnv.HARDWARE:
    backend: LoraBase = LoraHardwareModel(logger, args['port'])
  elif env== ArgEnv.SIMULATION:
    env_model: EnvironmentModel = EnvironmentModel(
      name=f"simulation-{distance}-meters",
      path_loss_exponent=2.5,
      shadow_sigma_db=3.0,
      sigma_noise_db=2.0,
      distance_m=distance,
      hb_m = 1.2,
      hm_m = 1.0,
      area_type=AreaType.SUBURBAN,
      description=f"Suburban {distance} meters"
    )
    backend = LoraSimulationModel(logger, env_model)
  elif env== ArgEnv.MATH:
    env_model: EnvironmentModel = EnvironmentModel(
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
    backend = LoraMathModel(
      env_model=env_model
    )
  else:
    logger.error(f'Unknown Env {env}')
    sys.exit(1)
  return backend

def get_description(backend: LoraBase, args: Args) -> ExperimentDescription:
  description: ExperimentDescription = {
    "name" :f"{backend.name}-{args['distance']}-meters",
    "type": args["env"],
    "avg_result_file_name": f"{backend.name}-{args['distance']}",
    "description": f"Suburban {args['distance']} meters.",
  }

  return description