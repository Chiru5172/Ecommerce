from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from flask_login import login_required, current_user
from models.product_model import Product
from models.order_model import Order
from config import db

cart_bp = Blueprint('cart', __name__)

# --- Initialize cart in session ---
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

# --- Add product to cart ---
@cart_bp.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    init_cart()
    product = Product.query.get_or_404(product_id)
    cart = session['cart']

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1
        }

    session['cart'] = cart
    flash(f"{product.name} added to cart!", "success")
    return redirect(request.referrer or url_for('product.view_products'))

# --- View cart page ---
@cart_bp.route('/cart')
@login_required
def view_cart():
    init_cart()
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

# --- Remove item from cart ---
@cart_bp.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        flash("Item removed from cart.", "info")

    return redirect(url_for('cart.view_cart'))

# --- Checkout (POST method) ---
@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('product.view_products'))

    try:
        # Loop through cart items
        for product_id, item in cart.items():
            product = Product.query.get(int(product_id))
            if not product:
                flash(f"Product ID {product_id} not found.", "danger")
                continue

            # Optional: Stock check
            if hasattr(product, 'stock') and item['quantity'] > product.stock:
                flash(f"Not enough stock for {product.name}. Available: {product.stock}", "danger")
                continue

            # Reduce stock
            if hasattr(product, 'stock'):
                product.stock -= item['quantity']

            # Create order
            order = Order(
                user_id=current_user.id,
                product_id=int(product_id),
                quantity=item['quantity'],
                status="Confirmed"
            )
            db.session.add(order)

        db.session.commit()
        session['cart'] = {}  # Clear cart after successful checkout
        flash("Order placed successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error placing order: {str(e)}", "danger")

    return redirect(url_for('product.view_products'))
@cart_bp.route('/view_checkout')
@login_required
def view_checkout():
    init_cart()
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total=total)
