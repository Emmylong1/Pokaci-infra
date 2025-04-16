from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_required, current_user
from app.main.order import Order, OrderItem
from app.main.product import Product
from app import db
import json

orders = Blueprint('orders', __name__, url_prefix='/orders')

@orders.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        if product:
            item_total = product.price * quantity
            total += item_total
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'item_total': item_total
            })
    
    return render_template('cart/cart.html', products=products, total=total)

@orders.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if product.stock < quantity:
        flash('Not enough stock available.')
        return redirect(url_for('products.detail', product_id=product_id))
    
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    session['cart'] = cart
    flash(f'{product.name} added to cart.')
    return redirect(url_for('orders.cart'))

@orders.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Your cart is empty.')
        return redirect(url_for('products.index'))
    
    if request.method == 'POST':
        # Process payment (mock)
        
        # Create order
        total_amount = 0
        for product_id, quantity in cart_items.items():
            product = Product.query.get(product_id)
            if product:
                total_amount += product.price * quantity
        
        order = Order(user_id=current_user.id, total_amount=total_amount, status='paid')
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID
        
        # Create order items
        for product_id, quantity in cart_items.items():
            product = Product.query.get(product_id)
            if product:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                product.stock -= quantity
                db.session.add(item)
        
        db.session.commit()
        session['cart'] = {}
        flash('Order completed successfully!')
        return redirect(url_for('orders.order_history'))
    
    # Calculate items and total for display
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        if product:
            item_total = product.price * quantity
            total += item_total
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'item_total': item_total
            })
    
    return render_template('orders/checkout.html', products=products, total=total)

@orders.route('/history')
@login_required
def order_history():
    orders_list = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/order_history.html', orders=orders_list)