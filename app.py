from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_mail import Mail
import json
import requests
import google.generativeai as genai






with open('templates/config.json','r') as c:
    params=json.load(c)["params"]


app=Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pass']
)

mail=Mail(app)


app.config["SQLALCHEMY_DATABASE_URI"] = params['database_uri']
db = SQLAlchemy(app)


app.secret_key =params['app.secret_key']

# sno,name,phone_num,email,msg,date

@app.context_processor
def inject_username():
    return dict(username=session.get('user'))

class Contact_table(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    phone_num=db.Column(db.String(12),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    msg=db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



class Signup(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(80),nullable=False)
    name=db.Column(db.String(20),nullable=False)
    sname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    pd=db.Column(db.String(12),nullable=False)
    cpd=db.Column(db.String(12),nullable=False)

class Posts(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    slug=db.Column(db.String(25),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=5, minutes=30), nullable=False)
    created=db.Column(db.String(20),nullable=False)
  
@app.route('/')
def show_login():
    return render_template('login.html')



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        user_name=request.form.get('user_name')
        name=request.form.get('First_name')
        sname=request.form.get('sur_name')
        email=request.form.get('email')
        pd=request.form.get('pd')
        cpd=request.form.get('cpd')
        

        if pd==cpd:
            entry=Signup(user_name=user_name,name=name,sname=sname,email=email,pd=pd,cpd=cpd)
            db.session.add(entry)
            db.session.commit()
            session['user_id'] = entry.sno
            session['user'] = entry.user_name
            session['name'] = entry.name
            session['sname'] = entry.sname
            session['email'] = entry.email
            return redirect(url_for('show_home',name=name,sname=sname))
        else:
            return "Password don not match",405
    else:
        return render_template('signup.html')
    
@app.route('/profile')
def profile():
    
    name=session.get('name') + " " + session.get('sname')
    # sname=session.get('sname')
    email=session.get('email')
    username=session.get('user')


    return render_template("profile.html",name=name,email=email,username=username)


@app.route('/home',methods=['GET','POST'])
def show_home():
    name = session.get('name')
    sname = session.get('sname')
    latest_posts = Posts.query.order_by(Posts.date.desc()).limit(2).all() 

    return render_template('home.html',name=name,sname=sname,posts=latest_posts)


@app.route('/login',methods=['GET','POST'])
def show():
    if request.method=='POST':
        username=request.form['username']
        pd=request.form['password']

        user = Signup.query.filter_by(user_name=username, pd=pd).first()
        if user:
           session['user_id']=user.sno
           session['user'] = user.user_name
           session['name'] = user.name
           session['sname'] = user.sname
           session['email'] = user.email
           
           flash("Login successful!", "success")
           return redirect(url_for('show_home'))
        else:
            flash("Invalid username or password", "danger")
            return "Invalid credentials"

@app.route("/edit/<int:sno>",methods=["GET","POST"])
def edit(sno):
    post=Posts.query.filter_by(sno=sno).first()
    if request.method=='POST':
        updated_title=request.form['title']
        updated_slug=request.form['slug']
        updated_content=request.form['content']
        post.title=updated_title
        post.slug=updated_slug
        post.content=updated_content
        date=datetime.now()
        db.session.commit()

        return redirect(url_for('post_specific_route',Post_slug=post.slug))
    return render_template("edit.html",post=post,sno=sno)




@app.route("/post/<string:Post_slug>",methods=["GET"])
def post_specific_route(Post_slug):
    post=Posts.query.filter_by(slug=Post_slug).first()
    
    return render_template("specific_post.html",post=post)




@app.route("/post")
def blogs():
    posts = Posts.query.order_by(Posts.date.desc()).all()
    return render_template("posts.html",posts=posts)


@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=='POST':
        title=request.form.get('title')
        slug=request.form.get('slug')
        content=request.form.get('content')
        created = session.get('user')
        date=datetime.now()
        entry=Posts(title=title,slug=slug,content=content,date=date,created=created)
        db.session.add(entry)
        db.session.commit()

    return render_template("create.html",)

@app.route("/delete/<int:sno>",methods=["GET","POST"])
def delete(sno):
    Posts.query.filter_by(sno=sno).delete()
    db.session.commit()
    return redirect(url_for('My_blogs'))

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=session['name']
        number=request.form.get('number')
        email=session['email']
        message=request.form.get('message')
        entry=Contact_table(name=name,phone_num=number,email=email,msg=message)
        date=datetime.now()
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New msg from  ' + name + ' via blog',
            sender=email,
            recipients=[params['gmail-user']],
            body=f"""
            Name:{name}
            Email:{email}
            Number:{number}
            Message:{message}
            """
            

        )
    return render_template("contact.html")

@app.route("/myblogs")
def My_blogs():
    posts=Posts.query.filter_by(created=session.get('user'))
    return render_template("my_blogs.html",posts=posts)

@app.route("/logout")
def del_log():
    session.clear()
    session.pop('user_id', None)
    return redirect(url_for('show_login'))

if __name__=='__main__':
    app.run(debug=False)