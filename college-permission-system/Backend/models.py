from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PermissionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    letter = db.Column(db.Text, nullable=True)

def init_db():
    db.create_all()
