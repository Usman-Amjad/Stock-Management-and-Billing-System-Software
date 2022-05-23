import sqlite3


def asbDatabase():
    con = sqlite3.connect(database=r'asb.db')
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT,"
        "contact TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS locations(lid INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, address TEXT)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,"
        "name TEXT, price INTEGER, qty INTEGER, totalPrice INTEGER, status TEXT, location TEXT)")
    con.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS sellDetails(item_id INTEGER,'''
                '''name TEXT, price INTEGER, qty INTEGER, totalPrice INTEGER, sellerName TEXT, location TEXT, discount INTEGER, netPay INTEGER, sellDate TEXT);''')
    con.commit()


asbDatabase()
