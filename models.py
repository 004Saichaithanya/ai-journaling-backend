from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
