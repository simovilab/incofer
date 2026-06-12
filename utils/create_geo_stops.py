import csv
import json
from pathlib import Path

stops_path = Path("files/stops.csv")
output_path = Path("aux/geojson/stops.geojson")
output_path.parent.mkdir(parents=True, exist_ok=True)

features = []

with open(stops_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lon = float(row.pop("stop_lon"))
        lat = float(row.pop("stop_lat"))
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": dict(row),
            }
        )

geojson = {"type": "FeatureCollection", "features": features}

with open(output_path, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Created {output_path} with {len(features)} features")
