from flask import Flask, render_template, request, session, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random, copy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///teacher.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'abc'

db = SQLAlchemy(app)

class addQuiz(db.Model):
	id = db.Column('quiz_id', db.Integer, primary_key = True)
	teacher= db.Column(db.String(100))
	subject = db.Column(db.String(100))
	q1 = db.Column(db.String(50))
	q1o1 = db.Column(db.String(50))
	q1o2 = db.Column(db.String(50))
	q1o3 = db.Column(db.String(50))
	q1o4 = db.Column(db.String(50))
	q1ans = db.Column(db.Integer)

	q2 = db.Column(db.String(50))
	q2o1 = db.Column(db.String(50))
	q2o2 = db.Column(db.String(50))
	q2o3 = db.Column(db.String(50))
	q2o4 = db.Column(db.String(50))
	q2ans = db.Column(db.Integer)

	q3 = db.Column(db.String(50))
	q3o1 = db.Column(db.String(50))
	q3o2 = db.Column(db.String(50))
	q3o3 = db.Column(db.String(50))
	q3o4 = db.Column(db.String(50))
	q3ans = db.Column(db.Integer)

	q4 = db.Column(db.String(50))
	q4o1 = db.Column(db.String(50))
	q4o2 = db.Column(db.String(50))
	q4o3 = db.Column(db.String(50))
	q4o4 = db.Column(db.String(50))
	q4ans = db.Column(db.Integer)

	q5 = db.Column(db.String(50))
	q5o1 = db.Column(db.String(50))
	q5o2 = db.Column(db.String(50))
	q5o3 = db.Column(db.String(50))
	q5o4 = db.Column(db.String(50))
	q5ans = db.Column(db.Integer)


class feedbacks(db.Model):
	id = db.Column('student_id', db.Integer, primary_key = True)
	fname = db.Column(db.String(100))
	lname = db.Column(db.String(20))
	email = db.Column(db.String(20)) 
	comm = db.Column(db.String(100))

class teacher(db.Model):
	id = db.Column('teacher_id', db.Integer, primary_key = True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(50))  

@app.route('/')
def home():
	t = teacher.query.all()
	return render_template('home.html',t=t)

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form.get('username')
		password = request.form.get('password')
		t = teacher(username=name,password=password)
		db.session.add(t)
		db.session.commit()
		return redirect('login1')
	return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		name = request.form.get('username')
		password = request.form.get('password')
		t = teacher.query.filter_by(username=name,password=password).first()
		if t:
			session['user'] = name
			return redirect('add')
		return "Error you need to sign-up first"
	return render_template('login.html')
	
@app.route('/account/<string:name>',methods=['GET','POST'])
def account(name):
	if g.user:
		t = teachers.query.filter_by(username=g.user).first()
		return render_template('account.html',u=s)
	return 'You need to login first'

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')

@app.before_request
def before_request():
	g.user=None

	if 'user' in session:
		g.user = session['user']


@app.route('/about')
def about():
	 return render_template("about.html")

@app.route('/contact',methods=['GET','POST'])
def contact():
	if request.method == 'POST':
		if not request.form['fname'] or not request.form['lname'] or not request.form['email'] or not request.form['comm']:
			flash('Please enter all the fields', 'error')
		else:
			feedback = feedbacks(fname = request.form['fname'],lname= request.form['lname'], email=request.form['email'], comm= request.form['comm'])
			
			db.session.add(feedback)
			db.session.commit()
			flash('Record was successfully added')
			return redirect(url_for('show'))
	return render_template('contact.html')


@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
	if request.method == 'POST':
		name = request.form.get('name')
		password = request.form.get('pass')
		if name == 'admin' and password == 'admin123':
			session['user'] = name
			return redirect(url_for('admin'))
		else:
			return 'unmatched {} and {}'.format(name,password)
	return 'This is get'
	
@app.route('/admin',methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		if g.user == 'admin':
			t = Teacher.query.all()
			return render_template('admin.html',t=t,log=1)
		return render_template('admin.html',log=0)
	else:
		if g.user == 'admin':
			t = teacher.query.all()
			return render_template('admin.html',t=t,log=1)
		return render_template('admin.html',log=0)


@app.route('/adminQ/<string:uname>')
def adminQ(uname):
	q = Quiz.query.filter_by(creator=uname).all()
	return render_template('adminQ.html',q=q)

@app.route('/adminQQ/<string:uname>/<string:uid>')
def adminQQ(uname,uid):
	q = Quiz.query.filter_by(creator=uname,url_id=uid).first()
	ans = Ans.query.filter_by(of=uid).all()
	return render_template('adminQQ.html',q=q,ans=ans)

@app.route('/')
def show_all():
	return render_template('show.html')

@app.route('/login1')
def login1():
	return render_template('login1.html')


@app.route('/add',methods=['GET','POST'])
def add():
	if request.method == 'POST':
		name = request.form.get('name')
		subject = request.form.get('subject')
		q1 = request.form.get('q1')
		ans1 = request.form.get('q1o')
		q1o1 = request.form.get('q1o1')
		q1o2 = request.form.get('q1o2')
		q1o3 = request.form.get('q1o3')
		q1o4= request.form.get('q1o4')

		q2 = request.form.get('q2')
		ans2 = request.form.get('q2o')
		q2o1 = request.form.get('q2o1')
		q2o2 = request.form.get('q2o2')
		q2o3 = request.form.get('q2o3')
		q2o4= request.form.get('q2o4')

		q3 = request.form.get('q3')
		ans3 = request.form.get('q3o')
		q3o1 = request.form.get('q3o1')
		q3o2 = request.form.get('q3o2')
		q3o3 = request.form.get('q3o3')
		q3o4= request.form.get('q3o4')

		q4 = request.form.get('q4')
		ans4 = request.form.get('q4o')
		q4o1 = request.form.get('q4o1')
		q4o2 = request.form.get('q4o2')
		q4o3 = request.form.get('q4o3')
		q4o4= request.form.get('q4o4')

		q5 = request.form.get('q5')
		ans5 = request.form.get('q5o')
		q5o1 = request.form.get('q5o1')
		q5o2 = request.form.get('q5o2')
		q5o3 = request.form.get('q5o3')
		q5o4= request.form.get('q5o4')

		q = addQuiz(teacher=name,subject=subject,q1=q1,q1o1=q1o1,q1o2=q1o2,q1o3=q1o3,q1o4=q1o4,q1ans=ans1,
			q2=q2,q2o1=q2o1,q2o2=q2o2,q2o3=q2o3,q2o4=q2o4,q2ans=ans2,q3=q3,q3o1=q3o1,q3o2=q3o2,q3o3=q3o3,q3o4=q3o4,q3ans=ans3,
			q4=q4,q4o1=q4o1,q4o2=q4o2,q4o3=q4o3,q4o4=q4o4,q4ans=ans4)
	return render_template('add.html')



@app.route('/ans')
def ans():
	return render_template('ans.html')


@app.route('/view')
def view():
	return render_template('view.html')


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
	



