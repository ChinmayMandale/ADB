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
        net = request.form.get("net")
        inputGapValue = request.form.get("inputGapValue")
        range1 = request.form.get("range1")
        range2 = request.form.get("range2")
        place = request.form.get("place")
        degrees = request.form.get("degrees")
        latitude = request.form.get("latitude")
        typeValue = request.form.get("typeValue")
        netValue = request.form.get("netValue")
        typeToUpdate = request.form.get("typeToUpdate")
        netToUpdate = request.form.get("netToUpdate")
        placeToUpdate = request.form.get("placeToUpdate")

        if magnitude != None:
            result = searchByMagnitude(magnitude)
            print(result)
            return render_template('data.html',result=result)
        elif range1 != None and range2 != None and place != None:
            result = searchByRange(range1,range2, place)
            print(result)
            return render_template('data.html', result=result)
        elif degrees != None and latitude != None:
            floatLatitude = float(latitude)
            floatDegrees = float(degrees)
            result = searchByDistance(floatLatitude, floatDegrees)
            print(result)
            return render_template('data.html', result=result)
        elif net != None:
            if inputGapValue != '':
                result = updateNetValue(net, inputGapValue)
                return render_template('data.html', result=result)
            else:
                result = searchByNet(net)
                return render_template('data.html', result=result)
        elif netValue != None and typeValue != None:
            result = fetchByNetAndType(netValue, typeValue)
            return render_template('data.html', result=result)
        elif netToUpdate != None and typeToUpdate != None and placeToUpdate != None:
            result = updatePlace(netToUpdate, typeToUpdate, placeToUpdate)
            return render_template('data.html', result=result)
        # elif startTimeHr != None and endTimeHr != None:
        #     floatStart = float(startTimeHr)
        #     floatEnd = float(endTimeHr)
        #     result = nightTimeData(floatStart, floatEnd)
        #     print(result)
        #     return render_template('data.html', result=result)


#Form for search criteria
@app.route("/form")
def form():
    return render_template('form.html')


#Form for search criteria
@app.route("/formLatitudeRange")
def formLatitudeRange():
    return render_template('formLatitudeRange.html')


#Form for search criteria
@app.route("/formMagRangePlace")
def formMagRangePlace():
    return render_template('formMagRangePlace.html')


@app.route("/formNetTypeValue")
def formNetTypeValue():
    return render_template('formNetTypeValue.html')

@app.route("/formUpdateNetTypePlaceValue")
def formUpdateNetTypePlaceValue():
    return render_template('formUpdateNetTypePlaceValue.html')


def updatePlace(net,type,place):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""update [dbo].[eq] set place=? where net=? and type=?""", place,net,type )
    cursor.execute("""SELECT * FROM [dbo].[eq] where net=? and type=?""", net, type)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes

#
# #Form for search criteria
# @app.route("/formMagnitudeRange")
# def formMagnitudeRange():
#     return render_template('formMagnitudeRange.html')

#
# #Form for search criteria
# @app.route("/nightData")
# def nightData():
#     return render_template('nightData.html')
#
#
# #Search Earthquake by NightTime
# def nightTimeData(startTimeHr, endTimeHr):
#
#     conn = pyodbc.connect(
#         'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
#     cursor = conn.cursor()
#     cursor.execute("""SELECT * FROM [dbo].[eq] WHERE type='earthquake' AND datepart(hh, time) >= ? OR datepart(hh, time) <= ?""", startTimeHr, endTimeHr)
#     earthquakes = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return earthquakes


#
# #Search Earthquake by NightTime
# def searchByDates(startDate, endDate):
#
#     conn = pyodbc.connect(
#         'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
#     cursor = conn.cursor()
#     cursor.execute("""SELECT * FROM [dbo].[eq] WHERE type='earthquake' AND datepart(hh, time) >= ? OR datepart(hh, time) <= ?""", startTimeHr, endTimeHr)
#     earthquakes = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return earthquakes



#Search All Earthquakes
def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.executemany("""DECLARE @t1 DATETIME;DECLARE @t2 DATETIME;SET @t1 = GETDATE();
        DECLARE @i int = 0
        WHILE @i < 3
        BEGIN
            SET @i = @i + 1
            SELECT COUNT(*)  FROM [dbo].[eq]
        END;
        
        SET @t2 = GETDATE();
        SELECT DATEDIFF(millisecond,@t1,@t2) AS [elapsed_ms], @t1 as [t1], @t2 as [t2];
    """)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


def radToDegrees(radians):
    return math.degrees(radians)

def degreeToRad(degrees):
    return math.radians(degrees)

#Search Earthquake by Distance
def searchByDistance(latitude, degrees):
    maxLatitude = latitude + degrees
    minLatitude = latitude - degrees

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE latitude >= ? AND latitude <= ?""", minLatitude, maxLatitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


#Search Earthquake by Magnitude
def searchByMagnitude(magnitude):
    print(searchByMagnitude)
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE mag >= ?""", magnitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes

def searchByNet(net):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE net=?""", net)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes

def fetchByNetAndType(netValue, typeValue):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE net=? AND type=?""", netValue, typeValue)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



def updateNetValue(net, value):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    
    cursor.execute("""update [dbo].[eq] set gap = ? where net = ?;""", value, net)
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE net=?""", net)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes



#Search Earthquake by Magnitude Range
def searchByRange(range1,range2, place):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE mag >= ? AND mag <= ? and place like concat('%', ?, '%')""", range1, range2, place)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes

if (__name__ == "__app__"):
    app.run(port = 5000)

# SELECT TOP 5 * FROM eq ORDER BY mag DESC
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)