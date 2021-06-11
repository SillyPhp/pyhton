from flask import Flask, render_template, request, session, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.secret_key = 'abc'

db = SQLAlchemy(app)

class Teacher(db.Model):
	id = db.Column('teacher_id', db.Integer, primary_key = True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(50)) 

class Quiz(db.Model):
	id = db.Column('quiz_id', db.Integer, primary_key = True)
	url_id = db.Column(db.String(20))
	subject = db.Column(db.String(50))
	Note = db.Column(db.String(200))
	creator = db.Column(db.String(50))
	q1 = db.Column(db.String(50))
	q2 = db.Column(db.String(50))
	q3 = db.Column(db.String(50))
	q4 = db.Column(db.String(50))
	q5 = db.Column(db.String(50))
	q6 = db.Column(db.String(50))
	q7 = db.Column(db.String(50))
	q8 = db.Column(db.String(50))
	q9 = db.Column(db.String(50))
	q10 = db.Column(db.String(50))
	a1 = db.Column(db.Integer)
	a2 = db.Column(db.Integer)
	a3 = db.Column(db.Integer)
	a4 = db.Column(db.Integer)
	a5 = db.Column(db.Integer)
	a6 = db.Column(db.Integer)
	a7 = db.Column(db.Integer)
	a8 = db.Column(db.Integer)
	a9 = db.Column(db.Integer)
	a10 = db.Column(db.Integer)
	q1o1 = db.Column(db.String(20))
	q1o2 = db.Column(db.String(20))
	q1o3 = db.Column(db.String(20))
	q1o4 = db.Column(db.String(20))
	q2o1 = db.Column(db.String(20))
	q2o2 = db.Column(db.String(20))
	q2o3 = db.Column(db.String(20))
	q2o4 = db.Column(db.String(20))
	q3o1 = db.Column(db.String(20))
	q3o2 = db.Column(db.String(20))
	q3o3 = db.Column(db.String(20))
	q3o4 = db.Column(db.String(20))
	q4o1 = db.Column(db.String(20))
	q4o2 = db.Column(db.String(20))
	q4o3 = db.Column(db.String(20))
	q4o4 = db.Column(db.String(20))
	q5o1 = db.Column(db.String(20))
	q5o2 = db.Column(db.String(20))
	q5o3 = db.Column(db.String(20))
	q5o4 = db.Column(db.String(20))
	q6o1 = db.Column(db.String(20))
	q6o2 = db.Column(db.String(20))
	q6o3 = db.Column(db.String(20))
	q6o4 = db.Column(db.String(20))
	q7o1 = db.Column(db.String(20))
	q7o2 = db.Column(db.String(20))
	q7o3 = db.Column(db.String(20))
	q7o4 = db.Column(db.String(20))
	q8o1 = db.Column(db.String(20))
	q8o2 = db.Column(db.String(20))
	q8o3 = db.Column(db.String(20))
	q8o4 = db.Column(db.String(20))
	q9o1 = db.Column(db.String(20))
	q9o2 = db.Column(db.String(20))
	q9o3 = db.Column(db.String(20))
	q9o4 = db.Column(db.String(20))
	q10o1 = db.Column(db.String(20))
	q10o2 = db.Column(db.String(20))
	q10o3 = db.Column(db.String(20))
	q10o4 = db.Column(db.String(20))


class Ans(db.Model):
	id = db.Column('ans_id', db.Integer, primary_key = True)
	of = db.Column(db.String(20))
	name = db.Column(db.String(20))
	rollno = db.Column(db.String(20))
	score = db.Column(db.Integer)

@app.route('/')
def home():
	if g.user:
		return render_template('home.html',log=1)
	return render_template('home.html',log=0)



@app.route('/loginpage')
def loginpage():
	return render_template('login.html')

@app.route('/ind')
def ind():
	return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form.get('name')
		password = request.form.get('password')
		t = Teacher(username=name,password=password)
		db.session.add(t)
		db.session.commit()
		return render_template('home.html',info='Sign-Up success now you can login')
	return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		name = request.form.get('lname')
		password = request.form.get('lpassword')
		print(name+' '+password)
		t = Teacher.query.filter_by(username=name,password=password).first()
		if t:
			session['user'] = name
			return redirect(url_for('account'))
		else:
			return render_template('home.html',info='Username or password is incorrect',t=t)
	return render_template('home.html')


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
	

@app.route('/admin')
def admin():
	if g.user == 'admin':
		t = Teacher.query.all()
		return render_template('admin.html',t=t,log=1)
	else:
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

@app.route('/account')
def account():
	if g.user:
		t = Teacher.query.filter_by(username=g.user).first()
		q = Quiz.query.filter_by(creator=g.user).all()
		return render_template('account.html',t=t,q=q)
	return 'You need to login First !'

@app.route('/logout')
def logout():
	session.pop('user',None)
	return render_template('home.html',info='You have been logged out',log=0)

@app.route('/createQuiz', methods=['GET','POST'])
def createQuiz():
	if request.method == 'POST':
		content = request.json
		subject = content['subject']
		notes = content['notes']
		q1 = content['q1']
		q1a1 = content['q1a1']
		q1a2 = content['q1a2']
		q1a3 = content['q1a3']
		q1a4 = content['q1a4']
		q1ans = content['q1ans']
		q2 = content['q2']
		q2a1 = content['q2a1']
		q2a2 = content['q2a2']
		q2a3 = content['q2a3']
		q2a4 = content['q2a4']
		q2ans = content['q2ans']
		q3 = content['q3']
		q3a1 = content['q3a1']
		q3a2 = content['q3a2']
		q3a3 = content['q3a3']
		q3a4 = content['q3a4']
		q3ans = content['q3ans']
		q4 = content['q4']
		q4a1 = content['q4a1']
		q4a2 = content['q4a2']
		q4a3 = content['q4a3']
		q4a4 = content['q4a4']
		q4ans = content['q4ans']
		q5 = content['q5']
		q5a1 = content['q5a1']
		q5a2 = content['q5a2']
		q5a3 = content['q5a3']
		q5a4 = content['q5a4']
		q5ans = content['q5ans']
		q6 = content['q6']
		q6a1 = content['q6a1']
		q6a2 = content['q6a2']
		q6a3 = content['q6a3']
		q6a4 = content['q6a4']
		q6ans = content['q6ans']
		q7 = content['q7']
		q7a1 = content['q7a1']
		q7a2 = content['q7a2']
		q7a3 = content['q7a3']
		q7a4 = content['q7a4']
		q7ans = content['q7ans']
		q8 = content['q8']
		q8a1 = content['q8a1']
		q8a2 = content['q8a2']
		q8a3 = content['q8a3']
		q8a4 = content['q8a4']
		q8ans = content['q8ans']
		q9 = content['q9']
		q9a1 = content['q9a1']
		q9a2 = content['q9a2']
		q9a3 = content['q9a3']
		q9a4 = content['q9a4']
		q9ans = content['q9ans']
		q10 = content['q10']
		q10a1 = content['q10a1']
		q10a2 = content['q10a2']
		q10a3 = content['q10a3']
		q10a4 = content['q10a4']
		q10ans = content['q10ans']
		url_id = shortuuid.ShortUUID().random(length=4)
		q = Quiz(subject=subject,Note=notes,creator=g.user,
			q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=q10,
			a1=q1ans,a2=q2ans,a3=q3ans,a4=q4ans,a5=q5ans,a6=q6ans,a7=q7ans,a8=q8ans,a9=q9ans,a10=q10ans,
			q1o1=q1a1,q1o2=q1a2,q1o3=q1a3,q1o4=q1a4,
			q2o1=q2a1,q2o2=q2a2,q2o3=q2a3,q2o4=q2a4,
			q3o1=q3a1,q3o2=q3a2,q3o3=q3a3,q3o4=q3a4,
			q4o1=q4a1,q4o2=q4a2,q4o3=q4a3,q4o4=q4a4,
			q5o1=q5a1,q5o2=q5a2,q5o3=q5a3,q5o4=q5a4,
			q6o1=q6a1,q6o2=q6a2,q6o3=q6a3,q6o4=q6a4,
			q7o1=q7a1,q7o2=q7a2,q7o3=q7a3,q7o4=q7a4,
			q8o1=q8a1,q8o2=q8a2,q8o3=q8a3,q8o4=q8a4,
			q9o1=q9a1,q9o2=q9a2,q9o3=q9a3,q9o4=q9a4,
			q10o1=q10a1,q10o2=q10a2,q10o3=q10a3,q10o4=q10a4,
			url_id=url_id
			)
		db.session.add(q)
		db.session.commit()
		return 'question paper created successfully {}'.format(url_id)
	if g.user:
		return render_template('createQuiz.html')
	else:
		return render_template('error.html',error='You need to login first')


@app.route('/checkres', methods=['GET','POST'])
def checkres():
	if request.method == 'POST':
		score = 0
		content = request.json
		a1 = content['a1']
		a2 = content['a2']
		a3 = content['a3']
		a4 = content['a4']
		a5 = content['a5']
		a6 = content['a6']
		a7 = content['a7']
		a8 = content['a8']
		a9 = content['a9']
		a10 = content['a10']
		url_id = content['uid']
		name = content['name']
		rollno = content['roll']
		q = Quiz.query.filter_by(url_id=url_id).first()
		if a1 == q.a1:
			score+=1
		if a2 == q.a2:
			score+=1
		if a3 == q.a3:
			score+=1
		if a4 == q.a4:
			score+=1
		if a5 == q.a5:
			score+=1
		if a6 == q.a6:
			score+=1
		if a7 == q.a7:
			score+=1
		if a8 == q.a8:
			score+=1
		if a9 == q.a9:
			score+=1
		if a10 == q.a10:
			score+=1
		a = Ans(of=url_id,name=name,rollno=rollno,score=score)
		db.session.add(a)
		db.session.commit()
		return 'Success your score is : {}'.format(score)
	return 'You cannot access this page...'

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/chooseRes')
def chooseRes():
	q = Quiz.query.filter_by(creator=g.user).all()
	if q:
		return render_template('chooseRes.html',q=q)
	else:
		return 'You have to create a quiz first'

@app.route('/SubRes/<string:uid>')
def SubRes(uid):
	q = Quiz.query.filter_by(url_id=uid).first()
	a = Ans.query.filter_by(of=uid).all()
	if q:
		return render_template('SubRes.html',q=q,a=a)
	else:
		return 'result not found '

@app.route('/showResult/<string:uid>') #7dTV
def showResult(uid):
	q = Quiz.query.filter_by(url_id=uid).first()
	a = Ans.query.filter_by(of=uid).all()
	if q:
		return render_template('result.html',q=q,a=a)
	else:
		return render_template('result.html',q='error')

@app.route('/<string:uid>') #7dTV
def showQuiz(uid):
	q = Quiz.query.filter_by(url_id=uid).first()
	if q:
		return render_template('quiz.html',q=q)
	else:
		return render_template('quiz.html',q='error')


@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)