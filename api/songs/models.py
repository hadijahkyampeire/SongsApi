from api import db

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))

    def __repr__(self):
        """defines the representation of an object"""
        return "Songs: {}".format(self.title)

    def save(self):
        """defines the save method for the songs"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """defines the delete method for the songs"""
        db.session.delete(self)
        db.session.commit()