import csv


def parse_rows(path):
    with open(path, newline="") as f:
        return [row for row in csv.DictReader(f) if row.get("sku")]


def main(path):
    rows = parse_rows(path)
    print(f"{len(rows)} rows")
