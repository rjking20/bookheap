from flask import Flask, flash, render_template, request, url_for, session, redirect
import dbHandler as db
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime

UPLOAD = 'static/image'
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=2)
lan = None


@app.route('/')
def index():
    time = datetime.now()
    greet = ''
    hour = int(time.strftime('%H'))

    if lan == 'english':
        if hour < 12:
            greet = 'Good Morning'
        elif hour < 17:
            greet = 'Good Afternoon'
        else:
            greet = 'Good Evening'
    elif lan == 'hindi':
        if hour < 12:
            greet = 'सुप्रभात'
        elif hour < 17:
            greet = 'शुभ दिन'
        else:
            greet = 'शुभ संध्या'

    if 'user' in session:
        user = session['user']
        return render_template('index.html', books=[db.col2.estimated_document_count(), db.get_book()], user=user,
                               greet=greet, lan=lan)
    else:
        return redirect('login')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('register.html')


# ------------------ Register ------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        try:

            name = request.form.get('name')
            passwd = request.form.get('pass')

            try:
                db.insert_user(name, passwd)

            except:
                pass



        except:
            pass

    return redirect('/signup')


# ------------------- Login ----------------------

@app.route('/login', methods=['POST', 'GET'])
def login():
    global lan
    if request.method == 'POST':

        name = request.form.get('name')
        passwd = request.form.get('pass')
        lan = request.form.get('radio')
        session["user"] = name
        values = db.get_user()

        for value in values:

            if value['name'] == name and value['password'] == passwd:
                return redirect('/')

    return redirect(url_for('signin'))


# ---------------- Logout -----------------

@app.route('/logout')
def logout():
    global lan
    session.pop('user', None)
    lan = None
    return redirect('/')


ALLOWED = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


# -------------- userdata---------------------

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if session['user'] == 'admin':
        return render_template('userdata.html', data=enumerate(db.get_user()))
    else:
        return redirect('/error')


# ------------------imgdata----------------------

@app.route('/imgdata', methods=['GET', 'POST'])
def imgdata():
    if session['user'] == 'admin':
        return render_template('imgdata.html', data=enumerate(db.get_book()))
    else:
        return redirect('/error')


# ------- Add and update user data---------------

@app.route('/addupdate', methods=['POST'])
def addupdate():
    if request.method == 'POST':
        nam = request.form.get('name')
        passwd = request.form.get('pass')

        if nam is not None and passwd is not None:
            if request.form['btn'] == 'add':
                db.insert_user(nam, passwd)
                flash('New user is added')
            if request.form['btn'] == 'update':
                db.update_user(nam, passwd)
                flash('Password is updated')
        else:
            flash("Don't leave any field empty")

        redirect('/userdata')

    return redirect('/userdata')


# ----- Add and update book data-------------------

@app.route('/bookdata', methods=['POST'])
def bookdata():
    if request.method == 'POST':

        file = request.files['files']
        url = request.form['urls']
        filename = secure_filename(file.filename)
        if file != '' and url != '':
            if file and allowed_files(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.insert_book(file.filename, url)
                flash('Image Data inserted')

            else:
                flash('Invalid upload only txt, pdf, png, jpg, jpeg, gif')
        else:
            flash('Fields are empty')
            redirect('/imgdata')
    return redirect('/imgdata')


# ---------------delete user ----------------

@app.route('/deleteuser/<name>')
def deleteuser(name):
    db.delete_user(name)
    flash('Data is deleted')
    return redirect('/userdata')


# -----------------delete image-----------------

@app.route('/deleteimg/<img>')
def deleteimg(img):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img))
    db.delete_book(img)
    flash('Image Data is deleted')
    return redirect('/imgdata')


# ------------------- error -----------------------

@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8085)
