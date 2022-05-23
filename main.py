from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
from product import productClass
from category import categoryClass
from locations import locationClass
from billing import BillClass
from summary import allSummary


class stockManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1425x700+50+20")
        self.root.title("ASB")

        # ===== Style =====
        style = ttk.Style(root)
        style.theme_use('clam')

        # ===== Background Image =====
        self.bg = ImageTk.PhotoImage(file="images/fieldBg.jpg")
        self.bgImage = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ====== Title =======
        title = Label(self.root, text="ASB", font=("Imprint MT Shadow", 50, "bold")
                      , bg="#F9B763", fg="black", anchor="n").pack(side=TOP, fill=X)

        # ===== Menu Bar =====
        lbl_menu = Frame(bg="#333333")
        lbl_menu.pack(side=TOP, fill=X, ipady=15)

        btn_category = Button(lbl_menu, text="CATEGORY", command=self.category, font=("times new roman", 12, "bold"),
                              bg="#333333", fg="white", bd=0, cursor="hand2")
        btn_category.place(x=2, y=0, width=90, height=30)

        btn_location = Button(lbl_menu, text="LOCATIONS", command=self.location, font=("times new roman", 12, "bold"),
                              bg="#333333", fg="white", bd=0, cursor="hand2")
        btn_location.place(x=110, y=0, width=95, height=30)

        btn_product = Button(lbl_menu, text="PRODUCT", command=self.product, font=("times new roman", 12, "bold"),
                             bg="#333333", fg="white", bd=0, cursor="hand2")
        btn_product.place(x=220, y=0, width=80, height=30)

        btn_billing = Button(lbl_menu, text="BILLING", command=self.billing, font=("times new roman", 12, "bold"),
                             bg="#333333", fg="white", bd=0, cursor="hand2")
        btn_billing.place(x=310, y=0, width=80, height=30)

        btn_summary = Button(lbl_menu, text="SUMMARY", command=self.summary, font=("times new roman", 12, "bold"),
                             bg="#333333", fg="white", bd=0, cursor="hand2")
        btn_summary.place(x=400, y=0, width=85, height=30)

    def category(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = categoryClass(self.new_win)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def location(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = locationClass(self.new_win)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def product(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = productClass(self.new_win)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def billing(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = BillClass(self.new_win)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def summary(self):
        try:
            self.new_win = Toplevel(self.root)
            self.new_obj = allSummary(self.new_win)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = stockManagement(root)
    root.mainloop()

# Software By Usman Amjad(UA)
