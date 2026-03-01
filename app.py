import streamlit as st
import psycopg2
import pandas as pd
import live
import playerstat
import sqlquery
import crudops
import home

# creating SQL connection
con = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    database = 'Cricbuzz-stats',
    password = 'armaaz911',
    port = 5432
)

cursor = con.cursor()
con.autocommit=True

st.set_page_config(layout="wide")

# create a naviagation side bar
st.sidebar.title("Dashboard")


#create 5 pages
select = st.sidebar.radio(
    "Select Page",
    ["🏠 Home","⌚ Live Matches", "🔍 Search Players", "📊SQL Query", "🛠️ CRUD Operations"]
)

if select == "🏠 Home":
    home.homepage()

# when live page selected
if select == "⌚ Live Matches":
    live.title()
    # live.match()
    st.sidebar.divider()
    st.sidebar.markdown("""
        Live Score Page: <br>
        - Real-time match data
        - Detailed scorecard
        - Series Information
        - Interactive match selection
    """, True)

# when player search page selected   
elif select == "🔍 Search Players":
    playerstat.title()
    # playerstat.playerstatistics()
    st.sidebar.divider()
    st.sidebar.markdown("""
        Player Search Page: <br>
        - Search any player
        - Detailed profile
        - Career statistics
    """, True)


# when SQL query page selected
elif select == "📊SQL Query":
    st.title("🏏 Database Query Questions")
    st.sidebar.divider()
    st.sidebar.markdown("""
        SQL Analytics Page: <br>
        - Practice SQL Questions
        - Selective Query Execution
        - Real Cricket Statistics
    """, True)


    question_list = [
        "1- Players representing India",
        "2 -Recent matches",
        "3- Top 10 highest run scorers in ODI",
        "4- Venue having capacity of more than 25,000 spectators",
        "5- Win count of each team",
        "6- Count of players belonging to each playing role",
        "7- Highest individual batting score in each format",
        "8- Series started in 2024",
        "9- All rounder player statistics",
        "10- Last 20 completed matches",
        "11- Player performance comparision across different formats",
        "12- Team performance at home vs away",
        "13- Batting partnership of cinsecutive batsmen",
        "14- Bowling performance at different venues",
        "15- Close match performing players",
        "16- Batting perfromance over the year",
        "17- Win percentage when winning the toss by toss decision",
        "18- Best Economical bowlers in limited overs",
        "19- Consistent batsmen",
        "20- Matches played in different format by each player",
        "21- Player ranking",
        "22- Head-to-head match prediction analysis between teams",
        "23- Recent form and momentum of player",
        "24- Best player combination",
        "25- Time-series analysis"
    ]

    selection = st.selectbox(
        "☑️ Select a question to analyse",
        question_list
    )

    # Question 1
    if selection == question_list[0]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question1()
            st.markdown("📊 Query Result:")

            # get data from database table
            query1 ="""
                    select
                    name, playing_role, batting_style, bowling_style
                    from players_representing_India
                """
            players_table = pd.read_sql(query1, con)

            # display on dashboard
            st.dataframe(players_table, use_container_width=True, hide_index=True)
    

    # Question 2
    elif selection == question_list[1]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question2()
            st.markdown("📊 Query Result:")

            query2 = """
                select
                match_description,
                team1,
                team2,
                venue,
                cast(match_date as date)
                from recent_matches order by match_date desc
            """

            # get data from database table 
            matches = pd.read_sql(query2, con)

            # display on dashboard
            st.dataframe(
                matches,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "match_description" : st.column_config.TextColumn(
                        "Match Description",
                        width= "large"
                    ),
                    "team1" : st.column_config.TextColumn(
                        "Team 1"
                    ),
                    "team2" : st.column_config.TextColumn(
                        "Team 2"
                    ),
                    "venue" : st.column_config.TextColumn(
                        "Venue"
                    ),
                    "match_date" : st.column_config.DateColumn(
                        "Date"
                    )
                }
            )
    
    # QUESTION 3
    elif selection == question_list[2]:
        st.markdown(f"#### {selection}")
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question3()
            st.markdown("📊 Query Result:")
            query3 = """
                select name,
                runs,
                average,
                innings
                from toprunscorers
                limit 10
            """
            # get data from database table 
            top_scorers = pd.read_sql(query3, con)

            # display on dashboard
            st.dataframe(
                top_scorers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name" : st.column_config.TextColumn(
                        "Batsman Name"
                    ),
                    "runs" : st.column_config.TextColumn(
                        "Runs Scored"
                    ),
                    "average" : st.column_config.TextColumn(
                        "Batting Average"
                    ),
                    "innings" : st.column_config.TextColumn(
                        "Innings Played"
                    )
                }
            )

    
    # QUESTION 4

    elif selection == question_list[3]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question4()
            st.markdown("📊 Query Result:")

            query4 = """
                select 
                    venue,
                    city,
                    country,
                    capacity
                from venue_list
                order by capacity desc
                """
            
            # get data from database table 
            data4 = pd.read_sql(query4, con)

            # display on dashboard
            st.dataframe(
                data4,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "venue" : st.column_config.TextColumn(
                        "Venue"
                    ),
                    "city" : st.column_config.TextColumn(
                        "City"
                    ),
                    "country" : st.column_config.TextColumn(
                        "Country"
                    ),
                    "capacity" : st.column_config.TextColumn(
                        "Capacity"
                    )
                }
            )

    # QUESTION 5
    elif selection == question_list[4]:
        st.markdown(f"#### {selection}")
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question5()
            st.markdown("📊 Query Result:")
            query5 = """
                select 
                team,
                wincount
                from wins
                order by wincount desc
            """
            # get data from database table 
            win_count = pd.read_sql(query5, con)

            # display on dashboard
            st.dataframe(
                win_count,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "team" : st.column_config.TextColumn(
                        "Team Name"
                    ),
                    "wincount" : st.column_config.TextColumn(
                        "Count of wins"
                    )
                }
            )


    # QUESTION 6
    elif selection == question_list[5]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question6()
            st.markdown("📊 Query Result:")
            query6 = """
                select 
                playing_role,
                count(playing_role) as count
                from player_role
                group by playing_role
            """
            # get data from database table 
            player_role_count = pd.read_sql(query6, con)

            # display on dashboard
            st.dataframe(
                player_role_count,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "playing_role" : st.column_config.TextColumn(
                        "Playing Role"
                    ),
                    "count" : st.column_config.TextColumn(
                        "Count of players"
                    )
                }
            )

        
    # QUESTION 7
    elif selection == question_list[6]:
        st.markdown(f"#### {selection}")

        if st.button("🏃🏻‍➡️ Execute Query"):
            sqlquery.question7()
            st.markdown("📊 Query Result:")
            query7 = """
                select 
                format,
                max(highest_score) as highest_indi_score
                from highest_indi_score
                group by format
                order by highest_indi_score desc
            """
            # get data from database table 
            win_count = pd.read_sql(query7, con)

            # display on dashboard
            st.dataframe(
                win_count,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "format" : st.column_config.TextColumn(
                        "Format"
                    ),
                    "wincount" : st.column_config.TextColumn(
                        "Highest Score"
                    )
                }
            )
    # QUESTION 8
    elif selection == question_list[7]:
        st.markdown(f"#### {selection}")
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question8()
            st.markdown("📊 Query Result:")
            query8 = """
                    select 
                    name, 
                    host_country, 
                    matchtype, 
                    start_date,
                    matchcount
                    from series_in_2024
                    order by start_date desc
                """
            # get data from database table 
            series_data = pd.read_sql(query8, con)
            series_data["start_date"] = pd.to_datetime(series_data["start_date"])
            # display on dashboard
            st.dataframe(
                series_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name" : st.column_config.TextColumn(
                        "Series Name"
                    ),
                    "host_country" : st.column_config.TextColumn(
                        "Host"
                    ),
                    "matchtype" : st.column_config.TextColumn(
                        "Match Type"
                    ),
                    "start_date" : st.column_config.DateColumn(
                        "Start Date",
                        format="YYYY-MM-DD"
                    ),
                    "matchcount" : st.column_config.TextColumn(
                        "Number of matches"
                    )
                }
            )
            


    # QUESTION 9
    elif selection == question_list[8]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question9()
            st.markdown("📊 Query Result:")
            query9 = """
                    select allR_batting.name, 
                    wickets_test, wickets_odi, wickets_t20, wickets_ipl,
                    runs_test, runs_odi, runs_t20, runs_ipl
                    from allR_bowling inner join allR_batting
                    on allR_bowling.name = allR_batting.name
                    where ((wickets_test >= 50) or (wickets_odi >= 50) or (wickets_t20 >= 50)or (wickets_ipl >= 50))
                    and ((runs_test >= 1000) or (runs_odi >= 1000) or (runs_t20 >= 1000) or (runs_ipl >= 1000))
                """
            # get data from database table 
            data9 = pd.read_sql(query9, con)

            # display on dashboard
            st.dataframe(
                data9,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name" : st.column_config.TextColumn(
                        "Name"
                    ),
                    "wickets_test" : st.column_config.TextColumn(
                        "Test Wickets"
                    ),
                    "wickets_odi" : st.column_config.TextColumn(
                        "ODI Wickets"
                    ),
                    "wickets_t20" : st.column_config.TextColumn(
                        "T20 Wickets"
                    ),
                    "wickets_ipl" : st.column_config.TextColumn(
                        "IPL Wickets"
                    ),
                    "runs_test" : st.column_config.TextColumn(
                        "Test Runs"
                    ),
                    "runs_odi" : st.column_config.TextColumn(
                        "ODI Runs"
                    ),
                    "runs_t20" : st.column_config.TextColumn(
                        "T20 Runs"
                    ),
                    "runs_ipl" : st.column_config.TextColumn(
                        "IPL Runs"
                    )
                }
            )   
    # QUESTION 10
    elif selection == question_list[9]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question10()
            st.markdown("📊 Query Result:")
            query10 = """
                    select
                    matchdes, team1, team2, winner, margin, victype, venue
                    from recent_matches
                    where state = 'Complete'
                    order by recent_matches.date desc
                    limit 20
                """
            # get data from database table 
            data10 = pd.read_sql(query10, con)

            # display on dashboard
            st.dataframe(
                data10,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "matchdes" : st.column_config.TextColumn(
                        "Match Description"
                    ),
                    "team1" : st.column_config.TextColumn(
                        "Team1 Name"
                    ),
                    "team2" : st.column_config.TextColumn(
                        "Team2 Name"
                    ),
                    "winner" : st.column_config.TextColumn(
                        "Winning team"
                    ),
                    "margin" : st.column_config.TextColumn(
                        "Victory Margin"
                    ),
                    "victype" : st.column_config.TextColumn(
                        "Victory type"
                    ),
                    "venue" : st.column_config.TextColumn(
                        "Venue name"
                    )
                }
            )


    # QUESTION 11
    elif selection == question_list[10]:
        st.markdown(f"#### {selection}")
        search = st.text_input(
        "Search a player",
        placeholder="like Virat Kohli, Sachin, Rohit, etc. "
        )
        # player search api
        import requests

        url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"

        querystring = {"plrN":f"{search}"}

        headers = {
            "x-rapidapi-key": "0eb31f6f87msh2fcd39fd572db57p1c64a6jsna48eb1cac023",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        # print(response.json())
        search_data = response.json()

        # create player search list
        search_list = []
        for plyr in search_data['player']:
            search_list.append({
                'Name' : plyr['name'],
                'PlayerID' : plyr['id']
            })
        
        # searched names list
        search_names = []
        for names in search_list:
            search_names.append(names['Name'])
        
        # searches players ids list
        search_id = []
        for ids in search_list:
            search_id.append(ids['PlayerID'])

        # create a select box

        selected_player = st.selectbox(
            "Found Player",
            search_names
        )

        selected_player_id = next(
            i['PlayerID'] for i in search_list if i['Name']==selected_player
        )
        
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question11(id=selected_player_id)
            st.markdown("📊 Query Result:")
            query11 = """
                    select 
                    test, odi, t20, ipl,
                    ROUND(((test + odi + t20 + ipl)/4.0)::numeric,2) as overall_average
                    from player_bat_stat
                """
            # get data from database table 
            data11 = pd.read_sql(query11, con)

            # display on dashboard
            st.dataframe(
                data11,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "test" : st.column_config.TextColumn(
                        "Test runs"
                    ),
                    "odi" : st.column_config.TextColumn(
                        "ODI runs"
                    ),
                    "t20" : st.column_config.TextColumn(
                        "T20 runs"
                    ),
                    "ipl" : st.column_config.TextColumn(
                        "IPL runs"
                    ),
                    "overall_average" : st.column_config.TextColumn(
                        "Overall Average"
                    )
                }
            )

    # QUESTION 12
    elif selection == question_list[11]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question12()
            st.markdown("📊 Query Result:")
            query12 = """
                    Select 
                        team_country,
                        CASE 
                            WHEN team_country = ven_country THEN 'Home'
                            ELSE 'Away'
                        END AS home_away,
                        COUNT(*) AS wins
                    FROM ven_win
                    WHERE team_country = winner
                    GROUP BY team_country, home_away
                    ORDER BY team_country
                """
            # get data from database table 
            data12 = pd.read_sql(query12, con)

            # display on dashboard
            st.dataframe(
                data12,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "team_country" : st.column_config.TextColumn(
                        "Team Country"
                    ),
                    "home_away" : st.column_config.TextColumn(
                        "Home/Away"
                    ),
                    "wins" : st.column_config.TextColumn(
                        "Win Count"
                    )
                }
            )

    # QUESTION 13
    elif selection == question_list[12]:
        st.markdown(f"#### {selection}")
    # QUESTION 14
    elif selection == question_list[13]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question14()
            st.markdown("📊 Query Result:")
            query14 = """
                    select playerid, 
                            playername,
                            sum(wickets) as total_wickets,
                            round(avg(economy)::numeric,2) as average_eco, 
                            venue,
                            count(venue) as venue_count
                    from bowler_stat
                    group by playerid, playername, venue
                    having count(venue) >= 3
                """
            # get data from database table 
            data14 = pd.read_sql(query14, con)

            # display on dashboard
            st.dataframe(
                data14,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "playerid" : st.column_config.TextColumn(
                        "Player ID"
                    ),
                    "playername" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "total_wickets" : st.column_config.TextColumn(
                        "Total wickets"
                    ),
                    "venue" : st.column_config.TextColumn(
                        "Venue"
                    ),
                    "average_eco" : st.column_config.TextColumn(
                        "Average economy"
                    ),
                    "venue_count" : st.column_config.TextColumn(
                        "Count of Venue"
                    )
                }
            )

            st.markdown("Focusing on players who bowled atleast 4 overs in each match:")
            query14_4 = """
                    select playerid, 
                            playername,
                            sum(wickets) as total_wickets, 
                            venue,
                            round(avg(economy)::numeric,2) as average_eco,
                            count(venue) as venue_count
                    from bowler_stat
                    where overs >= 4
                    group by playerid, playername, venue
                    having count(venue) >= 3;
                """
            # get data from database table 
            data14_4 = pd.read_sql(query14_4, con)

            # display on dashboard
            st.dataframe(
                data14_4,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "playerid" : st.column_config.TextColumn(
                        "Player ID"
                    ),
                    "playername" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "total_wickets" : st.column_config.TextColumn(
                        "Total wickets"
                    ),
                    "venue" : st.column_config.TextColumn(
                        "Venue"
                    ),
                    "average_eco" : st.column_config.TextColumn(
                        "Average economy"
                    ),
                    "venue_count" : st.column_config.TextColumn(
                        "Count of Venue"
                    )
                }
            )

    # QUESTION 15
    elif selection == question_list[14]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question15()
            st.markdown("📊 Query Result:")
            query15 = """
                    select 
                    playerid, playername, round(avg(runs),2) as average_runs, count(winner) as win_count
                    from close_match_stat
                    where trim(playerteam) = trim(winner)
                    group by playerid, playername
                    order by win_count desc;
                """
            # get data from database table 
            data15 = pd.read_sql(query15, con)

            # display on dashboard
            st.dataframe(
                data15,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "playerid" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "playername" : st.column_config.TextColumn(
                        "Player Name"
                    ),
                    "average_runs" : st.column_config.TextColumn(
                        "Average run"
                    ),
                    "win_count" : st.column_config.TextColumn(
                        "Team Win count when played"
                    )
                }
            )

    # Question 17
    elif selection == question_list[16]:
        st.markdown(f"### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question17()
            query17 = """
                    select 
                        decision,
                        count(*) as total_matches,
                        count(*) filter (where toss_winner = winner) as match_won_after_winning_toss,
                        Round(
                            count(*) filter (where toss_winner = winner) * 100.0/count(*),2
                            )
                            as win_perc_after_winning_toss
                    from win_by_toss
                    group by decision
                """
            # get data from database table 
            data17 = pd.read_sql(query17, con)

            # display on dashboard
            st.dataframe(
                data17,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "decision" : st.column_config.TextColumn(
                        "Toss decision"
                    ),
                    "total_matches" : st.column_config.TextColumn(
                        "Total matches"
                    ),
                    "match_won_after_winning_toss" : st.column_config.TextColumn(
                        "Number of matches won"
                    ),
                    "win_perc_after_winning_toss" : st.column_config.TextColumn(
                        "Win %"
                    )
                }
            )
            st.markdown("###### based on recent completed matches where match gave a proper win/lose result")
   
    # QUESTION 18
    elif selection == question_list[17]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question18()
            query18 = """
                    select
                        odi_bowlers.id as id,
                        odi_bowlers.name as name,
                        round(
                            ((odi_bowlers.economy + t20_bowlers.economy)/2)
                            ::numeric, 2
                            )
                            as overall_eco
                    from odi_bowlers inner join t20_bowlers
                    on odi_bowlers.id = t20_bowlers.id
                    where ( odi_bowlers.matches > 10 
                            and 
                            t20_bowlers.matches > 10
                            and 
                            (odi_bowlers.overs/odi_bowlers.matches) > 2 
                            and 
                            (t20_bowlers.overs/t20_bowlers.matches) > 2
                            )
                """
            # get data from database table 
            data18 = pd.read_sql(query18, con)

            # display on dashboard
            st.dataframe(
                data18,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id" : st.column_config.TextColumn(
                        "Bowler ID"
                    ),
                    "name" : st.column_config.TextColumn(
                        "Bowler name"
                    ),
                    "overall_eco" : st.column_config.TextColumn(
                        "Overall Economy"
                    )
                }
            )

    # QUESTION 19
    elif selection == question_list[18]:
        st.markdown(f"#### {selection}")
    # QUESTION 20
    elif selection == question_list[19]:
        st.markdown(f"#### {selection}")
    # QUESTION 21
    elif selection == question_list[20]:
        st.markdown(f"#### {selection}")
    # QUESTION 22
    elif selection == question_list[21]:
        st.markdown(f"#### {selection}")
    # QUESTION 23
    elif selection == question_list[22]:
        st.markdown(f"#### {selection}")
    # QUESTION 24
    elif selection == question_list[23]:
        st.markdown(f"#### {selection}")
    # QUESTION 25
    elif selection == question_list[24]:
        st.markdown(f"#### {selection}")


# when CRUDs page selected
elif select == "🛠️ CRUD Operations":
    st.title("🛠️ CRUD Operations")
    st.sidebar.divider()
    st.sidebar.markdown("""
        CRUD operations Page: <br>
        - Create/add players
        - View all players
        - Update player information
        - Delete player
    """, True)


    crudops.title()

    choice = st.selectbox(
        "Chose an operation:",
        ["➕Create (Add Player)", "📖Read (Load Players)", "🖊️Update player (Edit Player)", "🗑️Delete (Remove Player)"]
    )

    if choice == "➕Create (Add Player)":
        # crudops.create()
        crudops.add()
    
    elif choice == "📖Read (Load Players)":
        crudops.read()

    elif choice == "🖊️Update player (Edit Player)":
            crudops.update()

    elif choice == "🗑️Delete (Remove Player)":
            crudops.delete()

st.divider()
st.markdown("""
        # 📠 About This Dashboard
        This comprehensive Cricket Dashboard demonstrates:
        - APl Integration: Real-time data from Cricbuzz API
        - Database Operations: PostgreSQL with full CRUD functionality
        - Data Analysis: 15+ different SQL analytics queries
        - Interactive UI: Streamlit components
        - Player Statistics: Detailed batting and bowling stats of players
    """, True)


