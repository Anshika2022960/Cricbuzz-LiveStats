import streamlit as st

from utils.api_handler import get_live_matches
from utils.theme import apply_dashboard_theme, hero,sidebar_brand,footer,live_matches_sidebar


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Live Cricket Matches",
    page_icon="🏏",
    layout="wide"
)


# ============================================================
# APPLY CUSTOM THEME
# ============================================================

apply_dashboard_theme()
live_matches_sidebar()


# ============================================================
# SIDEBAR BRANDING
# ============================================================


sidebar_brand()


# ============================================================
# HERO SECTION
# ============================================================

hero(
    "Live Cricket Matches",
    "Follow ongoing cricket matches, scores, venues and real-time match status",
    "📡"
)


# ============================================================
# REFRESH BUTTON
# ============================================================

top_left, top_right = st.columns([1, 4])


with top_left:

    if st.button(
        "🔄 Refresh Live Matches",
        use_container_width=True
    ):
        st.retun()




# ============================================================
# LOAD API DATA
# ============================================================

with st.spinner("Fetching live cricket matches..."):

    data = get_live_matches()


# ============================================================
# HANDLE EMPTY RESPONSE
# ============================================================

if not data:

    st.warning(
        "Live cricket data is currently unavailable. "
        "Please check the API connection or try again later."
    )

    footer()

    st.stop()


# ============================================================
# COUNT LIVE MATCHES
# ============================================================

live_match_count = 0


for match_type in data.get("typeMatches", []):

    for series in match_type.get(
        "seriesMatches",
        []
    ):

        wrapper = series.get(
            "seriesAdWrapper",
            {}
        )

        live_match_count += len(
            wrapper.get(
                "matches",
                []
            )
        )


# ============================================================
# TOP KPI CARDS
# ============================================================

kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "📡 Live Matches",
        live_match_count
    )


with kpi2:

    match_types = len(
        data.get(
            "typeMatches",
            []
        )
    )

    st.metric(
        "🏆 Match Categories",
        match_types
    )


with kpi3:

    st.metric(
        "🌐 Data Source",
        "Cricbuzz API"
    )




# ============================================================
# PAGE INTRODUCTION
# ============================================================

st.markdown(
    """
    
            View ongoing cricket matches with team scores,
            wickets, overs, match status, venue and series details.
            Use the refresh button to retrieve the latest available
            match information.
        

    """
    
)


# ============================================================
# DISPLAY LIVE MATCHES
# ============================================================

matches_found = False


for match_type in data.get(
    "typeMatches",
    []
):

    category = match_type.get(
        "matchType",
        "Other Matches"
    )


    

    for series in match_type.get(
        "seriesMatches",
        []
    ):

        wrapper = series.get(
            "seriesAdWrapper",
            {}
        )


        # Some API responses may contain advertisements
        # instead of a series wrapper.
        if not wrapper:

            continue


        series_name = wrapper.get(
            "seriesName",
            "Unknown Series"
        )


        matches = wrapper.get(
            "matches",
            []
        )


        if not matches:

            continue


        


        for match in matches:

            info = match.get(
                "matchInfo",
                {}
            )

            score = match.get(
                "matchScore",
                {}
            )


            team1_info = info.get(
                "team1",
                {}
            )

            team2_info = info.get(
                "team2",
                {}
            )


            team1 = team1_info.get(
                "teamName",
                "Team 1"
            )

            team2 = team2_info.get(
                "teamName",
                "Team 2"
            )


            status = info.get(
                "status",
                "Status unavailable"
            )


            venue_info = info.get(
                "venueInfo",
                {}
            )


            venue = venue_info.get(
                "ground",
                "Venue unavailable"
            )


            city = venue_info.get(
                "city",
                ""
            )


            match_desc = info.get(
                "matchDesc",
                ""
            )


            matches_found = True


            # =================================================
            # MATCH CARD
            # =================================================

            with st.container(border=True):



                if match_desc:

                    st.caption(
                        f"📌 {match_desc}"
                    )


                # ---------------------------------------------
                # VENUE AND STATUS
                # ---------------------------------------------

                info_col1, info_col2 = st.columns(2)


                


                # =================================================
                # SCORE SECTION
                # =================================================

                team1_score = score.get(
                    "team1Score",
                    {}
                )

                team2_score = score.get(
                    "team2Score",
                    {}
                )


                score_col1, score_col2 = st.columns(2)


                # =================================================
                # TEAM 1 SCORE
                # =================================================

                with score_col1:

                    innings1 = team1_score.get(
                        "inngs1",
                        {}
                    )


                    if innings1:

                        runs1 = innings1.get(
                            "runs",
                            "-"
                        )

                        wickets1 = innings1.get(
                            "wickets",
                            "-"
                        )

                        overs1 = innings1.get(
                            "overs",
                            "-"
                        )


                        


                # =================================================
                # TEAM 2 SCORE
                # =================================================

                with score_col2:

                    innings2 = team2_score.get(
                        "inngs1",
                        {}
                    )


                    if innings2:

                        runs2 = innings2.get(
                            "runs",
                            "-"
                        )

                        wickets2 = innings2.get(
                            "wickets",
                            "-"
                        )

                        overs2 = innings2.get(
                            "overs",
                            "-"
                        )


                        

                # =================================================
                # SECOND INNINGS IF AVAILABLE
                # =================================================

                team1_innings2 = team1_score.get(
                    "inngs2",
                    {}
                )

                team2_innings2 = team2_score.get(
                    "inngs2",
                    {}
                )


                if team1_innings2 or team2_innings2:

                    st.markdown(
                        "#### 🧾 Additional Innings"
                    )


                    extra1, extra2 = st.columns(2)


                    with extra1:

                        if team1_innings2:

                            runs = team1_innings2.get(
                                "runs",
                                "-"
                            )

                            wickets = team1_innings2.get(
                                "wickets",
                                "-"
                            )

                            overs = team1_innings2.get(
                                "overs",
                                "-"
                            )


                            st.info(
                                f"{team1}: "
                                f"{runs}/{wickets} "
                                f"({overs} overs)"
                            )


                    with extra2:

                        if team2_innings2:

                            runs = team2_innings2.get(
                                "runs",
                                "-"
                            )

                            wickets = team2_innings2.get(
                                "wickets",
                                "-"
                            )

                            overs = team2_innings2.get(
                                "overs",
                                "-"
                            )


                            st.info(
                                f"{team2}: "
                                f"{runs}/{wickets} "
                                f"({overs} overs)"
                            )


                # =================================================
                # RAW API DETAILS
                # =================================================

                with st.expander(
                    "🔎 View Raw Match API Data"
                ):

                    st.json(
                        match
                    )


                st.markdown(
                    "<br>",
                    unsafe_allow_html=True
                )


# ============================================================
# NO LIVE MATCHES
# ============================================================

if not matches_found:

    st.info(
        "🏏 No live cricket matches are available at the moment."
    )


# ============================================================
# FOOTER
# ============================================================

footer()


hero(
    "Live Cricket Matches",
    "Follow ongoing cricket matches, scores, venues and real-time match status",
    "📡"
)