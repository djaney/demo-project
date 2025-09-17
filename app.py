import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your model (e.g., User)
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(80))
    visited_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Visit {self.origin}>'


@app.route('/')
def index():  # put application's code here
    visit = Visit(
        origin=request.remote_addr,
        visited_at=datetime.now(),
    )
    db.session.add(visit)
    db.session.commit()
    now = datetime.now()
    visits = db.session.execute(db.select(Visit).order_by(Visit.id.desc()).limit(10)).scalars()

    return render_template("home.html", visits=visits, now=now)


if __name__ == '__main__':
    app.run()
