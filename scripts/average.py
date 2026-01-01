from pathlib import Path
import pandas as pd

def find_results():
  results = []
  scripts_dir = Path(__file__).resolve().parent
  results_dir = scripts_dir.parent / "results"
  filename = "results.csv"

  files = list(results_dir.rglob(filename))

  for f in files:
    results.append(f)

  return results


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

def run():
  results = find_results()
  for r in results:
    avg_results(r)

run()