from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product_model import Product
from config import db
import os
from werkzeug.utils import secure_filename
from flask import current_app


# ✅ Define blueprint
product_bp = Blueprint('product', __name__)

# --- VIEW ALL PRODUCTS ---
@product_bp.route('/products')
def view_products():
    products = Product.query.all()

    categories = {}
    for product in products:
        category = product.category if product.category else "Others"
        categories.setdefault(category, []).append(product)

    return render_template('products.html', categories=categories)

# --- ADD PRODUCT (ADMIN ONLY) ---
@product_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin():
        flash("Admins only", "danger")
        return redirect(url_for('product.view_products'))

    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            category=request.form['category'],   # 👈 SAVE CATEGORY
            image=None
        )

        db.session.add(product)
        db.session.commit()
        flash("Product added successfully", "success")
        return redirect(url_for('product.view_products'))

    return render_template('add_product.html')

# --- Edit Product Admin only ---
@product_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin():
        flash("Admins only", "danger")
        return redirect(url_for('product.view_products'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']  # 👈 UPDATE CATEGORY

        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for('product.view_products'))

    return render_template('edit_product.html', product=product)


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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
