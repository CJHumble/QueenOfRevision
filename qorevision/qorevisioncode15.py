from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import ttk

root = Tk()
abspath = /
ico = abspath +"qorevision/db/straw2.ico"
root.title("Queen of Revision")
root.iconbitmap(ico)
root.configure(background="#a09dbf")
dbs = abspath +'qorevision/db/Revision.db'

editing_frame = LabelFrame(root, text="Deleting and Editing", padx=10, pady=10, width=450, bg="#a09dbf")
editing_frame.grid(row=10, column=0, padx=2, pady=2)
entry_frame = LabelFrame(root, text="Add Entries", padx=20, pady=10, width=450, bg="#a09dbf")
entry_frame.grid(row=0, column=0, padx=2, pady=2)
search_frame = LabelFrame(root, text="Search", padx=13, pady=10, width=450, bg="#a09dbf")
search_frame.grid(row=7, column=0, padx=2, pady=2)
conn = sqlite3.connect('revision.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS acronyms (
   acronym text,
    longform text,
    definition text,
    moduleno text,
    notes text,
    contentlink text,
    images text
    )""")


# update func
def savechanges():

    conn = sqlite3.connect(dbs)
    c = conn.cursor()

    record_id = select_box.get()

    c.execute("""UPDATE acronyms SET
        acronym = :acronym,
        longform = :longform,
        definition = :definition,
        moduleno = :moduleno,
        notes = :notes,
        contentlink = :contentlink,
        images= :images


        WHERE oid = :oid""",
              {'acronym': acronym_edit.get(),
               'longform': longform_edit.get(),
               'definition': definition_edit.get(),
               'moduleno': moduleno_edit.get(),
               'notes': notes_edit.get(),
               'contentlink': contentlink_edit.get(),
               'images': images_edit.get(),
               'oid': record_id
               })

    conn.commit()
    conn.close()
    editor.destroy()


def update():
    global editor
    editor = Tk()
    editor.title("Edit Entry")
    editor.iconbitmap(ico)
    editor.geometry("400x200")
    editor.configure(background="#a09dbf")

    conn = sqlite3.connect(ico)
    c = conn.cursor()

    record_id = select_box.get()
    c.execute("SELECT * FROM acronyms WHERE oid =" + record_id)
    records = c.fetchall()

    # create global var for txt box names
    global acronym_edit
    global longform_edit
    global definition_edit
    global moduleno_edit
    global notes_edit
    global contentlink_edit
    global images_edit

    # create text boxes
    acronym_edit = Entry(editor, width=30)
    acronym_edit.grid(row=0, column=1, padx=20, pady=(10, 0))
    longform_edit = Entry(editor, width=30)
    longform_edit.grid(row=1, column=1)
    definition_edit = Entry(editor, width=30)
    definition_edit.grid(row=2, column=1)
    moduleno_edit = Entry(editor, width=30)
    moduleno_edit.grid(row=3, column=1)
    notes_edit = Entry(editor, width=30)
    notes_edit.grid(row=4, column=1)
    contentlink_edit = Entry(editor, width=30)
    contentlink_edit.grid(row=5, column=1)
    images_edit = Entry(editor, width=30)
    images_edit.grid(row=6, column=1)

    # create text box labels

    acronym_edit_label = Label(editor, text="Acronym", bg="#a09dbf")
    acronym_edit_label.grid(row=0, column=0, pady=(10, 0))
    longform_edit_label = Label(editor, text="Meaning", bg="#a09dbf")
    longform_edit_label.grid(row=1, column=0)
    definition_edit_label = Label(editor, text="Definition", bg="#a09dbf")
    definition_edit_label.grid(row=2, column=0)
    moduleno_edit_label = Label(editor, text="Module", bg="#a09dbf")
    moduleno_edit_label.grid(row=3, column=0)
    notes_edit_label = Label(editor, text="Notes", bg="#a09dbf")
    notes_edit_label.grid(row=4, column=0)
    contentlink_edit_label = Label(editor, text="Content Link", bg="#a09dbf")
    contentlink_edit_label.grid(row=5, column=0)
    images_edit_label = Label(editor, text="Images", bg="#a09dbf")
    images_edit_label.grid(row=6, column=0)

    for record in records:
        acronym_edit.insert(0, record[0])
        longform_edit.insert(0, record[1])
        definition_edit.insert(0, record[2])
        moduleno_edit.insert(0, record[3])
        notes_edit.insert(0, record[4])
        contentlink_edit.insert(0, record[5])
        images_edit.insert(0, record[6])

    submit_button = Button(editor, text="Save Changes", command=savechanges, bg="#c1d9d2")
    submit_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# del func creation
def delete():
    conn = sqlite3.connect(dbs)
    c = conn.cursor()

    # del rec
    c.execute("DELETE from acronyms WHERE oid=" + select_box.get())

    conn.commit()
    conn.close()


# create submit func
def submit():
    conn = sqlite3.connect(dbs)
    c = conn.cursor()

    # insert into table
    c.execute(
        "INSERT INTO acronyms VALUES (:acronym, :longform, :definition, :moduleno, :notes, :contentlink, :images)",
        {
            'acronym': acronym.get(),
            'longform': longform.get(),
            'definition': definition.get(),
            'moduleno': moduleno.get(),
            'notes': notes.get(),
            'contentlink': contentlink.get(),
            'images': images.get()
        })

    conn.commit()
    conn.close()

    # clear the text boxes
    acronym.delete(0, END)
    longform.delete(0, END)
    definition.delete(0, END)
    moduleno.delete(0, END)
    notes.delete(0, END)
    contentlink.delete(0, END)
    images.delete(0, END)


# search specific
def search_data():
    global result
    results = Toplevel()
    results.title("Search Results")
    results.iconbitmap(ico)
    results.configure(background="#a09dbf")
    results.geometry("1200x800")

    main_frame = Frame(results, bg="#a09dbf")
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set, background="#a09dbf")
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    result = Frame(my_canvas, bg="#a09dbf")
    my_canvas.create_window((0, 0), window=result, anchor="nw")

    conn = sqlite3.connect(dbs)
    c = conn.cursor()

    c.execute("SELECT *, oid FROM acronyms WHERE acronym LIKE ?", ('%' + str(search_box.get()) + '%',))
    records = c.fetchall()

    for record in records:
        global diagram
        global imagelink
        imagelink = str(record[6])
        special_frame = LabelFrame(result, text=str(record[0]) + " - From Module " + str(record[3]), padx=10, pady=10,
                                   font=30, width=800, height=200, bg="#a09dbf")
        special_frame.grid(column=0, padx=10, pady=10, sticky=W + E)

        special_label = Label(special_frame, text=str(record[1]) + "\n\n" + str(record[2]) + "\n", font=20,
                              wraplength=500, justify="left", bg="#a09dbf")
        special_label.grid(row=0, column=0, sticky=W)

        if "D:" in imagelink:
            diagram = ImageTk.PhotoImage(Image.open(imagelink))
            diagram_label = Label(special_frame, image=diagram)
            diagram_label.grid(row=1, column=0)

    # diagramlabel = Label(special_frame, image=diagram)
    # diagramlabel.grid(row=1, column=0, sticky=W)

    # query_labelid = Label(result, text=print_recordsid)
    # query_labelid.grid(row=15, column=0)
    # query_labelname = Label(result, text=print_recordsname)
    # query_labelname.grid(row=15, column=1)

    conn.commit()
    conn.close()


# query func
def showall():
    global allresults
    allresults = Tk()
    allresults.title("All Entries")
    allresults.iconbitmap(ico)
    allresults.configure(background="#a09dbf")

    conn = sqlite3.connect(dbs)
    c = conn.cursor()

    c.execute("SELECT *, oid FROM acronyms")
    records = c.fetchall()
    results_titleid = Label(allresults, text="ID", bg="#a09dbf")
    results_titleid.grid(row=12, column=0)
    results_titlename = Label(allresults, text="Name", bg="#a09dbf")
    results_titlename.grid(row=12, column=1)
    print_recordsid = ""
    print_recordsname = ""
    for record in records:
        print_recordsid += str(record[7]) + "\n"
        print_recordsname += str(record[0]) + "\n"

    query_labelid = Label(allresults, text=print_recordsid, bg="#a09dbf")
    query_labelid.grid(row=15, column=0)
    query_labelname = Label(allresults, text=print_recordsname, bg="#a09dbf")
    query_labelname.grid(row=15, column=1)

    conn.commit()
    conn.close()


# create text boxes
acronym = Entry(entry_frame, width=30)
acronym.grid(row=1, column=1, pady=(10, 0))
longform = Entry(entry_frame, width=30)
longform.grid(row=2, column=1)
definition = Entry(entry_frame, width=30)
definition.grid(row=3, column=1)
moduleno = Entry(entry_frame, width=30)
moduleno.grid(row=4, column=1)
notes = Entry(entry_frame, width=30)
notes.grid(row=5, column=1)
contentlink = Entry(entry_frame, width=30)
contentlink.grid(row=6, column=1)
images = Entry(entry_frame, width=30)
images.grid(row=7, column=1)

search_box = Entry(search_frame, width=50)
search_box.grid(row=8, column=0)
select_box = Entry(editing_frame, width=30)
select_box.grid(row=11, column=1)

# create text box labels

acronym_label = Label(entry_frame, text="Acronym", bg="#a09dbf")
acronym_label.grid(row=1, column=0, pady=(10, 0))
longform_label = Label(entry_frame, text="Meaning", bg="#a09dbf")
longform_label.grid(row=2, column=0)
definition_label = Label(entry_frame, text="Definition", bg="#a09dbf")
definition_label.grid(row=3, column=0)
moduleno_label = Label(entry_frame, text="Module", bg="#a09dbf")
moduleno_label.grid(row=4, column=0)
notes_label = Label(entry_frame, text="Notes", bg="#a09dbf")
notes_label.grid(row=5, column=0)
contentlink_label = Label(entry_frame, text="Course Content", bg="#a09dbf")
contentlink_label.grid(row=6, column=0)
images_label = Label(entry_frame, text="Images", bg="#a09dbf")
images_label.grid(row=7, column=0)

select_box_label = Label(editing_frame, text="Select ID", bg="#a09dbf")
select_box_label.grid(row=11, column=0)

# submit button
submit_button = Button(entry_frame, text="Add Record to Database", command=submit, bg="#c1d9d2")
submit_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# specific acronym search
search_button = Button(search_frame, text="Search", command=search_data, bg="#c1d9d2")
search_button.grid(row=8, column=1, pady=1, padx=1, ipadx=10)
# all records button
query_btn = Button(search_frame, text="All Contents Index", command=showall, bg="#c1d9d2")
query_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=107)

# del button
delete_btn = Button(editing_frame, text="Delete Record", command=delete, bg="#c1d9d2")
delete_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# update button
update_btn = Button(editing_frame, text="Edit Record", command=update, bg="#c1d9d2")
update_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

conn.commit()
conn.close()

root.mainloop()
