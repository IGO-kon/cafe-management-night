from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])

        print(f"商品名: {name}")
        print(f"カテゴリ: {category}")
        print(f"価格: {price}")

        return redirect(url_for('add_product'))

    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
