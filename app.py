from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your model (e.g., User)
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(80))
    verified = db.Column(db.Boolean)
    visited_at = db.Column(db.DateTime)


    def __repr__(self):
        return f'<Visit {self.origin}>'

@app.route('/')
def index():  # put application's code here
    if request.headers.getlist("X-Forwarded-For"):
        # The first IP in the list is usually the client's
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr
    visit = Visit(
        origin=client_ip,
        visited_at=datetime.now(),
    )
    db.session.add(visit)
    db.session.commit()
    now = datetime.now()
    visits = db.session.execute(db.select(Visit).order_by(Visit.id.desc()).limit(10)).scalars()

    return render_template("home.html", visits=visits, now=now)

@app.route('/verify', methods=['POST'])
def verify():
    visit = db.session.execute(
        db.select(Visit).filter_by(verified=None).limit(1)
    ).scalar_one_or_none()
    if visit:
        visit.verified = True
        db.session.commit()
    return "OK"


if __name__ == '__main__':
    app.run()
