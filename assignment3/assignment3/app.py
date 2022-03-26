from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import math
from datetime import datetime, timedelta
from time import time
import redis



myHostname = "chinmayassignment3.redis.cache.windows.net"
myPassword = "8nKUyx2vtIHIEBQCKuEcpKt5bGWRVDSQVAzCaIci4Ys="

r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)


app = Flask(__name__)
app.config["DEBUG"] = True

earthRadius = 6371


# Link to home page
@app.route('/')
def index():
    return render_template('index.html')


# Search people by criteria
@app.route("/data", methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        result = allData()
        return render_template('data.html', result=result)
    if request.method == 'POST':

        n = request.form.get("n")

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
        id1 = request.form.get("id1")
        id2 = request.form.get("id2")
        code = request.form.get("code")
        codeNum = request.form.get("codeNum")

        if magnitude != None:
            result = searchByMagnitude(magnitude)
            print(result)
            return render_template('data.html', result=result)


        elif range1 != None and range2 != None and n != None:
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



class EQ:
  def __init__(self, object, time = '', latitude = '', longitude = '', depth = '', mag = '', magType='', nst = '', gap= '', dmin = '', rms = '', net = '', id = '', updated = '', place = '', type = '', horizontalError = '', magError = '', magNst= '', status= '', locationSource = '', magSource = ''):
    self.object = object
    self.time = time
    self.latitude = latitude
    self.longitude = longitude
    self.depth = depth
    self.mag = mag
    self.magType = magType
    self.nst = nst
    self.gap = gap
    self.dmin = dmin
    self.rms = rms
    self.net = net
    self.id = id
    self.updated = updated
    self.place = place
    self.type = type
    self.horizontalError = horizontalError
    self.magError = magError
    self.magNst = magNst
    self.status = status
    self.locationSource = locationSource
    self.magSource = magSource

# Form for search criteria
@app.route("/form")
def form():
    return render_template('form.html')


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


@app.route("/formUpdateNetTypePlaceValue")
def formUpdateNetTypePlaceValue():
    return render_template('formUpdateNetTypePlaceValue.html')


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


# Search All Earthquakes
def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq]""")
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


def radToDegrees(radians):
    return math.degrees(radians)


def degreeToRad(degrees):
    return math.radians(degrees)


# Search Earthquake by Distance
def searchByDistance(latitude, degrees):
    maxLatitude = latitude + degrees
    minLatitude = latitude - degrees

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE latitude >= ? AND latitude <= ?""", minLatitude, maxLatitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


# Search Earthquake by Magnitude
def searchByMagnitude(magnitude):
    print(searchByMagnitude)
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE net=? AND type=?""", netValue, typeValue)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


def updateNetValue(net, value):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()

    cursor.execute("""update [dbo].[eq] set gap = ? where net = ?;""", value, net)
    cursor.execute("""SELECT * FROM [dbo].[eq] WHERE net=?""", net)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    return earthquakes


# Search Earthquake by Magnitude Range
def question5(range1, range2, n):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    time1 = time()
    for i in range(n):
        cursor.execute("""SELECT * FROM [dbo].[ni] WHERE id >= ? AND id <= ? """,range1, range2)
    names = cursor.fetchall()
    time2 = time()
    t = (time2 - time1)
    conn.commit()
    conn.close()
    smallest = min(names, key=lambda name: name.id)
    largest = max(names, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(names)
    result.append(smallest)
    result.append(largest)
    return result



    # redisResult = r.ping()
    # print("Ping returned : " + str(redisResult))
    #
    # temp = []
    # for e in earthquakes:
    #     temp.append(str(e))
    #
    # r.rpush("key", *temp)
    # test = r.lrange("key", 0, len(temp))
    #
    # res = []
    # for i in range(0, len(temp)):
    #     res.append(test[i].decode('utf-8'))
    # print(res)


def question6a(id1, id2, num):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    time1 = time()
    for i in range(num):
        cursor.execute("""SELECT ni.name, ni.id, di.pwd, di.code FROM ni, di WHERE ni.id = di.id AND ni.id >= ? AND ni.id <= ? """, id1, id2)
    names = cursor.fetchall()
    time2 = time()
    t = (time2 - time1)
    conn.commit()
    conn.close()
    smallest = min(names, key=lambda name: name.id)
    largest = max(names, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(names)
    result.append(smallest)
    result.append(largest)
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
    conn.commit()
    conn.close()
    smallest = min(test, key=lambda name: name.id)
    largest = max(test, key=lambda name: name.id)

    result = []
    result.append(t)
    result.append(test)
    result.append(smallest)
    result.append(largest)
    return result


def cleanString(string):
    return string.decode("utf-8")



if (__name__ == "__app__"):
    app.run(port=5000)

# SELECT TOP 5 * FROM eq ORDER BY mag DESC
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)