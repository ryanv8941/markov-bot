CREATE TABLE IF NOT EXISTS transitions (
    state1     TEXT NOT NULL,
    state2     TEXT NOT NULL,
    next_word  TEXT NOT NULL,
    count      INTEGER DEFAULT 1,
    PRIMARY KEY (state1, state2, next_word)
);

CREATE INDEX IF NOT EXISTS idx_state_lookup
ON transitions (state1, state2);