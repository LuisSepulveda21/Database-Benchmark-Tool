from django.shortcuts import render
from django.db import connections, transaction
import time
from faker import Faker


ChartData = {'sqliteINS':0,'sqliteDEL':0,'sqliteUPD':0,'sqliteNES':0,
                 'postgreINS':0,'postgreDEL':0,'postgreUPD':0,'postgreNES':0,
                 'mysqlINS':0,'mysqlDEL':0,'mysqlUPD':0,'MysqlNES':0   
            }
GLOBAL_Entry = None

def home(request):
    return render(request, "home.html")



  

    


""" INSERT SCRIPT """
def my_custom_sql(request):
    db_motor = request.GET.get('database')
    cursor = connections[db_motor].cursor()
    average = 0

    if(db_motor == 'sqlite'):
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("BEGIN TRANSACTION") 






    if(request.GET.get('operation') == 'insert'):
        data = []

        for i in range(100):
            data.append(('Juan','Perez','juan.com','M','CO','Barranquilla'))
            data.append(('Maria','Rodriguez','maria.com','F','MX','Monterrey'))

        for i in range(10):
            start = time.time()
            cursor.executemany('''
                INSERT INTO information
                (first_name,last_name,email,gender,country,city) 
                VALUES (%s,%s,%s,%s,%s,%s); 
                ''', data)    
            connections[db_motor].commit()
            end = time.time()
            average = average + (end-start)

        ChartData["{}INS".format(db_motor)] = average/10
  
    '--------------DELETE QUERY----------------------'

    if(request.GET.get('operation') == 'delete'):

        for i in range(10):
            start = time.time()
            cursor.execute('''DELETE FROM information WHERE country LIKE '%CO%' ''')
            cursor.execute('''DELETE FROM information WHERE country LIKE '%MX%' ''')
            connections[db_motor].commit()
            end = time.time()
            average = average + (end-start)

        ChartData["{}DEL".format(db_motor)] = average/10
    
    '--------------UPDATE QUERY----------------------'

    if(request.GET.get('operation') == 'update'):

        for i in range(10):
            start = time.time()
            cursor.execute('''UPDATE information SET country = 'CO' WHERE country LIKE '%CO%' ''')
            connections[db_motor].commit()
            end = time.time() 
            average = average + (end-start)
        
        ChartData["{}UPD".format(db_motor)] = average/10
    
    '--------------NESTED QUERYS----------------------(falta hacer)'

    if(request.GET.get('operation') == 'nested'):

        for i in range(10):

            start = time.time()
            cursor.execute('''SELECT * FROM information WHERE  country LIKE '%ID' ''')
            connections[db_motor].commit()
            end = time.time()
            average = average + (end-start)

        ChartData["{}NES".format(db_motor)] = end-start

    
    
    connections[db_motor].close()
    print('tiempo promedio en realizacion de query = {}s usando la bdd {}'.format(average, db_motor) )
    return render(request, "home.html",ChartData)
