import mysql.connector
from henryInterfaceClasses import *

class HenryDAO():
  def __init__(self):
    self.db = mysql.connector.connect(
      host='localhost',
      database='henry',
      user='root',
      password='mysql'
    )
    self.cur = self.db.cursor()
  
  def close(self):
    self.db.commit()
    self.db.close()

  def getAuthorData(self):
    sql = "SELECT * FROM henry_author WHERE author_num IN (SELECT author_num FROM HENRY_WROTE) ORDER BY author_last"
    # Ignore authors with no books. Sort by last name.
    self.cur.execute(sql)

    authors = []
    for row in self.cur:
      a = Author(row[0], row[1], row[2])
      authors.append(a)
    return authors

  def getBookData(self):
    sql = "SELECT * FROM henry_book"
    self.cur.execute(sql)

    books = []
    for row in self.cur:
      b = Book(row[0], row[1], row[2], row[3], row[4], row[5])
      books.append(b)
    return books

  def getBranchData(self):
    sql = "SELECT * FROM henry_branch"
    self.cur.execute(sql)

    branches = []
    for row in self.cur:
      b = Branch(row[0], row[1], row[2], row[3])
      branches.append(b)
    return branches

  def getInventoryData(self):
    sql = "SELECT * FROM henry_inventory"
    self.cur.execute(sql)

    inventories = []
    for row in self.cur:
      i = Inventory(row[0], row[1], row[2])
      inventories.append(i)
    return inventories

  def getPublisherData(self):
    sql = "SELECT * FROM henry_publisher WHERE PUBLISHER_CODE IN (SELECT PUBLISHER_CODE FROM henry_book)"
    # Ignore publishers with no books
    self.cur.execute(sql)

    publishers = []
    for row in self.cur:
      p = Publisher(row[0], row[1], row[2])
      publishers.append(p)
    return publishers

  def getWroteData(self):
    sql = "SELECT * FROM henry_wrote"
    self.cur.execute(sql)

    wrotes = []
    for row in self.cur:
      w = Wrote(row[0], row[1], row[2])
      wrotes.append(w)
    return wrotes