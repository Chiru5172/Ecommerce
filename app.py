from flask import render_template
from config import app, db
from models import User, Product, Order
from routes.auth_routes import auth_bp, login_manager
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp  # 👈 NEW
from routes.user_routes import user_bp

# Initialize login manager
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp) 

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("✅ Tables verified and ready.")
    app.run(debug=True)
