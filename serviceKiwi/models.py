from ext import db

class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(256), nullable = False)
    price = db.Column(db.Float, nullable=False)

    def __str__(self):
        return self.location
