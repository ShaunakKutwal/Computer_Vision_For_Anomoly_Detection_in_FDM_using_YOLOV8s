from pathlib import Path

mapping = {
    "stringing": 0,
    "cracking": 1,
    "off_platform": 2
}

base = Path("label_backup")

for cls, cls_id in mapping.items():
    folder = base / cls
    if not folder.exists():
        print(f" Folder not found: {folder}")
        continue

    for file in folder.glob("*.txt"):
        new_lines = []
        for line in file.read_text().splitlines():
            if not line.strip():
                continue
            parts = line.split()
            parts[0] = str(cls_id)
            new_lines.append(" ".join(parts))
        file.write_text("\n".join(new_lines))

print(" Label fixing completed successfully")