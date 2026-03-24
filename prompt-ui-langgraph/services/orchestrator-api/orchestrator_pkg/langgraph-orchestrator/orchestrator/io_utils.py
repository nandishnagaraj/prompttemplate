from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime


def make_run_dir(base: str = "runs") -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    p = Path(base) / ts
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def write_artifact(run_dir: str, filename: str, content: str) -> None:
    p = Path(run_dir) / filename
    p.write_text(content, encoding="utf-8")
