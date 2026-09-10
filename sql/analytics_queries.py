"""
Cricbuzz LiveStats
SQL Analytics Queries - Q1 to Q25

Database: SQLite
"""

# ============================================================
# BEGINNER LEVEL - Q1 TO Q8
# ============================================================


# ============================================================
# Q1 - INDIAN PLAYERS
# ============================================================

query_1 = """
SELECT
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name;
"""


# ============================================================
# Q2 - MATCHES PLAYED IN LAST 30 DAYS
# ============================================================

query_2 = """
SELECT
    m.match_description,
    t1.team_name AS team1,
    t2.team_name AS team2,
    v.venue_name,
    v.city,
    m.match_date
FROM matches m
JOIN teams t1
    ON m.team1_id = t1.team_id
JOIN teams t2
    ON m.team2_id = t2.team_id
LEFT JOIN venues v
    ON m.venue_id = v.venue_id
WHERE DATE(m.match_date) >= DATE('now', '-30 days')
ORDER BY m.match_date DESC;
"""


# ============================================================
# Q3 - TOP 10 ODI RUN SCORERS
# ============================================================

query_3 = """
SELECT
    p.full_name,
    pcs.runs,
    pcs.batting_average,
    pcs.centuries
FROM player_career_stats pcs
JOIN players p
    ON pcs.player_id = p.player_id
WHERE UPPER(pcs.format) = 'ODI'
ORDER BY pcs.runs DESC
LIMIT 10;
"""


# ============================================================
# Q4 - VENUES WITH CAPACITY ABOVE 50,000
# ============================================================

query_4 = """
SELECT
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""


# ============================================================
# Q5 - TOTAL MATCHES WON BY EACH TEAM
# ============================================================

query_5 = """
SELECT
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
LEFT JOIN matches m
    ON t.team_id = m.winning_team_id
GROUP BY
    t.team_id,
    t.team_name
ORDER BY total_wins DESC;
"""


# ============================================================
# Q6 - NUMBER OF PLAYERS BY PLAYING ROLE
# ============================================================

query_6 = """
SELECT
    playing_role,
    COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
"""


# ============================================================
# Q7 - HIGHEST BATTING SCORE BY FORMAT
# ============================================================

query_7 = """
SELECT
    format,
    MAX(highest_score) AS highest_score
FROM player_career_stats
GROUP BY format
ORDER BY highest_score DESC;
"""


# ============================================================
# Q8 - SERIES STARTED IN 2024
# ============================================================

query_8 = """
SELECT
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date;
"""


# ============================================================
# INTERMEDIATE LEVEL - Q9 TO Q16
# ============================================================


# ============================================================
# Q9 - ALL-ROUNDERS WITH 1000+ RUNS AND 50+ WICKETS
# ============================================================

query_9 = """
SELECT
    p.full_name,
    pcs.runs AS total_runs,
    pcs.wickets AS total_wickets,
    pcs.format
FROM player_career_stats pcs
JOIN players p
    ON pcs.player_id = p.player_id
WHERE
    LOWER(p.playing_role) IN (
        'all-rounder',
        'all rounder',
        'allrounder'
    )
    AND pcs.runs > 1000
    AND pcs.wickets > 50
ORDER BY
    pcs.runs DESC,
    pcs.wickets DESC;
"""


# ============================================================
# Q10 - LAST 20 COMPLETED MATCHES
# ============================================================

query_10 = """
SELECT
    m.match_description,
    t1.team_name AS team1,
    t2.team_name AS team2,
    wt.team_name AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name,
    m.match_date
FROM matches m
JOIN teams t1
    ON m.team1_id = t1.team_id
JOIN teams t2
    ON m.team2_id = t2.team_id
LEFT JOIN teams wt
    ON m.winning_team_id = wt.team_id
LEFT JOIN venues v
    ON m.venue_id = v.venue_id
WHERE LOWER(m.match_status) = 'completed'
ORDER BY m.match_date DESC
LIMIT 20;
"""


# ============================================================
# Q11 - PERFORMANCE ACROSS DIFFERENT FORMATS
# ============================================================

query_11 = """
SELECT
    p.full_name,

    SUM(
        CASE
            WHEN UPPER(pcs.format) = 'TEST'
            THEN COALESCE(pcs.runs, 0)
            ELSE 0
        END
    ) AS test_runs,

    SUM(
        CASE
            WHEN UPPER(pcs.format) = 'ODI'
            THEN COALESCE(pcs.runs, 0)
            ELSE 0
        END
    ) AS odi_runs,

    SUM(
        CASE
            WHEN UPPER(pcs.format) IN ('T20', 'T20I')
            THEN COALESCE(pcs.runs, 0)
            ELSE 0
        END
    ) AS t20i_runs,

    ROUND(
        AVG(pcs.batting_average),
        2
    ) AS overall_batting_average,

    COUNT(DISTINCT pcs.format) AS formats_played

FROM player_career_stats pcs
JOIN players p
    ON pcs.player_id = p.player_id

GROUP BY
    p.player_id,
    p.full_name

HAVING COUNT(DISTINCT pcs.format) >= 2

ORDER BY overall_batting_average DESC;
"""


# ============================================================
# Q12 - HOME VS AWAY TEAM PERFORMANCE
# ============================================================

query_12 = """
SELECT
    t.team_name,

    SUM(
        CASE
            WHEN LOWER(v.country) = LOWER(t.country)
                 AND m.winning_team_id = t.team_id
            THEN 1
            ELSE 0
        END
    ) AS home_wins,

    SUM(
        CASE
            WHEN LOWER(v.country) <> LOWER(t.country)
                 AND m.winning_team_id = t.team_id
            THEN 1
            ELSE 0
        END
    ) AS away_wins,

    SUM(
        CASE
            WHEN LOWER(v.country) = LOWER(t.country)
            THEN 1
            ELSE 0
        END
    ) AS home_matches,

    SUM(
        CASE
            WHEN LOWER(v.country) <> LOWER(t.country)
            THEN 1
            ELSE 0
        END
    ) AS away_matches

FROM teams t
JOIN matches m
    ON (
        m.team1_id = t.team_id
        OR m.team2_id = t.team_id
    )
JOIN venues v
    ON m.venue_id = v.venue_id

GROUP BY
    t.team_id,
    t.team_name

ORDER BY
    home_wins DESC,
    away_wins DESC;
"""


# ============================================================
# Q13 - CONSECUTIVE BATSMEN WITH 100+ COMBINED RUNS
# ============================================================

query_13 = """
SELECT
    p1.full_name AS batsman_1,
    p2.full_name AS batsman_2,
    b1.match_id,
    b1.innings,
    b1.runs AS batsman_1_runs,
    b2.runs AS batsman_2_runs,
    (b1.runs + b2.runs) AS combined_runs
FROM batting_stats b1
JOIN batting_stats b2
    ON b1.match_id = b2.match_id
    AND b1.innings = b2.innings
    AND b2.batting_position = b1.batting_position + 1
JOIN players p1
    ON b1.player_id = p1.player_id
JOIN players p2
    ON b2.player_id = p2.player_id
WHERE (b1.runs + b2.runs) >= 100
ORDER BY combined_runs DESC;
"""


# ============================================================
# Q14 - BOWLING PERFORMANCE AT DIFFERENT VENUES
# ============================================================

query_14 = """
SELECT
    p.full_name AS bowler,
    v.venue_name,

    ROUND(
        AVG(bs.economy_rate),
        2
    ) AS average_economy_rate,

    SUM(bs.wickets) AS total_wickets,

    COUNT(DISTINCT bs.match_id) AS matches_played

FROM bowling_stats bs
JOIN players p
    ON bs.player_id = p.player_id
JOIN matches m
    ON bs.match_id = m.match_id
JOIN venues v
    ON m.venue_id = v.venue_id

WHERE bs.overs >= 4

GROUP BY
    p.player_id,
    p.full_name,
    v.venue_id,
    v.venue_name

HAVING COUNT(DISTINCT bs.match_id) >= 3

ORDER BY
    average_economy_rate ASC,
    total_wickets DESC;
"""


# ============================================================
# Q15 - PLAYER PERFORMANCE IN CLOSE MATCHES
# ============================================================

query_15 = """
SELECT
    p.full_name,

    ROUND(
        AVG(bs.runs),
        2
    ) AS average_runs,

    COUNT(DISTINCT bs.match_id) AS close_matches_played,

    MAX(bs.runs) AS highest_score_in_close_match

FROM batting_stats bs
JOIN players p
    ON bs.player_id = p.player_id
JOIN matches m
    ON bs.match_id = m.match_id

WHERE
    (
        LOWER(m.victory_type) = 'runs'
        AND m.victory_margin < 50
    )
    OR
    (
        LOWER(m.victory_type) = 'wickets'
        AND m.victory_margin < 5
    )

GROUP BY
    p.player_id,
    p.full_name

ORDER BY
    average_runs DESC,
    close_matches_played DESC;
"""


# ============================================================
# Q16 - YEARLY BATTING PERFORMANCE SINCE 2020
# ============================================================

query_16 = """
SELECT
    p.full_name,

    strftime('%Y', m.match_date) AS year,

    ROUND(
        AVG(bs.runs),
        2
    ) AS average_runs_per_match,

    ROUND(
        AVG(bs.strike_rate),
        2
    ) AS average_strike_rate,

    COUNT(DISTINCT bs.match_id) AS matches_played

FROM batting_stats bs
JOIN players p
    ON bs.player_id = p.player_id
JOIN matches m
    ON bs.match_id = m.match_id

WHERE DATE(m.match_date) >= DATE('2020-01-01')

GROUP BY
    p.player_id,
    p.full_name,
    strftime('%Y', m.match_date)

HAVING COUNT(DISTINCT bs.match_id) >= 5

ORDER BY
    p.full_name,
    year;
"""


# ============================================================
# ADVANCED LEVEL - Q17 TO Q25
# ============================================================


# ============================================================
# Q17 - TOSS WINNING ADVANTAGE
# ============================================================

query_17 = """
SELECT
    COALESCE(m.toss_decision, 'Unknown') AS toss_decision,

    COUNT(*) AS total_matches,

    SUM(
        CASE
            WHEN m.toss_winner_id = m.winning_team_id
            THEN 1
            ELSE 0
        END
    ) AS toss_winner_match_wins,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN m.toss_winner_id = m.winning_team_id
                THEN 1
                ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0),
        2
    ) AS toss_winner_win_percentage

FROM matches m

WHERE
    m.toss_winner_id IS NOT NULL
    AND m.winning_team_id IS NOT NULL

GROUP BY m.toss_decision

ORDER BY toss_winner_win_percentage DESC;
"""


# ============================================================
# Q18 - MOST ECONOMICAL LIMITED-OVERS BOWLERS
# ============================================================

query_18 = """
SELECT
    p.full_name AS bowler,

    ROUND(
        SUM(bs.runs_conceded) /
        NULLIF(SUM(bs.overs), 0),
        2
    ) AS overall_economy_rate,

    SUM(bs.wickets) AS total_wickets,

    COUNT(DISTINCT bs.match_id) AS matches_bowled,

    ROUND(
        AVG(bs.overs),
        2
    ) AS average_overs_per_match

FROM bowling_stats bs
JOIN players p
    ON bs.player_id = p.player_id
JOIN matches m
    ON bs.match_id = m.match_id

WHERE UPPER(m.match_format) IN (
    'ODI',
    'T20',
    'T20I'
)

GROUP BY
    p.player_id,
    p.full_name

HAVING
    COUNT(DISTINCT bs.match_id) >= 10
    AND AVG(bs.overs) >= 2

ORDER BY
    overall_economy_rate ASC,
    total_wickets DESC;
"""


# ============================================================
# Q19 - MOST CONSISTENT BATSMEN
# ============================================================

query_19 = """
WITH eligible_innings AS (
    SELECT
        bs.player_id,
        bs.runs,
        bs.balls
    FROM batting_stats bs
    JOIN matches m
        ON bs.match_id = m.match_id
    WHERE bs.balls >= 10
      AND DATE(m.match_date) >= DATE('2022-01-01')
),

player_summary AS (
    SELECT
        player_id,
        COUNT(*) AS innings_played,
        AVG(runs) AS average_runs,
        AVG(runs * runs) AS average_squared_runs
    FROM eligible_innings
    GROUP BY player_id
)

SELECT
    p.full_name,
    s.innings_played,

    ROUND(
        s.average_runs,
        2
    ) AS average_runs,

    ROUND(
        (
            s.average_squared_runs -
            (s.average_runs * s.average_runs)
        ),
        2
    ) AS runs_variance

FROM player_summary s

JOIN players p
    ON s.player_id = p.player_id

ORDER BY
    runs_variance ASC,
    average_runs DESC;
"""

# ============================================================
# Q20 - FORMAT-WISE MATCHES AND BATTING AVERAGES
# ============================================================

query_20 = """
SELECT
    p.full_name,

    SUM(
        CASE
            WHEN UPPER(pcs.format) = 'TEST'
            THEN COALESCE(pcs.matches, 0)
            ELSE 0
        END
    ) AS test_matches,

    ROUND(
        MAX(
            CASE
                WHEN UPPER(pcs.format) = 'TEST'
                THEN pcs.batting_average
            END
        ),
        2
    ) AS test_batting_average,

    SUM(
        CASE
            WHEN UPPER(pcs.format) = 'ODI'
            THEN COALESCE(pcs.matches, 0)
            ELSE 0
        END
    ) AS odi_matches,

    ROUND(
        MAX(
            CASE
                WHEN UPPER(pcs.format) = 'ODI'
                THEN pcs.batting_average
            END
        ),
        2
    ) AS odi_batting_average,

    SUM(
        CASE
            WHEN UPPER(pcs.format) IN ('T20', 'T20I')
            THEN COALESCE(pcs.matches, 0)
            ELSE 0
        END
    ) AS t20_matches,

    ROUND(
        MAX(
            CASE
                WHEN UPPER(pcs.format) IN ('T20', 'T20I')
                THEN pcs.batting_average
            END
        ),
        2
    ) AS t20_batting_average,

    SUM(COALESCE(pcs.matches, 0)) AS total_matches

FROM player_career_stats pcs
JOIN players p
    ON pcs.player_id = p.player_id

GROUP BY
    p.player_id,
    p.full_name

HAVING SUM(COALESCE(pcs.matches, 0)) >= 20

ORDER BY total_matches DESC;
"""


# ============================================================
# Q21 - COMPREHENSIVE PLAYER PERFORMANCE RANKING
# ============================================================

query_21 = """
WITH player_scores AS
(
    SELECT
        p.player_id,
        p.full_name,
        pcs.format,

        (
            COALESCE(pcs.runs, 0) * 0.01
            +
            COALESCE(pcs.batting_average, 0) * 0.5
            +
            COALESCE(pcs.strike_rate, 0) * 0.3
        ) AS batting_points,

        (
            COALESCE(pcs.wickets, 0) * 2
            +
            (
                50 -
                COALESCE(pcs.bowling_average, 50)
            ) * 0.5
            +
            (
                6 -
                COALESCE(pcs.economy_rate, 6)
            ) * 2
        ) AS bowling_points,

        (
            COALESCE(pcs.catches, 0) * 3
            +
            COALESCE(pcs.stumpings, 0) * 5
        ) AS fielding_points

    FROM player_career_stats pcs
    JOIN players p
        ON pcs.player_id = p.player_id
),

ranked_players AS
(
    SELECT
        full_name,
        format,
        batting_points,
        bowling_points,
        fielding_points,

        (
            batting_points +
            bowling_points +
            fielding_points
        ) AS total_score

    FROM player_scores
)

SELECT
    full_name,
    format,

    ROUND(
        batting_points,
        2
    ) AS batting_points,

    ROUND(
        bowling_points,
        2
    ) AS bowling_points,

    ROUND(
        fielding_points,
        2
    ) AS fielding_points,

    ROUND(
        total_score,
        2
    ) AS total_score,

    RANK() OVER
    (
        PARTITION BY format
        ORDER BY total_score DESC
    ) AS player_rank

FROM ranked_players

ORDER BY
    format,
    player_rank;
"""


# ============================================================
# Q22 - HEAD-TO-HEAD TEAM ANALYSIS
# ============================================================

query_22 = """
WITH recent_matches AS
(
    SELECT
        CASE
            WHEN team1_id < team2_id
            THEN team1_id
            ELSE team2_id
        END AS team_a_id,

        CASE
            WHEN team1_id < team2_id
            THEN team2_id
            ELSE team1_id
        END AS team_b_id,

        winning_team_id,
        victory_margin,
        victory_type,
        venue_id,
        toss_winner_id,
        toss_decision

    FROM matches

    WHERE
        DATE(match_date) >= DATE('now', '-3 years')
        AND winning_team_id IS NOT NULL
)

SELECT
    ta.team_name AS team_a,
    tb.team_name AS team_b,

    COUNT(*) AS total_matches,

    SUM(
        CASE
            WHEN rm.winning_team_id = rm.team_a_id
            THEN 1
            ELSE 0
        END
    ) AS team_a_wins,

    SUM(
        CASE
            WHEN rm.winning_team_id = rm.team_b_id
            THEN 1
            ELSE 0
        END
    ) AS team_b_wins,

    ROUND(
        AVG(
            CASE
                WHEN rm.winning_team_id = rm.team_a_id
                THEN rm.victory_margin
            END
        ),
        2
    ) AS team_a_average_victory_margin,

    ROUND(
        AVG(
            CASE
                WHEN rm.winning_team_id = rm.team_b_id
                THEN rm.victory_margin
            END
        ),
        2
    ) AS team_b_average_victory_margin,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN rm.winning_team_id = rm.team_a_id
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS team_a_win_percentage,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN rm.winning_team_id = rm.team_b_id
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS team_b_win_percentage

FROM recent_matches rm

JOIN teams ta
    ON rm.team_a_id = ta.team_id

JOIN teams tb
    ON rm.team_b_id = tb.team_id

GROUP BY
    rm.team_a_id,
    rm.team_b_id,
    ta.team_name,
    tb.team_name

HAVING COUNT(*) >= 5

ORDER BY total_matches DESC;
"""


# ============================================================
# Q23 - RECENT PLAYER FORM AND MOMENTUM
# ============================================================

query_23 = """
WITH ranked_innings AS (

    SELECT
        bs.player_id,
        bs.match_id,
        bs.runs,
        bs.strike_rate,
        m.match_date,

        ROW_NUMBER() OVER (
            PARTITION BY bs.player_id
            ORDER BY
                m.match_date DESC,
                bs.match_id DESC
        ) AS performance_number

    FROM batting_stats bs

    JOIN matches m
        ON bs.match_id = m.match_id
),

last_ten AS (

    SELECT *
    FROM ranked_innings
    WHERE performance_number <= 10
),

form_summary AS (

    SELECT
        player_id,

        COUNT(*) AS recent_performances,

        AVG(
            CASE
                WHEN performance_number <= 5
                THEN runs
            END
        ) AS average_last_5,

        AVG(runs) AS average_last_10,

        AVG(strike_rate) AS recent_strike_rate,

        SUM(
            CASE
                WHEN runs >= 50
                THEN 1
                ELSE 0
            END
        ) AS scores_50_plus,

        AVG(runs) AS mean_runs,

        AVG(runs * runs) AS average_squared_runs

    FROM last_ten

    GROUP BY player_id
)

SELECT
    p.full_name,

    ROUND(
        fs.average_last_5,
        2
    ) AS average_runs_last_5,

    ROUND(
        fs.average_last_10,
        2
    ) AS average_runs_last_10,

    ROUND(
        fs.recent_strike_rate,
        2
    ) AS recent_strike_rate,

    fs.scores_50_plus,

    ROUND(
        (
            fs.average_squared_runs -
            (fs.mean_runs * fs.mean_runs)
        ),
        2
    ) AS consistency_variance,

    CASE

        WHEN
            fs.average_last_5 >= 50
            AND fs.recent_strike_rate >= 100
        THEN 'Excellent Form'

        WHEN fs.average_last_5 >= 35
        THEN 'Good Form'

        WHEN fs.average_last_5 >= 20
        THEN 'Average Form'

        ELSE 'Poor Form'

    END AS form_category

FROM form_summary fs

JOIN players p
    ON fs.player_id = p.player_id

WHERE fs.recent_performances >= 5

ORDER BY
    average_runs_last_5 DESC,
    recent_strike_rate DESC;
"""

# ============================================================
# Q24 - SUCCESSFUL BATTING PARTNERSHIPS
# ============================================================

query_24 = """
WITH partnerships AS
(
    SELECT
        CASE
            WHEN b1.player_id < b2.player_id
            THEN b1.player_id
            ELSE b2.player_id
        END AS player_1_id,

        CASE
            WHEN b1.player_id < b2.player_id
            THEN b2.player_id
            ELSE b1.player_id
        END AS player_2_id,

        b1.match_id,
        b1.innings,

        (
            b1.runs +
            b2.runs
        ) AS partnership_runs

    FROM batting_stats b1

    JOIN batting_stats b2
        ON b1.match_id = b2.match_id
        AND b1.innings = b2.innings
        AND b2.batting_position =
            b1.batting_position + 1
)

SELECT
    p1.full_name AS player_1,
    p2.full_name AS player_2,

    COUNT(*) AS total_partnerships,

    ROUND(
        AVG(ps.partnership_runs),
        2
    ) AS average_partnership_runs,

    SUM(
        CASE
            WHEN ps.partnership_runs > 50
            THEN 1
            ELSE 0
        END
    ) AS partnerships_above_50,

    MAX(
        ps.partnership_runs
    ) AS highest_partnership,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN ps.partnership_runs > 50
                THEN 1
                ELSE 0
            END
        ) /
        NULLIF(COUNT(*), 0),
        2
    ) AS success_rate_percentage

FROM partnerships ps

JOIN players p1
    ON ps.player_1_id = p1.player_id

JOIN players p2
    ON ps.player_2_id = p2.player_id

GROUP BY
    ps.player_1_id,
    ps.player_2_id,
    p1.full_name,
    p2.full_name

HAVING COUNT(*) >= 5

ORDER BY
    success_rate_percentage DESC,
    average_partnership_runs DESC;
"""


# ============================================================
# Q25 - QUARTERLY PLAYER PERFORMANCE EVOLUTION
# ============================================================

query_25 = """
WITH quarterly_performance AS
(
    SELECT
        bs.player_id,

        CAST(
            strftime('%Y', m.match_date)
            AS INTEGER
        ) AS year,

        CASE
            WHEN CAST(
                strftime('%m', m.match_date)
                AS INTEGER
            ) BETWEEN 1 AND 3
            THEN 1

            WHEN CAST(
                strftime('%m', m.match_date)
                AS INTEGER
            ) BETWEEN 4 AND 6
            THEN 2

            WHEN CAST(
                strftime('%m', m.match_date)
                AS INTEGER
            ) BETWEEN 7 AND 9
            THEN 3

            ELSE 4
        END AS quarter,

        ROUND(
            AVG(bs.runs),
            2
        ) AS average_runs,

        ROUND(
            AVG(bs.strike_rate),
            2
        ) AS average_strike_rate,

        COUNT(DISTINCT bs.match_id) AS matches_played

    FROM batting_stats bs

    JOIN matches m
        ON bs.match_id = m.match_id

    GROUP BY
        bs.player_id,
        year,
        quarter

    HAVING COUNT(DISTINCT bs.match_id) >= 3
),

eligible_players AS
(
    SELECT
        player_id
    FROM quarterly_performance
    GROUP BY player_id
    HAVING COUNT(*) >= 6
),

quarterly_comparison AS
(
    SELECT
        qp.*,

        LAG(qp.average_runs) OVER
        (
            PARTITION BY qp.player_id
            ORDER BY qp.year, qp.quarter
        ) AS previous_quarter_runs,

        LAG(qp.average_strike_rate) OVER
        (
            PARTITION BY qp.player_id
            ORDER BY qp.year, qp.quarter
        ) AS previous_quarter_strike_rate,

        FIRST_VALUE(qp.average_runs) OVER
        (
            PARTITION BY qp.player_id
            ORDER BY qp.year, qp.quarter
        ) AS first_quarter_runs,

        FIRST_VALUE(qp.average_runs) OVER
        (
            PARTITION BY qp.player_id
            ORDER BY qp.year DESC, qp.quarter DESC
        ) AS latest_quarter_runs

    FROM quarterly_performance qp

    JOIN eligible_players ep
        ON qp.player_id = ep.player_id
)

SELECT
    p.full_name,
    qc.year,
    qc.quarter,
    qc.matches_played,
    qc.average_runs,
    qc.average_strike_rate,

    ROUND(
        qc.previous_quarter_runs,
        2
    ) AS previous_quarter_runs,

    ROUND(
        qc.average_runs -
        qc.previous_quarter_runs,
        2
    ) AS runs_change,

    ROUND(
        qc.average_strike_rate -
        qc.previous_quarter_strike_rate,
        2
    ) AS strike_rate_change,

    CASE
        WHEN qc.previous_quarter_runs IS NULL
        THEN 'Starting Quarter'

        WHEN qc.average_runs >
             qc.previous_quarter_runs * 1.05
        THEN 'Improving'

        WHEN qc.average_runs <
             qc.previous_quarter_runs * 0.95
        THEN 'Declining'

        ELSE 'Stable'
    END AS quarterly_trend,

    CASE
        WHEN qc.latest_quarter_runs >
             qc.first_quarter_runs * 1.10
        THEN 'Career Ascending'

        WHEN qc.latest_quarter_runs <
             qc.first_quarter_runs * 0.90
        THEN 'Career Declining'

        ELSE 'Career Stable'
    END AS career_phase

FROM quarterly_comparison qc

JOIN players p
    ON qc.player_id = p.player_id

ORDER BY
    p.full_name,
    qc.year,
    qc.quarter;
"""