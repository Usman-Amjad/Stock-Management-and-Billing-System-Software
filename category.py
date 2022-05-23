# -------Importing Modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+130")
        self.root.title("UA")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===== Variables =====
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # ===== Style =====
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # ====== Title ======
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white").place(x=50,
                                                                                                                y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="light yellow").place(
            x=50, y=170, width=300)

        btn_add = Button(self.root, text="ADD", font=("goudy old style", 15), bg="#4caf50",
                         fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)
        btn_add.bind("<Return>", self.add)
        btn_add.bind("<ButtonRelease-1>", self.add)

        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="red",
                            fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)
        btn_delete.bind("<Return>", self.delete)
        btn_delete.bind("<ButtonRelease-1>", self.delete)

        # ====== Category Details ======
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=390)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.categoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set,
                                          xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid", text="Category ID")
        self.categoryTable.heading("name", text="Name")

        self.categoryTable["show"] = "headings"

        self.categoryTable.column("cid", width=70)
        self.categoryTable.column("name", width=100)

        self.categoryTable.pack(fill=BOTH, expand=1)

        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ========================= Functions ==============================

    def add(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO category(name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                    self.show()
                    self.var_cat_id.set("")
                    self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please Select Category From The List", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Error, Please try Again", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
