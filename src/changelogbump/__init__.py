from pathlib import Path


src: Path = Path(__file__).parent.parent
header_path = src.parent / "static/header_1.1.0.txt"
