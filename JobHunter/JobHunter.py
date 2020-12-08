# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
#CNA 330
#Matthew Williams, mwilliams02@student.rtc.edu
#Worked with Dylan McCormack, Michael Horton, Eric Yevenko
import mysql.connector
import json
import urllib.request
import time

# Connect to database
# You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='jobhunter')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS Jobs_found (id INT PRIMARY KEY auto_increment,
                            Type varchar(10), Title varchar(100), Description TEXT, Job_id varchar(36),
                            Created_at DATE, Company varchar(100), location varchar(50),
                            How_to_apply varchar(1000)); ''')
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, jobdetails):
    ## Add your code here
    type = jobdetails['type']
    title = jobdetails['title']
    description = jobdetails ['description']
    job_id = jobdetails['id']
    created_at = time.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")
    company = jobdetails['company']
    location = jobdetails['location']
    how_to_apply = jobdetails['how_to_apply']
    query = cursor.execute("INSERT INTO jobs(Type, Title,Description, Job_id,Created_at, Company, Location, How_to_apply" ") "
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (type, title, description, job_id, created_at, company, location, how_to_apply))
    return query_sql(cursor, query)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here

    job_id = jobdetails['id']
    query = "SELECT * FROM jobs WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)

def delete_job(cursor, jobdetails):
    ## Add your code here

    job_id = jobdetails['id']
    query = "DELETE FROM jobs WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?search=SQL&location=Remote"
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        pass
    return jsonpage
# Main area of the code.
def jobhunt(arg_dict, cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)

    ## Add your code here to parse the job page
    add_or_delete_job(jobpage, cursor)
def add_or_delete_job(jobpage, cursor):

    # Add your code here to parse the job page
    for jobdetails in jobpage:
        # Add in your code here to check if the player already exists in the DB
        check_if_job_exists(cursor, jobdetails)
        is_job_found = len(cursor.fetchall()) > 0
        ## Add in your code here to notify the user of a new posting
        if is_job_found:
            print("job is found: " + jobdetails["title"] + " from " + jobdetails["company"])
        else:
            print("New job is found: " + jobdetails["title"] + " from " + jobdetails["company"])
            add_new_job(cursor, jobdetails)
    ## EXTRA CREDIT: Add your code to delete old entries

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while (1):
        jobhunt(arg_dict, cursor)
        time.sleep(3600)
        # Sleep for 1h


if __name__ == '__main__':
    main()
