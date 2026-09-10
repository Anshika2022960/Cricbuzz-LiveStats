import sqlite3


conn = sqlite3.connect("database/cricket.db")
cursor = conn.cursor()


players = [
    (1, "Virat Kohli", "India", "Batsman",
     "Right Handed Bat", "Right-arm Medium"),

    (2, "Rohit Sharma", "India", "Batsman",
     "Right Handed Bat", "Right-arm Offbreak"),

    (3, "Jasprit Bumrah", "India", "Bowler",
     "Right Handed Bat", "Right-arm Fast"),

    (4, "Ben Stokes", "England", "All-rounder",
     "Left Handed Bat", "Right-arm Fast"),

    (5, "Joe Root", "England", "Batsman",
     "Right Handed Bat", "Right-arm Offbreak")
]


cursor.executemany("""
INSERT OR REPLACE INTO players
(player_id, full_name, country, playing_role,
 batting_style, bowling_style)
VALUES (?, ?, ?, ?, ?, ?)
""", players)


teams = [
    (1, "India", "India"),
    (2, "England", "England"),
    (3, "Australia", "Australia")
]


cursor.executemany("""
INSERT OR REPLACE INTO teams
(team_id, team_name, country)
VALUES (?, ?, ?)
""", teams)


venues = [
    (
        1,
        "Narendra Modi Stadium",
        "Ahmedabad",
        "India",
        132000
    ),

    (
        2,
        "Melbourne Cricket Ground",
        "Melbourne",
        "Australia",
        100024
    ),

    (
        3,
        "Eden Gardens",
        "Kolkata",
        "India",
        68000
    )
]


cursor.executemany("""
INSERT OR REPLACE INTO venues
(venue_id, venue_name, city, country, capacity)
VALUES (?, ?, ?, ?, ?)
""", venues)


career_stats = [
    (1, "ODI", 300, 14000, 58.5, 93.6, 183,
     51, 74, 5, 0, 0, 160, 0),

    (2, "ODI", 270, 11000, 49.5, 92.4, 264,
     32, 55, 8, 45.0, 5.8, 95, 0),

    (3, "ODI", 100, 150, 7.5, 55.0, 16,
     0, 0, 180, 23.5, 4.6, 30, 0),

    (4, "ODI", 120, 3500, 39.0, 95.5, 102,
     5, 22, 90, 32.5, 5.7, 50, 0)
]


for data in career_stats:

    cursor.execute("""
    INSERT INTO player_career_stats
    (
        player_id,
        format,
        matches,
        runs,
        batting_average,
        strike_rate,
        highest_score,
        centuries,
        fifties,
        wickets,
        bowling_average,
        economy_rate,
        catches,
        stumpings
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)


conn.commit()
conn.close()

print("Sample data inserted successfully.")