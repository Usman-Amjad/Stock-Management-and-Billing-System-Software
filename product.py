# -------Importing Modules
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+130")
        self.root.title("UA")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===== Style =====
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # ================== Variables ======================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_loc = StringVar()

        self.cat_list = []  # List Variable
        self.loc_list = []  # List Variable
        self.fetch_cat_loc()  # Calling Function

        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # ==============================================================
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # ====== Title ======
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d",
                      fg="white").pack(side=TOP, fill=X)

        # ====== Column 1 ======
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=60)
        lbl_location = Label(product_Frame, text="Location", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=210)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=260)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white") \
            .place(x=30, y=310)

        # ====== Column 2 ======
        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,
                               values=self.cat_list, state='readonly', justify=CENTER,
                               font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        cmb_loc = ttk.Combobox(product_Frame, textvariable=self.var_loc,
                               values=self.loc_list, state='readonly', justify=CENTER,
                               font=("goudy old style", 15))
        cmb_loc.place(x=150, y=110, width=200)
        cmb_loc.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name,
                         font=("goudy old style", 15), bg="light yellow").place(x=150, y=160, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price,
                          font=("goudy old style", 15), bg="light yellow").place(x=150, y=210, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty,
                        font=("goudy old style", 15), bg="light yellow").place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status,
                                  values=("Active", "Inactive"), state='readonly', justify=CENTER,
                                  font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # ====== Buttons ======
        btn_add = Button(product_Frame, text="Save", font=("goudy old style", 15), bg="#2196f3",
                         fg="white", cursor="hand2")
        btn_add.place(x=10, y=400, width=100, height=40)
        btn_add.bind("<Return>", self.add)
        btn_add.bind("<ButtonRelease-1>", self.add)

        btn_update = Button(product_Frame, text="Update", font=("goudy old style", 15),
                            bg="#4caf50",
                            fg="white",
                            cursor="hand2")
        btn_update.place(x=120, y=400, width=100, height=40)
        btn_update.bind("<Return>", self.update)
        btn_update.bind("<ButtonRelease-1>", self.update)

        btn_delete = Button(product_Frame, text="Delete", font=("goudy old style", 15),
                            bg="#f44336",
                            fg="white",
                            cursor="hand2")
        btn_delete.place(x=230, y=400, width=100, height=40)
        btn_delete.bind("<Return>", self.delete)
        btn_delete.bind("<ButtonRelease-1>", self.delete)

        btn_clear = Button(product_Frame, text="Clear", font=("goudy old style", 15), bg="#607d8b",
                           fg="white",
                           cursor="hand2")
        btn_clear.place(x=340, y=400, width=100, height=40)
        btn_clear.bind("<Return>", self.clear)
        btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Search Frame ======
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=2,
                                 relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # ====== Options ======
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Category", "Location", "Name"), state='readonly', justify=CENTER,
                                  font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="light yellow").place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50",
                            fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # ====== Product Details ======
        p_Frame = Frame(self.root, bd=3, relief=RIDGE)
        p_Frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_Frame, orient=VERTICAL)
        scrollx = Scrollbar(p_Frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_Frame, columns=(
            "pid", "category", "name", "price", "qty", "totalPrice", "status", "location"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("totalPrice", text="Total Price")
        self.product_table.heading("status", text="Status")
        self.product_table.heading("location", text="Location")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("category", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("totalPrice", width=100)
        self.product_table.column("status", width=100)
        self.product_table.column("location", width=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ========================================================================================
    def fetch_cat_loc(self):
        self.cat_list.append("Empty")
        self.loc_list.append("Empty")

        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM locations")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.loc_list[:]
                self.loc_list.append("Select")
                for i in loc:
                    self.loc_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        total = int(self.var_price.get()) * int(self.var_qty.get())
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_loc.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    op = messagebox.askyesno("Error", "Product already present, do you really want to add", parent=self.root)
                    if op == True:
                        cur.execute(
                            "INSERT INTO product(category,name,price,qty,totalPrice,status,location) values(?,?,?,?,?,?,?)",
                            (
                                self.var_cat.get(),
                                self.var_name.get(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                total,
                                self.var_status.get(),
                                self.var_loc.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                        self.show()
                else:
                    cur.execute("INSERT INTO product(category,name,price,qty,totalPrice,status,location) values(?,?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        total,
                        self.var_status.get(),
                        self.var_loc.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.var_status.set(row[6])
        self.var_loc.set(row[7])

    def update(self, e):
        try:
            con = sqlite3.connect(database=r'asb.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            row = cur.fetchone()
            Quant = int(self.var_qty.get()) + int(row[4])
            total = int(self.var_price.get()) * int(Quant)
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please Select Product From List", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE product set category=?, name=?, price=?, qty=?, totalPrice=?, status=?, location=? WHERE pid=?",
                        (
                            self.var_cat.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            Quant,
                            total,
                            self.var_status.get(),
                            self.var_loc.get(),
                            self.var_pid.get(),
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def delete(self, e):
        con = sqlite3.connect(database=r'asb.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product From List", parent=self.root)
            else:
                cur.execute("SELECT * FROM Product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op is True:
                        cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
        self.var_cat.set("Select")
        self.var_loc.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")

        self.show()

    def search(self):
        try:
            con = sqlite3.connect(database=r'asb.db')
            cur = con.cursor()
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            else:
                cur.execute(
                    "SELECT * FROM product WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
