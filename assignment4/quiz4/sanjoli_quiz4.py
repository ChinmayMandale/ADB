#Name : Sanjoli Singh, Student ID : 1001843872, Course No : CSE-6331-001, Assignment No : 4
from flask import Flask, render_template, request
import pyodbc
import json
import numpy as np

server = 'myservernew.database.windows.net'
database = 'people'
username = 'serveradmin@myservernew'
password = 'Draconis@1306'   
driver= '{ODBC Driver 17 for SQL Server}'
table_name = "earthquakes"
app = Flask(__name__)
# enable debugging mode
app.config["DEBUG"] = True    

#This method renders the default landing page of the web application
@app.route('/')
def index():
     # Set The HTML template '\templates\index.html'
    return render_template('index.html')

@app.route('/earthquakeRCRange')
def earthquakeRCRange():
    return render_template('earthquakeRCRange.html')

@app.route('/earthquakeCount')
def earthquakeCount():
    return render_template('earthquakeCount.html') 
    

@app.route('/earthquakesOnRSRange', methods=['POST'])
def earthquakesOnRSRange():
    min = float(request.form.get("min"))
    max = float(request.form.get("max"))
    data = []
    step = np.round(np.divide(min+max, 5), 2)
    i = min
    while i < max:
        data.append(getEarthquakesOnRSRange(i,i+step))
        i = i + step
    print(data)
    jsonLst = generateBarChartData(data, min, max)
    return render_template('graph.html', data=jsonLst)

#This method retrieves all earthquakes in user entered magnitude ranges in past one month from database
def getEarthquakesOnRSRange(min,max):
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE mag >= ? and mag < ?"""
            ,min,max)
            row = cursor.fetchone()
    return row

def generatePieData(data, min, max):
    # Set The HTML template '\templates\pie.html'
    lst = []
    step = np.round(np.divide(min+max, 5), 2)
    total = 0
    for row in data:
        total = total + row[0]
    for row in data:
        step = round(step,2)
        last = round(min+step,2)
        instance = {}
        instance['category'] = "Range " + str(min) + "-" + str(last)
        instance['value'] = calculate_percentage(row[0],  total)
        lst.append(instance)
        min = round((min + step),2)
    print(json.dumps(lst))
    return json.dumps(lst)

def generateBarChartData(data, min, max):
    # Set The HTML template '\templates\graph.html'
    step = np.round(np.divide(min+max, 5), 2)
    lst = []
    total = 0
    for row in data:
        total = total + row[0]
    for row in data:
        step = round(step,2)
        last = round(min+step,2)
        instance = {}
        instance['category'] = "Range " + str(min) + "-" + str(last)
        instance['value'] = row[0]
        lst.append(instance)
        min = round((min + step),2)
    print(json.dumps(lst))
    return json.dumps(lst)

@app.route('/pie-chart')
def generatePie():
    # Set The HTML template '\templates\pie.html'
    pie_labels = ['Range 0-1', 'Range 1-2', 'Range 2-3', 'Range 3-4', 'Range > 4']
    data = getEarthquakeCount()
    lst = []
    count = 0
    total = 0
    for row in data:
        total = total + row[0]
    for row in data:
        instance = {}
        instance['category'] = pie_labels[count]
        instance['value'] = calculate_percentage(row[0],  total)
        lst.append(instance)
        count = count + 1
    print(json.dumps(lst))
    return render_template('pie.html', data=json.dumps(lst))

@app.route('/graph-bar')
def generateBarChart():
    # Set The HTML template '\templates\graph.html'
    graph_labels = ['Range 0-1', 'Range 1-2', 'Range 2-3', 'Range 3-4', 'Range > 4']
    data = getEarthquakeCount()
    lst = []
    count = 0
    total = 0
    for row in data:
        total = total + row[0]
    for row in data:
        instance = {}
        instance['category'] = graph_labels[count]
        instance['value'] = row[0]
        lst.append(instance)
        count = count + 1
    print(json.dumps(lst))
    return render_template('graph.html', data=json.dumps(lst))

def sortDepth(val):
    return val['depth']

@app.route('/scatter-plot', methods=['POST','GET'])
def generateScatterPlot():
    # Set The HTML template '\templates\scatterPlot.html'
    if request.form.get("count") is None:
        count = 100
    else:
        count = int(request.form.get("count"))
    data = getCountRecentEarthquakes(count)
    #data = get100RecentEarthquakes()
    lst = []
    for row in data:
        instance = {}
        instance['magnitude'] = row[4]
        instance['depth'] = row[3]
        lst.append(instance)
    lst.sort(key=sortDepth)
    return render_template('scatterPlot.html', data=json.dumps(lst))

@app.route('/line-graph', methods=['POST','GET'])
def generateLineGraph():
    # Set The HTML template '\templates\lineGraph.html'
    if request.form.get("count") is None:
        count = 100
    else:
        count = int(request.form.get("count"))
    data = getCountRecentEarthquakes(count)
    lst = []
    for row in data:
        instance = {}
        instance['magnitude'] = row[4]
        instance['depth'] = row[3]
        lst.append(instance)
    lst.sort(key=sortDepth)
    return render_template('lineGraph.html', data=json.dumps(lst))

def calculate_percentage(val, total):
   percent = np.round((np.divide(val, total) * 100), 2)
   return percent

def getEarthquakeCount():
    rows = []
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE type='earthquake' and mag >=0 and mag < 1;""")
            rows.append(cursor.fetchone())
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE type='earthquake' and mag >=1 and mag < 2;""")
            rows.append(cursor.fetchone())
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE type='earthquake' and mag >=2 and mag < 3;""")
            rows.append(cursor.fetchone())
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE type='earthquake' and mag >=3 and mag < 4;""")
            rows.append(cursor.fetchone())
            cursor.execute(f"""SELECT count(*) FROM [{table_name}] WHERE type='earthquake' and mag >=4;""")
            rows.append(cursor.fetchone())
    print(rows)
    return rows

def get100RecentEarthquakes():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT TOP 100 * FROM [{table_name}] WHERE type='earthquake' and depth > 0 ORDER BY time DESC""")
            rows = cursor.fetchall()
    return rows

def getCountRecentEarthquakes(count):
    query = "SELECT TOP "+str(count)+" * FROM earthquakes WHERE type='earthquake' and depth > 0 ORDER BY time DESC"
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    return rows