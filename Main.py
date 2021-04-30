from flask import Flask, render_template, request
import pyodbc
import os


app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def home() :
    global myMessage, conn, cursor
    myMessage = ""
    #Open an SQL Connection
    conn = pyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server = 'LAPTOP-M5TC3RQP', database = 'Cars' )

    #Get fastest car data from the database, 1 -initialize, 2 query execution
    cursor = conn.cursor()
    cursor.execute("SELECT id, manufactures, model, speed, year FROM Car WHERE speed = (SELECT MAX(speed) FROM Car)")
    fastest_car = cursor.fetchone()

    #Check which button is the user clicking
    if request.method == 'POST' :
        if request.form['myAction'] == "Create" :
            createObject()
        elif request.form['myAction'] == "Update" :
            updateObject()
        else :
            deleteObject()
    #Get all cars data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * from Car")
    data = cursor.fetchall()

    myPicturePath = os.path.join('static', 'images')

    #display all cars data on the index.html page
    # return '<html><body><h1>Hello World</h1></body></html>'
    return render_template(
        "Index.html",
        title = "This is my Car database",
        fastest_car = "The fastest car is " + fastest_car.manufactures + ", model: " + fastest_car.model + ". An amazing car from year: " + str(fastest_car.year) + ", with the speed of: " + str(fastest_car.speed) + " km/h ",
        all_cars = data, 
        path = myPicturePath,
        message = myMessage)

#Insert new records in the database
def createObject() :
    global myMessage, conn, cursor

    try :
        id = int(request.form['id'])  
        manufactures = request.form['manufactures']    
        model = request.form['model']
        speed = int(request.form['speed'])
        year = int(request.form['year'])
        image = request.form['image']
        cursor.execute("INSERT into Car values (?,?,?,?,?,?)", id, manufactures, model, speed, year, image)
        conn.commit()    
        myMessage = "The car with id:" + id + " was succesfully inserted in the database!"
    except Exception as ex :
        myMessage = "Error in the data, please contact your administrator"

#Update existing record, based on id in the database
def updateObject() :
    global myMessage, conn, cursor

    try :
        id = int(request.form['id'])  
        manufactures = request.form['manufactures']    
        model = request.form['model']
        speed = int(request.form['speed'])
        year = int(request.form['year'])
        image = request.form['image']
        cursor.execute("UPDATE Car SET manufactures = ?, model = ?, speed = ?, year = ?, image = ? WHERE id = ?", manufactures, model, speed, year, image, id)
        conn.commit()
        mymessage = "The car with id:" + id + " was succesfully updated in the database!"
    except Exception as ex :
        myMessage = "Error in the data, please contact your administrator"

#Delete existing record, based on id in the database
def deleteObject() :
    global myMessage, conn, cursor
    myMessage = "Delete button clicked"
    try :
        id = int(request.form['id'])
        cursor.execute("DELETE FROM Car WHERE id = ?", id)
        conn.commit()
        myMessage = "The car with id:" + id + " was succesfully deleted from the database!"
    except Exception as ex :
        myMessage = "Error in the data, please contact your administrator"

#Set localhost
if __name__ == '__main__' :
    app.run('localhost', 4449)