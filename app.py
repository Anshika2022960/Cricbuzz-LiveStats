import streamlit as st

from utils.theme import (
    apply_dashboard_theme,
    hero,sidebar_brand,live_matches_sidebar,
    footer
)


st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


apply_dashboard_theme()
live_matches_sidebar()
sidebar_brand()

# ============================================================
# HERO
# ============================================================

hero(
    "Cricbuzz LiveStats",
    "Real-Time Cricket Insights & SQL-Based Analytics",
    "🏏"
)


# ============================================================
# KPI ROW
# ============================================================

st.subheader("🚀 Application Modules")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("📡 Live Matches")

        st.write(
            "View real-time cricket scores, match status, "
            "venues and series information."
        )

        st.caption("Source: Cricbuzz API")


with col2:

    with st.container(border=True):

        st.subheader("📊 Player Statistics")

        st.write(
            "Analyze batting, bowling and player "
            "performance across cricket formats."
        )

        st.caption("Source: SQLite Database")


col3, col4 = st.columns(2)

with col3:

    with st.container(border=True):

        st.subheader("🔍 SQL Analytics")

        st.write(
            "Execute 25 structured SQL analytical "
            "questions from beginner to advanced level."
        )

        st.caption("Beginner • Intermediate • Advanced")


with col4:

    with st.container(border=True):

        st.subheader("🛠️ CRUD Operations")

        st.write(
            "Create, read, update and delete "
            "player records."
        )

        st.caption("SQLite Player Management")


# ============================================================
# WELCOME SECTION
# ============================================================

st.markdown(
    """
   

        Cricbuzz LiveStats is an interactive cricket analytics
        platform combining real-time cricket information with
        structured SQL-based analysis.

        Explore live matches, player statistics, team performance,
        historical trends, database operations and analytical
        insights from one application.

       
    """
)


# ============================================================
# TECH STACK
# ============================================================

st.markdown(
    '<div class="section-heading">🧰 Technology Stack</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <span class="tech-badge">🐍 Python</span>
    <span class="tech-badge">📊 Streamlit</span>
    <span class="tech-badge">🗄️ SQLite</span>
    <span class="tech-badge">🌐 REST API</span>
    <span class="tech-badge">📈 Pandas</span>
    <span class="tech-badge">{ } JSON</span>
    """,
    unsafe_allow_html=True
)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# APPLICATION MODULES
# ============================================================

st.markdown(
    '<div class="section-heading">🚀 Application Modules</div>',
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        """
        <div class="custom-card blue-card">

        <h3>📡 Live Matches</h3>

        <p>
        View real-time match status,
        venue information and score updates.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="custom-card green-card">

        <h3>📊 Player Stats</h3>

        <p>
        Explore batting, bowling and
        player performance statistics.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="custom-card purple-card">

        <h3>🔍 SQL Analytics</h3>

        <p>
        Execute analytical SQL queries
        and discover cricket insights.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        """
        <div class="custom-card orange-card">

        <h3>🛠️ CRUD Operations</h3>

        <p>
        Create, view, update and
        delete cricket records.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BUSINESS VALUE
# ============================================================

st.markdown(
    '<div class="section-heading">💡 Analytics Value</div>',
    unsafe_allow_html=True
)


left, middle, right = st.columns(3)


with left:

    st.markdown(
        """
        <div class="custom-card green-card">

        <h3>🎯 Our Mission</h3>

        <p>
        Convert cricket data into meaningful
        and actionable analytical insights.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with middle:

    st.markdown(
        """
        <div class="custom-card blue-card">

        <h3>👥 Who Can Use It?</h3>

        <p>
        Fans, analysts, students,
        developers and sports researchers.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    st.markdown(
        """
        <div class="custom-card purple-card">

        <h3>⭐ Key Features</h3>

        <p>
        Real-time • Interactive •
        SQL-driven • Easy to use
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


footer()


