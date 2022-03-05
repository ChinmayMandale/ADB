from flask import Flask
import pyodbc

app = Flask(__name__)
app.config["DEBUG"] = True

# Link to home page
@app.route('/')
def index():
    allData()
    return "Test"

def allData():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbserver.database.windows.net,1433;Database=quiz2db;Uid=chinmay;Pwd={Chinu@2516};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = conn.cursor()
    cursor.execute("""DECLARE @t1 DATETIME;
        DECLARE @t2 DATETIME;
        SET @t1 = GETDATE();
        
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
    print(earthquakes)


if (__name__ == "__app__"):
    app.run(port=5000)

# SELECT TOP 5 * FROM eq ORDER BY mag DESC
# cursor.execute("""UPDATE csvdemo set Keywords=? where Name=?;""",keywords,name)
# cursor.execute("""UPDATE csvdemo set Salary=? where Name=?;""", salary, name)
# cursor.execute("""UPDATE csvdemo set Picture=? where Name=?;""", filename, name)