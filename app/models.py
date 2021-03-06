import enum
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def to_dict(self, include_email=False, include_address=False):
        data = {
            "id": self.id,
            "username": self.username
        }
        if include_email:
            data['email'] = self.email
        if include_address:
            data['address'] = self.address
        return data
    
    def from_dict(self, data):
        for info in ['username', 'email', 'address']:
            if info in data:
                setattr(self, info, data[info])

    def __repr__(self):
        return f"<User: {self.username}>"

class Quality(enum.Enum):
    standard = 'standard'
    superior = 'superior'
    deluxe = 'deluxe'

class BBQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.Enum(Quality))
    instock = db.Column(db.Boolean)
    package = db.Column(db.String(100))

    def __repr__(self):
        return f"<BBQ quality: {self.quality}>"
