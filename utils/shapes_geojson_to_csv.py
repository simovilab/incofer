import csv
import json
from pathlib import Path

input_path = Path("aux/geojson/shapes.geojson")
output_path = Path("aux/csv/shapes.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

fieldnames = ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]

with open(input_path) as f:
    data = json.load(f)

rows = []
for feature in data["features"]:
    shape_id = feature["properties"]["shape_id"]
    geom = feature["geometry"]
    if geom["type"] == "LineString":
        coords = geom["coordinates"]
    elif geom["type"] == "MultiLineString":
        coords = [pt for line in geom["coordinates"] for pt in line]
    else:
        continue
    for seq, (lon, lat, *_) in enumerate(coords):
        rows.append(
            {
                "shape_id": shape_id,
                "shape_pt_lat": lat,
                "shape_pt_lon": lon,
                "shape_pt_sequence": seq,
            }
        )

with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"{input_path} -> {output_path} ({len(rows)} points)")
