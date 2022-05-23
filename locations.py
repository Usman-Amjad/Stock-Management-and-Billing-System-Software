# -------Importing Modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class locationClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+130")
        self.root.title("ASB")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===== Variables =====
        self.var_loc_id = StringVar()
        self.var_name = StringVar()
        self.address = StringVar()

        # ===== Style =====
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # ====== Title ======
        lbl_title = Label(self.root, text="Manage Location", font=("goudy old style", 30), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_name = Label(self.root, text="Name \t             Address", font=("goudy old style", 25),
                         bg="white").place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="light yellow").place(
            x=50, y=160, width=200)
        txtAddress = Entry(self.root, textvariable=self.address, font=("goudy old style", 18), bg="light yellow").place(
            x=290, y=160, width=300)

        btn_add = Button(self.root, text="ADD", font=("goudy old style", 15), bg="#4caf50",
                         fg="white", cursor="hand2")
        btn_add.place(x=280, y=210, width=150, height=30)
        btn_add.bind("<Return>", self.add)
        btn_add.bind("<ButtonRelease-1>", self.add)

        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="red",
                            fg="white", cursor="hand2")
        btn_delete.place(x=440, y=210, width=150, height=30)
        btn_delete.bind("<Return>", self.delete)
        btn_delete.bind("<ButtonRelease-1>", self.delete)

        # ====== Location Details ======
        loc_frame = Frame(self.root, bd=3, relief=RIDGE)
        loc_frame.place(x=700, y=100, width=380, height=390)

        scrolly = Scrollbar(loc_frame, orient=VERTICAL)
        scrollx = Scrollbar(loc_frame, orient=HORIZONTAL)

        self.locationTable = ttk.Treeview(loc_frame, columns=("lid", "name", "address"), yscrollcommand=scrolly.set,
                                          xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.locationTable.xview)
        scrolly.config(command=self.locationTable.yview)

        self.locationTable.heading("lid", text="Location ID")
        self.locationTable.heading("name", text="Name")
        self.locationTable.heading("address", text="Address")

        self.locationTable["show"] = "headings"

        self.locationTable.column("lid", width=70)
        self.locationTable.column("name", width=100)
        self.locationTable.column("address", width=100)

        self.locationTable.pack(fill=BOTH, expand=1)

        self.locationTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ========================= Functions ==============================

    def add(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Location Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM locations WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Location already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO locations(name, address) values(?,?)", (self.var_name.get(), self.address.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Location Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM locations")
            rows = cur.fetchall()
            self.locationTable.delete(*self.locationTable.get_children())
            for row in rows:
                self.locationTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_loc_id.set("")
        self.var_name.set("")
        self.address.set("")

    def get_data(self, ev):
        f = self.locationTable.focus()
        content = (self.locationTable.item(f))
        row = content['values']
        self.var_loc_id.set(row[0])
        self.var_name.set(row[1])
        self.address.set(row[2])

    def delete(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            if self.var_loc_id.get() == "":
                messagebox.showerror("Error", "Please Select Location From The List", parent=self.root)
            else:
                cur.execute("SELECT * FROM locations WHERE lid=?", (self.var_loc_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Error, Please try Again", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM locations WHERE lid=?", (self.var_loc_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Location Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = locationClass(root)
    root.mainloop()
