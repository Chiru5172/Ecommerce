from config import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    #image_url = db.Column(db.String(255), nullable=True)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255))
    category = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f"<Product {self.name}>"
