from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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
    conn.commit()
    conn.close()

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])

        # データベースに接続
        conn = sqlite3.connect('cafe_management.db')
        cursor = conn.cursor()

        # データベースにデータを挿入
        cursor.execute("INSERT INTO Products (name, category, price) VALUES (?, ?, ?)", (name, category, price))
        conn.commit()

        # データベース接続を閉じる
        conn.close()

        print("データベースに商品情報を追加しました。")

        return redirect(url_for('add_product'))

    return render_template('add_product.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
