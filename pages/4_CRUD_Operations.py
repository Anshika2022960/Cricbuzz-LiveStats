import streamlit as st
import pandas as pd
import sqlite3

from utils.db_connection import get_connection
from utils.theme import (
    apply_dashboard_theme,
    crud_sidebar,
    sidebar_brand,
    footer
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CRUD Operations",
    page_icon="🛠️",
    layout="wide"
)


# ============================================================
# APPLY THEME + SIDEBAR
# ============================================================

apply_dashboard_theme()
sidebar_brand()
crud_sidebar()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🛠️ Player Data Management")

st.write(
    "Create, read, update and delete cricket player records "
    "stored in the SQLite database."
)

st.info(
    "Use this page to view existing players, add new players, "
    "modify player information or delete player records."
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_players_dataframe():

    conn = None

    try:

        conn = get_connection()

        df = pd.read_sql_query(
            """
            SELECT
                player_id,
                full_name,
                country,
                playing_role,
                batting_style,
                bowling_style
            FROM players
            ORDER BY full_name
            """,
            conn
        )

        return df

    finally:

        if conn:
            conn.close()


# ============================================================
# OPERATION SELECTOR
# ============================================================

st.divider()

st.subheader("⚙️ Select Database Operation")

operation = st.selectbox(
    "Choose Operation",
    [
        "View Players",
        "Add Player",
        "Update Player",
        "Delete Player"
    ]
)


# ============================================================
# READ OPERATION
# ============================================================

if operation == "View Players":

    st.divider()

    st.subheader("👥 Player Database")

    try:

        df = get_players_dataframe()

        if df.empty:

            st.info(
                "No player records are currently available."
            )

        else:

            # =================================================
            # KPI CARDS
            # =================================================

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "👥 Total Players",
                    len(df)
                )

            with col2:

                country_count = (
                    df["country"]
                    .dropna()
                    .nunique()
                )

                st.metric(
                    "🌍 Countries",
                    country_count
                )

            with col3:

                role_count = (
                    df["playing_role"]
                    .dropna()
                    .nunique()
                )

                st.metric(
                    "🏏 Playing Roles",
                    role_count
                )

            with col4:

                batsmen_count = len(
                    df[
                        df["playing_role"]
                        .fillna("")
                        .str.contains(
                            "Batsman",
                            case=False
                        )
                    ]
                )

                st.metric(
                    "🏏 Batsmen",
                    batsmen_count
                )


            # =================================================
            # PLAYER TABLE
            # =================================================

            st.divider()

            st.subheader("📋 Player Records")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # DOWNLOAD DATA
            # =================================================

            csv_data = df.to_csv(
                index=False
            ).encode(
                "utf-8"
            )

            st.download_button(
                label="⬇️ Download Player Data",
                data=csv_data,
                file_name="players.csv",
                mime="text/csv"
            )


            # =================================================
            # PREPARE ROLE DATA
            # =================================================

            role_df = (
                df["playing_role"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Playing Role")
                .reset_index(name="Players")
            )


            # =================================================
            # PREPARE COUNTRY DATA
            # =================================================

            country_df = (
                df["country"]
                .fillna("Unknown")
                .value_counts()
                .rename_axis("Country")
                .reset_index(name="Players")
            )


            # =================================================
            # SIDE-BY-SIDE ANALYSIS
            # =================================================

            st.divider()

            chart1, chart2 = st.columns(2)


            # -------------------------------------------------
            # PLAYERS BY ROLE
            # -------------------------------------------------

            with chart1:

                st.subheader("📊 Players by Role")

                st.dataframe(
                    role_df,
                    use_container_width=True,
                    hide_index=True
                )

                if not role_df.empty:

                    st.bar_chart(
                        role_df.set_index(
                            "Playing Role"
                        ),
                        use_container_width=True
                    )

                    top_role = role_df.iloc[0]

                    st.success(
                        f"Most common role: "
                        f"{top_role['Playing Role']} "
                        f"({int(top_role['Players'])} player(s))"
                    )


            # -------------------------------------------------
            # PLAYERS BY COUNTRY
            # -------------------------------------------------

            with chart2:

                st.subheader("🌍 Players by Country")

                st.dataframe(
                    country_df,
                    use_container_width=True,
                    hide_index=True
                )

                if not country_df.empty:

                    st.bar_chart(
                        country_df.set_index(
                            "Country"
                        ),
                        use_container_width=True
                    )

                    top_country = country_df.iloc[0]

                    st.info(
                        f"Most represented country: "
                        f"{top_country['Country']} "
                        f"({int(top_country['Players'])} player(s))"
                    )


    except Exception as error:

        st.error(
            f"Database error: {error}"
        )


# ============================================================
# CREATE OPERATION
# ============================================================

elif operation == "Add Player":

    st.divider()

    st.subheader("➕ Add New Player")

    st.info(
        "Enter the player details below. "
        "Player ID must be unique."
    )

    with st.form(
        "add_player_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            player_id = st.number_input(
                "Player ID",
                min_value=1,
                step=1
            )

            full_name = st.text_input(
                "Full Name",
                placeholder="Example: Virat Kohli"
            )

            country = st.text_input(
                "Country",
                placeholder="Example: India"
            )

        with col2:

            playing_role = st.selectbox(
                "Playing Role",
                [
                    "Batsman",
                    "Bowler",
                    "All-rounder",
                    "Wicket-keeper"
                ]
            )

            batting_style = st.text_input(
                "Batting Style",
                placeholder="Example: Right Handed Bat"
            )

            bowling_style = st.text_input(
                "Bowling Style",
                placeholder="Example: Right-arm Fast"
            )

        submit_add = st.form_submit_button(
            "➕ Add Player",
            use_container_width=True
        )


    if submit_add:

        if not full_name.strip():

            st.warning(
                "Player name is required."
            )

        elif not country.strip():

            st.warning(
                "Country is required."
            )

        else:

            conn = None

            try:

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO players
                    (
                        player_id,
                        full_name,
                        country,
                        playing_role,
                        batting_style,
                        bowling_style
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        int(player_id),
                        full_name.strip(),
                        country.strip(),
                        playing_role,
                        batting_style.strip(),
                        bowling_style.strip()
                    )
                )

                conn.commit()

                st.success(
                    f"Player '{full_name.strip()}' "
                    f"added successfully."
                )

                st.balloons()

            except sqlite3.IntegrityError:

                st.error(
                    "This Player ID already exists. "
                    "Please enter a unique Player ID."
                )

            except Exception as error:

                st.error(
                    f"Unable to add player: {error}"
                )

            finally:

                if conn:
                    conn.close()


# ============================================================
# UPDATE OPERATION
# ============================================================

elif operation == "Update Player":

    st.divider()

    st.subheader("✏️ Update Player")

    try:

        players_df = get_players_dataframe()

        if players_df.empty:

            st.warning(
                "No players are available to update."
            )

        else:

            player_options = {

                f"{int(row['player_id'])} - {row['full_name']}":
                int(row["player_id"])

                for _, row in players_df.iterrows()
            }

            selected_player_label = st.selectbox(
                "Select Player",
                list(player_options.keys())
            )

            selected_player_id = player_options[
                selected_player_label
            ]

            selected_row = players_df[
                players_df["player_id"]
                == selected_player_id
            ].iloc[0]


            st.info(
                "Current player information is displayed below. "
                "Modify the required fields and click Save Changes."
            )


            detail1, detail2, detail3 = st.columns(3)

            with detail1:

                st.metric(
                    "Player ID",
                    selected_player_id
                )

            with detail2:

                st.metric(
                    "Country",
                    (
                        selected_row["country"]
                        if pd.notna(
                            selected_row["country"]
                        )
                        else "Not Available"
                    )
                )

            with detail3:

                st.metric(
                    "Role",
                    (
                        selected_row["playing_role"]
                        if pd.notna(
                            selected_row["playing_role"]
                        )
                        else "Not Available"
                    )
                )


            with st.form(
                "update_player_form"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    new_name = st.text_input(
                        "Full Name",
                        value=(
                            str(
                                selected_row["full_name"]
                            )
                            if pd.notna(
                                selected_row["full_name"]
                            )
                            else ""
                        )
                    )

                    new_country = st.text_input(
                        "Country",
                        value=(
                            str(
                                selected_row["country"]
                            )
                            if pd.notna(
                                selected_row["country"]
                            )
                            else ""
                        )
                    )

                    roles = [
                        "Batsman",
                        "Bowler",
                        "All-rounder",
                        "Wicket-keeper"
                    ]

                    current_role = (
                        str(
                            selected_row[
                                "playing_role"
                            ]
                        )
                        if pd.notna(
                            selected_row[
                                "playing_role"
                            ]
                        )
                        else "Batsman"
                    )

                    if current_role in roles:

                        role_index = roles.index(
                            current_role
                        )

                    else:

                        role_index = 0

                    new_role = st.selectbox(
                        "Playing Role",
                        roles,
                        index=role_index
                    )


                with col2:

                    new_batting_style = st.text_input(
                        "Batting Style",
                        value=(
                            str(
                                selected_row[
                                    "batting_style"
                                ]
                            )
                            if pd.notna(
                                selected_row[
                                    "batting_style"
                                ]
                            )
                            else ""
                        )
                    )

                    new_bowling_style = st.text_input(
                        "Bowling Style",
                        value=(
                            str(
                                selected_row[
                                    "bowling_style"
                                ]
                            )
                            if pd.notna(
                                selected_row[
                                    "bowling_style"
                                ]
                            )
                            else ""
                        )
                    )

                    st.text_input(
                        "Player ID",
                        value=str(
                            selected_player_id
                        ),
                        disabled=True
                    )

                submit_update = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True
                )


            if submit_update:

                if not new_name.strip():

                    st.warning(
                        "Player name cannot be empty."
                    )

                elif not new_country.strip():

                    st.warning(
                        "Country cannot be empty."
                    )

                else:

                    conn = None

                    try:

                        conn = get_connection()

                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            UPDATE players
                            SET
                                full_name = ?,
                                country = ?,
                                playing_role = ?,
                                batting_style = ?,
                                bowling_style = ?
                            WHERE player_id = ?
                            """,
                            (
                                new_name.strip(),
                                new_country.strip(),
                                new_role,
                                new_batting_style.strip(),
                                new_bowling_style.strip(),
                                selected_player_id
                            )
                        )

                        conn.commit()

                        if cursor.rowcount > 0:

                            st.success(
                                f"Player '{new_name.strip()}' "
                                f"updated successfully."
                            )

                        else:

                            st.info(
                                "No changes were made to the record."
                            )

                    except Exception as error:

                        st.error(
                            f"Unable to update player: {error}"
                        )

                    finally:

                        if conn:
                            conn.close()


    except Exception as error:

        st.error(
            f"Database error: {error}"
        )


# ============================================================
# DELETE OPERATION
# ============================================================

elif operation == "Delete Player":

    st.divider()

    st.subheader("🗑️ Delete Player")

    st.warning(
        "Deleting a player permanently removes the player "
        "record from the players table."
    )

    try:

        players_df = get_players_dataframe()

        if players_df.empty:

            st.info(
                "No players are available to delete."
            )

        else:

            player_options = {

                f"{int(row['player_id'])} - {row['full_name']}":
                int(row["player_id"])

                for _, row in players_df.iterrows()
            }

            selected_player_label = st.selectbox(
                "Select Player to Delete",
                list(player_options.keys())
            )

            selected_player_id = player_options[
                selected_player_label
            ]

            selected_row = players_df[
                players_df["player_id"]
                == selected_player_id
            ].iloc[0]


            st.subheader("Selected Player Details")

            detail1, detail2, detail3 = st.columns(3)

            with detail1:

                st.metric(
                    "Player ID",
                    selected_player_id
                )

            with detail2:

                st.metric(
                    "Country",
                    (
                        selected_row["country"]
                        if pd.notna(
                            selected_row["country"]
                        )
                        else "Not Available"
                    )
                )

            with detail3:

                st.metric(
                    "Playing Role",
                    (
                        selected_row["playing_role"]
                        if pd.notna(
                            selected_row["playing_role"]
                        )
                        else "Not Available"
                    )
                )


            st.write(
                f"**Player Name:** "
                f"{selected_row['full_name']}"
            )


            confirmation = st.checkbox(
                "I confirm that I want to delete this player."
            )


            if st.button(
                "🗑️ Delete Player",
                use_container_width=True,
                disabled=not confirmation
            ):

                conn = None

                try:

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM players
                        WHERE player_id = ?
                        """,
                        (
                            selected_player_id,
                        )
                    )

                    conn.commit()

                    if cursor.rowcount > 0:

                        st.success(
                            f"Player "
                            f"'{selected_row['full_name']}' "
                            f"deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "No player record was deleted."
                        )


                except sqlite3.IntegrityError:

                    st.error(
                        "This player cannot be deleted because "
                        "the player is referenced by batting, "
                        "bowling or career-stat records."
                    )

                    st.info(
                        "Delete the related statistics first, "
                        "or keep the player record to preserve "
                        "database relationships."
                    )


                except Exception as error:

                    st.error(
                        f"Unable to delete player: {error}"
                    )


                finally:

                    if conn:
                        conn.close()


    except Exception as error:

        st.error(
            f"Database error: {error}"
        )


# ============================================================
# ABOUT CRUD
# ============================================================

st.divider()

with st.expander(
    "📘 About CRUD Operations"
):

    st.subheader("CRUD Meaning")

    st.write(
        "**C — Create:** Add a new player to the database."
    )

    st.write(
        "**R — Read:** View existing player records."
    )

    st.write(
        "**U — Update:** Modify existing player information."
    )

    st.write(
        "**D — Delete:** Remove a player record from the database."
    )

    st.divider()

    st.write(
        "This page interacts directly with the SQLite "
        "`players` table."
    )

    st.write(
        "Parameterized SQL queries are used for Create, "
        "Update and Delete operations."
    )


# ============================================================
# FOOTER
# ============================================================

footer()