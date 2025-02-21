import tkinter as tk 
from tkinter import ttk 
from henryDAO import HenryDAO



class HenrySBA:
  def __init__(self, frame, dao):
    self.frame = frame
    self.authors_list = dao.getAuthorData()
    self.current_author = self.authors_list[0] # Author object currently selected in combobox

    self.wrote_list = dao.getWroteData()
    self.book_list = dao.getBookData()
    
    self.branch_list = dao.getBranchData()
  
    # Adding the author combo box label
    author_lab = ttk.Label(self.frame)
    author_lab.grid(column=3, row=5)
    author_lab['text'] = "Author Selection"

    # Adding the book combo box label
    book_lab = ttk.Label(self.frame)
    book_lab.grid(column=4, row=5)
    book_lab['text'] = "Book Selection"

    # Adding the author combobox
    self.author_combo = ttk.Combobox(self.frame, width=20, state="readonly")
    self.author_combo.grid(column=3, row=6)
    self.author_combo['values'] = self.authors_list # Putting values in the box. Calls __str__ method.
    self.author_combo.current(0) # Setting the first author as the initial value
    self.author_combo.bind("<<ComboboxSelected>>", self.author_selection)  # Bind a callback

    # Adding the books combobox
    self.book_combo = ttk.Combobox(self.frame, width=35, state="readonly")
    self.book_combo.grid(column=4, row=6)
    self.update_books() # Putting values in the box
    self.book_combo.bind("<<ComboboxSelected>>", self.book_selection) # Bind a callback

    # Setting the initial price
    self.price = ttk.Label(self.frame)
    self.price.grid(column=5, row=6)
    self.update_price()

    # Availability tree
    self.av = ttk.Treeview(self.frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
    avlab = ttk.Label(self.frame)
    avlab.grid(column=4, row=1)
    avlab['text'] = "Available Copies"
    self.av.heading('Branch', text='Branch Name')
    self.av.heading('Copies', text='Copies Available')
    self.av.grid(column=4, row=2)
    self.inventory = dao.getInventoryData()
    self.branches = dao.getBranchData()
    self.update_inventory()


  def author_selection(self, event):
    self.current_author = self.authors_list[self.author_combo.current()]
    self.update_books()
    self.update_price()
    self.update_inventory()

  def book_selection(self, event):
    self.update_price()
    self.update_inventory()


  def update_books(self):
    self.current_books = []
    for book in self.wrote_list:
      if (book.author_num == self.current_author.author_num):
        self.current_books.append(book.book_code)
    book_objs = []
    for book in self.book_list:
      if (book.book_code in self.current_books):
        book_objs.append(book)
    self.current_books = book_objs
    
    self.book_combo['values'] = self.current_books # Calls __str__ method.
    self.book_combo.current(0) # Setting the first book as the initial value

  def update_price(self):
    self.price['text'] = "Price: $" + str(self.current_books[self.book_combo.current()].price)

  def update_inventory(self):
    self.av.delete(*self.av.get_children()) # clear previous results
    for book in self.inventory:
      if (book.book_code == self.current_books[self.book_combo.current()].book_code):
        # book is in inventory, now find the name of the branch
        for branch in self.branches:
          if (branch.branch_num == book.branch_num):
            self.av.insert("", "end", values=[branch.branch_name, book.on_hand])



class HenrySBC:
  def __init__(self, frame, dao):
    self.frame = frame
    self.book_list = dao.getBookData()
    
    self.category_list = []
    for book in self.book_list:
      if (book.type not in self.category_list):
        self.category_list.append(book.type)
    
    self.current_category = self.book_list[0].type # Category (type) field currently selected in combobox
    
    self.branch_list = dao.getBranchData()
  
    # Adding the category combo box label
    category_lab = ttk.Label(self.frame)
    category_lab.grid(column=3, row=5)
    category_lab['text'] = "Category Selection"

    # Adding the book combo box label
    book_lab = ttk.Label(self.frame)
    book_lab.grid(column=4, row=5)
    book_lab['text'] = "Book Selection"

    # Adding the category combobox
    self.category_combo = ttk.Combobox(self.frame, width=20, state="readonly")
    self.category_combo.grid(column=3, row=6)
    self.category_combo['values'] = self.category_list # Putting values in the box
    self.category_combo.current(0) # Setting the first category as the initial value
    self.category_combo.bind("<<ComboboxSelected>>", self.category_selection)  # Bind a callback

    # Adding the books combobox
    self.book_combo = ttk.Combobox(self.frame, width=35, state="readonly")
    self.book_combo.grid(column=4, row=6)
    self.update_books() # Putting values in the box
    self.book_combo.bind("<<ComboboxSelected>>", self.book_selection) # Bind a callback

    # Setting the initial price
    self.price = ttk.Label(self.frame)
    self.price.grid(column=5, row=6)
    self.update_price()

    # Availability tree
    self.av = ttk.Treeview(self.frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
    avlab = ttk.Label(self.frame)
    avlab.grid(column=4, row=1)
    avlab['text'] = "Available Copies"
    self.av.heading('Branch', text='Branch Name')
    self.av.heading('Copies', text='Copies Available')
    self.av.grid(column=4, row=2)
    self.inventory = dao.getInventoryData()
    self.branches = dao.getBranchData()
    self.update_inventory()


  def category_selection(self, event):
    self.current_category = self.category_list[self.category_combo.current()]
    self.update_books()
    self.update_price()
    self.update_inventory()

  def book_selection(self, event):
    self.update_price()
    self.update_inventory()


  def update_books(self):
    self.current_books = []
    for book in self.book_list:
      if (book.type == self.current_category):
        self.current_books.append(book)
    
    self.book_combo['values'] = self.current_books # Calls __str__ method.
    self.book_combo.current(0) # Setting the first book as the initial value

  def update_price(self):
    self.price['text'] = "Price: $" + str(self.current_books[self.book_combo.current()].price)

  def update_inventory(self):
    self.av.delete(*self.av.get_children()) # clear previous results
    for book in self.inventory:
      if (book.book_code == self.current_books[self.book_combo.current()].book_code):
        # book is in inventory, now find the name of the branch
        for branch in self.branches:
          if (branch.branch_num == book.branch_num):
            self.av.insert("", "end", values=[branch.branch_name, book.on_hand])



class HenrySBP:
  def __init__(self, frame, dao):
    self.frame = frame
    self.book_list = dao.getBookData()
    
    self.publisher_list = dao.getPublisherData()
    self.current_publisher = self.publisher_list[0] # Publisher object currently selected in combobox
    
    self.branch_list = dao.getBranchData()
  
    # Adding the publisher combo box label
    publisher_lab = ttk.Label(self.frame)
    publisher_lab.grid(column=3, row=5)
    publisher_lab['text'] = "Publisher Selection"

    # Adding the book combo box label
    book_lab = ttk.Label(self.frame)
    book_lab.grid(column=4, row=5)
    book_lab['text'] = "Book Selection"

    # Adding the publisher combobox
    self.publisher_combo = ttk.Combobox(self.frame, width=20, state="readonly")
    self.publisher_combo.grid(column=3, row=6)
    self.publisher_combo['values'] = self.publisher_list # Putting values in the box. Calls __str__ method.
    self.publisher_combo.current(0) # Setting the first publisher as the initial value
    self.publisher_combo.bind("<<ComboboxSelected>>", self.publisher_selection)  # Bind a callback

    # Adding the books combobox
    self.book_combo = ttk.Combobox(self.frame, width=35, state="readonly")
    self.book_combo.grid(column=4, row=6)
    self.update_books() # Putting values in the box
    self.book_combo.bind("<<ComboboxSelected>>", self.book_selection) # Bind a callback

    # Setting the initial price
    self.price = ttk.Label(self.frame)
    self.price.grid(column=5, row=6)
    self.update_price()

    # Availability tree
    self.av = ttk.Treeview(self.frame, columns=('Branch', 'Copies'), show='headings', selectmode="extended")
    avlab = ttk.Label(self.frame)
    avlab.grid(column=4, row=1)
    avlab['text'] = "Available Copies"
    self.av.heading('Branch', text='Branch Name')
    self.av.heading('Copies', text='Copies Available')
    self.av.grid(column=4, row=2)
    self.inventory = dao.getInventoryData()
    self.branches = dao.getBranchData()
    self.update_inventory()


  def publisher_selection(self, event):
    self.current_publisher = self.publisher_list[self.publisher_combo.current()]
    self.update_books()
    self.update_price()
    self.update_inventory()

  def book_selection(self, event):
    self.update_price()
    self.update_inventory()


  def update_books(self):
    self.current_books = []
    for book in self.book_list:
      if (book.publisher_code == self.current_publisher.publisher_code):
        self.current_books.append(book)
    
    self.book_combo['values'] = self.current_books # Calls __str__ method.
    self.book_combo.current(0) # Setting the first book as the initial value

  def update_price(self):
    self.price['text'] = "Price: $" + str(self.current_books[self.book_combo.current()].price)

  def update_inventory(self):
    self.av.delete(*self.av.get_children()) # clear previous results
    for book in self.inventory:
      if (book.book_code == self.current_books[self.book_combo.current()].book_code):
        # book is in inventory, now find the name of the branch
        for branch in self.branches:
          if (branch.branch_num == book.branch_num):
            self.av.insert("", "end", values=[branch.branch_name, book.on_hand])




def main():
  dao = HenryDAO()

  # Making the initial window, adds title, and makes size
  root = tk.Tk()
  root.title('Henry Bookstore')
  root.geometry('900x400')
  # Setting up the tab control
  tabControl = ttk.Notebook(root) # Making a tab control
  tabControl.pack(expand=2, fill="both") # Making the tabs show up
  
  author_tab = HenrySBA(ttk.Frame(tabControl), dao)
  category_tab = HenrySBC(ttk.Frame(tabControl), dao)
  publisher_tab = HenrySBP(ttk.Frame(tabControl), dao)
  tabControl.add(author_tab.frame, text="Search by Author")
  tabControl.add(category_tab.frame, text="Search by Category")
  tabControl.add(publisher_tab.frame, text="Search by Publisher")

  root.mainloop()
  dao.close()

if __name__ == "__main__":
  main()