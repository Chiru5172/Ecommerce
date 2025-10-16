from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product_model import Product
from config import db

# ✅ Define blueprint
product_bp = Blueprint('product', __name__)

# --- VIEW ALL PRODUCTS ---
@product_bp.route('/products')
def view_products():
    search_query = request.args.get('q')
    category_filter = request.args.get('category')

    products = Product.query

    if search_query:
        products = products.filter(Product.name.ilike(f"%{search_query}%"))

    if category_filter:
        products = products.filter_by(category=category_filter)

    products = products.all()
    return render_template('products.html', products=products)

# --- ADD PRODUCT (ADMIN ONLY) ---
@product_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not getattr(current_user, 'is_admin', False):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            image_url = request.form['image_url']

            new_product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                image_url=image_url
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('product.view_products'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding product: {str(e)}", "danger")

    return render_template('add_product.html')

# --- DELETE PRODUCT (ADMIN ONLY) ---
@product_bp.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    if not getattr(current_user, 'is_admin', False):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting product: {str(e)}", "danger")

    return redirect(url_for('product.view_products'))
