from backend.database.Database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.LONGBLOB, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) #เวลาที่ไฟล์ถูกอัปโหลด
    seasonColorTone = db.Column(db.String(255), nullable=True)

