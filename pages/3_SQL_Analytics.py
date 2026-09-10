import streamlit as st
import pandas as pd

from utils.db_connection import get_connection
from utils.theme import (
    apply_dashboard_theme,
    sidebar_brand,
    sql_sidebar,
    footer
)

from sql.analytics_queries import (
    query_1,
    query_2,
    query_3,
    query_4,
    query_5,
    query_6,
    query_7,
    query_8,
    query_9,
    query_10,
    query_11,
    query_12,
    query_13,
    query_14,
    query_15,
    query_16,
    query_17,
    query_18,
    query_19,
    query_20,
    query_21,
    query_22,
    query_23,
    query_24,
    query_25
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SQL Cricket Analytics",
    page_icon="🔍",
    layout="wide"
)
apply_dashboard_theme()
sidebar_brand()
sql_sidebar()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏏 Cricbuzz")
    st.subheader("LiveStats")

    st.caption(
        "Live Cricket. Deeper Insights."
    )

    st.divider()

    st.subheader("📊 SQL Query Levels")

    st.write("🟢 Beginner: Q1–Q8")
    st.write("🟠 Intermediate: Q9–Q16")
    st.write("🔵 Advanced: Q17–Q25")

    st.divider()

    st.caption(
        "25 SQL analytical questions"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔍 SQL Cricket Analytics")

st.write(
    "Explore cricket data using 25 structured SQL analytical "
    "questions ranging from beginner to advanced level."
)

st.info(
    "Select an SQL question below. The selected query will be "
    "executed on the SQLite cricket database and the result "
    "will be displayed automatically."
)


# ============================================================
# QUERY DICTIONARY
# ============================================================

questions = {

    "Q1 - Indian Players":
        query_1,

    "Q2 - Matches Played in Last 30 Days":
        query_2,

    "Q3 - Top 10 ODI Run Scorers":
        query_3,

    "Q4 - Venues with Capacity Above 50,000":
        query_4,

    "Q5 - Total Matches Won by Each Team":
        query_5,

    "Q6 - Number of Players by Playing Role":
        query_6,

    "Q7 - Highest Batting Score by Format":
        query_7,

    "Q8 - Cricket Series Started in 2024":
        query_8,

    "Q9 - High-Performing All-Rounders":
        query_9,

    "Q10 - Last 20 Completed Matches":
        query_10,

    "Q11 - Player Performance Across Formats":
        query_11,

    "Q12 - Home vs Away Team Performance":
        query_12,

    "Q13 - Consecutive Batsmen Partnerships":
        query_13,

    "Q14 - Bowling Performance by Venue":
        query_14,

    "Q15 - Players in Close Matches":
        query_15,

    "Q16 - Yearly Batting Performance":
        query_16,

    "Q17 - Toss Advantage Analysis":
        query_17,

    "Q18 - Most Economical Limited-Overs Bowlers":
        query_18,

    "Q19 - Most Consistent Batsmen":
        query_19,

    "Q20 - Format-Wise Matches and Batting Average":
        query_20,

    "Q21 - Comprehensive Player Ranking":
        query_21,

    "Q22 - Team Head-to-Head Analysis":
        query_22,

    "Q23 - Recent Player Form and Momentum":
        query_23,

    "Q24 - Best Batting Partnerships":
        query_24,

    "Q25 - Player Performance Time-Series":
        query_25
}


# ============================================================
# QUESTION DESCRIPTIONS
# ============================================================

question_descriptions = {

    "Q1 - Indian Players":
        "Find all players representing India and display their "
        "playing role, batting style and bowling style.",

    "Q2 - Matches Played in Last 30 Days":
        "Display cricket matches played during the last 30 days "
        "with team names, venue and match date.",

    "Q3 - Top 10 ODI Run Scorers":
        "Identify the top 10 ODI run scorers using career runs, "
        "batting average and centuries.",

    "Q4 - Venues with Capacity Above 50,000":
        "Find cricket venues having a seating capacity greater "
        "than 50,000 spectators.",

    "Q5 - Total Matches Won by Each Team":
        "Calculate the total number of recorded match victories "
        "for every cricket team.",

    "Q6 - Number of Players by Playing Role":
        "Count players according to playing roles such as "
        "batsman, bowler, all-rounder and wicket-keeper.",

    "Q7 - Highest Batting Score by Format":
        "Find the highest individual batting score recorded "
        "for each cricket format.",

    "Q8 - Cricket Series Started in 2024":
        "Display cricket series whose starting date falls "
        "within the year 2024.",

    "Q9 - High-Performing All-Rounders":
        "Find all-rounders who have scored more than 1000 runs "
        "and taken more than 50 wickets.",

    "Q10 - Last 20 Completed Matches":
        "Display the 20 most recent completed matches including "
        "teams, winner, victory margin, victory type and venue.",

    "Q11 - Player Performance Across Formats":
        "Compare player batting performance across Test, ODI "
        "and T20I formats for players who have participated "
        "in at least two formats.",

    "Q12 - Home vs Away Team Performance":
        "Compare each team's wins when playing at home versus "
        "away using the venue country and team country.",

    "Q13 - Consecutive Batsmen Partnerships":
        "Identify consecutive batsmen whose combined runs were "
        "at least 100 in the same innings.",

    "Q14 - Bowling Performance by Venue":
        "Analyze bowling economy, wickets and matches played "
        "at different cricket venues.",

    "Q15 - Players in Close Matches":
        "Analyze batting performance in matches decided by "
        "less than 50 runs or fewer than 5 wickets.",

    "Q16 - Yearly Batting Performance":
        "Track average runs and strike rate for each player "
        "by year for matches played since 2020.",

    "Q17 - Toss Advantage Analysis":
        "Investigate whether winning the toss provides an "
        "advantage in winning the match based on toss decision.",

    "Q18 - Most Economical Limited-Overs Bowlers":
        "Identify economical bowlers in ODI and T20 cricket "
        "with sufficient bowling experience.",

    "Q19 - Most Consistent Batsmen":
        "Measure batting consistency using average runs and "
        "standard deviation for performances since 2022.",

    "Q20 - Format-Wise Matches and Batting Average":
        "Compare Test, ODI and T20 match counts and batting "
        "averages for experienced players.",

    "Q21 - Comprehensive Player Ranking":
        "Rank players using weighted batting, bowling and "
        "fielding performance scores.",

    "Q22 - Team Head-to-Head Analysis":
        "Analyze head-to-head records between teams that have "
        "played at least five matches against each other "
        "during the last three years.",

    "Q23 - Recent Player Form and Momentum":
        "Analyze recent player form using their last five and "
        "last ten batting performances.",

    "Q24 - Best Batting Partnerships":
        "Rank successful consecutive-batsman combinations "
        "using partnership runs, frequency and success rate.",

    "Q25 - Player Performance Time-Series":
        "Track quarterly batting performance and categorize "
        "players' career trajectory as ascending, declining "
        "or stable."
}


# ============================================================
# FUNCTION TO GET QUERY NUMBER
# ============================================================

def get_query_number(question_name):

    number_text = (
        question_name
        .split("-")[0]
        .replace("Q", "")
        .strip()
    )

    return int(number_text)


# ============================================================
# FUNCTION TO GET QUERY LEVEL
# ============================================================

def get_query_level(question_name):

    number = get_query_number(
        question_name
    )

    if number <= 8:
        return "Beginner"

    elif number <= 16:
        return "Intermediate"

    else:
        return "Advanced"


# ============================================================
# QUERY FILTER
# ============================================================

st.divider()

st.subheader("📚 Select SQL Analysis")


level_filter = st.selectbox(
    "Filter by SQL Level",
    [
        "All Questions",
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


# ============================================================
# FILTER QUESTIONS
# ============================================================

if level_filter == "All Questions":

    available_questions = list(
        questions.keys()
    )


elif level_filter == "Beginner":

    available_questions = [
        q
        for q in questions.keys()
        if 1 <= get_query_number(q) <= 8
    ]


elif level_filter == "Intermediate":

    available_questions = [
        q
        for q in questions.keys()
        if 9 <= get_query_number(q) <= 16
    ]


else:

    available_questions = [
        q
        for q in questions.keys()
        if 17 <= get_query_number(q) <= 25
    ]


# ============================================================
# SELECT QUESTION
# ============================================================

selected_question = st.selectbox(
    "Choose SQL Question",
    available_questions
)


query = questions[
    selected_question
]


description = question_descriptions[
    selected_question
]


query_level = get_query_level(
    selected_question
)


query_number = get_query_number(
    selected_question
)


# ============================================================
# SELECTED QUESTION INFORMATION
# ============================================================

st.divider()

st.subheader(
    f"❓ {selected_question}"
)


col1, col2 = st.columns(
    [1, 3]
)


with col1:

    st.metric(
        "Question",
        f"Q{query_number}"
    )


with col2:

    st.metric(
        "SQL Level",
        query_level
    )


st.info(
    description
)


# ============================================================
# DISPLAY SQL QUERY
# ============================================================

with st.expander(
    "💻 View SQL Query"
):

    st.code(
        query,
        language="sql"
    )


# ============================================================
# EXECUTE BUTTON
# ============================================================

run_query = st.button(
    "▶ Run SQL Analysis",
    type="primary",
    use_container_width=True
)


# ============================================================
# EXECUTE ONLY WHEN BUTTON CLICKED
# ============================================================

if run_query:

    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    try:

        conn = get_connection()

    except Exception as error:

        st.error(
            f"Unable to connect to database: {error}"
        )

        st.stop()


    # ========================================================
    # EXECUTE QUERY
    # ========================================================

    try:

        df = pd.read_sql_query(
            query,
            conn
        )

    except Exception as error:

        st.error(
            f"SQL query execution failed: {error}"
        )

        st.warning(
            "Check whether the tables and columns required "
            "by this analytical question exist in your database."
        )

        conn.close()

        st.stop()

    finally:

        try:
            conn.close()
        except Exception:
            pass


    # ========================================================
    # QUERY SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Query Summary"
    )


    metric1, metric2, metric3 = st.columns(3)


    with metric1:

        st.metric(
            "📄 Records Found",
            len(df)
        )


    with metric2:

        st.metric(
            "📊 Columns Returned",
            len(df.columns)
        )


    with metric3:

        if df.empty:

            st.metric(
                "Query Status",
                "No Data"
            )

        else:

            st.metric(
                "Query Status",
                "Success"
            )


    # ========================================================
    # EMPTY RESULT HANDLING
    # ========================================================

    if df.empty:

        st.warning(
            "The SQL query executed successfully, but no "
            "matching records were found in the current database."
        )

        st.info(
            "This is common for some intermediate and advanced "
            "queries because they require a larger amount of "
            "historical match, batting and bowling data."
        )

        st.stop()


    # ========================================================
    # QUERY RESULT TABLE
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Query Result"
    )


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DOWNLOAD QUERY RESULT
    # ========================================================

    csv_data = df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )


    st.download_button(
        label="⬇️ Download Result as CSV",
        data=csv_data,
        file_name=f"query_{query_number}_result.csv",
        mime="text/csv"
    )


    # ========================================================
    # FIND NUMERIC AND TEXT COLUMNS
    # ========================================================

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )


    text_columns = list(
        df.select_dtypes(
            include=[
                "object",
                "string"
            ]
        ).columns
    )


    # ========================================================
    # VISUAL ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Visual Analysis"
    )


    if numeric_columns:

        chart_col1, chart_col2 = st.columns(2)


        with chart_col1:

            chart_type = st.selectbox(
                "Select Chart Type",
                [
                    "Bar Chart",
                    "Line Chart"
                ]
            )


        with chart_col2:

            value_column = st.selectbox(
                "Select Numerical Value",
                numeric_columns
            )


        # ====================================================
        # IF TEXT COLUMN EXISTS
        # ====================================================

        if text_columns:

            category_column = st.selectbox(
                "Select Category",
                text_columns
            )


            chart_data = (
                df[
                    [
                        category_column,
                        value_column
                    ]
                ]
                .dropna()
                .head(20)
            )


            if not chart_data.empty:

                chart_data = (
                    chart_data
                    .set_index(
                        category_column
                    )
                )


                if chart_type == "Bar Chart":

                    st.bar_chart(
                        chart_data,
                        use_container_width=True
                    )


                else:

                    st.line_chart(
                        chart_data,
                        use_container_width=True
                    )


            else:

                st.info(
                    "There is not enough valid data "
                    "to generate the selected chart."
                )


        # ====================================================
        # IF NO TEXT COLUMN EXISTS
        # ====================================================

        else:

            chart_data = (
                df[
                    [
                        value_column
                    ]
                ]
                .dropna()
                .head(20)
            )


            if chart_type == "Bar Chart":

                st.bar_chart(
                    chart_data,
                    use_container_width=True
                )


            else:

                st.line_chart(
                    chart_data,
                    use_container_width=True
                )


    else:

        st.info(
            "This query does not return numerical columns, "
            "so a numerical chart cannot be generated."
        )


    # ========================================================
    # ANALYTICAL SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "💡 Analytical Insight"
    )


    st.success(
        f"Q{query_number} executed successfully and returned "
        f"{len(df)} records with {len(df.columns)} columns."
    )


    # ========================================================
    # NUMERICAL SUMMARY
    # ========================================================

    if numeric_columns:

        summary_column = st.selectbox(
            "Select a metric for statistical summary",
            numeric_columns
        )


        valid_values = pd.to_numeric(
            df[summary_column],
            errors="coerce"
        ).dropna()


        if not valid_values.empty:

            insight1, insight2, insight3 = st.columns(3)


            with insight1:

                st.metric(
                    f"Maximum {summary_column}",
                    round(
                        float(
                            valid_values.max()
                        ),
                        2
                    )
                )


            with insight2:

                st.metric(
                    f"Average {summary_column}",
                    round(
                        float(
                            valid_values.mean()
                        ),
                        2
                    )
                )


            with insight3:

                st.metric(
                    f"Minimum {summary_column}",
                    round(
                        float(
                            valid_values.min()
                        ),
                        2
                    )
                )


# ============================================================
# SQL LEVEL INFORMATION
# ============================================================

st.divider()


with st.expander(
    "📘 About the 25 SQL Questions"
):

    st.subheader(
        "🟢 Beginner Level — Q1 to Q8"
    )

    st.write(
        "These questions mainly demonstrate basic SQL "
        "operations such as SELECT, WHERE, JOIN, GROUP BY, "
        "ORDER BY and aggregate functions."
    )


    st.subheader(
        "🟠 Intermediate Level — Q9 to Q16"
    )

    st.write(
        "These questions use multiple joins, conditional "
        "aggregation, self joins, date analysis and more "
        "detailed player and match-level analytics."
    )


    st.subheader(
        "🔵 Advanced Level — Q17 to Q25"
    )

    st.write(
        "These questions demonstrate advanced SQL concepts "
        "including Common Table Expressions (CTEs), window "
        "functions, ranking, statistical analysis, recent-form "
        "analysis and time-series performance evaluation."
    )


# ============================================================
# IMPORTANT DATABASE NOTE
# ============================================================

with st.expander(
    "ℹ️ Database Note"
):

    st.write(
        "The SQL queries operate on the cricket data stored "
        "in the local SQLite database."
    )

    st.write(
        "Some advanced questions require significantly more "
        "historical match-level data than the current sample "
        "database may contain."
    )

    st.write(
        "Therefore, a query can execute correctly but return "
        "zero rows if the database does not yet satisfy its "
        "minimum data requirements."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏆 Cricbuzz LiveStats | "
    "Real-Time Cricket Insights & SQL-Based Analytics"
)