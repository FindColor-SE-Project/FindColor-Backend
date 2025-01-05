import base64

from backend.database.Database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) #เวลาที่ไฟล์ถูกอัปโหลด
    seasonColorTone = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'image_data': base64.b64encode(self.image_data).decode('utf-8'),  # ถ้าต้องการแปลงเป็น Base64
            'created_at': self.created_at,
            'seasonColorTone': self.seasonColorTone
        }