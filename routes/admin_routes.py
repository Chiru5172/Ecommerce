from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.order_model import Order
from models.user_model import User
from models.product_model import Product
from config import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required():
    return current_user.is_authenticated and current_user.is_admin()

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not admin_required():
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    return render_template(
        'admin_dashboard.html',
        users_count=User.query.count(),
        orders_count=Order.query.count(),
        products_count=Product.query.count()
    )

@admin_bp.route('/orders')
@login_required
def view_orders():
    if not admin_required():
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    return render_template('admin_orders.html', orders=Order.query.all())

@admin_bp.route('/users')
@login_required
def view_users():
    if not admin_required():
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    return render_template('admin_users.html', users=User.query.all())

@admin_bp.route('/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    if not admin_required():
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('product.view_products'))

    order = Order.query.get_or_404(order_id)
    order.status = request.form.get('status')
    db.session.commit()
    flash("Order updated successfully!", "success")
    return redirect(url_for('admin.view_orders'))
