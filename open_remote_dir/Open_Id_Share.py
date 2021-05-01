import pyodbc
import prompt
import os, subprocess

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SQL01;DATABASE=Share;UID=sa;PWD=passpass12345')
cursor = cnxn.cursor()

want_id = prompt.string('Enter id(only numbers): ')

cursor.execute("SELECT * FROM [Share].[dbo].[CloudShare]")

for row in cursor.fetchall():
    if str(row[0]) == want_id:
        the_path = str(row[1]) + '\id' + str(row[0])
        subprocess.run(['explorer', os.path.realpath(the_path)]) 
        break
    else:
        the_path = ''

if the_path == '':
    print("Sorry, I didn't find it")
    

      
