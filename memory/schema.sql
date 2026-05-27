-- Deep Tutor learning memory (MVP skeleton, docs/system-design.md §11)

CREATE TABLE IF NOT EXISTS weak_concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    project TEXT,
    concept TEXT NOT NULL,
    notes TEXT,
    updated_at TEXT NOT NULL,
    UNIQUE (domain, project, concept)
);

CREATE TABLE IF NOT EXISTS mistake_fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    project TEXT,
    fingerprint TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    UNIQUE (domain, project, fingerprint)
);

CREATE TABLE IF NOT EXISTS solved_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    project TEXT,
    topic TEXT NOT NULL,
    notes TEXT,
    solved_at TEXT NOT NULL,
    UNIQUE (domain, project, topic)
);

CREATE TABLE IF NOT EXISTS frustration_cues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    project TEXT,
    session_id TEXT,
    cue TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_weak_concepts_domain ON weak_concepts (domain);
CREATE INDEX IF NOT EXISTS idx_mistakes_domain ON mistake_fingerprints (domain);
CREATE INDEX IF NOT EXISTS idx_solved_domain ON solved_topics (domain);
CREATE INDEX IF NOT EXISTS idx_frustration_domain ON frustration_cues (domain);
