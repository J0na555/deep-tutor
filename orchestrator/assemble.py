"""Assemble inspectable preamble blocks for OpenCode."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from memory.store import format_memory_slice, open_store
from orchestrator.bind import Binding, load_config


VALID_MODES = ("mentor", "debug", "concept")


@dataclass(frozen=True)
class Preamble:
    text: str
    binding: Binding
    mode: str
    hint_level: int
    sources: list[str]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def resolve_domain_rules(repo_root: Path, binding: Binding) -> tuple[str, Path]:
    candidates: list[Path] = []
    if binding.leveling_root is not None and binding.domain != "generic":
        domain_dir = binding.leveling_root / "domains" / binding.domain
        candidates.extend([domain_dir / "RULES.md", domain_dir / "rules.md"])

    if binding.domain != "generic":
        candidates.append(repo_root / "domains" / binding.domain / "rules.md")

    candidates.append(repo_root / "domains" / "generic" / "rules.md")

    for path in candidates:
        if path.is_file():
            return _read(path), path

    raise FileNotFoundError("No domain rules bundle found (expected generic fallback).")


def extract_hint_block(hint_levels_text: str, level: int) -> str:
    pattern = rf"^## Level {level}\s*$"
    lines = hint_levels_text.splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(pattern, line)), None)
    if start is None:
        raise ValueError(f"Hint level {level} not found in prompts/hint-levels.md")

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^## Level \d+\s*$", lines[i]):
            end = i
            break

    block = "\n".join(lines[start:end]).strip()
    return block


def assemble_preamble(
    binding: Binding,
    *,
    mode: str = "mentor",
    hint_level: int = 2,
) -> Preamble:
    if mode not in VALID_MODES:
        raise ValueError(f"Unknown mode {mode!r}; expected one of {VALID_MODES}")
    if hint_level not in range(1, 6):
        raise ValueError(f"hint_level must be 1–5, got {hint_level}")

    repo_root = binding.repo_root
    sources: list[str] = []

    base_path = repo_root / "prompts" / "base.md"
    mode_path = repo_root / "prompts" / "modes" / f"{mode}.md"
    hint_path = repo_root / "prompts" / "hint-levels.md"

    for path in (base_path, mode_path, hint_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    domain_text, domain_path = resolve_domain_rules(repo_root, binding)
    hint_block = extract_hint_block(_read(hint_path), hint_level)

    sources.extend(
        [
            str(base_path.relative_to(repo_root)),
            str(mode_path.relative_to(repo_root)),
            str(domain_path.relative_to(repo_root)),
            f"prompts/hint-levels.md#level-{hint_level}",
        ]
    )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    leveling_display = str(binding.leveling_root) if binding.leveling_root else "—"
    project_display = binding.project or "—"

    header_lines = [
        "=== Deep Tutor preamble (inspect) ===",
        f"generated: {generated_at}",
        f"cwd: {binding.cwd}",
        f"leveling_root: {leveling_display}",
        f"domain: {binding.domain} (source: {binding.domain_source})",
        f"project: {project_display}",
        f"mode: {mode}",
        f"hint_level: {hint_level}",
        f"sources: {' + '.join(sources)}",
        "=====================================",
        "",
    ]

    sections = [
        _read(base_path),
        _read(mode_path),
        domain_text,
        hint_block,
    ]

    if binding.curated_context:
        sections.append(
            "## Curated domain context\n\n"
            "_From leveling workspace (README.md or CONTEXT.md):_\n\n"
            + binding.curated_context
        )
        sources.append("leveling curated context")

    config = load_config(repo_root)
    store = open_store(repo_root, config)
    memory_slice = store.read_slice(domain=binding.domain, project=binding.project)
    memory_text = format_memory_slice(memory_slice, db_path=store.db_path)
    if memory_text:
        sections.append(memory_text)
        sources.append("memory slice")

    body = "\n\n---\n\n".join(sections)
    text = "\n".join(header_lines) + body + "\n"

    return Preamble(
        text=text,
        binding=binding,
        mode=mode,
        hint_level=hint_level,
        sources=sources,
    )


def default_mode_and_hint(repo_root: Path) -> tuple[str, int]:
    config = load_config(repo_root)
    mode = config.get("default_mode", "mentor")
    hint_level = int(config.get("default_hint_level", 2))
    return mode, hint_level
