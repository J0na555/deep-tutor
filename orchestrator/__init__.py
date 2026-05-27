"""Deep Tutor orchestrator — binding, routing, and preamble assembly."""

from orchestrator.assemble import assemble_preamble
from orchestrator.bind import bind_context
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
    "extract_signals",
    "log_routing_decision",
    "route",
]
