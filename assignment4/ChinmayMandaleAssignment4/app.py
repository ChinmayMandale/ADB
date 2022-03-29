import datetime as datetime
from flask import Flask, render_template, request, redirect, url_for
import pyodbc

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
        result = allData()
        return render_template('data.html', result=result)

    if request.method == 'POST':
        magnitude = request.form.get("magnitude")
        range1 = request.form.get("range1")
        range2 = request.form.get("range2")
        top = request.form.get("top")
        typeOfGraph = request.form.get("typeOfGraph")

        if magnitude != None:
            result = []
            result.append(searchByMagnitude(magnitude))
            data = getLineGraph(result[0])
            result.append(data)
            return render_template('data.html', result=result)

        elif range1 != None and range2 != None:
            result = []
            result.append(searchByRange(range1, range2))
            data = getLineGraph(result[0])
            result.append(data)
            return render_template('data.html', result=result)

        elif top != None:
            result = []
            result.append(selectTop100Entries())
            data = getLineGraph(result[0])
            result.append(data)
            return render_template('data.html', result=result)

        elif typeOfGraph != None:
            if typeOfGraph == 'Bar':
                result = []
                result.append(selectTop100Entries())
                data = selectDataForBarChart()
                result.append(data)
                return render_template('data.html', result=result)
            elif typeOfGraph == 'Pie':
                result = []
                result.append(selectTop100Entries())
                data = selectDatForPieChart()
                result.append(data)
                return render_template('data.html', result=result)


def getDepth(data):
    return data.get('depth')


def getLineGraph(data):
    result = []
    for d in data:
        result.append({'depth': d.depth, 'mag': d.mag})
    result.sort(key=getDepth)
    return result


class LineGraphValues:
  def __init__(self, x = '', y = ''):
    self.x = x
    self.y = y


class EQ:
  def __init__(self, time = datetime.datetime.utcnow(), latitude = '', longitude = '', depth = '', mag = '', magType='', nst = '', gap= '', dmin = '', rms = '', net = '', id = '', updated = '', place = '', type = '', horizontalError = '', magError = '', magNst= '', status= '', locationSource = '', magSource = ''):
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
@app.route("/formMagnitude")
def formMagnitude():
    return render_template('formMagnitude.html')


@app.route("/formMagnitudeRange")
def formMagnitudeRange():
    return render_template('formMagnitudeRange.html')


@app.route("/formTopValues")
def formTopValues():
    return render_template('formTopValues.html')

@app.route("/formTypeOfGraph")
def formTypeOfGraph():
    return render_template('formTypeOfGraph.html')

@app.route("/barChart")
def barChart():
    result = []
    result.append(selectTop100Entries())
    data = selectDataForBarChart()
    result.append(data)
    return render_template('barchart.html', result = result)


@app.route("/lineChart")
def lineChart():
    result = []
    result.append(selectTop100Entries())
    data = getLineGraph(result[0])
    result.append(data)
    return render_template('lineChart.html', result=result)

@app.route("/pieChart")
def pieChart():
    return render_template('piechart.html')

# Search All Earthquakes
def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month]""")
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for eq in earthquakes:
        data.append(EQ(eq.time, eq.latitude, eq.longitude, eq.depth, eq.mag, eq.magType, eq.nst, eq.gap, eq.dmin, eq.rms, eq.net, eq.id, eq.updated, eq.place, eq.type, eq.horizontalError, eq.magError, eq.magNst, eq.status, eq.locationSource, eq.magSource))
    return data


# Search Earthquake by Magnitude
def searchByMagnitude(magnitude):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE mag >= ?""", magnitude)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for eq in earthquakes:
        data.append(
            EQ(eq.time, eq.latitude, eq.longitude, eq.depth, eq.mag, eq.magType, eq.nst, eq.gap, eq.dmin, eq.rms,
               eq.net, eq.id, eq.updated, eq.place, eq.type, eq.horizontalError, eq.magError, eq.magNst, eq.status,
               eq.locationSource, eq.magSource))
    return data


# Search Earthquake by Magnitude Range
def searchByRange(range1, range2):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[all_month] WHERE mag >= ? AND mag <= ? """,range1, range2)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for eq in earthquakes:
        data.append(
            EQ(eq.time, eq.latitude, eq.longitude, eq.depth, eq.mag, eq.magType, eq.nst, eq.gap, eq.dmin, eq.rms,
               eq.net, eq.id, eq.updated, eq.place, eq.type, eq.horizontalError, eq.magError, eq.magNst, eq.status,
               eq.locationSource, eq.magSource))
    return data


def selectTop100Entries():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""select top 100 * from [dbo].[all_month] order by time desc""")
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for eq in earthquakes:
        data.append(
            EQ(eq.time, eq.latitude, eq.longitude, eq.depth, eq.mag, eq.magType, eq.nst, eq.gap, eq.dmin, eq.rms,
               eq.net, eq.id, eq.updated, eq.place, eq.type, eq.horizontalError, eq.magError, eq.magNst, eq.status,
               eq.locationSource, eq.magSource))
    return data


def selectDatForPieChart():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    earthquakes = []

    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=0 and mag < 1;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=1 and mag < 2;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=2 and mag < 3;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=3 and mag < 4;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=4 and mag < 5;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=5;""")
    earthquakes.append(cursor.fetchone())

    data = []
    for i in range(0, len(earthquakes)):
        s = str(i) + '-' + str(i + 1)
        data.append({'x': s, 'y': earthquakes[i][0]})
    conn.commit()
    conn.close()
    return data



def selectDataForBarChart():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment4db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    earthquakes = []

    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=0 and mag < 1;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=1 and mag < 2;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=2 and mag < 3;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=3 and mag < 4;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=4 and mag < 5;""")
    earthquakes.append(cursor.fetchone())
    cursor.execute("""SELECT count(*) FROM [dbo].[all_month] WHERE type='earthquake' and mag >=5;""")
    earthquakes.append(cursor.fetchone())

    data = []
    for i in range(0,len(earthquakes)):
        s = str(i) +'-'+str(i+1)
        data.append({'x': s, 'y': earthquakes[i][0]})
    conn.commit()
    conn.close()
    return data



if (__name__ == "__app__"):
    app.run(port=5000)
