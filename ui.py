import tkinter as tk
from tkinter import messagebox
import csv
import keyloggerTest as kl
import os
import time

selected = None
homepage = True
editpage = False
returnedkeystrokes = None
shortcuts = kl.csvParser('keylogger.csv')
print(shortcuts)


def contentRenderer(shortcuts):
    canvas = tk.Canvas(frmBody, bg="Black", width=300, height=190, highlightbackground="White", highlightthickness=1)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrlbar = tk.Scrollbar(frmBody, orient='vertical', command=canvas.yview)
    scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrlbar.set)
    frmContent = tk.Frame(canvas, bg="Black", width=290, height=50)
    canvas.create_window((0, 0), window=frmContent, anchor=tk.NW)

    for i, shortcut in enumerate(shortcuts):
        keystrokes = shortcut[1]
        commands = shortcut[2]
        date = shortcut[3]
        name = shortcut[4]
        if len(str(keystrokes)) > 25:
            if str(keystrokes)[22] == '.':
                keystrokes = str(keystrokes)[:22] + '..'
            else:
                keystrokes = str(keystrokes)[:22] + '...'
        if len(str(commands)) > 18:
            if str(commands)[15] == '.':
                commands = str(commands)[:15] + '..'
            else:
                commands = str(commands)[:15] + '...'

        if len(str(name)) > 7:
            if str(name)[4] == '.':
                name = str(name)[:4] + '..'
            else:
                name = str(name)[:4] + '...'

        frmContentRow = tk.Frame(frmContent, bg="Black", width=290, height=50, highlightbackground="White", highlightthickness=1)
        frmContentRow.pack(side=tk.TOP, pady=2, padx=5, anchor=tk.W)
        lblName = tk.Label(frmContentRow, text=str(i+1) + ' - ' + name, bg="Black", fg="White", font=("Courier New", 11, 'bold'))
        lblName.place(relx=0.0, rely=0.0)
        lblDate = tk.Label(frmContentRow, text=date, bg="Black", fg="#dddddd", font=("Courier New", 9, 'bold'))
        lblDate.place(relx=0.0, rely=0.5)
        lblKeystrokes = tk.Label(frmContentRow, text=str(keystrokes), bg="Black", fg="White", font=("Courier New", 9))
        lblKeystrokes.place(relx=0.35, rely=0.0)
        lblCommands = tk.Label(frmContentRow, text=commands, bg="Black", fg="White", font=("Courier New", 9))
        lblCommands.place(relx=0.35, rely=0.5)
        bttnSelect = tk.Button(frmContentRow, text="Select", bg="Black", fg="White", font=("Arial", 9), command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: select(i, frmContentRow, frmContent))
        bttnSelect.place(relx=0.84, rely=0.44)

    frmBufferRow = tk.Frame(frmContent, bg="Black", width=290, height=24)
    frmBufferRow.pack(side=tk.TOP, pady=2, padx=5)
    bttnNew = tk.Button(frmBody, width=13, text="New +", bg="Black", fg="White", font=("Arial", 9))
    bttnNew.configure(command=new)
    bttnNew.place(relx=0.005, rely=0.86)

    bttnDelete = tk.Button(frmBody, width=13, text="Delete -", bg="Black", fg="White", font=("Arial", 9))
    bttnDelete.configure(command=delete)
    bttnDelete.place(relx=0.315, rely=0.86)

    bttnEdit = tk.Button(frmBody, width=13, text="Edit %", bg="Black", fg="White", font=("Arial", 9))
    bttnEdit.configure(command=lambda frmContentRow=frmContentRow, frmContent=frmContent: edit(selected, frmContentRow, frmContent))
    bttnEdit.place(relx=0.626, rely=0.86)

    frmContent.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


window = tk.Tk()
icon = tk.PhotoImage(file='shortcutmanagericon.ico')
window.title('Shortcut Manager')
window.geometry('400x300')
window.iconphoto(False, icon)
window.config(bg='Black')

frmTitle = tk.Frame(window, bg="Black", width=400, height=80)
frmTitle.grid(column=0, row=0)

lblTitle = tk.Label(frmTitle, text="Shortcut Manager", font=("Arial", 16), fg="White", bg="Black")
lblTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
lblSubtitle = tk.Label(frmTitle, text="v0.0.3 - Alpha", fg="White", bg="Black")
lblSubtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

frmBody = tk.Frame(window, bg="Black", width=300, height=210, highlightbackground="White", highlightthickness=1)
frmBody.grid(column=0, row=1, padx=50)


def select(i, frmContentRow, frmContent):
    global selected
    for widget in frmContentRow.winfo_children():
        widget.configure(bg="White", fg="Black")
    frmContentRow.configure(bg="White")
    for widget in frmContent.winfo_children():
        if widget != frmContentRow:
            widget.configure(bg="Black")
            for child in widget.winfo_children():
                child.configure(bg="Black", fg="White")
    selected = i
    print(i)


def closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        os.kill(os.getpid(), 9)

def edit(i, frmContentRow, frmContent):
    global homepage
    global editpage
    global selected
    homepage = False
    editpage = True
    #make new window for editing the shortcut
    new_window = tk.Toplevel(window)
    new_window.title("Edit Shortcut")
    new_window.geometry("400x200")
    new_window.config(bg="Black")

    frmEdit = tk.Frame(new_window, bg="Black", width=400, height=200)
    frmEdit.pack()

    lblEditTitle = tk.Label(frmEdit, text="Edit Shortcut", font=("Arial", 14), fg="White", bg="Black")
    lblEditTitle.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    lblEditName = tk.Label(frmEdit, text="Name:", font=("Arial", 12), fg="White", bg="Black")
    lblEditName.place(relx=0.1, rely=0.3)
    lblEditKeystrokes = tk.Label(frmEdit, text="Keystrokes:", font=("Arial", 12), fg="White", bg="Black")
    lblEditKeystrokes.place(relx=0.1, rely=0.42)
    lblEditCommands = tk.Label(frmEdit, text="Commands:", font=("Arial", 12), fg="White", bg="Black")
    lblEditCommands.place(relx=0.1, rely=0.54)
    
    entrEditName = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrEditName.place(relx=0.4, rely=0.3)

    bttnEditKeystrokes = tk.Button(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White', text='Record Keystrokes', command=recordkeystrokes)
    bttnEditKeystrokes.place(relx=0.4, rely=0.42)
    
    entrEditCommands = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrEditCommands.place(relx=0.4, rely=0.59)


    bttnEditSave = tk.Button(frmEdit, text="Save", bg="Black", fg="White", font=("Arial", 12))
    bttnEditSave.place(relx=0.47, rely=0.8, anchor=tk.CENTER)
    bttnEditSave.configure(command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: save(i, frmContentRow, frmContent, entrEditName, returnedkeystrokes, entrEditCommands, new_window))

    bttnEditCancel = tk.Button(frmEdit, text="Cancel", bg="Black", fg="White", font=("Arial", 12))
    bttnEditCancel.place(relx=0.62, rely=0.8, anchor=tk.CENTER)
    bttnEditCancel.configure(command=lambda: cancel(new_window))
    

    

    new_window.mainloop()
    print(i)

def recordkeystrokes():
    global returnedkeystrokes
    kl.startRecording()
    print("Recording started. Please hold shortcut for 5 seconds.")
    time.sleep(4.5)
    shortcut = kl.stopRecording()
    time.sleep(0.5)
    print(f"Captured shortcut: {shortcut}")

def save(i, frmContentRow, frmContent, entrEditName, entrEditKeystrokes, entrEditCommands, new_window):
    global shortcuts
    
    
    #input validation TODO
    
    #update the csv file
    with open('keylogger.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for index, shortcut in enumerate(shortcuts):
            if index == i:
                writer.writerow([index,returnedkeystrokes, entrEditCommands.get(), shortcut[3], entrEditName.get()])
            else:
                
                writer.writerow(shortcut)
    

    shortcuts = kl.csvParser('keylogger.csv')
    refreshcontent()
    cancel(new_window)

def cancel(new_window):
    new_window.destroy()
    global homepage
    global editpage
    homepage = True
    editpage = False

def refreshcontent():
    for widget in frmBody.winfo_children():
        widget.destroy()
    contentRenderer(shortcuts)

def delete():
    global selected
    global shortcuts    
    #update the csv file
    with open('keylogger.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for index, shortcut in enumerate(shortcuts):
            if index != selected:
                
                writer.writerow(shortcut)
            else:
                print(f'deleting {index}')
    

    shortcuts = kl.csvParser('keylogger.csv')

    refreshcontent()

def new():
    global homepage
    global editpage
    homepage = False
    editpage = True
    # make new window for creating a new shortcut
    new_window = tk.Toplevel(window)
    new_window.title("New Shortcut")
    new_window.geometry("400x200")
    new_window.config(bg="Black")

    frmNew = tk.Frame(new_window, bg="Black", width=400, height=200)
    frmNew.pack()

    lblNewTitle = tk.Label(frmNew, text="New Shortcut", font=("Arial", 14), fg="White", bg="Black")
    lblNewTitle.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    lblNewName = tk.Label(frmNew, text="Name:", font=("Arial", 12), fg="White", bg="Black")
    lblNewName.place(relx=0.1, rely=0.3)
    lblNewKeystrokes = tk.Label(frmNew, text="Keystrokes:", font=("Arial", 12), fg="White", bg="Black")
    lblNewKeystrokes.place(relx=0.1, rely=0.42)
    lblNewCommands = tk.Label(frmNew, text="Commands:", font=("Arial", 12), fg="White", bg="Black")
    lblNewCommands.place(relx=0.1, rely=0.54)

    entrNewName = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewName.place(relx=0.4, rely=0.3)
    entrNewKeystrokes = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewKeystrokes.place(relx=0.4, rely=0.42)
    entrNewCommands = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewCommands.place(relx=0.4, rely=0.54)

    bttnNewSave = tk.Button(frmNew, text="Save", bg="Black", fg="White", font=("Arial", 12))
    bttnNewSave.place(relx=0.47, rely=0.8, anchor=tk.CENTER)
    bttnNewSave.configure(command=lambda: saveNew(entrNewName, entrNewKeystrokes, entrNewCommands, new_window))

    bttnNewCancel = tk.Button(frmNew, text="Cancel", bg="Black", fg="White", font=("Arial", 12))
    bttnNewCancel.place(relx=0.62, rely=0.8, anchor=tk.CENTER)
    bttnNewCancel.configure(command=lambda: cancelNew(new_window))

def saveNew(entrNewName, entrNewKeystrokes, entrNewCommands, new_window):
    global shortcuts
    print("Save New")
    print(entrNewName.get())
    print(entrNewKeystrokes.get())
    print(entrNewCommands.get())

    # input validation TODO

    # append the new shortcut to the csv file
    with open('keylogger.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([len(shortcuts)+1, entrNewKeystrokes.get(), entrNewCommands.get(), kl.getToday(), entrNewName.get()])
    shortcuts = kl.csvParser('keylogger.csv')
    refreshcontent()
    cancelNew(new_window)

def cancelNew(new_window):
    new_window.destroy()
    global homepage
    global editpage
    homepage = True
    editpage = False



window.protocol("WM_DELETE_WINDOW", closing)

contentRenderer(shortcuts)

window.mainloop()
