"""Routing v1: signals → teach mode + optional logging (system-design §7)."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from orchestrator.bind import Binding, load_config

VALID_MODES = ("mentor", "debug", "concept")
CLASSIFICATIONS = ("debug", "concept", "guided_work", "meta")


@dataclass(frozen=True)
class Signals:
    has_stack_trace: bool = False
    test_failure: bool = False
    wrong_output: bool = False
    crash_language: bool = False
    reproduction_attempt: bool = False
    partial_code: bool = False
    approach_question: bool = False
    stuck_no_error: bool = False
    theory_question: bool = False
    comparison: bool = False
    definition: bool = False
    mental_model: bool = False
    meta_request: bool = False

    def has_hard_debug(self) -> bool:
        if self.has_stack_trace or self.test_failure:
            return True
        if self.wrong_output and (self.partial_code or self.reproduction_attempt):
            return True
        if not self.crash_language:
            return False
        if (
            self.partial_code
            or self.reproduction_attempt
            or self.wrong_output
        ):
            return True
        if self.theory_question or self.definition or self.mental_model:
            return False
        return True

    def has_theory(self) -> bool:
        return (
            self.theory_question
            or self.comparison
            or self.definition
            or self.mental_model
        )

    def has_guided_work(self) -> bool:
        return self.partial_code or self.approach_question or self.stuck_no_error

    def to_dict(self) -> dict[str, bool]:
        return {key: value for key, value in asdict(self).items()}


@dataclass(frozen=True)
class RoutingDecision:
    mode: str
    classification: str
    signals: Signals
    reasons: tuple[str, ...] = ()
    secondary: str | None = None
    rule_step: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "classification": self.classification,
            "secondary": self.secondary,
            "rule_step": self.rule_step,
            "reasons": list(self.reasons),
            "signals": self.signals.to_dict(),
        }


_TRACE_PATTERNS = (
    re.compile(r"Traceback \(most recent call last\)", re.I),
    re.compile(r"^\s*File \"[^\"]+\", line \d+", re.M),
    re.compile(r"^\s*at .+\(.+:\d+:\d+\)", re.M),
    re.compile(r"panicked at ", re.I),
    re.compile(r"thread '.+' panicked", re.I),
)

_TEST_FAILURE_PATTERNS = (
    re.compile(r"=+ FAILURES =+", re.I),
    re.compile(r"FAILED\s+[\w./-]+", re.I),
    re.compile(r"AssertionError", re.I),
    re.compile(r"assertion failed", re.I),
    re.compile(r"\d+ failed", re.I),
    re.compile(r"Test Suites:.*failed", re.I),
)

_WRONG_OUTPUT_PATTERNS = (
    re.compile(r"expected .+ (?:but )?got", re.I),
    re.compile(r"Expected:\s*.+\n\s*Actual:", re.I),
    re.compile(r"assert(?:Equal|AlmostEqual|Raises).*failed", re.I),
)

_CRASH_LANGUAGE_PATTERNS = (
    re.compile(
        r"\b(?:IndexError|KeyError|TypeError|ValueError|AttributeError|"
        r"NullPointerException|Segmentation fault|segfault|"
        r"panic!|unhandled exception|fatal error)\b",
        re.I,
    ),
    re.compile(r"\b500\b.*\b(?:trace|traceback|stack)\b", re.I),
    re.compile(r"\bwhy does (?:this|it) crash\b", re.I),
    re.compile(r"\bnull pointer\b", re.I),
)

_REPRODUCTION_PATTERNS = (
    re.compile(r"\bsteps to reproduce\b", re.I),
    re.compile(r"\b(?:always|reliably) fails when\b", re.I),
    re.compile(r"\bwhen I run\b", re.I),
    re.compile(r"\brepro(?:duces|duction)\b", re.I),
)

_PARTIAL_CODE_PATTERNS = (
    re.compile(r"```"),
    re.compile(r"^\s*(?:def |class |import |fn |func |const |let )", re.M),
    re.compile(r"[{;]\s*$", re.M),
)

_APPROACH_PATTERNS = (
    re.compile(r"\bhow should I (?:structure|approach|solve)\b", re.I),
    re.compile(r"\bwhich (?:data structure|algorithm|pattern)\b", re.I),
    re.compile(r"\bis this (?:the right|a good) approach\b", re.I),
    re.compile(r"\bhow do I (?:structure|design|implement)\b", re.I),
)

_STUCK_PATTERNS = (
    re.compile(r"\bI'?m stuck\b", re.I),
    re.compile(r"\bno idea (?:how|what) to\b", re.I),
)

_THEORY_PATTERNS = (
    re.compile(r"\bwhat is (?:a |an |the )?\w+", re.I),
    re.compile(r"\bexplain (?:how |what |why )?", re.I),
    re.compile(r"\bhelp me understand\b", re.I),
)

_COMPARISON_PATTERNS = (
    re.compile(r"\bvs\.?\b", re.I),
    re.compile(r"\bversus\b", re.I),
    re.compile(r"\bcompare\b", re.I),
    re.compile(r"\bdifference between\b", re.I),
)

_DEFINITION_PATTERNS = (
    re.compile(r"\bwhat does .+ mean\b", re.I),
    re.compile(r"\bdefine \w+\b", re.I),
)

_MENTAL_MODEL_PATTERNS = (
    re.compile(r"\bhow does .+ work conceptually\b", re.I),
    re.compile(r"\bmental model\b", re.I),
)

_META_PATTERNS = (
    re.compile(r"\bdeep tutor\b", re.I),
    re.compile(r"\bpreamble\b", re.I),
    re.compile(r"\bhint level\b", re.I),
)


def _any_match(patterns: tuple[re.Pattern[str], ...], text: str) -> bool:
    return any(p.search(text) for p in patterns)


def extract_signals(utterance: str) -> Signals:
    """Derive routing flags from the user message (§7 signal extraction)."""
    text = (utterance or "").strip()
    if not text:
        return Signals()

    has_trace = _any_match(_TRACE_PATTERNS, text)
    test_fail = _any_match(_TEST_FAILURE_PATTERNS, text)
    wrong_out = _any_match(_WRONG_OUTPUT_PATTERNS, text)
    crash = _any_match(_CRASH_LANGUAGE_PATTERNS, text)
    repro = _any_match(_REPRODUCTION_PATTERNS, text)
    partial = _any_match(_PARTIAL_CODE_PATTERNS, text)
    approach = _any_match(_APPROACH_PATTERNS, text)
    stuck = _any_match(_STUCK_PATTERNS, text) and not has_trace and not test_fail
    theory = _any_match(_THEORY_PATTERNS, text)
    comparison = _any_match(_COMPARISON_PATTERNS, text)
    definition = _any_match(_DEFINITION_PATTERNS, text)
    mental = _any_match(_MENTAL_MODEL_PATTERNS, text)
    meta = _any_match(_META_PATTERNS, text)

    return Signals(
        has_stack_trace=has_trace,
        test_failure=test_fail,
        wrong_output=wrong_out,
        crash_language=crash,
        reproduction_attempt=repro,
        partial_code=partial,
        approach_question=approach,
        stuck_no_error=stuck,
        theory_question=theory,
        comparison=comparison,
        definition=definition,
        mental_model=mental,
        meta_request=meta,
    )


def classify(signals: Signals) -> str:
    """Map signals to task type (§7 classification)."""
    if signals.meta_request and not signals.has_hard_debug():
        return "meta"
    if signals.has_hard_debug():
        return "debug"
    if signals.has_theory() and not signals.has_hard_debug():
        return "concept"
    if signals.has_guided_work():
        return "guided_work"
    return "guided_work"


def route(
    utterance: str,
    *,
    binding: Binding | None = None,
) -> RoutingDecision:
    """
    Select teach mode using default routing priorities (§8.2).

    binding is optional context for logging only in v1.
    """
    _ = binding
    signals = extract_signals(utterance)
    classification = classify(signals)
    reasons: list[str] = []
    secondary: str | None = None
    rule_step: int | None = None
    mode: str

    if classification == "meta":
        mode = "mentor"
        rule_step = 4
        reasons.append("meta_request → mentor (default posture)")
    elif signals.has_hard_debug():
        mode = "debug"
        rule_step = 2
        reasons.append("hard debug signals → debug")
        if signals.has_theory():
            secondary = "concept"
            rule_step = 5
            reasons.append("theory + failure → debug first; secondary concept")
    elif signals.has_theory():
        mode = "concept"
        rule_step = 3
        reasons.append("theory-first without runtime failure → concept")
    elif signals.has_guided_work():
        mode = "mentor"
        rule_step = 4
        reasons.append("guided work without clear runtime failure → mentor")
    else:
        mode = "mentor"
        rule_step = 4
        reasons.append("ambiguous signals → mentor (default)")

    if mode not in VALID_MODES:
        raise ValueError(f"internal routing produced invalid mode {mode!r}")

    return RoutingDecision(
        mode=mode,
        classification=classification,
        signals=signals,
        reasons=tuple(reasons),
        secondary=secondary,
        rule_step=rule_step,
    )


def _routing_log_path(repo_root: Path) -> Path | None:
    env = os.environ.get("DEEP_TUTOR_ROUTING_LOG")
    if env:
        if env.lower() in ("0", "false", "no", "off"):
            return None
        if env.lower() in ("1", "true", "yes", "on"):
            return repo_root / "memory" / "data" / "routing.jsonl"
        return Path(env).expanduser()

    config = load_config(repo_root)
    if config.get("routing_log_enabled") is False:
        return None
    configured = config.get("routing_log")
    if configured:
        path = Path(configured).expanduser()
        return path if path.is_absolute() else repo_root / path
    return repo_root / "memory" / "data" / "routing.jsonl"


def _redact_excerpt(utterance: str, *, max_len: int = 240) -> str:
    text = " ".join(utterance.split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


@dataclass
class RoutingLogEntry:
    timestamp: str
    mode: str
    classification: str
    reasons: list[str]
    signals: dict[str, bool]
    rule_step: int | None
    secondary: str | None
    domain: str | None
    project: str | None
    domain_source: str | None
    cwd: str | None
    utterance_excerpt: str
    utterance_sha256: str

    @classmethod
    def from_decision(
        cls,
        decision: RoutingDecision,
        *,
        utterance: str,
        binding: Binding | None = None,
    ) -> RoutingLogEntry:
        excerpt = _redact_excerpt(utterance)
        digest = hashlib.sha256(utterance.encode("utf-8")).hexdigest()
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            mode=decision.mode,
            classification=decision.classification,
            reasons=list(decision.reasons),
            signals=decision.signals.to_dict(),
            rule_step=decision.rule_step,
            secondary=decision.secondary,
            domain=binding.domain if binding else None,
            project=binding.project if binding else None,
            domain_source=binding.domain_source if binding else None,
            cwd=str(binding.cwd) if binding else None,
            utterance_excerpt=excerpt,
            utterance_sha256=digest,
        )


def log_routing_decision(
    decision: RoutingDecision,
    *,
    utterance: str,
    repo_root: Path,
    binding: Binding | None = None,
) -> Path | None:
    """Append one JSONL record when routing log is enabled (§11.4, §13)."""
    log_path = _routing_log_path(repo_root)
    if log_path is None:
        return None

    entry = RoutingLogEntry.from_decision(
        decision, utterance=utterance, binding=binding
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
    return log_path


def format_routing_summary(decision: RoutingDecision) -> str:
    """Human-readable routing line for CLI / preamble header."""
    parts = [
        f"classification: {decision.classification}",
        f"mode: {decision.mode}",
    ]
    if decision.secondary:
        parts.append(f"secondary: {decision.secondary}")
    if decision.rule_step is not None:
        parts.append(f"rule_step: {decision.rule_step}")
    if decision.reasons:
        parts.append(f"reasons: {'; '.join(decision.reasons)}")
    active = [name for name, on in decision.signals.to_dict().items() if on]
    if active:
        parts.append(f"signals: {', '.join(sorted(active))}")
    return " | ".join(parts)
