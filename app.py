import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, make_response


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

@app.route("/")
@app.route('/home', methods=['GET', 'POST'])
def home():
    title = 'Home'
    return render_template('index.html', title=title)

def create_html_table(table1="Projects",table2='ProjectStatus'):
    # Retrieve the data from the database
    data = read_tables(table1)['items']
    data2 = read_tables(table2)['items']
    print(data,data2)
    # Create an HTML table
    table = '<table style="" class="table-dark "id="CTable" border="1"><tr>'
    columns=["ProjectID","Title" ,"Description","Timeline","StdName" ,"StdRollID" ,"StdEmail", 'Status', 'Review-no' ]
    for column in columns:
        table += f'<th>{column}</th>'
    table += '</tr>'
    data3=[row + row2[1:] for row, row2 in zip(data, data2)]
    # print(data3)
    # Loop through the data and add each row to the table
    for row in data3:
        table += '<tr>'
        for value in row:
            table += f'<td>{value}</td>'
        table += '</tr>'

    table += '</table>'
    with open('./table.html', 'w') as f:
        f.write(table)
    # Return the HTML table as a string
    return table

@app.route('/table.html')
def tabler():
    f = open('table.html')
    # print(f.readlines)
    return(f)

@app.route('/projects')
def projects():
    data = create_html_table()
    title = 'Projects'
    return render_template('projects.html',title=title,data=data)


@app.route('/blogs', methods=['GET', 'POST'])
def second():
    title = "Blogs"
    return render_template('blogs.html', title=title)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        ProjectID = request.form
        pid = ProjectID['IdSelect']
        State = ProjectID['State']
        conn = create_connection()
        cursor = conn.cursor()
        query=f"UPDATE ProjectStatus SET Status = '{State}' WHERE ProjectID = {pid}"
        cursor.execute(query)
        conn.commit()
        conn.close()
    create_html_table()
    return render_template('contact.html')


def ProjectAdd(name,Rollno,email,subject,projectTitle,ProjectDesc):
    conn = create_connection()
    cursor = conn.cursor()
    query=f'INSERT INTO Projects (Title, Description, Timeline, StdName, StdRollID, StdEmail) VALUES ("{projectTitle}", "{ProjectDesc}", "{"IA3"}","{name}", "{Rollno}", "{email}")'
    # print(name,Rollno,email,subject,projectTitle,ProjectDesc)
    cursor.execute(query)
    rquery ='INSERT INTO ProjectStatus (Status, review_no) VALUES ("PENDING","0");'
    cursor.execute(rquery)
    conn.commit()
    conn.close()


@app.route('/test', methods=['GET', 'POST'])
def test():
    title = 'Test'
    if request.method == 'POST':
        ProjectID = request.form
        name = ProjectID['name']
        Rollno = ProjectID['Rollno']
        email = ProjectID['email']
        subject = ProjectID['subject']
        projectTitle= ProjectID['Project-title']
        ProjectDesc = ProjectID['ProjectDesc']
        ProjectAdd(name,Rollno,email,subject,projectTitle,ProjectDesc)
    return render_template('test.html', title=title)

@app.route('/read/<string:name>',methods=['GET'])
def read_tables(name):
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    query=f"SELECT * FROM {name}"
    rows=cursor.execute(query)
    item=[]
    # print("live",name, rows)
    if rows:
        for row in rows:
            item.append(row)
            # print("live")
        return {'items':item}
    return {'Message':'The Database is empty'},400

@app.route('/readTables',methods=['GET'])
def show_tables():
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    query="SELECT * FROM sqlite_master where type='table';"
    rows=cursor.execute(query)
    print(rows)
    item=[]
    # return {str(rows)}
    if rows:
        for row in rows:
            item.append({"id":row[0],"table Name":row[1]})
        return {'items':item}
    return {'Message':'The Database is empty'},400

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True)
