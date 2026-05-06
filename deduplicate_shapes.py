import csv
from collections import defaultdict
from pathlib import Path

shapes_path = Path("files/shapes.csv")

with open(shapes_path, newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Group row indices by shape_id, sorted by shape_pt_sequence
groups: dict[str, list[int]] = defaultdict(list)
for i, row in enumerate(rows):
    groups[row["shape_id"]].append(i)

keep: set[int] = set()
for indices in groups.values():
    indices.sort(key=lambda i: int(rows[i]["shape_pt_sequence"]))
    prev_coord = None
    for i in indices:
        coord = (rows[i]["shape_pt_lat"], rows[i]["shape_pt_lon"])
        if coord != prev_coord:
            keep.add(i)
            prev_coord = coord

removed = len(rows) - len(keep)
rows = [row for i, row in enumerate(rows) if i in keep]

with open(shapes_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Removed {removed} duplicate points, {len(rows)} rows remaining")
