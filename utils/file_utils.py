import csv
from pathlib import Path

def read_csv_for_parametrize(csv_path: Path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Return list of tuples in order matching your test parameters
        return [
            (row['username'], row['password'], row['expected_success'].lower() == 'true')
            for row in reader
        ]
