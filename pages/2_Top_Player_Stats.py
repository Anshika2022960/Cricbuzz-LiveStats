import streamlit as st
import pandas as pd

from utils.db_connection import get_connection
from utils.theme import apply_dashboard_theme, sidebar_brand, footer,player_stats_sidebar


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Top Player Statistics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# APPLY THEME
# ============================================================

apply_dashboard_theme()
sidebar_brand()
player_stats_sidebar()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📊 Top Player Statistics")

st.write(
    "Explore leading batting and bowling performances "
    "across different cricket formats."
)

st.info(
    "Player statistics are retrieved from the SQLite cricket "
    "database. Select an analysis below to explore rankings "
    "and performance indicators."
)


# ============================================================
# SELECT ANALYSIS
# ============================================================

st.subheader("🔎 Select Player Analysis")

option = st.selectbox(
    "Choose an analysis",
    [
        "Top ODI Run Scorers",
        "Top Wicket Takers",
        "Best Batting Average",
        "Highest Individual Scores"
    ]
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = get_connection()


# ============================================================
# QUERY 1 - TOP ODI RUN SCORERS
# ============================================================

if option == "Top ODI Run Scorers":

    query = """
    SELECT
        p.full_name AS Player,
        pcs.runs AS Runs,
        pcs.batting_average AS Average,
        pcs.centuries AS Centuries,
        pcs.strike_rate AS Strike_Rate
    FROM player_career_stats pcs
    JOIN players p
        ON pcs.player_id = p.player_id
    WHERE pcs.format = 'ODI'
    ORDER BY pcs.runs DESC
    LIMIT 10;
    """

    section_title = "🏆 Top ODI Run Scorers"


# ============================================================
# QUERY 2 - TOP WICKET TAKERS
# ============================================================

elif option == "Top Wicket Takers":

    query = """
    SELECT
        p.full_name AS Player,
        pcs.format AS Format,
        pcs.wickets AS Wickets,
        pcs.bowling_average AS Bowling_Average,
        pcs.economy_rate AS Economy_Rate
    FROM player_career_stats pcs
    JOIN players p
        ON pcs.player_id = p.player_id
    WHERE pcs.wickets IS NOT NULL
    ORDER BY pcs.wickets DESC
    LIMIT 10;
    """

    section_title = "🎯 Top Wicket Takers"


# ============================================================
# QUERY 3 - BEST BATTING AVERAGE
# ============================================================

elif option == "Best Batting Average":

    query = """
    SELECT
        p.full_name AS Player,
        pcs.format AS Format,
        pcs.runs AS Runs,
        pcs.batting_average AS Batting_Average,
        pcs.matches AS Matches
    FROM player_career_stats pcs
    JOIN players p
        ON pcs.player_id = p.player_id
    WHERE pcs.batting_average IS NOT NULL
    ORDER BY pcs.batting_average DESC
    LIMIT 10;
    """

    section_title = "📈 Best Batting Average"


# ============================================================
# QUERY 4 - HIGHEST INDIVIDUAL SCORES
# ============================================================

else:

    query = """
    SELECT
        p.full_name AS Player,
        pcs.format AS Format,
        pcs.highest_score AS Highest_Score,
        pcs.runs AS Career_Runs,
        pcs.centuries AS Centuries
    FROM player_career_stats pcs
    JOIN players p
        ON pcs.player_id = p.player_id
    WHERE pcs.highest_score IS NOT NULL
    ORDER BY pcs.highest_score DESC
    LIMIT 10;
    """

    section_title = "🔥 Highest Individual Scores"


# ============================================================
# EXECUTE QUERY
# ============================================================

try:

    df = pd.read_sql_query(
        query,
        conn
    )

except Exception as error:

    st.error(
        f"Database error: {error}"
    )

    conn.close()

    footer()

    st.stop()

finally:

    try:
        conn.close()
    except Exception:
        pass


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if df.empty:

    st.warning(
        "No player statistics are available for this analysis."
    )

    footer()

    st.stop()


# ============================================================
# SECTION TITLE
# ============================================================

st.subheader(section_title)


# ============================================================
# KPI SECTION
# ============================================================

if option == "Top ODI Run Scorers":

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "👥 Players",
            len(df)
        )

    with k2:
        st.metric(
            "🏏 Highest Runs",
            f"{int(df['Runs'].max()):,}"
        )

    with k3:
        st.metric(
            "📈 Best Average",
            f"{df['Average'].max():.2f}"
        )

    with k4:
        st.metric(
            "💯 Most Centuries",
            int(df["Centuries"].max())
        )


elif option == "Top Wicket Takers":

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "👥 Players",
            len(df)
        )

    with k2:
        st.metric(
            "🎯 Highest Wickets",
            int(df["Wickets"].max())
        )

    with k3:

        valid_avg = df["Bowling_Average"].dropna()

        if not valid_avg.empty:
            st.metric(
                "📊 Best Bowling Avg",
                f"{valid_avg.min():.2f}"
            )
        else:
            st.metric(
                "📊 Best Bowling Avg",
                "N/A"
            )

    with k4:

        valid_economy = df["Economy_Rate"].dropna()

        if not valid_economy.empty:
            st.metric(
                "⚡ Best Economy",
                f"{valid_economy.min():.2f}"
            )
        else:
            st.metric(
                "⚡ Best Economy",
                "N/A"
            )


elif option == "Best Batting Average":

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "👥 Players",
            len(df)
        )

    with k2:
        st.metric(
            "📈 Best Average",
            f"{df['Batting_Average'].max():.2f}"
        )

    with k3:
        st.metric(
            "🏏 Highest Runs",
            f"{int(df['Runs'].max()):,}"
        )


else:

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "👥 Players",
            len(df)
        )

    with k2:
        st.metric(
            "🔥 Highest Score",
            int(df["Highest_Score"].max())
        )

    with k3:
        st.metric(
            "💯 Most Centuries",
            int(df["Centuries"].max())
        )


st.divider()


# ============================================================
# TOP PLAYER HIGHLIGHT
# ============================================================

st.subheader("⭐ Top Performer")

top_player = df.iloc[0]


if option == "Top ODI Run Scorers":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏏 Player",
            top_player["Player"]
        )

    with col2:
        st.metric(
            "Runs",
            f"{int(top_player['Runs']):,}"
        )

    with col3:
        st.metric(
            "Average",
            f"{top_player['Average']:.2f}"
        )


elif option == "Top Wicket Takers":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏏 Player",
            top_player["Player"]
        )

    with col2:
        st.metric(
            "Wickets",
            int(top_player["Wickets"])
        )

    with col3:

        if pd.notna(top_player["Economy_Rate"]):
            economy = f"{top_player['Economy_Rate']:.2f}"
        else:
            economy = "N/A"

        st.metric(
            "Economy",
            economy
        )


elif option == "Best Batting Average":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏏 Player",
            top_player["Player"]
        )

    with col2:
        st.metric(
            "Batting Average",
            f"{top_player['Batting_Average']:.2f}"
        )

    with col3:
        st.metric(
            "Career Runs",
            f"{int(top_player['Runs']):,}"
        )


else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏏 Player",
            top_player["Player"]
        )

    with col2:
        st.metric(
            "Highest Score",
            int(top_player["Highest_Score"])
        )

    with col3:
        st.metric(
            "Career Runs",
            f"{int(top_player['Career_Runs']):,}"
        )


# ============================================================
# PLAYER RANKING TABLE
# ============================================================

st.divider()

st.subheader("📋 Player Ranking")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# VISUAL ANALYSIS
# ============================================================

st.divider()

st.subheader("📊 Visual Analysis")


if option == "Top ODI Run Scorers":

    chart_df = (
        df[
            [
                "Player",
                "Runs"
            ]
        ]
        .set_index("Player")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )


elif option == "Top Wicket Takers":

    chart_df = (
        df[
            [
                "Player",
                "Wickets"
            ]
        ]
        .set_index("Player")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )


elif option == "Best Batting Average":

    chart_df = (
        df[
            [
                "Player",
                "Batting_Average"
            ]
        ]
        .set_index("Player")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )


else:

    chart_df = (
        df[
            [
                "Player",
                "Highest_Score"
            ]
        ]
        .set_index("Player")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )


# ============================================================
# AUTOMATIC INSIGHT
# ============================================================

st.divider()

st.subheader("💡 Performance Insight")


if option == "Top ODI Run Scorers":

    st.success(
        f"{top_player['Player']} leads the ODI run-scorer "
        f"ranking with {int(top_player['Runs']):,} runs, "
        f"a batting average of {top_player['Average']:.2f}, "
        f"and {int(top_player['Centuries'])} centuries."
    )


elif option == "Top Wicket Takers":

    st.success(
        f"{top_player['Player']} is the leading wicket taker "
        f"in the available database with "
        f"{int(top_player['Wickets'])} wickets."
    )


elif option == "Best Batting Average":

    st.success(
        f"{top_player['Player']} has the highest batting "
        f"average in the available records at "
        f"{top_player['Batting_Average']:.2f}."
    )


else:

    st.success(
        f"{top_player['Player']} has the highest individual "
        f"score in the available records with "
        f"{int(top_player['Highest_Score'])} runs."
    )


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander(
    "ℹ️ About This Analysis"
):

    st.write(
        "Player statistics displayed on this page are retrieved "
        "from the SQLite cricket database."
    )

    st.write(
        "The analysis uses SQL JOIN operations between the "
        "`players` and `player_career_stats` tables."
    )

    st.write(
        "Rankings are generated dynamically according to the "
        "performance category selected above."
    )


# ============================================================
# FOOTER
# ============================================================

footer()