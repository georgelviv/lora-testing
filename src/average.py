from pathlib import Path
import pandas as pd

def avg_results(csv_path):
  df = pd.read_csv(csv_path)

  GROUP_COLS = ["SF", "FQ", "BW", "CR", "TP", "IH", "HS", "PL", "CL", "RT"]

  df_avg = (
    df.groupby(GROUP_COLS, as_index=False).mean(numeric_only=True).round(3)
  )
  out_path = csv_path.with_name("avg.csv")
  df_avg.to_csv(
    out_path,
    index=False
  )
  df_avg.to_csv(out_path, index=False)
  print(f"Saved: {out_path}")