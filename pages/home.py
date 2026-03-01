import streamlit as st

def homepage():
    st.title("📈 Cricbuzz Live-Stats Project")

    st.markdown("""
            ## 🏏 Cricbuzz LiveStats

            ## Real-Time Cricket Insights & SQL-Based Analytics
                

            Welcome to Cricbuzz LiveStats, an interactive cricket analytics dashboard built using Python, SQL, and Streamlit.
            This application integrates live cricket data from the Cricbuzz API with a structured SQL database to deliver real-time match updates, detailed player statistics, and advanced analytical insights.


            #### 🎯 Project Objective

            The goal of this project is to:

            - Integrate live cricket data using REST API

            - Store structured match and player data in a relational database

            - Perform 25+ analytical SQL queries (Beginner to Advanced)

            - Provide a user-friendly multi-page dashboard

            - Implement full CRUD operations for database learning


            #### 🛠️ Tools & Technologies Used

            - Python – Backend logic and API integration

            - Streamlit – Web application framework

            - SQL (MySQL / PostgreSQL / SQLite) – Database management

            - REST API (Cricbuzz API) – Real-time data fetching

            - pandas – Data processing

            - requests – API handling

            - GitHub – Version control
                

            ---
            #### 📊 Application Modules

            This dashboard consists of the following pages:

            ##### 🏠 Home Page

            - Project overview

            - Tools used

            - Navigation guide


            #### ⚡ Live Match Page

            - View ongoing matches

            - Real-time scorecard

            - Batsman and bowler statistics

            - Match status and venue details


            #### 🧮 SQL Analytics Page

            - 25+ SQL analytical queries

            - Beginner, Intermediate, and Advanced levels

            - Uses JOINs, GROUP BY, CTEs, Window Functions


            #### 🛠️ CRUD Operations Page

            - Add new player records

            - Update existing data

            - Delete records

            - View database entries



            ---
            #### 🧭 How to Navigate

            Use the sidebar menu on the left side of the application to switch between different pages:

            1. Select Live Match to view real-time data


            2. Select Top Player Stats for performance insights


            3. Select SQL Analytics to explore database queries


            4. Select CRUD Operations to manage records


            Each page is designed to provide interactive and user-friendly experience.

            ---
            #### 🚀 Key Features

            - ⚡ Real-time API integration

            - 🗄️ Structured relational database

            - 📊 Advanced SQL analytics

            - 🛠️ Full CRUD functionality

            - 📈 Data-driven cricket insights



            ---
            #### 📌 Project Outcome

            This project demonstrates practical implementation of:

            - API Integration

            - Database Design

            - Advanced SQL Querying

            - Streamlit Web Development

            - Modular Python Programming
                

            🔗Link to project documentation: https://docs.google.com/document/d/1LpjVvTTespcAdsF9gWe2KGQORHTBoBh95MH4hpVGvus/edit?usp=sharing
        """, True)