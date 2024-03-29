from db.database import db


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    pipeline = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Model: {self.session_id}\nPipeline: {self.pipeline}"
