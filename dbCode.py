import pymysql
import pymysql.cursors
import creds
import boto3

TABLE_NAME = "projectone"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

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
    query = "select Language, count(Language) AS count FROM countrylanguage WHERE IsOfficial LIKE 'T' GROUP BY Language ORDER BY count(Language) DESC LIMIT 20;"
    return execute_query(query)

def user_add(name, countries):
    # Assume countries is already a list from the form
    table.put_item(
        Item={
            'User': name,
            'CountriesVisited': countries
        }
    )




def user_delete(name):
    try:
        response = table.get_item(Key={"User": name})
        if 'Item' not in response:
            print("This user is not in the database.")
        else:
            table.delete_item(
                Key={
                'User': name
                }
                )
    except Exception as e: #Try catch
        print("error in deleting user", {str(e)})

def get_all_users(): #Helper function
    response = table.scan()
    return sorted([user["User"] for user in response["Items"]])

def update_user_countries(name, new_countries):
    current = user_read(name)
    # Combine and remove duplicates
    updated = list(set(current + new_countries))
    table.put_item(
        Item={
            'User': name,
            'CountriesVisited': updated
        }
    )


def user_read(name):
    country_visit = []
    response = table.scan()
    for user in response["Items"]:
        if name == user["User"]:
            raw_countries = user.get("CountriesVisited", []) #Added from chatGPT
            country_visit = raw_countries if isinstance(raw_countries, list) else []
    return country_visit

def get_all_country_names():
    query = "SELECT Name FROM country ORDER BY Name"
    results = execute_query(query)
    return [row['Name'] for row in results]

