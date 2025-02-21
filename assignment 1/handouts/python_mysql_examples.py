# more python mysql examples

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
               VALUES (%s, %s, %s, %s) """

  records_to_insert = [(4, 'HP Pavilion Power', 1999, '2019-01-11'),
             (5, 'MSI WS75 9TL-496', 5799, '2019-02-27'),
             (6, 'Microsoft Surface', 2330, '2019-07-23')]

  cursor = connection.cursor()
  cursor.executemany(mySql_insert_query, records_to_insert)
  connection.commit()
  print(cursor.rowcount, "Record inserted successfully into Laptop table")

except mysql.connector.Error as error:
  print("Failed to insert record into MySQL table {}".format(error))

finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
#%%

# another example
import mysql.connector

def insert_varibles_into_table(id, name, price, purchase_date):
  try:
    connection = mysql.connector.connect(host='localhost',
                       database='comp3421',
                       user='root',
                       password='mysql')
    cursor = connection.cursor()
    mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
                VALUES (%s, %s, %s, %s) """

    record = (id, name, price, purchase_date)
    cursor.execute(mySql_insert_query, record)
    connection.commit()
    print("Record inserted successfully into Laptop table")

  except mysql.connector.Error as error:
    print("Failed to insert into MySQL table {}".format(error))

  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
      print("MySQL connection is closed")


insert_varibles_into_table(2, 'Area 51M', 6999, '2019-04-14')
insert_varibles_into_table(3, 'MacBook Pro', 2499, '2019-06-20')

#%%

from datetime import datetime

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
              VALUES (%s, %s, %s, %s) """

  cursor = connection.cursor()
  current_Date = datetime.now()
  # convert date in the format you want
  formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
  insert_tuple = (7, 'Acer Predator Triton', 2435, current_Date)

  result = cursor.execute(mySql_insert_query, insert_tuple)
  connection.commit()
  print("Date Record inserted successfully")

except mysql.connector.Error as error:
  connection.rollback()
  print("Failed to insert into MySQL table {}".format(error))

finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
# update

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()

  print("Before updating a record ")
  sql_select_query = """select * from Laptop where id = 2"""
  cursor.execute(sql_select_query)
  record = cursor.fetchone()
  print(record)

   # Update single record now
  sql_update_query = """Update Laptop set Price = 8000 where id = 2"""
  cursor.execute(sql_update_query)
  connection.commit()
  print("Record Updated successfully ")

  print("After updating record ")
  cursor.execute(sql_select_query)
  record = cursor.fetchone()
  print(record)

except mysql.connector.Error as error:
  print("Failed to update table record: {}".format(error))
finally:
  if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")
#%%

# update with variable
import mysql.connector

def update_laptop_price(id, price):
  try:
    connection = mysql.connector.connect(host='localhost',
                       database='comp3421',
                       user='root',
                       password='mysql')

    cursor = connection.cursor()
    sql_update_query = """Update laptop set price = %s where id = %s"""
    input_data = (price, id)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    print("Record Updated successfully ")

  except mysql.connector.Error as error:
    print("Failed to update record to database: {}".format(error))
  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
      print("MySQL connection is closed")

update_laptop_price(7500, 3)
update_laptop_price(5000, 2)

#%%
# update multiple rows

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  cursor = connection.cursor()
  sql_update_query = """Update Laptop set Price = %s where id = %s"""

  # multiple records to be updated in tuple format
  records_to_update = [(3000, 3), (2750, 2)]
  cursor.executemany(sql_update_query, records_to_update)
  connection.commit()

  print(cursor.rowcount, "Records of a laptop table updated successfully")

except mysql.connector.Error as error:
  print("Failed to update records to database: {}".format(error))
finally:
  if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")

#%%
# update multiple columns
import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  cursor = connection.cursor()
  sql_update_query = """Update Laptop set Name = %s, Price = %s where id = %s"""

  name = "HP Pavilion"
  price = 2200
  id = 4
  input = (name, price, id)

  cursor.execute(sql_update_query, input)
  connection.commit()
  print("Multiple columns updated successfully ")

except mysql.connector.Error as error:
  print("Failed to update columns of table: {}".format(error))

finally:
  if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")

#%%
# delete from mysql

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  print("Laptop table before deleting a row")
  sql_select_query = """select * from Laptop where id = 7"""
  cursor.execute(sql_select_query)
  record = cursor.fetchone()
  print(record)

  # Delete a record
  sql_Delete_query = """Delete from Laptop where id = 7"""
  cursor.execute(sql_Delete_query)
  connection.commit()
  print('number of rows deleted', cursor.rowcount)

  # Verify using select query (optional)
  cursor.execute(sql_select_query)
  records = cursor.fetchall()
  if len(records) == 0:
    print("Record Deleted successfully ")

except mysql.connector.Error as error:
  print("Failed to delete record from table: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
# delete with variable

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  sql_Delete_query = """Delete from Laptop where id = %s"""
  # row to delete
  laptopId = 6
  cursor.execute(sql_Delete_query, (laptopId,))
  connection.commit()
  print("Record Deleted successfully ")

except mysql.connector.Error as error:
   print("Failed to Delete record from table: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
# delete multiple rows

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  cursor = connection.cursor()
  sql_Delete_query = """Delete from Laptop where id = %s"""
  records_to_delete = [(6,), (5,)]
  cursor.executemany(sql_Delete_query, records_to_delete)
  connection.commit()
  print(cursor.rowcount, " Record Deleted successfully")

except mysql.connector.Error as error:
  print("Failed to Delete records from MySQL table: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
#################’
# delete all rows
import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  Delete_all_rows = """truncate table Laptop """
  cursor.execute(Delete_all_rows)
  connection.commit()
  print("All Record Deleted successfully ")

except mysql.connector.Error as error:
  print("Failed to Delete all records from database table: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
############### 
# drop table

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  delete_table_query = """DROP TABLE Laptop"""
  cursor.execute(delete_table_query)

  delete_database_query = """DROP DATABASE Electronics"""
  cursor.execute(delete_database_query)
  connection.commit()
  print("Table and Database Deleted successfully ")

except mysql.connector.Error as error:
  print("Failed to Delete table and database: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
    
#%%
# delete column

import mysql.connector

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  alter_column = """ALTER TABLE Laptop DROP COLUMN Purchase_date"""
  cursor.execute(alter_column)
  connection.commit()
  print("Column Deleted successfully ")

except mysql.connector.Error as error:
  print("Failed to Delete column: {}".format(error))
finally:
  if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

#%%
# call mysql stored procedure

import mysql.connector
from mysql.connector import Error

try:
  connection = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')
  cursor = connection.cursor()
  cursor.callproc('add_num', [1,1,1 ])
  # print results
  print("Printing laptop details")
  for result in cursor.stored_results():
    print(result.fetchall())

except mysql.connector.Error as error:
  print("Failed to execute stored procedure: {}".format(error))
finally:
   if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

# how to create a mysql stored procedure
'''
CREATE PROCEDURE add_num(IN num1 INT, IN num2 INT, OUT sum INT)
BEGIN
SET sum := num1 + num2;
END;
To use this proc: 
args = (5, 6, 0) # 0 is to hold value of the OUT parameter sum
cursor.callproc('add_num', args)
'''

#%%
# commit and rollback

import mysql.connector

try:
  conn = mysql.connector.connect(host='localhost',
                     database='comp3421',
                     user='root',
                     password='mysql')

  conn.autocommit = False
  cursor = conn.cursor()
  # withdraw from account A 
  sql_update_query = """Update account_A set balance = 1000 where id = 1"""
  cursor.execute(sql_update_query)

  # Deposit to account B 
  sql_update_query = """Update account_B set balance = 1500 where id = 2"""
  cursor.execute(sql_update_query)
  print("Record Updated successfully ")

  # Commit your changes
  conn.commit()

except mysql.connector.Error as error:
  print("Failed to update record to database rollback: {}".format(error))
  # reverting changes because of exception
  conn.rollback()
finally:
  # closing database connection.
  if conn.is_connected():
    cursor.close()
    conn.close()
    print("connection is closed")
    
#%%
# Mysql blobs
'''
CREATE TABLE `Python_Employee` ( `id` INT NOT NULL , `name` TEXT NOT NULL , `photo` BLOB NOT NULL , `biodata` BLOB NOT NULL , PRIMARY KEY (`id`))
'''

import mysql.connector

def convertToBinaryData(filename):
  # Convert digital data to binary format
  with open(filename, 'rb') as file:
    binaryData = file.read()
  return binaryData


def insertBLOB(emp_id, name, photo, biodataFile):
  print("Inserting BLOB into python_employee table")
  try:
    connection = mysql.connector.connect(host='localhost',
                       database='comp3421',
                       user='root',
                       password='mysql')

    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO python_employee
              (id, name, photo, biodata) VALUES (%s,%s,%s,%s)"""

    empPicture = convertToBinaryData(photo)
    file = convertToBinaryData(biodataFile)

    # Convert data into tuple format
    insert_blob_tuple = (emp_id, name, empPicture, file)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    connection.commit()
    print("Image and file inserted successfully as a BLOB into python_employee table", result)

  except mysql.connector.Error as error:
    print("Failed inserting BLOB data into MySQL table {}".format(error))

  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
      print("MySQL connection is closed")

insertBLOB(1, "Eric", "Statistical analysis cheat sheet.png",
     "DBTest.py")
insertBLOB(2, "Scott", "Liunx_arch.gv.png",
     "Henry.sql")
#%%
# retrieve blob

import mysql.connector


def write_file(data, filename):
  # Convert binary data to proper format and write it on Hard Disk
  with open(filename, 'wb') as file:
    file.write(data)


def readBLOB(emp_id, photo, bioData):
  print("Reading BLOB data from python_employee table")

  try:
    connection = mysql.connector.connect(host='localhost',
                       database='comp3421',
                       user='root',
                       password='mysql')

    cursor = connection.cursor()
    sql_fetch_blob_query = """SELECT * from python_employee where id = %s"""

    cursor.execute(sql_fetch_blob_query, (emp_id,))
    record = cursor.fetchall()
    for row in record:
      print("Id = ", row[0], )
      print("Name = ", row[1])
      image = row[2]
      file = row[3]
      print("Storing employee image and bio-data on disk \n")
      write_file(image, photo)
      write_file(file, bioData)

  except mysql.connector.Error as error:
    print("Failed to read BLOB data from MySQL table {}".format(error))

  finally:
    if connection.is_connected():
      cursor.close()
      connection.close()
      print("MySQL connection is closed")


readBLOB(1, "Statistical analysis cheat sheet.png",
     "DBTest.py")
readBLOB(2, "Liunx_arch.gv.png",
     "Henry.sql")
