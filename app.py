from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('cafe_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price FLOAT NOT NULL
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        display_name TEXT NOT NULL,
        role TEXT NOT NULL
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stock_History (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        entry_date DATETIME NOT NULL,
        notes TEXT,
        recorded_by INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (recorded_by) REFERENCES Users(id)
    );
    ''')
    conn.commit()
    conn.close()

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])

        conn = sqlite3.connect('cafe_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (name, category, price) VALUES (?, ?, ?)", (name, category, price))
        conn.commit()
        conn.close()

        print("データベースに商品情報を追加しました。")
        return redirect(url_for('add_product'))

    return render_template('add_product.html')

@app.route('/products')
def list_products():
    conn = sqlite3.connect('cafe_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()

    return render_template('list_products.html', products=products)

@app.route('/stock/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        notes = request.form['notes']
        recorded_by = 1  # Replace with user ID (Here, user ID is 1)

        conn = sqlite3.connect('cafe_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Stock_History (product_id, quantity, entry_date, notes, recorded_by) VALUES (?, ?, ?, ?, ?)",
                       (product_id, quantity, datetime.now(), notes, recorded_by))
        conn.commit()
        conn.close()

        print("データベースに在庫履歴を追加しました。")
        return redirect(url_for('add_stock'))

    conn = sqlite3.connect('cafe_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Products")
    products = cursor.fetchall()
    conn.close()

    return render_template('add_stock_history.html', products=products)

@app.route('/stock_history')
def list_stock_history():
    conn = sqlite3.connect('cafe_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sh.id, p.name, sh.quantity, sh.entry_date, sh.notes FROM Stock_History sh JOIN Products p ON sh.product_id = p.id")
    stock_history = cursor.fetchall()
    conn.close()

    return render_template('list_stock_history.html', stock_history=stock_history)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
