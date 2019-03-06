from mercy_light import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()
# password_hash = bcrypt.generate_password_hash(pw_in)
# check_isOK = bcrypt.check_password_hash(pw_hash, pw_in)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(64))
    password_hash= db.Column(db.String(128))
    nutrients = db.relationship('Nutrient', backref='user', lazy='dynamic') #

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return "{}  username {} food:{} ".format(self.id, self.username, self.nutrients)

    def check_password(self, pw):
        return bcrypt.check_password_hash(self.password_hash, pw)

    def report_food(self):
        print('Recent food:')
        for eachfood in self.nutrients:
            print(eachfood.item)


class Nutrient(db.Model):

    __tablename__ = 'nutrient'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50))
    n_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    kcal = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, item, kcal=0, fat=0, carbs=0, protein=0, user_id=1):
        self.item = item
        self.kcal = kcal
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.user_id = user_id

    def __repr__():
        return "{}  Nutrient {}: Calories: {}".format(self.id, self.item,self.kcal)


# class User(db.Model):
#
#     __tablename__ = 'user'
#
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(32))
#     password_hash= db.Column(db.String(128))
#     nutrients = db.relationship('Nutrient', backref='user', lazy='dynamic') #
#
#     def __init__(self, username, email, password_hash):
#         self.username = username
#         self.email = email
#         self.password_hash = password_hash
#
#
#     def __repr__(self):
#         return "{}  username {} food:{} ".format(self.id, self.username, self.nutrients)
#
#     def report_food(self):
#         print('Recent food:')
#         for eachfood in self.nutrients:
#             print(eachfood.item)
