from flask import *
from flask_sqlalchemy import *
from sqlalchemy.orm import *
from flask_login import *
from hashlib import *
import os

secret_key = 'c9a8585f8f84621a1e0c6841121bb08f11cb4377d8c569a42b95871bd56c3893'
app = Flask(__name__)
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

try:
    class Base(DeclarativeBase):
        pass
except:
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tg = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    class_number = db.Column(db.Integer, nullable=False)
    author_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<items %r>' % self.itemid


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/login/<string:name>', methods=['GET', 'POST'])
def login(name):
    if request.method == 'POST' and list(request.values.values())[1] == secret_key:
        if not User.query.filter_by(tg=list(request.values.values())[0]).first():
            new_user = User(tg=list(request.values.values())[0])
            db.session.add(new_user)
            db.session.commit()
    if name:
        user = User.query.filter_by(tg=name).first()
        login_user(user)
    return redirect('/')


@app.route('/subject/<int:ch>/<string:obj>', methods=['GET', 'POST'])
def subject(ch, obj):
    item = items.query.all()
    return render_template('subject.html', changer=ch, object=obj, item=item)


@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        file = request.files['file']
        subject = request.form['subject']
        class_number = request.form['class_number']
        descr = request.form['descr']
        cost = request.form['cost']
        if file.filename == '':
            return redirect('/user_profile')
        else:
            if file_type(file.content_type) != 'no_type':
                file.save('static/uploaded_files/' + file.filename)
                item = items(subject=subject, class_number=class_number, description=descr, cost=cost, author_name=current_user.tg)
                db.session.add(item)
                db.session.commit()
            else:
                pass
    return render_template('user_profile.html')


def file_type(ftype):
    a = ['pdf', 'doc', 'docx', 'txt', 'image']
    for i in a:
        if i in ftype:
            return i
    return 'no_type'


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
