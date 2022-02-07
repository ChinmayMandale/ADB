from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import pyodbc
from azure.storage.blob import BlobServiceClient


app = Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:chinmayadbserver.database.windows.net,1433;Database=assignment1db1;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()

connect_str = 'DefaultEndpointsProtocol=https;AccountName=chinmaystorageaccount;AccountKey=7B2eUPyikZVLzGP5EdlpaRQV4IG1dckKbG/4q3gnNFPnLs78yvLkpt77BctLUUwwwH++yIJuD/WW1lBOoqK4Dw==;EndpointSuffix=core.windows.net'
container_name = "assignment1container"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
try:
    container_client = blob_service_client.get_container_client(container_name)
    container_client.get_container_properties()
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        parseCSV(file_path) # save the file
    return redirect(url_for('index'))


@app.route("/user/<name>")
def user(name):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:chinmayadbserver.database.windows.net,1433;Database=assignment1db1;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM people WHERE name = ?""", name)
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    data = []
    data.append(user)
    blob_client = container_client.get_blob_client(user.Picture)
    img_html = blob_client.url  # get the blob url and append it to the html
    data.append(img_html)
    return render_template('user.html', data = data)


def parseCSV(filePath):
    csvData = pd.read_csv(filePath, index_col=False)
    csvData.head()
    # df = pd.DataFrame(csvData)
    # cursor.execute("drop table if exists people;")
    # cursor.execute('''CREATE TABLE people
    # (Name nvarchar(50) primary key,
    # State nvarchar(50),
    # Salary nvarchar(50),
    # Grade nvarchar(50),
    # Room nvarchar(50),
    # Telnum nvarchar(50),
    # Picture nvarchar(50),
    # Keywords nvarchar(50))''')
    #
    # for index, row in csvData.interrows():
    #     cursor.executemany('''
    #     INSERT INTO people (Name, State, Salary, Grade, Room, Telnum, Picture, Keywords) VALUES (?,?,?,?,?,?,?,?)
    #     ''',row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
    conn.commit()
    conn.close()


if (__name__ == "__app__"):
    app.run(port = 5000)
