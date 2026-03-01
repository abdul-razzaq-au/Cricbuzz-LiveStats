# Cricbuzz-LiveStats

Real-time cricket analytics dashboard built with Streamlit, REST API, and SQL.
Cricbuzz LiveStats is a real-time cricket analytics dashboard built using Python, SQL, and Streamlit. The application integrates live cricket data from the Cricbuzz API and stores structured match and player data in a
relational database to perform advanced SQL-based analytics. The platform provides real-time match updates, detailed player statistics, SQL-driven analytics, and full CRUD operations for database management.

### Technologies Used
Python (Backend Logic), Streamlit (Web Application Framework), SQL (Database Management), REST API (Live Data Integration), Pandas (Data Processing), Requests (API Handling), Git (Version Control)

### System Architecture

Cricbuzz API → Python (Requests) → SQL Database → Streamlit Dashboard.

Data is fetched from the API, processed using Python, stored in SQL tables, analyzed using queries, and displayed in an interactive dashboard.

### Application Features
- Home Page: Project description and navigation.

- Live Match Page: Displays ongoing matches, scorecards, and venue details.

- Top Player Stats Page: Shows highest runs, best averages, most wickets, etc.

- SQL Analytics Page: Implements analytical SQL queries (Beginner, Intermediate, Advanced).

- CRUD Operations Page: Add, View player records, Update, and Delete.

#### Key Business Use Cases
• Sports Media & Broadcasting
• Fantasy Cricket Platforms
• Cricket Analytics Firms
• Educational Institutions
• Sports Betting & Prediction Analysis

#### Challenges Faced
• Handling nested JSON data from API.
• Designing optimized relational schema.
• Writing complex analytical SQL queries.
• Implementing window functions and performance optimization.

### Set-up Instructions
- Create a new folder to place all files in a same folder.
- Install and Import requirements in each code file mentioned in the requirements.txt file.
- Use your own api keys to fetch data as the keys in the code files are already used and exhausted.
- For SQL analytics you can comment down calling question functions from sqlquery.py file after getting data once. In the uploaded file, these may already be commented down.

## Conclusion
- Cricbuzz LiveStats successfully integrates real-time API data with SQL-based analytics to create a comprehensive cricket dashboard.
- The project demonstrates strong skills in API integration, database design, SQL analytics, Streamlit web development, and modular Python programming.






