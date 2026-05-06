import json
from pathlib import Path

aux = Path("aux/geojson/")

with open(aux / "shapes.geojson") as f:
    shapes = json.load(f)

with open(aux / "stops.geojson") as f:
    stops = json.load(f)

geojson = {
    "type": "FeatureCollection",
    "features": shapes["features"] + stops["features"],
}

output_path = aux / "features.geojson"
with open(output_path, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Created {output_path} with {len(geojson['features'])} features")
