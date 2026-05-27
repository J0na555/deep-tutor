"""Minimal SQLite learning memory (docs/system-design.md §11)."""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_db_path(repo_root: Path) -> Path:
    return repo_root / "memory" / "data" / "learning.sqlite"


def resolve_db_path(repo_root: Path, config: dict | None = None) -> Path:
    env = os.environ.get("DEEP_TUTOR_MEMORY_DB")
    if env:
        return Path(env).expanduser().resolve()

    config = config or {}
    configured = config.get("memory_db")
    if configured:
        path = Path(configured).expanduser()
        if not path.is_absolute():
            path = repo_root / path
        return path.resolve()

    return default_db_path(repo_root)


@dataclass(frozen=True)
class WeakConcept:
    concept: str
    notes: str | None
    updated_at: str


@dataclass(frozen=True)
class MistakeFingerprint:
    fingerprint: str
    count: int
    notes: str | None
    first_seen_at: str
    last_seen_at: str


@dataclass(frozen=True)
class SolvedTopic:
    topic: str
    notes: str | None
    solved_at: str


@dataclass(frozen=True)
class FrustrationCue:
    cue: str
    session_id: str | None
    recorded_at: str


@dataclass
class MemorySlice:
    domain: str
    project: str | None
    weak_concepts: list[WeakConcept] = field(default_factory=list)
    mistakes: list[MistakeFingerprint] = field(default_factory=list)
    solved_topics: list[SolvedTopic] = field(default_factory=list)
    frustration_cues: list[FrustrationCue] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (
            self.weak_concepts
            or self.mistakes
            or self.solved_topics
            or self.frustration_cues
        )


class MemoryStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def ensure_schema(self) -> None:
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        sql = schema_path.read_text(encoding="utf-8")
        with self.connect() as conn:
            conn.executescript(sql)

    def read_slice(
        self,
        *,
        domain: str,
        project: str | None = None,
        mistake_limit: int = 10,
        frustration_limit: int = 5,
    ) -> MemorySlice:
        slice_ = MemorySlice(domain=domain, project=project)
        if domain == "generic":
            return slice_

        with self.connect() as conn:
            slice_.weak_concepts = self._fetch_weak_concepts(conn, domain, project)
            slice_.mistakes = self._fetch_mistakes(
                conn, domain, project, limit=mistake_limit
            )
            slice_.solved_topics = self._fetch_solved(conn, domain, project)
            slice_.frustration_cues = self._fetch_frustration(
                conn, domain, project, limit=frustration_limit
            )
        return slice_

    def add_weak_concept(
        self,
        concept: str,
        *,
        domain: str,
        project: str | None = None,
        notes: str | None = None,
    ) -> None:
        now = _utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO weak_concepts (domain, project, concept, notes, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(domain, project, concept) DO UPDATE SET
                    notes = COALESCE(excluded.notes, weak_concepts.notes),
                    updated_at = excluded.updated_at
                """,
                (domain, project, concept.strip(), notes, now),
            )

    def record_mistake(
        self,
        fingerprint: str,
        *,
        domain: str,
        project: str | None = None,
        notes: str | None = None,
    ) -> int:
        now = _utc_now()
        fp = fingerprint.strip()
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT id, count FROM mistake_fingerprints
                WHERE domain = ? AND project IS ? AND fingerprint = ?
                """,
                (domain, project, fp),
            ).fetchone()
            if row is None:
                conn.execute(
                    """
                    INSERT INTO mistake_fingerprints
                        (domain, project, fingerprint, count, notes, first_seen_at, last_seen_at)
                    VALUES (?, ?, ?, 1, ?, ?, ?)
                    """,
                    (domain, project, fp, notes, now, now),
                )
                return 1
            new_count = int(row["count"]) + 1
            conn.execute(
                """
                UPDATE mistake_fingerprints
                SET count = ?, last_seen_at = ?,
                    notes = COALESCE(?, notes)
                WHERE id = ?
                """,
                (new_count, now, notes, row["id"]),
            )
            return new_count

    def mark_solved(
        self,
        topic: str,
        *,
        domain: str,
        project: str | None = None,
        notes: str | None = None,
    ) -> None:
        now = _utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO solved_topics (domain, project, topic, notes, solved_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(domain, project, topic) DO UPDATE SET
                    notes = COALESCE(excluded.notes, solved_topics.notes),
                    solved_at = excluded.solved_at
                """,
                (domain, project, topic.strip(), notes, now),
            )

    def record_frustration(
        self,
        cue: str,
        *,
        domain: str,
        project: str | None = None,
        session_id: str | None = None,
    ) -> None:
        now = _utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO frustration_cues
                    (domain, project, session_id, cue, recorded_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (domain, project, session_id, cue.strip(), now),
            )

    @staticmethod
    def _scope_clause(project: str | None) -> tuple[str, tuple[str, ...]]:
        if project is None:
            return "domain = ? AND project IS NULL", ()
        return "domain = ? AND (project IS NULL OR project = ?)", (project,)

    def _fetch_weak_concepts(
        self,
        conn: sqlite3.Connection,
        domain: str,
        project: str | None,
    ) -> list[WeakConcept]:
        extra, extra_params = self._scope_clause(project)
        rows = conn.execute(
            f"""
            SELECT concept, notes, updated_at FROM weak_concepts
            WHERE {extra}
            ORDER BY updated_at DESC
            """,
            (domain, *extra_params),
        ).fetchall()
        return [
            WeakConcept(
                concept=row["concept"],
                notes=row["notes"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    def _fetch_mistakes(
        self,
        conn: sqlite3.Connection,
        domain: str,
        project: str | None,
        *,
        limit: int,
    ) -> list[MistakeFingerprint]:
        extra, extra_params = self._scope_clause(project)
        rows = conn.execute(
            f"""
            SELECT fingerprint, count, notes, first_seen_at, last_seen_at
            FROM mistake_fingerprints
            WHERE {extra}
            ORDER BY count DESC, last_seen_at DESC
            LIMIT ?
            """,
            (domain, *extra_params, limit),
        ).fetchall()
        return [
            MistakeFingerprint(
                fingerprint=row["fingerprint"],
                count=int(row["count"]),
                notes=row["notes"],
                first_seen_at=row["first_seen_at"],
                last_seen_at=row["last_seen_at"],
            )
            for row in rows
        ]

    def _fetch_solved(
        self,
        conn: sqlite3.Connection,
        domain: str,
        project: str | None,
    ) -> list[SolvedTopic]:
        extra, extra_params = self._scope_clause(project)
        rows = conn.execute(
            f"""
            SELECT topic, notes, solved_at FROM solved_topics
            WHERE {extra}
            ORDER BY solved_at DESC
            """,
            (domain, *extra_params),
        ).fetchall()
        return [
            SolvedTopic(
                topic=row["topic"],
                notes=row["notes"],
                solved_at=row["solved_at"],
            )
            for row in rows
        ]

    def _fetch_frustration(
        self,
        conn: sqlite3.Connection,
        domain: str,
        project: str | None,
        *,
        limit: int,
    ) -> list[FrustrationCue]:
        extra, extra_params = self._scope_clause(project)
        rows = conn.execute(
            f"""
            SELECT cue, session_id, recorded_at FROM frustration_cues
            WHERE {extra}
            ORDER BY recorded_at DESC
            LIMIT ?
            """,
            (domain, *extra_params, limit),
        ).fetchall()
        return [
            FrustrationCue(
                cue=row["cue"],
                session_id=row["session_id"],
                recorded_at=row["recorded_at"],
            )
            for row in rows
        ]


def format_memory_slice(slice_: MemorySlice, *, db_path: Path) -> str:
    if slice_.is_empty:
        return ""

    scope_bits = [f"domain `{slice_.domain}`"]
    if slice_.project:
        scope_bits.append(f"project `{slice_.project}`")
    scope = ", ".join(scope_bits)

    lines = [
        "## Learning memory",
        "",
        f"_Slice for {scope} (from `{db_path}`)._",
        "",
        "Use this to calibrate hints—not to preempt the learner's next step.",
        "",
    ]

    if slice_.weak_concepts:
        lines.append("### Weak concepts")
        for item in slice_.weak_concepts:
            line = f"- **{item.concept}**"
            if item.notes:
                line += f" — {item.notes}"
            lines.append(line)
        lines.append("")

    if slice_.mistakes:
        lines.append("### Repeated mistakes (fingerprints)")
        for item in slice_.mistakes:
            line = f"- **{item.fingerprint}** (×{item.count}, last {item.last_seen_at})"
            if item.notes:
                line += f" — {item.notes}"
            lines.append(line)
        lines.append("")

    if slice_.solved_topics:
        lines.append("### Solved topics (avoid redundant drilling)")
        for item in slice_.solved_topics:
            line = f"- **{item.topic}** (since {item.solved_at})"
            if item.notes:
                line += f" — {item.notes}"
            lines.append(line)
        lines.append("")

    if slice_.frustration_cues:
        lines.append("### Recent frustration cues")
        for item in slice_.frustration_cues:
            line = f"- {item.cue} ({item.recorded_at})"
            if item.session_id:
                line += f" [session {item.session_id}]"
            lines.append(line)
        lines.append("")

    return "\n".join(lines).strip()


def open_store(repo_root: Path, config: dict | None = None) -> MemoryStore:
    db_path = resolve_db_path(repo_root, config)
    store = MemoryStore(db_path)
    store.ensure_schema()
    return store
