import csv
import json
from pathlib import Path

input_dir = Path("aux/geojson")
output_dir = Path("aux/csv")
output_dir.mkdir(parents=True, exist_ok=True)

fieldnames = ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]

for geojson_path in sorted(input_dir.glob("*.geojson")):
    name = geojson_path.stem

    with open(geojson_path) as f:
        data = json.load(f)

    rows = []
    for feature in data["features"]:
        shape_id = feature["properties"].get("shape_id", name)
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

    out = output_dir / f"{name}.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{geojson_path.name} -> {out} ({len(rows)} points)")