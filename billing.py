# -------Importing Modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import tempfile
import time
from datetime import datetime


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+90+40")
        self.root.title("ASB")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # ===== Style =====
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # ===== Variables =====
        self.loc_list = []  # List Variable
        self.fetch_cat_loc()  # Calling Function

        self.cart_list = []
        self.chk_print = 0

        # ====== Title =======
        title = Label(self.root, text="ASB", font=("times new roman", 40, "bold"), bg="#010c48",
                      fg="white", anchor="n", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ====== Clock ======
        self.lbl_clock = Label(self.root, text="Welcome to Stock Management System\t\t Date:DD-MM-YYYY\t\t Time: "
                                               "HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ====== Product Frame ======
        # ===== Variable =====
        self.var_search = StringVar()
        self.search_loc = StringVar()

        ProductFrame1 = Frame(self.root, bg="white", bd=4, relief=RIDGE)
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)

        # ===== Product Search Frame =====
        ProductFrame2 = Frame(ProductFrame1, bg="white", bd=2, relief=RIDGE)
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=("times new roman", 15, "bold"),
                           bg="white", fg="green").place(x=2, y=5)

        searchLoc = ttk.Combobox(ProductFrame2, font=("times new roman", 13), textvariable=self.search_loc,
                                 values=self.loc_list, state="readonly", justify=CENTER)
        searchLoc.place(x=2, y=45, width=120)
        searchLoc.current(0)

        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow").place(x=128, y=47, width=150, height=22)

        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15),
                              bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        # ===== Product Detail Frame =====
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.Product_Table = ttk.Treeview(ProductFrame3, columns=(
            "pid", "category", "name", "price", "qty", "location"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        for column in self.Product_Table["columns"]:
            self.Product_Table.column(column, anchor=CENTER)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid", text="PID")
        self.Product_Table.heading("category", text="Category")
        self.Product_Table.heading("name", text="Name")
        self.Product_Table.heading("price", text="Price")
        self.Product_Table.heading("qty", text="Quantity")
        self.Product_Table.heading("location", text="Location")

        self.Product_Table["show"] = "headings"

        self.Product_Table.column("pid", width=40)
        self.Product_Table.column("category", width=100)
        self.Product_Table.column("name", width=100)
        self.Product_Table.column("price", width=40)
        self.Product_Table.column("qty", width=90)
        self.Product_Table.column("location", width=90)

        self.Product_Table.pack(fill=BOTH, expand=1)
        self.Product_Table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="Note: Enter 0 Quantity to remove the product from cart",
                         font=("goudy old style", 12), anchor="w", bg="white", fg="red").pack(side=BOTTOM, fill=X)

        # ===== Customer frame =====
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bg="white", bd=4, relief=RIDGE)
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="light gray").pack(
            side=TOP, fill=X)

        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(
            x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13),
                         bg="light yellow").place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(
            x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13),
                            bg="light yellow").place(x=380, y=35, width=140)

        # ===== Cal Cart Frame =====
        Cal_Cart_Frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        # ===== Calculator Frame =====
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_Cart_Frame, bg="white", bd=9, relief=RIDGE)
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=("arial", 15, "bold"), width=21, bd=10,
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)
        txt_cal_input.focus()

        btn_7 = Button(Cal_Frame, text="7", font=("arial", 15, "bold"), command=lambda: self.get_input(7), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_7.grid(row=1, column=0)
        txt_cal_input.bind('7', lambda event: self.get_input(7))
        btn_8 = Button(Cal_Frame, text="8", font=("arial", 15, "bold"), command=lambda: self.get_input(8), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_8.grid(row=1, column=1)
        txt_cal_input.bind('8', lambda event: self.get_input(8))
        btn_9 = Button(Cal_Frame, text="9", font=("arial", 15, "bold"), command=lambda: self.get_input(9), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_9.grid(row=1, column=2)
        txt_cal_input.bind('9', lambda event: self.get_input(9))
        btn_sum = Button(Cal_Frame, text='+', font=("arial", 15, "bold"), command=lambda: self.get_input('+'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_sum.grid(row=1, column=3)
        txt_cal_input.bind('+', lambda event: self.get_input('+'))

        btn_4 = Button(Cal_Frame, text="4", font=("arial", 15, "bold"), command=lambda: self.get_input(4), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_4.grid(row=2, column=0)
        txt_cal_input.bind('4', lambda event: self.get_input(4))
        btn_5 = Button(Cal_Frame, text="5", font=("arial", 15, "bold"), command=lambda: self.get_input(5), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_5.grid(row=2, column=1)
        txt_cal_input.bind('5', lambda event: self.get_input(5))
        btn_6 = Button(Cal_Frame, text="6", font=("arial", 15, "bold"), command=lambda: self.get_input(6), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_6.grid(row=2, column=2)
        txt_cal_input.bind('6', lambda event: self.get_input(6))
        btn_sub = Button(Cal_Frame, text='-', font=("arial", 15, "bold"), command=lambda: self.get_input('-'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_sub.grid(row=2, column=3)
        txt_cal_input.bind('-', lambda event: self.get_input('-'))

        btn_1 = Button(Cal_Frame, text="1", font=("arial", 15, "bold"), command=lambda: self.get_input(1), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_1.grid(row=3, column=0)
        txt_cal_input.bind('1', lambda event: self.get_input(1))
        btn_2 = Button(Cal_Frame, text="2", font=("arial", 15, "bold"), command=lambda: self.get_input(2), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_2.grid(row=3, column=1)
        txt_cal_input.bind('2', lambda event: self.get_input(2))
        btn_3 = Button(Cal_Frame, text="3", font=("arial", 15, "bold"), command=lambda: self.get_input(3), bd=5,
                       width=4, pady=10, cursor="hand2")
        btn_3.grid(row=3, column=2)
        txt_cal_input.bind('3', lambda event: self.get_input(3))
        btn_mul = Button(Cal_Frame, text='x', font=("arial", 15, "bold"), command=lambda: self.get_input('*'), bd=5,
                         width=4, pady=10, cursor="hand2")
        btn_mul.grid(row=3, column=3)
        txt_cal_input.bind('*', lambda event: self.get_input('*'))

        btn_0 = Button(Cal_Frame, text="0", font=("arial", 15, "bold"), command=lambda: self.get_input(0), bd=5,
                       width=4, pady=15, cursor="hand2")
        btn_0.grid(row=4, column=0)
        txt_cal_input.bind('0', lambda event: self.get_input(0))
        btn_c = Button(Cal_Frame, text="c", font=("arial", 15, "bold"), command=self.clear_cal, bd=5, width=4, pady=15,
                       cursor="hand2")
        btn_c.grid(row=4, column=1)
        txt_cal_input.bind('c', lambda event: self.clear_cal())
        btn_eq = Button(Cal_Frame, text="=", font=("arial", 15, "bold"), command=self.perform_cal, bd=5, width=4,
                        pady=15, cursor="hand2")
        btn_eq.grid(row=4, column=2)
        txt_cal_input.bind('<Return>', lambda event: self.perform_cal())
        btn_div = Button(Cal_Frame, text='/', font=("arial", 15, "bold"), command=lambda: self.get_input('/'), bd=5,
                         width=4, pady=15, cursor="hand2")
        btn_div.grid(row=4, column=3)
        txt_cal_input.bind('/', lambda event: self.get_input('/'))

        # ===== Cart Frame =====
        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)

        self.cartTitle = Label(cart_Frame, text="Cart \t Total Products: [0]", font=("goudy old style", 15),
                               bg="light gray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        for column in self.CartTable["columns"]:
            self.CartTable.column(column, anchor=CENTER)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")

        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ===== Add Cart Widgets Frame =====
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(
            x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
                           bg="light yellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(
            x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
                            bg="light yellow").place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=390,
                                                                                                                 y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
                          bg="light yellow").place(x=390, y=35, width=120, height=22)

        self.lbl_instock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_instock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear",
                                font=("times new roman", 15, "bold"), bg="light gray", cursor="hand2")
        btn_clear_cart.place(x=180, y=70, width=150, height=30)

        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart",
                              font=("times new roman", 15, "bold"), bg="orange", cursor="hand2")
        btn_add_cart.place(x=340, y=70, width=180, height=30)
        btn_add_cart.bind("<Return>", self.add_update_cart)
        btn_add_cart.bind("<ButtonRelease-1>", self.add_update_cart)

        # ===== Billing Area =====
        billFrame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        billFrame.place(x=953, y=110, width=410, height=550)

        BTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ===== Billing Buttons =====
        self.txt_disc = IntVar()

        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n[0]", font=("goudy old style", 15, "bold"),
                              bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n", font=("goudy old style", 15, "bold"), bg="#8bc34a",
                                  fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        txt_discount = Entry(billMenuFrame, textvariable=self.txt_disc, font=("goudy old style", 15, "bold")).place(
            x=146, y=42, width=75, height=30)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=("goudy old style", 15, "bold"), bg="#607d8b",
                                 fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, cursor="hand2",
                           font=("goudy old style", 15, "bold"),
                           bg="light green", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Clear All", command=self.clear_all, cursor="hand2",
                               font=("goudy old style", 15, "bold"),
                               bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, command=self.generate_bill, text="Generate\nSave Bill", cursor="hand2",
                              font=("goudy old style", 15, "bold"),
                              bg="#009688", fg="white")
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ===== Footer =====
        footer = Label(self.root,
                       text="IMS-Stock Management System | Developed By UA\nFor any Technical Issue contact: "
                            "+923448112288",
                       font=("times new roman", 11), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    # ==================== All Functions ==========================================

    def fetch_cat_loc(self):
        try:
            self.loc_list.append("Empty")
            con = sqlite3.connect(database=r'asb.db')
            cur = con.cursor()

            cur.execute("SELECT name FROM locations")
            loc = cur.fetchall()
            if len(loc) > 0:
                del self.loc_list[:]
                self.loc_list.append("Select")
                for i in loc:
                    self.loc_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        conn = sqlite3.connect(database=r'asb.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT pid, category, name, price, qty, location FROM product WHERE status='Active'")
            rows = cursor.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        conn = sqlite3.connect(database=r'asb.db')
        cursor = conn.cursor()

        if self.search_loc.get() in self.loc_list:
            cursor.execute(
                "SELECT pid, category, name, price, qty, location FROM product WHERE name LIKE '%" + self.var_search.get() + "%' AND status='Active'")
            rows = cursor.fetchall()
            if len(rows) != 0:
                self.Product_Table.delete(*self.Product_Table.get_children())
                for row in rows:
                    self.Product_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!!!", parent=self.root)
        else:
            messagebox.showerror("Error", "Select Valid Location", parent=self.root)

    def get_data(self, ev):
        f = self.Product_Table.focus()
        content = (self.Product_Table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[2])
        self.var_price.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_qty.set('1')
        self.search_loc.set(row[5])

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self, e):
        if self.var_pid.get() == '':
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror("Error", "Quantity is Required", parent=self.root)
        elif float(self.var_qty.get()) > float(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            conn = sqlite3.connect(database=r'asb.db')
            cursor = conn.cursor()

            billAmt = float(self.var_price.get()) * float(self.var_qty.get())
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get(), billAmt, self.search_loc.get()]

            # ===== Update Cart =====
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            if present == 'yes':
                op = messagebox.askyesno('Confirm',
                                         "Product already present\nDo you want to Update | Remove from the Cart List",
                                         parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * float(row[3]))

        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.bill_amnt)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        conn = sqlite3.connect(database=r'asb.db')
        cursor = conn.cursor()

        op = messagebox.askyesno("Confirm", "Do you really want to Generate Bill?", parent=self.root)
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add Product to the Cart!!!", parent=self.root)
        elif op == True:
            # ===== Bill Top =====
            self.bill_top()
            # ===== Bill Middle =====
            self.bill_middle()
            # ===== Bill Bottom =====
            self.bill_bottom()

            for row in self.cart_list:
                name = row[1]
                bill_amt = row[2]
                totalPrice = row[5]
                getLocation = row[6]
                cursor.execute(
                    "INSERT INTO sellDetails(item_id, name, price, qty, totalPrice, location, discount, netPay, sellDate) VALUES(?,?,?,?,?,?,?,?,?)",
                    (
                        self.pid,
                        name,
                        bill_amt,
                        self.var_qty.get(),
                        totalPrice,
                        getLocation,
                        self.discount,
                        self.net_pay,
                        self.time_1
                    ))
                conn.commit()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/Save in Backend", parent=self.root)

        self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t   ASB, Ghalla Mandi, Sadiqabad
\t     Phone No. +923043786863
{str("=" * 47)}
 Customer Name: {self.var_cname.get()}
 Ph No: {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%m/%d/%Y"))}
{str("=" * 47)}
 Product Name\t\t\tQty\tPrice
{str("=" * 47)} 
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        self.discount = float(self.txt_disc.get())
        self.net_pay = float(self.bill_amnt) - float(self.discount)
        bill_bottom_temp = f'''
{str("=" * 47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("=" * 47)}\n

Sold By Ahmed Hussain
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        try:
            conn = sqlite3.connect(database=r'asb.db')
            cursor = conn.cursor()

            self.time_1 = datetime.now().strftime("%m/%d/%Y")
            self.total_price = float(self.var_price.get()) * float(self.var_qty.get())
            if self.search_loc.get() in self.loc_list:
                for row in self.cart_list:
                    self.pid = row[0]
                    self.name = row[1]
                    qty = float(row[4]) - float(row[3])
                    if float(row[3]) == float(row[4]):
                        status = 'Inactive'
                    if float(row[3]) != float(row[4]):
                        status = 'Active'
                    price = float(row[2]) * float(row[3])
                    price = str(price)
                    self.txt_bill_area.insert(END, "\n " + self.name + "\t\t\t" + row[3] + "\tRs." + price)

                    cursor.execute("SELECT price FROM product WHERE pid=?", (
                        self.pid,
                    ))
                    row = cursor.fetchone()
                    totalPrice = float(qty) * float(row[0])

                    # ===== Update Qty In Product Table =====
                    cursor.execute("UPDATE product SET qty=?, totalPrice=?, status=? WHERE pid=?", (
                        qty,
                        totalPrice,
                        status,
                        self.pid
                    ))
                    conn.commit()
                conn.close()
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Stock Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showinfo('Print', "Please generate bill, to print the receipt", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
