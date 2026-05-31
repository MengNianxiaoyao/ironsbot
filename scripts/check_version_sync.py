# SPDX-License-Identifier: MIT
"""校验根目录 `__version__` 与 `pyproject.toml` 中 [project].version 一致。

供 pre-commit 使用；也可手动运行: python scripts/check_version_sync.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "__version__"
PYPROJECT = ROOT / "pyproject.toml"


def read_project_version(pyproject: Path) -> str | None:
    text = pyproject.read_text(encoding="utf-8")
    in_project = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = False
            continue
        if in_project and stripped.startswith("version"):
            m = re.match(r'version\s*=\s*"([^"]+)"', stripped)
            if m:
                return m.group(1)
    return None


def main() -> None:
    if not PYPROJECT.is_file():
        sys.exit(f"未找到 {PYPROJECT}")
    if not VERSION_FILE.is_file():
        sys.exit(f"未找到 {VERSION_FILE}")

    pv = read_project_version(PYPROJECT)
    if pv is None:
        sys.exit("无法在 pyproject.toml 的 [project] 段解析 version")

    try:
        file_body = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError as e:
        sys.exit(f"无法读取 __version__: {e}")

    expected = f"v{pv}"
    if file_body != expected:
        sys.exit(
            "版本不一致：\n"
            f"  pyproject.toml [project].version = {pv!r}\n"
            f"  __version__ 应为单行 {expected!r}，当前为 {file_body!r}\n"
            "请运行: uv run python scripts/set_version.py "
            f"{pv!r}（或手动将 __version__ 改为与 pyproject 一致）"
        )


if __name__ == "__main__":
    main()
