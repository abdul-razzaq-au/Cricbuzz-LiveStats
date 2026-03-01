import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import re

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


def question1():
    # Question 1
    # api call
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/2/players"

    headers = {
        "x-rapidapi-key": "1b9db4757cmsha2ff3d635d2f5f5p1c73eejsn40138e04243a",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    team_player_data = response.json()
    tp_data = team_player_data.get('player', [])

    # separating dataset for all player roles
    separated = {}
    current_category = None

    for player in tp_data:
        # If it's a category row (no 'id')
        if "id" not in player:
            current_category = player["name"]
            separated[current_category] = []
        else:
            separated[current_category].append(player)
    batsmen = separated.get('BATSMEN', [])
    all_rounders = separated.get('ALL ROUNDER', [])
    bowlers = separated.get('BOWLER', [])
    wk = separated.get('WICKET KEEPER', [])

    # database operations

    cursor.execute("drop table if exists players_representing_India")
    cursor.execute("""
        create table players_representing_India(
        Name varchar(30),
        Playing_role varchar(25),
        Batting_style varchar(25),
        Bowling_style varchar(25),
        id int primary key
        )
    """)
    # insert query
    query = """
        insert into players_representing_India values
        (%s,%s,%s,%s,%s)
    """
    # inserting every row in the database table
    for ba in batsmen:
        row = (ba.get('name',''), "Batsman", ba.get('battingStyle', ''), ba.get('bowlingStyle', ''), ba.get('id', ''))
        cursor.execute(query, row)
    for bo in bowlers:
        row = (bo.get('name',''), "Bowler", bo.get('battingStyle', ''), bo.get('bowlingStyle', ''), bo.get('id', ''))
        cursor.execute(query, row)
    for a in all_rounders:
        row = (a.get('name',''), "All-rounder", a.get('battingStyle', ''), a.get('bowlingStyle', ''), a.get('id', ''))
        cursor.execute(query, row)
    for w in wk:
        row = (w.get('name',''), "Wicket keeper", w.get('battingStyle', ''), w.get('bowlingStyle', ''), w.get('id', ''))
        cursor.execute(query, row)

#Question2
def question2():
    
    # Question 2

    # api call
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "1b9db4757cmsha2ff3d635d2f5f5p1c73eejsn40138e04243a",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    recent_matches = response.json()

    # getting readable information about recent matches
    RecentMatches = []
    for matchtype in recent_matches['typeMatches']:
        for seriesmatch in matchtype['seriesMatches']:
            if 'seriesAdWrapper' in seriesmatch:
                seriesmatch = seriesmatch['seriesAdWrapper']
                Series_ID = seriesmatch['seriesId']
                Series_Name = seriesmatch['seriesName']
                Matches = seriesmatch['matches']
                for match in Matches:
                    match_info = match.get('matchInfo',[])

                    # takeaways
                    match_desc = match_info.get('matchDesc')
                    team1 = match_info.get('team1').get('teamName')
                    team2 = match_info.get('team2').get('teamName')
                    venue = f"{match_info.get('venueInfo').get('ground')}, {match_info.get('venueInfo').get('city')}"
                    dt = match_info.get('startDate')
                    date = datetime.fromtimestamp(int(dt)/1000)
                    
                    RecentMatches.append({
                            'Match Description' : match_desc,
                            'Team 1' : team1,
                            'Team 2' : team2,
                            'Venue' : venue,
                            'Date' : date.strftime("%d-%m-%Y %H:%M:%S")
                        })             

    # database implementation

    cursor.execute("drop table if exists recent_matches")
    cursor.execute("""
        create table recent_matches(
        Match_description varchar(100),
        Team1 varchar(30),
        Team2 varchar(50),
        Venue varchar(100),
        Match_date varchar(20)
        )
    """)
    insert2 = """
        insert into recent_matches values
        (%s,%s,%s,%s,%s)
    """

    for i in RecentMatches:
        row = (i.get('Match Description'), i.get('Team 1'), i.get('Team 2'), i.get('Venue'), i.get('Date'))
        cursor.execute(insert2, row)

# Question 3
def question3():
    
    # api call

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"mostRuns", "matchType":"2"}

    headers = {
        "x-rapidapi-key": "1b9db4757cmsha2ff3d635d2f5f5p1c73eejsn40138e04243a",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    d_mostRuns = response.json()

    cursor.execute("drop table if exists toprunscorers")
    cursor.execute("""
                    create table toprunscorers(
                    playerid varchar(30),
                    name varchar(30),
                    matches varchar(30),
                    innings varchar(30),
                    runs varchar(30),
                    average varchar(30)
                )
            """)
    insert3 = """
    insert into toprunscorers values
    (%s,%s,%s,%s,%s,%s)
    """
    for i in d_mostRuns.get('values', []):
        row  = i.get('values', [])
        cursor.execute(insert3, tuple(row))


# QUESTION 4

def question4():
    cursor.execute("drop table if exists venue_list")
    cursor.execute("""
            create table venue_list 
                (
                venue varchar(100),
                city varchar(50),
                country varchar(50),
                capacity bigint
                )
    """)
    insert4 = """
        insert into venue_list values
        (%s,%s,%s,%s)
    """
    venue_ids = [11,15,19,22,24,26,29,50,81,254]

    for vId in venue_ids:
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/venues/v1/{vId}"

        headers = {
            "x-rapidapi-key": "1b9db4757cmsha2ff3d635d2f5f5p1c73eejsn40138e04243a",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        venue_data = response.json()
        venue = venue_data.get('ground', '')
        city = venue_data.get('city', '')
        country = venue_data.get('country', '')
        capacity_str = venue_data.get('capacity')
        nums = re.search(r'\d+', capacity_str.replace(',', ''))
        capacity = int(nums.group()) if nums else None
        row = (venue, city, country, capacity)
        cursor.execute(insert4, row)


# Question 5

def question5():

    # data extraction
    import requests
    from collections import defaultdict

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "1b9db4757cmsha2ff3d635d2f5f5p1c73eejsn40138e04243a",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data5 = response.json()

    win_count = defaultdict(int)  # dictionary to store win count
    for typematch in data5.get('typeMatches', []):
        for seriesmatch in typematch.get('seriesMatches', []):
            series_info = seriesmatch.get('seriesAdWrapper', {})
            for match in series_info.get('matches', []):
                matchinfo = match.get('matchInfo', {})
                status = matchinfo.get('status', '')

                if 'won by' in status:
                    winner = status.split('won')[0]
                    win_count[winner] += 1

    # insert win result into table

    cursor.execute("drop table if exists wins")
    cursor .execute("""
                create table wins (
                team varchar(30),
                wincount smallint)
            """)
    query5 = """
        insert into wins values
        (%s,%s)
    """
    for i,j in win_count.items():
        row = (i,j)
        cursor.execute(query5, row)

# Question 6

def question6():
    # data extraction

    # get team list
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/international"

    headers = {
        "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    team_list = response.json()

    # database operations

    cursor.execute("drop table if exists player_role")
    cursor.execute("""
        create table player_role(
        Name varchar(30),
        Playing_role varchar(25),
        Batting_style varchar(25),
        Bowling_style varchar(25)
        )
    """)
    # create a dictionary of team names with their id
    teamList_dict = []
    for team in team_list.get('list', []):
        if 'teamId' in team:
            teamList_dict.append({
                'Team Name' : team['teamName'],
                'TeamID' : team['teamId']
            })

    # loop to get player detail of all team in the list
    for tid in teamList_dict:
        teamID = tid['TeamID']
        

        # get player detail for the team
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/teams/v1/{teamID}/players"

        headers = {
            "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        team_player_data = response.json()
        tp_data = team_player_data.get('player', [])

        # separating dataset for all player roles
        separated = {}
        current_category = None

        for player in tp_data:
            # If it's a category row (no 'id')
            if "id" not in player:
                current_category = player["name"]
                separated[current_category] = []
            else:
                separated[current_category].append(player)
        batsmen = separated.get('BATSMEN', [])
        all_rounders = separated.get('ALL ROUNDER', [])
        bowlers = separated.get('BOWLER', [])
        wk = separated.get('WICKET KEEPER', [])

        # insert query
        insert6 = """
            insert into player_role values
            (%s,%s,%s,%s)
        """
        # inserting every row in the database table
        for ba in batsmen:
            row = (ba.get('name',''), "Batsman", ba.get('battingStyle', ''), ba.get('bowlingStyle', ''))
            cursor.execute(insert6, row)
        for bo in bowlers:
            row = (bo.get('name',''), "Bowler", bo.get('battingStyle', ''), bo.get('bowlingStyle', ''))
            cursor.execute(insert6, row)
        for a in all_rounders:
            row = (a.get('name',''), "All-rounder", a.get('battingStyle', ''), a.get('bowlingStyle', ''))
            cursor.execute(insert6, row)
        for w in wk:
            row = (w.get('name',''), "Wicket keeper", w.get('battingStyle', ''), w.get('bowlingStyle', ''))
            cursor.execute(insert6, row)


# Question 7

def question7():

    # data extraction

    import requests

    # api call for highest individual score in test

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"highestScore", "matchType":"1"}

    headers = {
        "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    test_data = response.json()   # highest score data in test

    # api call for highest individual score in odi

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"highestScore", "matchType":"2"}

    headers = {
        "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    odi_data = response.json()   # highest score data in odi

    # api call for highest individual score in t20

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"highestScore", "matchType":"3"}

    headers = {
        "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    t20_data = response.json()   # highest score data in t20

    # creating table in database

    cursor.execute("drop table if exists highest_indi_score")
    cursor.execute("""
        create table highest_indi_score(
                    player_id varchar(30),
                    player_name varchar(30),
                    highest_score varchar(30),
                    balls varchar(30),
                    sr varchar(30),
                    vs varchar(30),
                    format varchar(30)
                )
    """)

    # insert query
    q7 = """
            insert into highest_indi_score values
            (%s,%s,%s,%s,%s,%s,%s)
        """

    # nesting every format data to insert into table
    # test
    for values in test_data.get('values'):
        row = values['values']
        row.append('test')
        cursor.execute(q7,tuple(row))

    # odi
    for values in odi_data.get('values'):
        row = values['values']
        row.append('odi')
        cursor.execute(q7,tuple(row))
    # t20
    for values in t20_data.get('values'):
        row = values['values']
        row.append('t20')
        cursor.execute(q7, tuple(row))

# Question 8

def question8():
    st.write("8")
    # Question 8

    from datetime import datetime

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/archives/international"

    querystring = {"year":"2024"}

    headers = {
        "x-rapidapi-key": "1e06182f48mshbab832f23b46b74p1431c2jsncdb53b1ee0a7",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    d8i = response.json()

    series_list_int = []
    for series in d8i.get('seriesMapProto', []):
        for s_info in series.get('series', []):
            dt = s_info.get('startDt')
            date = datetime.fromtimestamp(int(dt)/1000)    # divided by 1000 to get time in secs
            Date = date.strftime("%d-%m-%y %H:%M:%S")
            series_list_int.append({
                'series name' : s_info.get('name').split(',')[0],
                'seriesID' : s_info.get('id'),
                'start date' : date,
                'match type' : 'International'
            })
    series_list_int    

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/archives/domestic"

    querystring = {"year":"2024"}

    headers = {
        "x-rapidapi-key": "1e06182f48mshbab832f23b46b74p1431c2jsncdb53b1ee0a7",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    d8D = response.json()

    series_list_dom = []
    for series in d8D.get('seriesMapProto', []):
        for s_info in series.get('series', []):
            dt = s_info.get('startDt')
            date = datetime.fromtimestamp(int(dt)/1000)    # divided by 1000 to get time in secs
            Date = date.strftime("%d-%m-%y %H:%M:%S")
            series_list_dom.append({
                'series name' : s_info.get('name').split(',')[0],
                'seriesID' : s_info.get('id'),
                'start date' : date,
                'match type' : 'Domestic'
            })

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/archives/league"

    querystring = {"year":"2024"}

    headers = {
        "x-rapidapi-key": "1e06182f48mshbab832f23b46b74p1431c2jsncdb53b1ee0a7",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    d8L = response.json()

    series_list_L = []
    for series in d8L.get('seriesMapProto', []):
        for s_info in series.get('series', []):
            dt = s_info.get('startDt')
            date = datetime.fromtimestamp(int(dt)/1000)    # divided by 1000 to get time in secs
            Date = date.strftime("%d-%m-%y %H:%M:%S")
            series_list_L.append({
                'series name' : s_info.get('name').split(',')[0],
                'seriesID' : s_info.get('id'),
                'start date' : date,
                'match type' : 'League'
            })

    series_combined = series_list_int + series_list_dom + series_list_L
    cursor.execute("drop table if exists series_in_2024")
    cursor.execute("""
                create table if not exists series_in_2024
                (
                id varchar(10),
                name text,
                start_date timestamp,
                matchtype varchar(30),
                matchcount int,
                host_country varchar(30)
                )
                """)
    insert = """
        insert into series_in_2024 values
        (%s,%s,%s,%s,%s,%s)
    """

    for series in series_combined:
        id = series.get('seriesID')
        import requests

        # to fetch match count
        url = f"https://cricbuzz-cricket.p.rapidapi.com/series/v1/{id}"

        headers = {
            "x-rapidapi-key": "1e06182f48mshbab832f23b46b74p1431c2jsncdb53b1ee0a7",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        series_matches = response.json()

        count_match = 0
        for match_details in series_matches.get('matchDetails', []):
            count_match += len(match_details.get('matchDetailsMap', {}).get('match', {}))

        count_match

        series['match count'] = count_match
        
        # to fetch venue/host country
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/series/v1/{id}/venues"

        headers = {
            "x-rapidapi-key": "1e06182f48mshbab832f23b46b74p1431c2jsncdb53b1ee0a7",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        venue_data = response.json()

        venue_list = venue_data.get('seriesVenue',[])
        if venue_list and 'country' in venue_list[0]:
            host = venue_list[0]['country']

        series['host country'] = host

        row = (series.get('seriesID'), series.get('series name'), series.get('start date'), series.get('match type'), series.get('match count'), series.get('host country'))
        cursor.execute(insert, row)


# Question 9

def question9():
    st.write("9")
    q9 = """
    select id, name
    from players_representing_India
    where playing_role = 'All-rounder'
    """
    cursor.execute("drop table if exists allR_batting")
    cursor.execute("""
                    create table allR_batting (
                    name varchar(30),
                    runs_test int,
                    runs_odi int,
                    runs_t20 int,
                    runs_ipl int
                )
    """)
    cursor.execute("drop table if exists allR_bowling")
    cursor.execute("""
                    create table allR_bowling (
                    name varchar(30),
                    wickets_test int,
                    wickets_odi int,
                    wickets_t20 int,
                    wickets_ipl int
                )
    """)
    q9data = pd.read_sql(q9, con)

    # for batting
    plyr_btst = [{'label' : ['ROWHEADER', 'Test', 'ODI', 'T20', 'IPL']}]

    for id, name in zip(q9data['id'], q9data['name']):
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{id}/batting"

        headers = {
            "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        batting_data = response.json()

        for values in batting_data.get('values', []):
            if 'Runs' in values.get('values', []):
                row = values.get('values', [])
                row[0] = name
                plyr_btst.append({
                    'values' : row
                })
    insert9bt = """
        insert into allR_batting values 
        (%s,%s,%s,%s,%s)
    """
    for i in plyr_btst:
        if 'values' in i:
            row = i.get('values', [])
            cursor.execute(insert9bt, tuple(row))
    # for bowlig
    plyr_bwst = [{'label' : ['ROWHEADER', 'Test', 'ODI', 'T20', 'IPL']}]

    for id, name in zip(q9data['id'], q9data['name']):
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{id}/bowling"

        headers = {
            "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)


        bowling_data = response.json()

        for values in bowling_data.get('values', []):
            if 'Wickets' in values.get('values', []):
                row = values.get('values', [])
                row[0] = name
                plyr_bwst.append({
                    'values' : row
                })
    insert9bo = """
        insert into allR_bowling values 
        (%s,%s,%s,%s,%s)
    """
    for i in plyr_bwst:
        if 'values' in i:
            row = i.get('values', [])
            cursor.execute(insert9bo, tuple(row))
    

# Question 10

def question10():
    
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "f6052d753cmsh68c28e2b46a678dp19d10cjsne69b033a9f87",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    recent_matches = response.json()

    # data extraction
    RecentMatches = []

    for matchtype in recent_matches.get('typeMatches', []):
        for seriesmatch in matchtype.get('seriesMatches', []):
            seriesmatch = seriesmatch.get('seriesAdWrapper',{})
            for match in seriesmatch.get('matches', []):
                matchinfo = match.get('matchInfo', {})
                venueinfo = matchinfo.get('venueInfo', {})
                team1 = matchinfo.get('team1', {})
                team2 = matchinfo.get('team2', {})
                dt = matchinfo.get('startDate')
                date = datetime.fromtimestamp(int(dt)/1000)
                if 'won' in matchinfo.get('status'):
                    winner = matchinfo.get('status').split('won')[0]
                    victory_m = matchinfo.get('status').split('won')[1]
                else:
                    winner = 'not available'
                    victory_m = 'not available'
                if 'runs' in victory_m:
                    v_type = 'Runs'
                elif 'wkts' in victory_m:
                    v_type = 'Wickets'
                else:
                    v_type = 'unavailable'
                RecentMatches.append({
                    'matchID' : matchinfo.get('matchId'),
                    'matchdcs' : matchinfo.get('matchDesc', ''),
                    'team1' : team1.get('teamName', ''),
                    'team2' : team2.get('teamName', ''),
                    'state' : matchinfo.get('state'),
                    'winner' : winner,
                    'margin' : victory_m,
                    'victype' : v_type,
                    'venue' : f"{venueinfo.get('ground', '')}, {venueinfo.get('city', '')}",
                    'date' : date
                })

    # database operations
    cursor.execute("drop table if exists recent_matches")
    cursor.execute("""
                    create table recent_matches(
                    matchID int,
                    matchdes text,
                    team1 varchar(50),
                    team2 varchar(50),
                    state varchar(50),
                    winner varchar(50),
                    margin varchar(50),
                    victype varchar(50),
                    venue varchar(100),
                    date timestamp
                )
    """)
    q10 = """
        insert into recent_matches values
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    for i in RecentMatches:
        row = (
            i.get('matchID'),
            i.get('matchdcs'),
            i.get('team1'),
            i.get('team2'),
            i.get('state'),
            i.get('winner'),
            i.get('margin'),
            i.get('victype'),
            i.get('venue'),
            i.get('date')
        )
        cursor.execute(q10, row)

# Question 11

def question11(id):
    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{id}/batting"

    headers = {
    "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    bat_stat = response.json()
    # query to create bat stat table
    cursor.execute("drop table if exists player_bat_stat")
    cursor.execute("""
            create table player_bat_stat (
                    Statistic varchar(15),
                    Test float,
                    ODI float,
                    T20 float,
                    IPL float
                    )
        """)

        # query to insert batting statistics into the table
    query = """
            insert into player_bat_stat values
            (%s,%s,%s,%s,%s)
        """

        # nested execution of query to insert every row in the table
    for values in bat_stat['values']:
        if 'Runs' in values.get('values'):
            row = values['values']
            cursor.execute(query, row)
        if 'Average' in values.get('values'):
            row = values['values']
            cursor.execute(query, row)

# Question 12

def question12():
    st.write("12")

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    recent_matches = response.json()

    cursor.execute("""
        create table ven_win(
                name varchar(30),
                ven_country varchar(30),
                team_country varchar(30),
                winner varchar(30)
                )
    """)
    q12 = """
        insert into ven_win
        values (%s,%s,%s,%s)
    """

    team1D = []
    team2D = []

    for matchtype in recent_matches.get('typeMatches', []):
        for seriesmatch in matchtype.get('seriesMatches', []):
            seriesmatch = seriesmatch.get('seriesAdWrapper',{})
            for match in seriesmatch.get('matches', []):
                matchinfo = match.get('matchInfo', {})
                if 'won' in matchinfo.get('status'):
                    team1 = matchinfo.get('team1').get('teamName')
                    t1cntry = team1
                    team2 = matchinfo.get('team2').get('teamName')
                    t2cntry = team2
                    win_text = matchinfo.get('status').split(' won ')
                    winner = win_text[0]

                    v_id = matchinfo.get('venueInfo').get('id')

                    # call api for venue info
                    import requests

                    url = f"https://cricbuzz-cricket.p.rapidapi.com/venues/v1/{v}"

                    headers = {
                        "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
                        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
                    }

                    response = requests.get(url, headers=headers)

                    venue_data = response.json()

                    v_country = venue_data.get('country')

                    team1D.append({
                        'name' : team1,
                        'vencon' : v_country,
                        'country' : t1cntry,
                        'winner' : winner
                        })
                    team2D.append({
                        'name' : team2,
                        'vencon' : v_country,
                        'country' : t2cntry,
                        'winner' : winner
                        })
                    
    for i,j in zip(team1D,team2D):
        row1 = (i['name'], i['vencon'], i['country'], i['winner'])
        row2 = (j['name'], j['vencon'], j['country'], j['winner'])
        cursor.execute(q12, row1)
        cursor.execute(q12, row2)
        

                

# Question 13

def question13():
    st.write("13")

# Question 14

def question14():
    st.write("14")
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    recent_matches = response.json()
    bowlers_stat = []
    match_list_bowlers = []
    for matchtype in recent_matches.get('typeMatches', []):
        for seriesmatch in matchtype.get('seriesMatches', []):
            seriesmatch = seriesmatch.get('seriesAdWrapper',{})
            for match in seriesmatch.get('matches', []):
                matchinfo = match.get('matchInfo', {})
                if 'won' in matchinfo.get('status'):
                    match_list_bowlers.append({
                        'matchID' : matchinfo.get('matchId'),
                        'matchdes' : matchinfo.get('matchDesc'),
                        'team1' : matchinfo.get('team1', '').get('teamName'),
                        'team2' : matchinfo.get('team2', '').get('teamName'),
                        'venue' : matchinfo.get('venueInfo', '').get('ground')  
                    })

    for match in match_list_bowlers:
        match_id = match.get('matchID')
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

        headers = {
            "x-rapidapi-key": "c7e7dd73b8mshb476392299f2140p197a35jsn6e6517c46011",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        match_sc = response.json()

        for scorecard in match_sc.get('scorecard', []):
            for bowler in scorecard.get('bowler', []):
                if scorecard.get('inningsid') == 1:
                    team = match.get('team1')
                elif scorecard.get('inningsid') == 2:
                    team = match.get('team1')
                winner = match_sc.get('status', '').split(' won')[0]
                bowlers_stat.append({
                    'id' : bowler.get('id'),
                    'name' : bowler.get('name'),
                    'wickets' : bowler.get('wickets'),
                    'overs' : bowler.get('overs'),
                    'economy' : bowler.get('economy'),
                    'playerteam' : team,
                    'winner' : winner,
                    'venue' : match.get('venue')
                })
    cursor.execute("drop table if exists bowler_stat")
    cursor.execute("""
        create table bowler_stat(
        playerid int,
        playername varchar(30),
        wickets int,
        overs float,
        economy float,
        playerteam varchar(30),
        winner varchar(30),
        venue varchar(50)
        )
    """)

    q14 = """
        insert into bowler_stat values
        (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for i in bowlers_stat:
        row = (i.get('id'), i.get('name', ''), i.get('wickets', ''), i.get('overs'), i.get('economy'), i.get('playerteam', ''), i.get('winner', ''), i.get('venue', ''))
        cursor.execute(q14, row)
      
        

# Question 15

def question15():
    st.write("15")
    import re
    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    recent_matches = response.json()
    CloseMatches = []
    play_exc = []
    for matchtype in recent_matches.get('typeMatches', []):
        for seriesmatch in matchtype.get('seriesMatches', []):
            seriesmatch = seriesmatch.get('seriesAdWrapper',{})
            for match in seriesmatch.get('matches', []):
                
                matchinfo = match.get('matchInfo', {})
                if 'won' in matchinfo.get('status',''):
                    
                    if 'runs' in matchinfo.get('status', ''):
                        text = matchinfo.get('status', '')
                        margin = int(re.search(r'\d+', text).group())
                        if margin < 50:
                            
                            CloseMatches.append({
                                'matchID' : matchinfo.get('matchId', ''),
                                'matchdes' : matchinfo.get('matchDesc', ''),
                                'team1' : matchinfo.get('team1', '').get('teamName'),
                                'team2' : matchinfo.get('team2', '').get('teamName')
                            })
                    elif 'wkts' in matchinfo.get('status', ''):
                        text = text = matchinfo.get('status', '')
                        margin = int(re.search(r'\d+', text).group())
                        if margin < 5:
                            
                            CloseMatches.append({
                                'matchID' : matchinfo.get('matchId', ''),
                                'matchdes' : matchinfo.get('matchDesc', ''),
                                'team1' : matchinfo.get('team1', '').get('teamName'),
                                'team2' : matchinfo.get('team2', '').get('teamName')
                            })

    for closematch in CloseMatches:
        match_id = closematch.get('matchID', '')
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

        headers = {
            "x-rapidapi-key": "c7e7dd73b8mshb476392299f2140p197a35jsn6e6517c46011",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        match_sc = response.json()

        for scorecard in match_sc.get('scorecard', ''):
            for batsman in scorecard.get('batsman'):
                if scorecard.get('inningsid') == 1:
                    team = closematch.get('team1')
                elif scorecard.get('inningsid') == 2:
                    team = closematch.get('team2')
                name = batsman.get('name', '')
                runs = int(batsman.get('runs'))
                winner = match_sc.get('status', '').split('won')[0]
                if runs > 30:
                    play_exc.append({
                        'id' : batsman.get('id', ''),
                        'name' : name,
                        'playerteam' : team,
                        'runs' : runs,
                        'winner' : winner
                    })

    cursor.execute("drop table if exists close_match_stat")
    cursor.execute("""
        create table close_match_stat(
        playerid int,
        playername varchar(30),
        playerteam varchar(30),
        runs int,
        winner varchar(30)
        )
    """)

    q15 = """
        insert into close_match_stat values
        (%s,%s,%s,%s,%s)
    """

    for i in play_exc:
        row = (i.get('id'), i.get('name', ''), i.get('playerteam', ''), i.get('runs'), i.get('winner'))
        cursor.execute(q15, row)

# Question 16

def question16():
    st.write("16")

# Question 17

def question17():
    st.write("17")

    # database operations
    cursor.execute("drop table if exists win_by_toss")
    cursor.execute("""
                create table win_by_toss (
                toss_winner varchar(50),
                decision varchar(10),
                winner varchar(50)
                )
            """)
    q17 = """
        insert into win_by_toss values
        (%s,%s,%s)
        """

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "x-rapidapi-key": "9e47d70039msh8126e7683bf588cp14230ajsned6298322c21",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    recent_matches = response.json()

    win_toss = []
    match_ids = []
    for matchtype in recent_matches.get('typeMatches', []):
        for seriesmatch in matchtype.get('seriesMatches', []):
            seriesmatch = seriesmatch.get('seriesAdWrapper',{})
            for match in seriesmatch.get('matches', []):
                matchinfo = match.get('matchInfo', {})
                if 'won' in matchinfo.get('status'):
                    match_ids.append(matchinfo.get('matchId'))

    for id in match_ids:
        import requests

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{id}"

        headers = {
            "x-rapidapi-key": "c7e7dd73b8mshb476392299f2140p197a35jsn6e6517c46011",
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        match_details = response.json()

        team1ab = match_details.get('team1').get('teamsname')
        team2ab = match_details.get('team2').get('teamsname')

        # team1ab, team2ab
        if team1ab in match_details.get('shortstatus'):
            winner = match_details.get('team1').get('teamname')
        elif team2ab in match_details.get('shortstatus'):
            winner = match_details.get('team2').get('teamname')

        toss_result = match_details.get('tossstatus', '').split(' opt to ')
        win_toss.append({
            'tosswinner' : toss_result[0],
            'tossdes' : toss_result[1],
            'winner' : winner
        })

    for i in win_toss:
        row = (i.get('tosswinner', ''), i.get('tossdes', ''), i.get('winner', ''))
        cursor.execute(q17, row)

# Question 18

def question18():
    st.write("18")

    # for odi bowlers
    cursor.execute("drop table if exists odi_bowlers")
    cursor.execute("""
        create table odi_bowlers (
        id int,
        name varchar(50),
        matches int,
        overs float,
        wickets int,
        economy float
        )                
    """)
    insert18odi = """
        insert into odi_bowlers values
        (%s,%s,%s,%s,%s,%s)
    """

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"lowestEcon","matchType":"2"}

    headers = {
        "x-rapidapi-key": "c7e7dd73b8mshb476392299f2140p197a35jsn6e6517c46011",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data18odi = response.json()

    for i in data18odi.get('values', []):
        row = i.get('values', [])
        cursor.execute(insert18odi, row)

    # for t20 bowlers
    cursor.execute("drop table if exists t20_bowlers")
    cursor.execute("""
        create table t20_bowlers (
        id int,
        name varchar(50),
        matches int,
        overs float,
        wickets int,
        economy float
        )                
    """)
    insert18t20 = """
        insert into t20_bowlers values
        (%s,%s,%s,%s,%s,%s)
    """

    import requests

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"

    querystring = {"statsType":"lowestEcon","matchType":"3"}

    headers = {
        "x-rapidapi-key": "c7e7dd73b8mshb476392299f2140p197a35jsn6e6517c46011",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data18t20 = response.json()

    for i in data18t20.get('values', []):
        row = i.get('values', [])
        cursor.execute(insert18t20, row)


# Question 19

def question19():
    st.write("19")

# Question 20

def question20():
    st.write("20")

# Question 21

def question21():
    st.write("21")

# Question 22

def question22():
    st.write("22")

# Question 23

def question23():
    st.write("23")

# Question 24

def question24():
    st.write("25")

# Question 25

def question25():
    st.write("25")
