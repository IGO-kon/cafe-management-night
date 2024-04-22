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
def show_products():
    conn = sqlite3.connect('cafe_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM Products")
    products = cursor.fetchall()
    conn.close()

    return render_template('show_products.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
