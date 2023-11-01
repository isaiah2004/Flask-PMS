import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_users_table(conn):
    try:
        query = '''CREATE TABLE Users
                    (StudentID text PRIMARY KEY, 
                    TeacherEmail text, 
                    PasswordHash text NOT NULL);'''
        conn.execute(query)
        print("Table Users created successfully")
    except Error as e:
        print(e)


def create_project_applicants_table(conn):
    try:
        query = '''CREATE TABLE ProjectApplicants
                    (StudentID text, 
                    ProjectID integer, 
                    PRIMARY KEY (StudentID, ProjectID), 
                    FOREIGN KEY (StudentID) REFERENCES Users(StudentID), 
                    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID));'''
        conn.execute(query)
        print("Table ProjectApplicants created successfully")
    except Error as e:
        print(e)
def create_projects_table(conn):
    try:
        query = '''CREATE TABLE Projects
                    (ProjectID integer PRIMARY KEY,
                    Title text NOT NULL,
                    Description text,
                    Timeline text,
                    StdName text,
                    StdRollID text,
                    StdEmail text);'''
        conn.execute(query)
        print("Table Projects created successfully")
    except Error as e:
        print(e)

def create_project_status_table(conn):
    try:
        query = '''CREATE TABLE ProjectStatus
                    (ProjectID integer PRIMARY KEY, 
                    Status text,
                    review_no integer);'''
        conn.execute(query)
        print("Table ProjectApplicants created successfully")
    except Error as e:
        print(e)


rquery ='INSERT INTO ProjectStatus (Status, review_no) VALUES ("PENDING","0");'
conn = create_connection()
cursor = conn.cursor()
query=rquery

# rquery ='DROP TABLE Project_status'
# conn = create_connection()
# cursor = conn.cursor()
# query=rquery

# print(name,Rollno,email,subject,projectTitle,ProjectDesc)
cursor.execute(query)
conn.commit()
conn.close()
# create_project_status_table(conn=con)


