class Author:
  def __init__(self, author_num, author_last, author_first):
    self.author_num = author_num
    self.author_last = author_last
    self.author_first = author_first
  
  def __str__(self):
    return f"{self.author_first} {self.author_last}"

class Book:
  def __init__(self, book_code, title, publisher_code, type, price, paperback):
    self.book_code = book_code
    self.title = title
    self.publisher_code = publisher_code
    self.type = type
    self.price = price
    self.paperback = paperback
  
  def __str__(self):
    return f"{self.title}"

class Branch:
  def __init__(self, branch_num, branch_name, branch_location, num_employees):
    self.branch_num = branch_num
    self.branch_name = branch_name
    self.branch_location = branch_location
    self.num_employees = num_employees
  
  def __str__(self):
    return f"{self.branch_name}"

class Inventory:
  def __init__(self, book_code, branch_num, on_hand):
    self.book_code = book_code
    self.branch_num = branch_num
    self.on_hand = on_hand

class Publisher:
  def __init__(self, publisher_code, publisher_name, city):
    self.publisher_code = publisher_code
    self.publisher_name = publisher_name
    self.city = city
  
  def __str__(self):
    return f"{self.publisher_name}"

class Wrote:
  def __init__(self, book_code, author_num, sequence):
    self.book_code = book_code
    self.author_num = author_num
    self.sequence = sequence