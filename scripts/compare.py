from pathlib import Path
import pandas as pd

def find_avg():
  results = []
  scripts_dir = Path(__file__).resolve().parent
  results_dir = scripts_dir.parent / "results"
  filename = "avg.csv"

  files = list(results_dir.rglob(filename))

  for f in files:
    results.append(f)

  return results

def compare_avg(csv_path):
  df = pd.read_csv(csv_path)

  KEEP_COLS = [ "RTOA"]
  # KEEP_COLS = ["SF", "BW", "CR", "TP", "PL", "DELAY", "TOA", "RTOA"]

  df_compare = df[KEEP_COLS].copy()
  out_path = csv_path.with_name("compare.csv")
  df_compare.to_csv(
    out_path,
    index=False,
    sep=";",
    decimal=","
  )
  print(f"Saved: {out_path}")

def run():
  results = find_avg()
  for r in results:
    compare_avg(r)

run()