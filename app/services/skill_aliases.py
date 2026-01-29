from typing import Dict, List
from pathlib import Path


def load_skill_aliases(file_name: str) -> dict[str, list[str]]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    file_path = base_dir / "app" / "resources" / file_name

    aliases = {}
    current_skill = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()

            if not line or line.startswith("#"):
                continue

            if line.startswith(">"):
                current_skill = line[1:].strip()
                aliases[current_skill] = []
            elif current_skill:
                aliases[current_skill].append(line)

    return aliases
