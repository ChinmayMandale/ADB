import datetime as datetime
from flask import Flask, render_template, request, redirect, url_for
import pyodbc

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
        magnitude = request.form.get("magnitude")

        # low = int(request.form.get("low"))
        # high = int(request.form.get("high"))
        # n = int(request.form.get("n"))

        LOWQ7 = int(request.form.get("LOWQ7"))
        HIGHQ7 = int(request.form.get("HIGHQ7"))

        if LOWQ7 != None and HIGHQ7 != None:

            data = selectTop(LOWQ7, HIGHQ7)
            result = getLineGraph(data)

            return render_template('lineChart.html', result=result)

        # elif low != None and high != None and n != None:
        #     result = searchByRange(low, high, n)
        #     return render_template('barchart.html', result=result)
        # #
        # elif top != None:
        #     result = []
        #     result.append(selectTop())
        #     data = getLineGraph(result[0])
        #     result.append(data)
        #     return render_template('data.html', result=result)
        #
        # elif typeOfGraph != None:
        #     if typeOfGraph == 'Bar':
        #         result = []
        #         result.append(selectTop())
        #         data = selectDataForBarChart()
        #         result.append(data)
        #         return render_template('data.html', result=result)


def getDepth(data):
    return data.get('column3')

def getColumn2(data):
    return data.get(data[1])


def getLineGraph(data):
    result = []
    for d in data:
        result.append({'depth': d.column3, 'mag': d.column1*d.column2})
    # result.sort(key=getDepth)
    print(result)
    return result


def getMagnitudeQuantity(data):
    result = []
    for d in data:
        if d.mag > 0 and d.mag <=1:
            result.append(BarGraphValues())
        elif d.mag > 1 and d.mag <= 2:
                result.two = result.two + 1
        elif d.mag > 2 and d.mag <= 3:
                result.three = result.three + 1
        elif d.mag > 3 and d.mag <= 4:
                result.four = result.four + 1
        elif d.mag > 4 and d.mag <= 5:
                result.five = result.five + 1
        elif d.mag > 5 and d.mag <= 6:
                result.six = result.six + 1
        elif d.mag > 6 and d.mag <= 7:
                result.seven = result.seven + 1
        else:
            result.eight = result.eight + 1
    return result


class BarGraphValues:
  def __init__(self, one = 0, two = 0, three = 0, four = 0, five = 0, six = 0, seven = 0, eight = 0):
      self.one = one
      self.two = two
      self.three = three
      self.four = four
      self.five = five
      self.six = six
      self.seven = seven
      self.eight = eight

class LineGraphValues:
  def __init__(self, x = '', y = ''):
    self.x = x
    self.y = y


class EQ:
  def __init__(self, column1 = '', column2 = '', column3 = ''):
    self.column1 = column1
    self.column2 = column2
    self.column3 = column3

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
    result.append(selectTop())
    data = selectDataForBarChart()
    result.append(data)
    return render_template('barchart.html', result = result)


@app.route("/lineChart")
def lineChart():
    result = []
    result.append(selectTop())
    data = getLineGraph(result[0])
    result.append(data)
    return render_template('lineChart.html', result=result)

@app.route("/pieChart")
def pieChart():
    return render_template('piechart.html')

# Search All Earthquakes
def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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
def searchByRange(low, high, n):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM [dbo].[data-1] WHERE column2 >= ? AND column2 <= ? """,low, high)
    result = cursor.fetchall()
    conn.commit()
    conn.close()

    res = []
    for eq in result:
        res.append(
            EQ(eq.column1, eq.column2, eq.column3))

    data = []
    ran = (high - low) / (n);

    for i in range(1, n):
        s = str(low + (i-1)*ran) + '-' +str(low + i*ran)
        data.append({'x': s, 'y': n})
    print(result)
    print(data)
    return data


def selectTop(low, high):
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""select top 100 * from [dbo].[data-1] where column3 >= ? and column3 <= ?""", low, high)
    earthquakes = cursor.fetchall()
    conn.commit()
    conn.close()
    data = []
    for eq in earthquakes:
        data.append(EQ(eq.column1, eq.column2, eq.column3))

    return data


def selectDataForBarChart():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=assignment3db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
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
    print(data)
    conn.commit()
    conn.close()

    return data




if (__name__ == "__app__"):
    app.run(port=5000)
