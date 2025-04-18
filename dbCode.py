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

def execute_query(query, args=()): # allows for execution of SQL in all functions
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
        if 'Item' not in response: #Check to ensure user is in, should be due to list
            print("This user is not in the database.")
        else:
            table.delete_item( #if in, remove the user from table
                Key={
                'User': name
                }
                )
    except Exception as e: #Try catch
        print("error in deleting user", {str(e)})

def get_all_users(): #Helper function for lists and to ensure no duplication
    response = table.scan()
    return sorted([user["User"] for user in response["Items"]])

def update_user_countries(name, new_countries):
    current = user_read(name)
    # Combine and remove duplicates
    updated = list(set(current + new_countries))
    table.put_item( #input the updated countries to the list
        Item={
            'User': name,
            'CountriesVisited': updated
        }
    )


def user_read(name): # take a username from the list, create a list of countries that they have visited
    country_visit = []
    response = table.scan()
    for user in response["Items"]: #if user is in database, get the list of countries
        if name == user["User"]:
            raw_countries = user.get("CountriesVisited", []) #Added from chatGPT
            country_visit = raw_countries if isinstance(raw_countries, list) else [] #if empty return empty list
    return country_visit #return the list, if empty or not a valid user, will be empty

def get_all_country_names(): #used for allowing the lists to select are populated on webpage
    query = "SELECT Name FROM country ORDER BY Name"
    results = execute_query(query)
    return [row['Name'] for row in results]

