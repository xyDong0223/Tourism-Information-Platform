from serviceBooking.ext import db

#create a table for flights
class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(256), nullable = False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(256), nullable = False)
    plan_type = db.Column(db.String(20), nullable = False)

    def __str__(self):
        return self.location

