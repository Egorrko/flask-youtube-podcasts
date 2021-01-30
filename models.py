from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
