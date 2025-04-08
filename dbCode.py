import pymysql
import pymysql.cursors
import creds
import boto3

# RDS Connection helpers

def get_conn():
    #Establish the connection to RDS database using creds file
    return pymysql.connect(
        host = creds.host,
        user = creds.user,
        password = creds.password,
        database = creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, args=()):
    #Execute SQL query with RDS connection and close connection after, return as dict
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()

def get_most_pop_off_lang():
    #Returns the 20 most popular official languages in the world in descending order
    query = "select Language, count(Language) FROM countrylanguage WHERE IsOfficial LIKE 'T' GROUP BY Language ORDER BY count(Language) DESC LIMIT 20;"
    return execute_query(query)