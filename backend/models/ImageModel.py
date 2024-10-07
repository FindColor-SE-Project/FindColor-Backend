from backend.database.Database import db


class Image(db.Model):
    __bind_keys__ = 'images'
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
