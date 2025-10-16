from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.order_model import Order
from models.user_model import User
from models.product_model import Product
from config import db

admin_bp = Blueprint('admin', __name__)

# --- Restrict access to admin only ---
def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin():
        flash("Access denied! Admins only.", "danger")
        return False
    return True


# --- Admin Dashboard ---
@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if not admin_required():
        return redirect(url_for('product.view_products'))
    
    users_count = User.query.count()
    orders_count = Order.query.count()
    products_count = Product.query.count()

    return render_template('admin_dashboard.html',
                           users_count=users_count,
                           orders_count=orders_count,
                           products_count=products_count)


# --- View All Orders ---
@admin_bp.route('/admin/orders')
@login_required
def view_orders():
    if not admin_required():
        return redirect(url_for('product.view_products'))
    
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)


# --- Update Order Status ---
@admin_bp.route('/admin/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    if not admin_required():
        return redirect(url_for('product.view_products'))
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    order.status = new_status
    db.session.commit()
    flash("Order status updated successfully!", "success")
    return redirect(url_for('admin.view_orders'))


# --- View All Users ---
@admin_bp.route('/admin/users')
@login_required
def view_users():
    if not admin_required():
        return redirect(url_for('product.view_products'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)
