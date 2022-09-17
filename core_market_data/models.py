from . import db,bcrypt
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id =db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    email_address=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(100),nullable=False)
    budget=db.Column(db.Integer(),nullable=False, default=1000)
    items_owned=db.relationship('Items',backref="owned_user",lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    def can_sell(self,item_obj):
        return item_obj in self.items_owned

class Items(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=200),nullable=False, unique=True)
    price=db.Column(db.Float(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False)
    description=db.Column(db.String(length=200),nullable=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Item : {self.name}"

    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()