# creating SQL connection
con = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    database = 'database_name',
    password = 'passwprd',
    port = 5432
)

# if you dont remember your port:
# in your database open query tool and type SHOW port;
# it is mostly 5432 by default

cursor = con.cursor()
con.autocommit=True

