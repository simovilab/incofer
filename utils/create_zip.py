import zipfile
from pathlib import Path

files_dir = Path("files")
zip_path = Path("incofer.zip")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for csv_file in sorted(files_dir.glob("*.csv")):
        txt_name = csv_file.with_suffix(".txt").name
        zf.write(csv_file, txt_name)

print(f"Created {zip_path} with {len(list(files_dir.glob('*.csv')))} files")