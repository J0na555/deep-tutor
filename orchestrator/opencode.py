"""OpenCode integration — resolve repo root and build injectable preamble context."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from orchestrator.assemble import assemble_preamble, default_mode_and_hint
from orchestrator.bind import bind_context
from orchestrator.routing import RoutingDecision, log_routing_decision, route

_REPO_MARKERS = (
    Path("orchestrator") / "assemble.py",
    Path("configs") / "default.json",
)


def is_deep_tutor_root(path: Path) -> bool:
    resolved = path.resolve()
    return all((resolved / marker).is_file() for marker in _REPO_MARKERS)


def resolve_deep_tutor_root(
    start: Path | None = None,
    *,
    explicit: str | None = None,
) -> Path | None:
    """
    Locate the deep-tutor repository from env, explicit path, or filesystem walk.

    Search order:
    1. ``explicit`` argument
    2. ``DEEP_TUTOR_ROOT`` environment variable
    3. Walk upward from ``start`` (or cwd) for orchestrator/assemble.py + configs/default.json
    4. Sibling ``deep-tutor/`` next to a discovered leveling root
    """
    if explicit:
        path = Path(explicit).expanduser().resolve()
        return path if is_deep_tutor_root(path) else None

    env = os.environ.get("DEEP_TUTOR_ROOT")
    if env:
        path = Path(env).expanduser().resolve()
        return path if is_deep_tutor_root(path) else None

    resolved_start = (start or Path.cwd()).expanduser().resolve()
    for parent in [resolved_start, *resolved_start.parents]:
        if is_deep_tutor_root(parent):
            return parent
        sibling = parent / "deep-tutor"
        if is_deep_tutor_root(sibling):
            return sibling.resolve()

    return None


def build_opencode_context(
    repo_root: Path,
    *,
    cwd: Path,
    message: str | None = None,
    domain: str | None = None,
    leveling_root: str | None = None,
    mode: str | None = None,
    hint_level: int | None = None,
    log_routing: bool = True,
) -> dict[str, Any]:
    """
    Assemble preamble text and metadata for OpenCode system-prompt injection.

    When ``message`` is provided, routing v1 selects the teach mode unless
    ``mode`` is set explicitly.
    """
    binding = bind_context(
        repo_root=repo_root,
        cwd=cwd,
        domain_flag=domain,
        leveling_root_override=leveling_root,
    )

    routing_decision: RoutingDecision | None = None
    selected_mode = mode
    if message and message.strip():
        routing_decision = route(message, binding=binding)
        if selected_mode is None:
            selected_mode = routing_decision.mode
        if log_routing:
            log_routing_decision(
                routing_decision,
                utterance=message,
                repo_root=repo_root,
                binding=binding,
            )

    if selected_mode is None:
        selected_mode, default_hint = default_mode_and_hint(repo_root)
        if hint_level is None:
            hint_level = default_hint

    if hint_level is None:
        _, hint_level = default_mode_and_hint(repo_root)

    preamble = assemble_preamble(
        binding,
        mode=selected_mode,
        hint_level=hint_level,
        routing=routing_decision,
    )

    payload: dict[str, Any] = {
        "text": preamble.text,
        "mode": preamble.mode,
        "hint_level": preamble.hint_level,
        "domain": binding.domain,
        "project": binding.project,
        "domain_source": binding.domain_source,
        "cwd": str(binding.cwd),
        "leveling_root": str(binding.leveling_root) if binding.leveling_root else None,
        "sources": preamble.sources,
    }
    if routing_decision is not None:
        payload["routing"] = routing_decision.to_dict()
    return payload
