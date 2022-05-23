# -------Importing Modules
from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry


class allSummary:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x608+-5+134")
        self.root.title("RFC By UA")
        self.root.config(bg="#333333")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ==Declaring Variables==
        self.invoice_no = StringVar()
        self.item_name = StringVar()  # For Row 2
        self.search_txt = StringVar()  # For search
        self.search_cmb = StringVar()  # For search

        self.var_loc = StringVar()
        self.loc_list = []
        self.fetch_cat_loc()

        # ===== Title Label =====
        lbl_title = Label(self.root, text="Sells Details", font=("times new roman", 30), bg="#184a45",
                          fg="white").pack(side=TOP, fill=X, padx=10, pady=0)

        # ===== Style =====
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Create a Frame for border
        self.sales_border = Frame(self.root, background="#009688")
        self.totalSales = Label(self.sales_border, text="Total Sales\n 0 ", bg="white", fg="black",
                                font=("times new roman", 20, "bold"))
        self.totalSales.place(x=3, y=3, height=100, width=220)
        self.sales_border.place(x=9, y=53, height=106, width=226)

        self.salary_border = Frame(self.root, background="#009688")
        self.lblTotalPrice = Label(self.salary_border, text="Total Sales\n 0 ", bg="white", fg="black",
                                   font=("times new roman", 20, "bold"))
        self.lblTotalPrice.place(x=3, y=3, height=100, width=220)
        self.salary_border.place(x=9, y=160, height=106, width=226)

        self.net_border = Frame(self.root, background="#009688")
        self.lblPriceByLoc = Label(self.net_border, text="Location\n 0 ", bg="white", fg="black",
                                   font=("times new roman", 20, "bold"))
        self.lblPriceByLoc.place(x=3, y=3, height=100, width=220)
        self.net_border.place(x=9, y=267, height=106, width=226)

        # ===== Product Search Frame =====
        ProductFrame2 = Frame(self.root, bg="#184a45", bd=3, relief=RIDGE)
        ProductFrame2.place(x=380, y=52, width=300, height=393)

        lbl_search = Label(ProductFrame2, text="Search By Name And Date",
                           font=("times new roman", 15, "bold"),
                           bg="#184a45", fg="white").place(x=25, y=5)

        lbl_search_name = Label(ProductFrame2, text="NAME", font=("times new roman", 15, "bold"), bg="#184a45"
                                , fg="white").place(x=20, y=47)
        txt_search_name = ttk.Entry(ProductFrame2, textvariable=self.search_txt, font=("times new roman", 15)
                                    )
        txt_search_name.place(x=120, y=47, width=150, height=25)
        txt_search_name.focus()

        lbl_search_date = Label(ProductFrame2, text="FROM", font=("times new roman", 15, "bold"), bg="#184a45"
                                , fg="white")
        lbl_search_date.place(x=20, y=100)
        self.cal = DateEntry(ProductFrame2, selectmode='day', background="black", disabledbackground="black",
                             bordercolor="black",
                             headersbackground="black", normalbackground="black", foreground='white',
                             normalforeground='white', headersforeground='white')
        self.cal.place(x=120, y=100, width=150, height=25)

        lbl_search_date1 = Label(ProductFrame2, text="TO", font=("times new roman", 15, "bold"), bg="#184a45"
                                 , fg="white")
        lbl_search_date1.place(x=20, y=153)
        self.cal1 = DateEntry(ProductFrame2, selectmode='day', background="black", disabledbackground="black",
                              bordercolor="black",
                              headersbackground="black", normalbackground="black", foreground='white',
                              normalforeground='white', headersforeground='white')
        self.cal1.place(x=120, y=153, width=150, height=25)

        cmb_loc = ttk.Combobox(ProductFrame2, textvariable=self.var_loc,
                               values=self.loc_list, state='readonly', justify=CENTER,
                               font=("goudy old style", 15))
        cmb_loc.place(x=120, y=195, width=150)
        cmb_loc.current(0)

        btn_search = Button(ProductFrame2, text="Search", font=("goudy old style", 15),
                            command=lambda: [self.search(), self.update_content()],
                            bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=60, y=250, width=100, height=40)

        btn_clear = Button(ProductFrame2, text="Clear", font=("goudy old style", 15), bg="light green",
                           fg="white",
                           cursor="hand2")
        btn_clear.place(x=170, y=250, width=100, height=40)
        btn_clear.bind("<Return>", self.clear)
        btn_clear.bind("<ButtonRelease-1>", self.clear)

        # ====== Summary Details ======
        summaryFrame = Frame(self.root, bd=3, relief=RIDGE)
        summaryFrame.place(x=680, y=52, width=840, height=390)

        scrolly = Scrollbar(summaryFrame, orient=VERTICAL)
        scrollx = Scrollbar(summaryFrame, orient=HORIZONTAL)

        self.summaryTable = ttk.Treeview(summaryFrame, columns=(
            "item_id", "name", "price", "qty", "totalPrice", "sellerName", "location", "discount", "netPay",
            "sellDate"),
                                         yscrollcommand=scrolly.set,
                                         xscrollcommand=scrollx.set)
        for column in self.summaryTable["columns"]:
            self.summaryTable.column(column, anchor=CENTER)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.summaryTable.xview)
        scrolly.config(command=self.summaryTable.yview)

        self.summaryTable.heading("item_id", text="Product ID")
        self.summaryTable.heading("name", text="Name")
        self.summaryTable.heading("price", text="Price")
        self.summaryTable.heading("qty", text="Quantity")
        self.summaryTable.heading("totalPrice", text="Total Price")
        self.summaryTable.heading("sellerName", text="Sell By")
        self.summaryTable.heading("location", text="Location")
        self.summaryTable.heading("discount", text="Discount")
        self.summaryTable.heading("netPay", text="Net Pay")
        self.summaryTable.heading("sellDate", text="Sell Date")

        self.summaryTable["show"] = "headings"

        self.summaryTable.column("item_id", width=80)
        self.summaryTable.column("name", width=100)
        self.summaryTable.column("price", width=100)
        self.summaryTable.column("qty", width=100)
        self.summaryTable.column("totalPrice", width=100)
        self.summaryTable.column("sellerName", width=100)
        self.summaryTable.column("location", width=100)
        self.summaryTable.column("discount", width=100)
        self.summaryTable.column("netPay", width=100)
        self.summaryTable.column("sellDate", width=130)

        self.summaryTable.pack(fill=BOTH, expand=1)

        self.summaryTable.bind("<ButtonRelease-1>", self.get_data)

        self.update_content()

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

    def get_data(self, ev):
        try:
            f = self.summaryTable.focus()
            content = (self.summaryTable.item(f))
            row = content['values']

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self, e):
        try:
            self.search_txt.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = sqlite3.connect(database=r'asb.db')
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM sellDetails WHERE name LIKE '%" + self.search_txt.get() + "%'")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.summaryTable.delete(*self.summaryTable.get_children())
                for row in rows:
                    self.summaryTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def update_content(self):
        try:
            conn = sqlite3.connect(database=r'asb.db')
            cursor = conn.cursor()

            dt = self.cal.get_date()
            date1 = str(dt.strftime("%m/%d/%Y"))

            dt1 = self.cal1.get_date()
            date2 = str(dt1.strftime("%m/%d/%Y"))

            cursor.execute("SELECT * FROM sellDetails WHERE sellDate BETWEEN ? AND ?", (date1, date2))
            self.sales = cursor.fetchall()
            if len(self.sales) < int(50):
                self.sales_border.config(bg='red')
                self.totalSales.config(text=f"Total Sales\n {len(self.sales)} ")
            else:
                self.totalSales.config(text=f"Total Sales\n {len(self.sales)} ")

            cursor.execute("SELECT SUM(netPay) FROM sellDetails WHERE sellDate BETWEEN ? AND ?", (date1, date2))
            self.byDatePrice = cursor.fetchone()
            saarr = [str(a) for a in self.byDatePrice]
            self.byDatePrice = (", ".join(saarr))
            self.lblTotalPrice.config(text=f"Total Sales\n Rs. {self.byDatePrice} ")

            cursor.execute("SELECT SUM(totalPrice) FROM product WHERE location = ?", (self.var_loc.get(),))
            self.tPrice = cursor.fetchone()
            saar = [str(a) for a in self.tPrice]
            self.tPrice = (", ".join(saar))
            self.lblPriceByLoc.config(text=f"{self.var_loc.get()}\n {self.tPrice}")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = allSummary(root)
    root.mainloop()
