import streamlit as st


# ============================================================
# APPLY DASHBOARD THEME
# ============================================================

def apply_dashboard_theme():
    """
    Pure Streamlit theme helper.

    No HTML
    No CSS
    No unsafe_allow_html

    Visual appearance will follow the Streamlit theme
    configured in .streamlit/config.toml.
    """
    pass


# ============================================================
# OLD FUNCTION NAME
# Kept so existing pages do not produce ImportError
# ============================================================

def apply_theme():
    """
    Compatibility function for pages that still call
    apply_theme().
    """
    apply_dashboard_theme()


# ============================================================
# HERO SECTION
# Pure Streamlit version
# ============================================================

def hero(
    title,
    subtitle,
    icon="🏏"
):
    """
    Display a page heading using native Streamlit components.
    """

    st.title(
        f"{icon} {title}"
    )

    st.write(
        subtitle
    )

    st.caption(
        "Live Cricket • SQL Analytics • Interactive Insights"
    )

    st.divider()


# ============================================================
# SIDEBAR BRAND
# Pure Streamlit version
# ============================================================

def sidebar_brand():
    """
    Display Cricbuzz LiveStats branding in the sidebar.
    """

    with st.sidebar:

        st.divider()

        st.subheader(
            "🏏 Cricbuzz"
        )

        st.write(
            "**LiveStats**"
        )

        st.caption(
            "Live Cricket. Deeper Insights."
        )


# ============================================================
# SQL SIDEBAR
# ============================================================

def sql_sidebar():
    """
    Sidebar information for SQL Analytics page.
    """

    with st.sidebar:

        st.subheader(
            "📊 SQL Query Levels"
        )

        st.write(
            "🟢 Beginner: Q1–Q8"
        )

        st.write(
            "🟠 Intermediate: Q9–Q16"
        )

        st.write(
            "🔵 Advanced: Q17–Q25"
        )

        st.divider()

        st.caption(
            "25 SQL analytical questions"
        )


# ============================================================
# CRUD SIDEBAR
# ============================================================

def crud_sidebar():
    """
    Sidebar information for CRUD Operations page.
    """

    with st.sidebar:

        st.subheader(
            "🛠️ CRUD Operations"
        )

        st.write(
            "➕ Create Player"
        )

        st.write(
            "👥 Read Players"
        )

        st.write(
            "✏️ Update Player"
        )

        st.write(
            "🗑️ Delete Player"
        )

        st.divider()

        st.caption(
            "Manage records in the SQLite players table."
        )


# ============================================================
# TOP PLAYER SIDEBAR
# ============================================================

def player_stats_sidebar():
    """
    Sidebar information for Top Player Statistics.
    """

    with st.sidebar:

        st.subheader(
            "📊 Player Statistics"
        )

        st.write(
            "🏏 ODI Run Scorers"
        )

        st.write(
            "🎯 Wicket Takers"
        )

        st.write(
            "📈 Batting Average"
        )

        st.write(
            "🏆 Highest Scores"
        )

        st.divider()

        st.caption(
            "Player performance analytics"
        )


# ============================================================
# LIVE MATCHES SIDEBAR
# ============================================================

def live_matches_sidebar():
    """
    Sidebar information for Live Matches.
    """

    with st.sidebar:

        st.subheader(
            "📡 Live Matches"
        )

        st.write(
            "🏏 Live Scores"
        )

        st.write(
            "📍 Match Venues"
        )

        st.write(
            "📊 Match Status"
        )

        st.write(
            "🔄 Live API Data"
        )

        st.divider()

        st.caption(
            "Real-time cricket information"
        )


# ============================================================
# PAGE INTRODUCTION
# ============================================================

def page_intro(
    message
):
    """
    Standard information box used below page titles.
    """

    st.info(
        message
    )


# ============================================================
# SECTION HEADING
# ============================================================

def section_heading(
    title,
    icon=""
):
    """
    Standard section title.
    """

    if icon:

        st.subheader(
            f"{icon} {title}"
        )

    else:

        st.subheader(
            title
        )


# ============================================================
# FOOTER
# ============================================================

def footer():
    """
    Standard dashboard footer.
    """

    st.divider()

    st.caption(
        "🏆 Cricbuzz LiveStats | "
        "Real-Time Cricket Insights & SQL-Based Analytics"
    )