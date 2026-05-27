"""Resolve cwd and leveling layout into domain/project keys."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Binding:
    cwd: Path
    repo_root: Path
    leveling_root: Path | None
    domain: str
    project: str | None
    domain_source: str  # "path" | "flag" | "fallback"
    curated_context: str | None


def repo_root_from_module() -> Path:
    return Path(__file__).resolve().parent.parent


def load_config(repo_root: Path) -> dict:
    import json

    config_path = repo_root / "configs" / "default.json"
    if not config_path.is_file():
        return {}
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_leveling_root(
    repo_root: Path,
    cwd: Path,
    *,
    override: str | None = None,
) -> Path | None:
    if override:
        path = Path(override).expanduser().resolve()
        return path if path.is_dir() else None

    env = os.environ.get("DEEP_TUTOR_LEVELING_ROOT")
    if env:
        path = Path(env).expanduser().resolve()
        return path if path.is_dir() else None

    config = load_config(repo_root)
    configured = config.get("leveling_root")
    if configured:
        path = Path(configured).expanduser().resolve()
        return path if path.is_dir() else None

    sibling = repo_root.parent / "leveling-arc"
    if is_leveling_root(sibling):
        return sibling

    return find_leveling_root_from_cwd(cwd)


def is_leveling_root(path: Path) -> bool:
    """Leveling workspaces have both domains/ and projects/ (see docs/system-design.md §4.2)."""
    return (path / "domains").is_dir() and (path / "projects").is_dir()


def find_leveling_root_from_cwd(cwd: Path) -> Path | None:
    resolved = cwd.resolve()
    for parent in [resolved, *resolved.parents]:
        if is_leveling_root(parent):
            return parent
    return None


def _segment_after(parts: tuple[str, ...], anchor: str) -> str | None:
    try:
        index = parts.index(anchor)
    except ValueError:
        return None
    if index + 1 >= len(parts):
        return None
    return parts[index + 1]


def infer_keys_from_path(path: Path, leveling_root: Path | None) -> tuple[str | None, str | None]:
    if leveling_root is None:
        return None, None

    try:
        relative = path.resolve().relative_to(leveling_root.resolve())
    except ValueError:
        return None, None

    parts = relative.parts
    domain = _segment_after(parts, "domains")
    project = _segment_after(parts, "projects")
    return domain, project


def load_curated_context(leveling_root: Path | None, domain: str) -> str | None:
    if leveling_root is None or domain == "generic":
        return None

    domain_dir = leveling_root / "domains" / domain
    if not domain_dir.is_dir():
        return None

    for name in ("CONTEXT.md", "README.md"):
        candidate = domain_dir / name
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8").strip()
    return None


def bind_context(
    *,
    repo_root: Path,
    cwd: Path | None = None,
    domain_flag: str | None = None,
    leveling_root_override: str | None = None,
) -> Binding:
    resolved_cwd = (cwd or Path.cwd()).expanduser().resolve()
    leveling_root = resolve_leveling_root(
        repo_root, resolved_cwd, override=leveling_root_override
    )

    path_domain, project = infer_keys_from_path(resolved_cwd, leveling_root)

    if domain_flag:
        domain = domain_flag
        domain_source = "flag"
    elif path_domain:
        domain = path_domain
        domain_source = "path"
    else:
        domain = "generic"
        domain_source = "fallback"

    curated = load_curated_context(leveling_root, domain)

    return Binding(
        cwd=resolved_cwd,
        repo_root=repo_root,
        leveling_root=leveling_root,
        domain=domain,
        project=project,
        domain_source=domain_source,
        curated_context=curated,
    )
