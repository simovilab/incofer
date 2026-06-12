import csv
import json
from collections import defaultdict
from pathlib import Path

shapes_path = Path("files/shapes.csv")
output_path = Path("aux/geojson/shapes.geojson")
output_path.parent.mkdir(parents=True, exist_ok=True)

shapes: dict[str, list[tuple[int, float, float]]] = defaultdict(list)

with open(shapes_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        shapes[row["shape_id"]].append(
            (
                int(row["shape_pt_sequence"]),
                float(row["shape_pt_lon"]),
                float(row["shape_pt_lat"]),
            )
        )

features = []
for shape_id, points in shapes.items():
    points.sort(key=lambda p: p[0])
    coordinates = [[lon, lat] for _, lon, lat in points]
    features.append(
        {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coordinates},
            "properties": {"shape_id": shape_id},
        }
    )

geojson = {"type": "FeatureCollection", "features": features}

with open(output_path, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Created {output_path} with {len(features)} features")
