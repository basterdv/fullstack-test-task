from pathlib import Path

class FileStorage:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, content: bytes):
        path = self.storage_dir / name
        path.write_bytes(content)

    def delete(self, name: str):
        path = self.storage_dir / name
        if path.exists():
            path.unlink()

    def get_full_path(self, name: str) -> Path:
        return self.storage_dir / name
