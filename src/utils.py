from pathlib import Path
import pandas as pd
import logging
import json
from .models import ExperimentDescription

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