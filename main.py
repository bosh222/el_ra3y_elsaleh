import json
import os
from flask import Flask, abort, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'elra3y-elsaleh-secret-key')

BRAND_CATALOGS = {
    'fresh': {'name': 'فريش'},
    'tornado': {'name': 'تورنيدو'},
    'sharp': {'name': 'شارب'},
    'toshiba': {
        'name': 'توشيبا ميديا',
        'note': 'لم يتوفر كتالوج منتجات منزلية موثوق لهذه العلامة في السوق المصري، لذلك لم نضف منتجات غير مؤكدة.',
    },
    'media': {'name': 'ميديا'},
    'akai': {'name': 'أكاي'},
    'sokany': {'name': 'سوكاني'},
    'national': {
        'name': 'ناشونال',
        'note': 'ناشونال علامة قديمة، ولم يتوفر كتالوج موثوق لمنتجات جديدة بهذا الاسم في مصر.',
    },
}

CATEGORY_LABELS = {
    'refrigerators': 'ثلاجات',
    'mini-bars': 'ميني بار',
    'deep-freezers': 'ديب فريزر',
    'cookers': 'بوتاجازات',
    'washing-machines': 'غسالات ملابس',
    'dishwashers': 'غسالات أطباق',
    'televisions': 'شاشات',
    'air-conditioners': 'تكييفات',
    'microwaves': 'ميكروويف',
    'electric-ovens': 'أفران كهربائية',
    'vacuum-cleaners': 'مكانس',
    'fans': 'مراوح',
    'water-heaters': 'سخانات مياه',
    'air-fryers': 'قلايات هوائية',
    'kitchen-appliances': 'أجهزة المطبخ',
    'water-coolers': 'مبردات مياه',
    'kettles': 'غلايات',
    'coffee-appliances': 'أجهزة القهوة',
    'blenders': 'خلاطات',
    'personal-care': 'أجهزة العناية الشخصية',
    'juicers': 'عصارات',
    'irons': 'مكاوي',
    'other-appliances': 'أجهزة منزلية أخرى',
}


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


def load_brand_products(brand):
    catalog_path = os.path.join(app.static_folder, f'{brand}-products.json')
    if not os.path.isfile(catalog_path):
        return []

    with open(catalog_path, encoding='utf-8') as products_file:
        products = json.load(products_file)

    image_dir = os.path.join(app.static_folder, 'product-images', brand)
    local_images = os.listdir(image_dir) if os.path.isdir(image_dir) else []
    for index, product in enumerate(products):
        product.setdefault('id', str(index))
        product.setdefault('description', '')
        product['category'] = local_product_category(brand, product)

        image_stem = f'{brand}-{index + 1:04d}'
        local_image = next((name for name in local_images if name.startswith(image_stem + '.')), None)
        if local_image:
            product['image'] = f'/static/product-images/{brand}/{local_image}'

    return products


def local_product_category(brand, product):
    current = product.get('category', '')
    if current in CATEGORY_LABELS:
        return current
    if current and '?' not in current:
        return current

    searchable = f"{product.get('name', '')} {product.get('source_url', '')}".casefold()
    rules = [
        (('mini bar', 'minibar'), 'mini-bars'),
        (('dishwasher', 'غسالة أطباق', 'غسالات أطباق'), 'dishwashers'),
        (('washing machine', 'washer', 'غسالة', 'غسالات'), 'washing-machines'),
        (('refrigerator', 'ثلاجة', 'ثلاجات'), 'refrigerators'),
        (('deep freezer', 'freezer', 'فريزر'), 'deep-freezers'),
        (('gas cooker', 'cooker', 'cookers', 'بوتاجاز'), 'cookers'),
        (('air conditioner', 'split-air', 'تكييف'), 'air-conditioners'),
        (('television', '/tv', 'smart tv', 'شاشة', 'تليفزيون'), 'televisions'),
        (('microwave', 'ميكروويف'), 'microwaves'),
        (('electric oven', 'oven', 'فرن كهربائي'), 'electric-ovens'),
        (('ventilation-fan', 'tornado-fans', 'fan', 'مروحة', 'مراوح'), 'fans'),
        (('water-heater', 'سخان'), 'water-heaters'),
        (('vacuum', 'مكنسة'), 'vacuum-cleaners'),
        (('kettle', 'غلاية'), 'kettles'),
        (('coffee', 'قهوة'), 'coffee-appliances'),
        (('fryer', 'قلاية'), 'air-fryers'),
        (('iron', 'مكواة'), 'irons'),
        (('juicer', 'عصارة'), 'juicers'),
        (('water-dispenser', 'water-cooler', 'مبرد مياه'), 'water-coolers'),
        (('blender', 'mixer', 'خلاط', 'عجان'), 'blenders'),
        (('dryer', 'hair', 'شعر'), 'personal-care'),
    ]
    for keywords, label in rules:
        if any(keyword in searchable for keyword in keywords):
            return label

    if brand in ('akai', 'sokany'):
        return 'other-appliances'
    return 'other-appliances'


@app.route('/products')
def products():
    brands = {
        slug: {**catalog, 'product_count': len(load_brand_products(slug))}
        for slug, catalog in BRAND_CATALOGS.items()
    }
    return render_template('products.html', brands=brands)


@app.route('/product/<brand>')
def brand_detail(brand):
    catalog = BRAND_CATALOGS.get(brand)
    if catalog is None:
        abort(404)

    products = load_brand_products(brand)
    categories = sorted({product['category'] for product in products if product.get('category')})
    category_rows = [
        {
            'name': CATEGORY_LABELS.get(category, category),
            'id': index,
            'count': sum(product.get('category') == category for product in products),
        }
        for index, category in enumerate(categories)
    ]
    return render_template(
        'brand_detail.html', brand=brand, catalog=catalog,
        categories=category_rows, product_count=len(products),
    )


@app.route('/product/<brand>/category/<int:category_id>')
def category_products(brand, category_id):
    catalog = BRAND_CATALOGS.get(brand)
    if catalog is None:
        abort(404)

    products = load_brand_products(brand)
    categories = sorted({product['category'] for product in products if product.get('category')})
    if category_id < 0 or category_id >= len(categories):
        abort(404)

    category = categories[category_id]
    matches = [product for product in products if product.get('category') == category]
    page = max(request.args.get('page', 1, type=int), 1)
    per_page = 36
    start = (page - 1) * per_page
    page_products = matches[start:start + per_page]
    total_pages = max((len(matches) + per_page - 1) // per_page, 1)
    if page > total_pages:
        abort(404)

    return render_template(
        'product_list.html', brand=brand, catalog=catalog, category=category,
        category_label=CATEGORY_LABELS.get(category, category),
        products=page_products, page=page, total_pages=total_pages,
        category_id=category_id,
    )


@app.route('/product/<brand>/refrigerators')
def refrigerator_products(brand):
    if brand != 'fresh':
        abort(404)
    categories = sorted({product['category'] for product in load_brand_products(brand)})
    if 'refrigerators' not in categories:
        abort(404)
    return category_products(brand, categories.index('refrigerators'))


@app.route('/product/<brand>/item/<product_id>')
def product_detail(brand, product_id):
    catalog = BRAND_CATALOGS.get(brand)
    if catalog is None:
        abort(404)

    products = load_brand_products(brand)
    product = next((item for item in products if item.get('id') == product_id), None)
    if product is None:
        abort(404)

    categories = sorted({item['category'] for item in products if item.get('category')})
    return render_template(
        'product_detail.html', brand=brand, catalog=catalog, product=product,
        category_label=CATEGORY_LABELS.get(product['category'], product['category']),
        category_id=categories.index(product['category']),
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
