from pathlib import Path


def read_attachment(root: Path, name: str) -> bytes:
    return (root / name).read_bytes()
