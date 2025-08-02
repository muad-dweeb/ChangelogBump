from datetime import date
from pathlib import Path

import click


class Changelog:
    path: Path = Path("CHANGELOG.md")

    @staticmethod
    def generate_sections() -> dict[str, list[str]]:
        result: dict[str, list[str]] = {"added": [], "changed": [], "removed": []}
        for key in result.keys():
            while True:
                resp: str = click.prompt(
                    f"{key.title()}: (empty moves to next section)",
                    default="",
                )
                if not resp or resp.strip() == "":
                    break
                result[key].append(resp)
        return result

    @classmethod
    def update(cls, new_version: str, summary_text: str | None = None):
        content = cls.path.read_text()
        today = date.today().strftime("%Y-%m-%d")

        # Prepare a new version section
        new_entry = f"## [{new_version}] - {today}\n\n{summary_text}\n\n"
        for key, value in cls.generate_sections().items():
            if len(value) > 0:
                new_entry += f"### {key.title()}\n\n"
                ents = [f"- {ent}" for ent in value]
                new_entry += "\n".join(ents) + "\n\n"

        lines = content.splitlines()
        # Insert the new version section before the first existing version heading
        for i, line in enumerate(lines):
            if line.startswith("## ["):
                lines.insert(i, new_entry)
                break
        else:
            # If no headings are found, just append to the end
            lines.append(new_entry)

        updated_content = "\n".join(lines)
        cls.path.write_text(updated_content)
