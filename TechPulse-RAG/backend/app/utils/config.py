from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

for name in ("raw", "processed", "knowledge", "vectorstore"):
    (BASE_DIR / "data" / name).mkdir(parents=True, exist_ok=True)
