"""Deep Tutor orchestrator — binding, routing, preamble assembly, OpenCode hook."""

from orchestrator.assemble import assemble_preamble
from orchestrator.bind import bind_context
from orchestrator.opencode import build_opencode_context, resolve_deep_tutor_root
from orchestrator.routing import (
    RoutingDecision,
    Signals,
    extract_signals,
    log_routing_decision,
    route,
)

__all__ = [
    "RoutingDecision",
    "Signals",
    "assemble_preamble",
    "bind_context",
    "build_opencode_context",
    "extract_signals",
    "log_routing_decision",
    "resolve_deep_tutor_root",
    "route",
]
