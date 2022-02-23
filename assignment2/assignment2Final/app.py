from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import math


app = Flask(__name__)
app.config["DEBUG"] = True

earthRadius = 6371

#Link to home page
@app.route('/')
def index():
    return render_template('index.html')

#Search people by criteria
@app.route("/data", methods=['POST','GET'])
def data():
    if request.method == 'GET':
        result = allData()
        print(result)
        return render_template('data.html', result=result)
    if request.method == 'POST':
        magnitude = request.form.get("magnitude")
        range1 = request.form.get("range1")
        range2 = request.form.get("range2")
        distance = request.form.get("distance")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        startTimeHr = request.form.get("startTimeHr")
        endTimeHr = request.form.get("endTimeHr")

        if magnitude != None:
            result = searchByMagnitude(magnitude)
            print(result)
            return render_template('data.html',result=result)
        elif range1 != None and range2 != None:
            result = searchByRange(range1,range2)
            print(result)
            return render_template('data.html', result=result)
        elif distance != None and latitude != None and longitude != None:
            floatDistance = float(distance)
            floatLatitude = float(latitude)
            floatLongitude = float(longitude)
            result = searchByDistance(floatLatitude, floatLongitude, floatDistance)
            print(result)
            return render_template('data.html', result=result)
        elif startTimeHr != None and endTimeHr != None:
            floatStart = float(startTimeHr)
            floatEnd = float(endTimeHr)
            result = nightTimeData(floatStart, floatEnd)
            print(result)
            return render_template('data.html', result=result)


#Form for search criteria
@app.route("/form")
def form():
    return render_template('form.html')


#Form for search criteria
@app.route("/formDistanceRange")
def formDistanceRange():
    return render_template('formDistanceRange.html')


#Form for search criteria
@app.route("/formMagnitudeRange")
def formMagnitudeRange():
    return render_template('formMagnitudeRange.html')


#Form for search criteria
@app.route("/nightData")
def nightData():
    return render_template('nightData.html')


#Search Earthquake by NightTime
def nightTimeData(startTimeHr, endTimeHr):

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake' AND datepart(hh, time) >= ? OR datepart(hh, time) <= ?""", startTimeHr, endTimeHr)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



#Search Earthquake by NightTime
def searchByDates(startTimeHr, endTimeHr):

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake' AND datepart(hh, time) >= ? OR datepart(hh, time) <= ?""", startTimeHr, endTimeHr)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



#Search All Earthquakes
def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake'""")
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


def radToDegrees(radians):
    return math.degrees(radians)

def degreeToRad(degrees):
    return math.radians(degrees)

#Search Earthquake by Distance
def searchByDistance(latitude, longitude, distance):
    maxLatitude = latitude + radToDegrees(distance/earthRadius)
    minLatitude = latitude - radToDegrees(distance/earthRadius)
    maxLongitude = longitude + radToDegrees( math.asin(distance/earthRadius) / math.cos(degreeToRad(latitude)) )
    minLongitude = longitude - radToDegrees( math.asin(distance/earthRadius) / math.cos(degreeToRad(latitude)) )

    print(maxLatitude)
    print(minLatitude)
    print(maxLongitude)
    print(minLongitude)

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake' AND latitude >= ? AND latitude <= ? AND longitude >= ? AND longitude <= ?""", minLatitude, maxLatitude, minLongitude, maxLongitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


#Search Earthquake by Magnitude
def searchByMagnitude(magnitude):
    print(searchByMagnitude)
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake' AND mag >= ?""", magnitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


#Search Earthquake by Magnitude Range
def searchByRange(range1,range2):
    print(searchByRange)
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE type='earthquake' AND mag >= ? AND mag <= ?""", range1, range2)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



#Show first top x earthquakes
def topXMagnitudeEarthquakes(top):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment2database;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT TOP ? * FROM all_month ORDER BY mag DESC""", top)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


if (__name__ == "__app__"):
    app.run(port = 5000)

# SELECT TOP 5 * FROM all_month ORDER BY mag DESC
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)