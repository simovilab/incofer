import csv
import math
from collections import defaultdict
from pathlib import Path

EARTH_RADIUS_KM = 6371.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in km between two points."""
    lat1, lon1, lat2, lon2 = (
        math.radians(v) for v in (lat1, lon1, lat2, lon2)
    )
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


shapes_path = Path("files/shapes.csv")

# Read all rows and group indices by shape_id
with open(shapes_path, newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

if "shape_dist_traveled" not in fieldnames:
    fieldnames.append("shape_dist_traveled")

# Group row indices by shape_id
groups: dict[str, list[int]] = defaultdict(list)
for i, row in enumerate(rows):
    groups[row["shape_id"]].append(i)

# Calculate cumulative distance for each shape
for indices in groups.values():
    indices.sort(key=lambda i: int(rows[i]["shape_pt_sequence"]))
    rows[indices[0]]["shape_dist_traveled"] = "0"
    cumulative = 0.0
    for prev, curr in zip(indices, indices[1:]):
        cumulative += haversine(
            float(rows[prev]["shape_pt_lat"]),
            float(rows[prev]["shape_pt_lon"]),
            float(rows[curr]["shape_pt_lat"]),
            float(rows[curr]["shape_pt_lon"]),
        )
        rows[curr]["shape_dist_traveled"] = f"{cumulative:.6f}"

# Write back
with open(shapes_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {shapes_path} ({len(groups)} shapes, {len(rows)} rows)")