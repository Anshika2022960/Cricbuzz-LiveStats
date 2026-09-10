import sqlite3


conn = sqlite3.connect("database/cricket.db")
cursor = conn.cursor()


# -------------------------------------------------
# PLAYERS
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    country TEXT,
    playing_role TEXT,
    batting_style TEXT,
    bowling_style TEXT
)
""")


# -------------------------------------------------
# TEAMS
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL,
    country TEXT
)
""")


# -------------------------------------------------
# VENUES
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name TEXT,
    city TEXT,
    country TEXT,
    capacity INTEGER
)
""")


# -------------------------------------------------
# SERIES
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY,
    series_name TEXT,
    host_country TEXT,
    match_type TEXT,
    start_date TEXT,
    end_date TEXT,
    total_matches INTEGER
)
""")


# -------------------------------------------------
# MATCHES
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    match_description TEXT,
    team1_id INTEGER,
    team2_id INTEGER,
    venue_id INTEGER,
    series_id INTEGER,
    match_date TEXT,
    match_format TEXT,
    match_status TEXT,
    winning_team_id INTEGER,
    victory_margin INTEGER,
    victory_type TEXT,
    toss_winner_id INTEGER,
    toss_decision TEXT,

    FOREIGN KEY(team1_id) REFERENCES teams(team_id),
    FOREIGN KEY(team2_id) REFERENCES teams(team_id),
    FOREIGN KEY(venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY(series_id) REFERENCES series(series_id)
)
""")


# -------------------------------------------------
# BATTING STATISTICS
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS batting_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    innings INTEGER,
    batting_position INTEGER,
    runs INTEGER,
    balls INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate REAL,
    not_out INTEGER DEFAULT 0,

    FOREIGN KEY(match_id) REFERENCES matches(match_id),
    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")


# -------------------------------------------------
# BOWLING STATISTICS
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS bowling_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    innings INTEGER,
    overs REAL,
    runs_conceded INTEGER,
    wickets INTEGER,
    economy_rate REAL,

    FOREIGN KEY(match_id) REFERENCES matches(match_id),
    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")


# -------------------------------------------------
# CAREER STATISTICS
# -------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_career_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    format TEXT,
    matches INTEGER,
    innings INTEGER,
    runs INTEGER,
    batting_average REAL,
    strike_rate REAL,
    highest_score INTEGER,
    centuries INTEGER,
    fifties INTEGER,
    wickets INTEGER,
    bowling_average REAL,
    economy_rate REAL,
    catches INTEGER,
    stumpings INTEGER,

    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")


conn.commit()
conn.close()

print("Database tables created successfully.")