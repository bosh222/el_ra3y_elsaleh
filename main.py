import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'elra3y-elsaleh-secret-key')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    error = None

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        if not all([name, email, message]):
            error = 'يرجى ملء جميع الحقول المطلوبة.'
        else:
            success = True
            return render_template('contact.html', success=True, customer_name=name)

    return render_template('contact.html', success=success, error=error)

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product/<brand>')
def product_detail(brand):
    return render_template('product_detail.html', brand=brand)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
