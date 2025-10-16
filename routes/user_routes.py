from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.order_model import Order

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, orders=orders)
