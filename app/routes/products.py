# app/routes/products.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from app.main.product import Product
from app import db
from app.utils.helpers import get_filter_params, paginate_query

products = Blueprint('products', __name__)

@products.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    products_list = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('index.html', products=products_list)

@products.route('/products')
def list():
    page = request.args.get('page', 1, type=int)
    filters = get_filter_params(request)
    
    # Base query
    query = Product.query
    
    # Apply filters
    if 'min_price' in filters:
        query = query.filter(Product.price >= filters['min_price'])
    if 'max_price' in filters:
        query = query.filter(Product.price <= filters['max_price'])
    if 'in_stock' in filters:
        query = query.filter(Product.stock > 0)
    
    # Apply sorting
    sort = filters.get('sort', 'newest')
    if sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Product.name.desc())
    
    # Paginate results
    products_list = paginate_query(query, page)
    
    return render_template('products/list.html', products=products_list)

@products.route('/product/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)

@products.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('products.list'))
    
    # Search in product name and description
    search_query = f"%{query}%"
    products_list = Product.query.filter(
        (Product.name.ilike(search_query)) | 
        (Product.description.ilike(search_query))
    ).paginate(page=page, per_page=12)
    
    return render_template('products/list.html', products=products_list, search_term=query)

@products.route('/api/products')
def api_products():
    products_list = Product.query.all()
    return jsonify([product.to_dict() for product in products_list])

# Admin routes - would require admin role check in a real application
@products.route('/admin/products')
@login_required
def admin_products():
    # This would be restricted to admin users in a real application
    products_list = Product.query.all()
    return render_template('admin/products.html', products=products_list)

@products.route('/orders/update_cart', methods=['POST'])
def update_cart():
    """Handle AJAX requests to update cart quantities"""
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 0))
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        cart[product_id] = quantity
    else:
        if product_id in cart:
            del cart[product_id]
    
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})