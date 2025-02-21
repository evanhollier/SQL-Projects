import tkinter as tk 
from tkinter import ttk 

def comCallback(event):
    # get will get its value - note that this is always a string
    selIndex = event.widget.current()
    print("Index selected is: " + str(selIndex))


# Main window
root = tk.Tk()
root.title("TKinter Example") 
root.geometry('800x400') 

# Tab control
tabControl = ttk.Notebook(root) 
tab1 = ttk.Frame(tabControl)  # tab1 and tab2 are tab window names
tab2 = ttk.Frame(tabControl) 
tabControl.add(tab1, text ='Blue') # Blue and Red are tab titles
tabControl.add(tab2, text ='Red') 
tabControl.pack(expand = 1, fill ="both") 

# Label
lab1 = ttk.Label(tab1)
lab1.grid(column=1, row=0)
lab1['text'] = "This is a label"

# Combobox
com1 = ttk.Combobox(tab1, width = 20, state="readonly")
com1.grid(column=1, row=2)
myList = ['cat', 'dog', 'fish']
com1['values'] = myList
com1.current(0)
com1.bind("<<ComboboxSelected>>", comCallback)

# Treeview
tree1 = ttk.Treeview(tab2, columns=('Animals', 'Names'), show='headings')
tree1.heading('Animals', text='The Animals')
tree1.heading('Names', text='Their Names')
tree1.grid(column=1, row=1)

for i in tree1.get_children():  # Remove any old values in tree list
    tree1.delete(i)
    
for row in myList:
    tree1.insert("", "end", values=[row, "Name Unknown"])

root.mainloop()   




