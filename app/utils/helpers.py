# app/utils/helpers.py

import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def save_image(form_picture):
    """
    Save product or user image with a random hex name
    Returns the new filename
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    
    # Resize image
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

def format_price(amount):
    """
    Format price to currency display
    """
    return "${:,.2f}".format(amount)

def get_or_create_csrf_token():
    """
    Get or create a CSRF token for form protection
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

def validate_csrf_token(form_token):
    """
    Validate that the submitted CSRF token matches the one in session
    """
    session_token = session.get('csrf_token', '')
    return secrets.compare_digest(session_token, form_token)

def send_order_confirmation_email(order, user):
    """
    Send order confirmation email to user
    (This would connect to an email service in production)
    """
    subject = f"Emmanuelibok - Order #{order.id} Confirmation"
    sender = "noreply@emmanuelibok.com"
    recipient = user.email
    
    # In a real application, you would use a service like Flask-Mail
    # Example is available upon request
    
    print(f"Email would be sent to {recipient} with subject: {subject}")
    return True

def calculate_shipping_cost(total_amount, country_code='US'):
    """
    Calculate shipping cost based on order total and country
    """
    if total_amount >= 100:
        return 0  # Free shipping for orders above $100
    
    # Base shipping rates by country code
    shipping_rates = {
        'US': 10.00,
        'CA': 15.00,
        'GB': 25.00,
        'AU': 30.00,
        # Add more countries as needed
    }
    
    # Default to US shipping rate if country not found
    return shipping_rates.get(country_code, shipping_rates['US'])

def paginate_query(query, page, per_page=12):
    """
    Helper to paginate query results
    """
    return query.paginate(page=page, per_page=per_page, error_out=False)

def get_filter_params(request):
    """
    Extract and validate filter parameters from request
    """
    filters = {}
    
    # Extract min and max price
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    if min_price is not None:
        filters['min_price'] = min_price
    if max_price is not None:
        filters['max_price'] = max_price
    
    # Extract stock filter
    in_stock = request.args.get('in_stock')
    if in_stock:
        filters['in_stock'] = True
    
    # Extract sorting
    sort = request.args.get('sort', 'newest')
    filters['sort'] = sort
    
    return filters