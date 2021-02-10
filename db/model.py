from db.database import db


class Model(db.Model):
    id = db.Column(db.Text, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    pipeline = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Model: {self.id}\nPipeline: {self.pipeline}"
