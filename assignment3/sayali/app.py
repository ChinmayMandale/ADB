from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from time import time
import redis



myHostname = "chinmayassignment3.redis.cache.windows.net"
myPassword = "8nKUyx2vtIHIEBQCKuEcpKt5bGWRVDSQVAzCaIci4Ys="

r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)


app = Flask(__name__)
app.config["DEBUG"] = True


# Link to home page
@app.route('/')
def index():
    return render_template('index.html')


# Search people by criteria
@app.route("/data", methods=['POST', 'GET'])
def data():
    if request.method == 'GET':

        return "Post Method"
    if request.method == 'POST':

        n = request.form.get("n")

        range1 = request.form.get("range1")
        range2 = request.form.get("range2")

        id1 = request.form.get("id1")
        id2 = request.form.get("id2")
        code = request.form.get("code")
        codeNum = request.form.get("codeNum")

        if range1 != None and range2 != None and n != None:
            num = int(n)
            result = searchByRange(range1, range2, num)
            return render_template('data.html', result=result)

        elif id1 != None and id2 != None and n != None:
            num = int(n)
            result = joinOnID(id1, id2, num)
            return render_template('data.html', result=result)

        elif code != None and codeNum != None and n != None:
            num = int(n)
            result = question6b(code, codeNum, num)
            return render_template('data.html', result=result)



# Form for search criteria
@app.route("/formLatitudeRange")
def formLatitudeRange():
    return render_template('formLatitudeRange.html')


# Form for search criteria
@app.route("/formMagRangePlace")
def formMagRangePlace():
    return render_template('formMagRangePlace.html')


@app.route("/formNetTypeValue")
def formNetTypeValue():
    return render_template('formNetTypeValue.html')



def updatePlace(net, type, place):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""update [dbo].[eq] set place=? where net=? and type=?""", place, net, type)
    cursor.execute("""SELECT * FROM [dbo].[eq] where net=? and type=?""", net, type)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



# Search Earthquake by Magnitude Range
def searchByRange(range1, range2, n):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    time1 = time()
    for i in range(n):
        cursor.execute("""SELECT * FROM [dbo].[ni] WHERE id >= ? AND id <= ? """,range1, range2)
    names = cursor.fetchall()
    time2 = time()
    t = (time2 - time1)
    print(t)
    conn.commit()
    conn.close()
    smallest = min(names, key=lambda name: name.id)
    largest = max(names, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(names)
    result.append(smallest)
    result.append(largest)
    print(smallest)
    print(largest)
    return result


def joinOnID(id1, id2, num):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    time1 = time()
    for i in range(num):
        cursor.execute("""SELECT ni.name, ni.id, di.pwd, di.code FROM ni, di WHERE ni.id = di.id AND ni.id >= ? AND ni.id <= ? """, id1, id2)
    names = cursor.fetchall()
    time2 = time()
    t = (time2 - time1)
    print(t)
    conn.commit()
    conn.close()

    smallest = min(names, key=lambda name: name.id)
    largest = max(names, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(names)
    result.append(smallest)
    result.append(largest)
    print(smallest)
    print(largest)
    return result


def question6b(code, codeNum, num):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    time1 = time()
    for i in range(num):
        cursor.execute("""SELECT ni.name, ni.id, di.pwd, di.code FROM ni, di WHERE ni.id = di.id AND di.code = ? """, code)
    names = cursor.fetchall()
    number = int(codeNum)
    test = names[0: number]
    time2 = time()
    t = (time2 - time1)
    print(t)
    conn.commit()
    conn.close()


    smallest = min(test, key=lambda name: name.id)
    largest = max(test, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(test)
    result.append(smallest)
    result.append(largest)
    print(smallest)
    print(largest)
    return result


def cleanString(string):
    return string.decode("utf-8")



if (__name__ == "__app__"):
    app.run(port=5000)

# SELECT TOP 5 * FROM eq ORDER BY mag DESC
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)