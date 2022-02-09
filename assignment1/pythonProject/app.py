from flask import Flask, render_template, request, redirect, url_for
import os
import pyodbc
from azure.storage.blob import BlobServiceClient


app = Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def getImageUrl(imageName):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.get_container_properties()
    except Exception as e:
        print(e)
        print("Creating container...")
        container_client = blob_service_client.create_container(container_name)
    blob_client = container_client.get_blob_client(imageName)
    return blob_client.url

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return redirect(url_for('index'))


@app.route("/search", methods=['POST','GET'])
def searchByName():
    if request.method == 'POST':
        name = request.form.get("username")
        if name != '':
            return redirect(f'/userName/{name}')
        salary = request.form.get("salary")
        if salary != '':
            return redirect(f'/userSalary/{salary}')


@app.route("/form")
def form():
    return render_template('form.html')


class Person:
  def __init__(self, Name, State = '', Salary = '', Grade = '', Room = '', Telnum = '', Picture = '', Keywords = '', ImageURL = ''):
    self.Name = Name
    self.State = State
    self.Salary = Salary
    self.Grade = Grade
    self.Room = Room
    self.Telnum = Telnum
    self.Picture = Picture
    self.Keywords = Keywords
    self.ImageURL = ImageURL


@app.route("/allPeople")
def allPeople():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:chinmayadbserver.database.windows.net,1433;Database=assignment1db1;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM people;""")
    data = []
    users = cursor.fetchall()
    conn.commit()
    conn.close()
    for user in users:
        imageUrl = "_"
        if user.Picture != None:
            imageUrl = getImageUrl(user.Picture)
        data.append(Person(user.Name, user.State, user.Salary, user.Grade, user.Room, user.Telnum, user.Picture, user.Keywords, imageUrl))
    return render_template('user.html', data = data)


@app.route("/userSalary/<salary>")
def userSalary(salary):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:chinmayadbserver.database.windows.net,1433;Database=assignment1db1;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM people WHERE salary <= ?""", salary)
    users = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for user in users:
        imageUrl = "_"
        if user.Picture != None:
            imageUrl = getImageUrl(user.Picture)
        data.append(Person(user.Name, user.State, user.Salary, user.Grade, user.Room, user.Telnum, user.Picture, user.Keywords, imageUrl))
    return render_template('user.html', data = data)



@app.route("/userName/<name>")
def userName(name):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:chinmayadbserver.database.windows.net,1433;Database=assignment1db1;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM people WHERE name = ?""", name)
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    data = []
    blob_client = container_client.get_blob_client(user.Picture)
    imageUrl = "_"
    if user.Picture != None:
        imageUrl = getImageUrl(user.Picture)
    data.append(Person(user.Name, user.State, user.Salary, user.Grade, user.Room, user.Telnum, user.Picture, user.Keywords, imageUrl))
    return render_template('user.html', data = data)


@app.route("/upload-photos")
def view_photos():
    blob_items = container_client.list_blobs()
    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"
    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob.name)
        print(blob.name)
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/>".format(
            blob_client.url)
    img_html += "</div>"
    return """
    <head>
    <!-- CSS only -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    </head>
    <body>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
                <h3>Upload new photos</h3>
                <div class="form-group">
                    <form method="post" action="/upload-photos" 
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-control" style="margin-right: 1em;">
                            <input type="submit" class="btn btn-primary">
                        </div>
                    </form>
                </div> 
            </div>
    """ + img_html + "</div></body>"


@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""
    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename,file)
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames")  # ignore duplicate filenames
    return redirect('/upload-photos')


if (__name__ == "__app__"):
    app.run(port = 5000)
#
# cursor.execute("""DELETE FROM csvdemo where Name=?;""", name)
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)