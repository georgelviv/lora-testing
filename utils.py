from pathlib import Path
import csv
from typing import Iterable, Dict, Any


def save_results(rows: Iterable[Dict[str, Any]], output_path: Path) -> None:
  rows = list(rows)
  if not rows:
    return

  output_path.parent.mkdir(exist_ok=True, parents=True)
  fieldnames = list(rows[0].keys())

  with output_path.open("w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
