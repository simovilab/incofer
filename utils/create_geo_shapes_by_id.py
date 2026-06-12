import csv
import json
from collections import defaultdict
from pathlib import Path

shapes_path = Path("files/shapes.csv")
output_dir = Path("aux/geojson/")
output_dir.mkdir(parents=True, exist_ok=True)

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

for shape_id, points in shapes.items():
    points.sort(key=lambda p: p[0])
    coordinates = [[lon, lat] for _, lon, lat in points]
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": coordinates},
                "properties": {"shape_id": shape_id},
            }
        ],
    }
    out = output_dir / f"{shape_id}.geojson"
    with open(out, "w") as f:
        json.dump(geojson, f, indent=2)

print(f"Created {len(shapes)} GeoJSON files in {output_dir}/")
