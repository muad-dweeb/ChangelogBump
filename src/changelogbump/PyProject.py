from pathlib import Path

import toml


class PyProject:
    path: Path = Path("pyproject.toml")

    @classmethod
    def update(cls, new_version: str):
        """Set the new version in pyproject.toml."""
        data = toml.load(cls.path)
        data["project"]["version"] = new_version
        with cls.path.open("w") as fh:
            toml.dump(data, fh)  # type: ignore
