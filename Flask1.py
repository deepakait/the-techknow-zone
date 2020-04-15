from flask import Flask, render_template, request
import pymysql.cursors
import json
from datetime import datetime
from flask_mail import Mail
import uuid

para = {}
with open('config.json','r') as c:
    para = json.load(c)["para"]

d_h = para['dev']['database_host']
d_u = para['dev']['database_user']
d_p = para['dev']['database_password']
d_n = para['dev']['database_name']

app = Flask(__name__)
db = pymysql.connect(f"{d_h}", f"{d_u}", f"{d_p}", f"{d_n}")

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=para['gmail_sender'],
    MAIL_PASSWORD=para['gmail_password']
)

mail = Mail(app)


@app.route("/")
def home():

    return render_template('index.html', para=para)



@app.route("/about")
def about():

    return render_template('about.html', para=para)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        ''' Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        '''
            S_no , Name , Email , Phone_No , Msg , Date
        '''

        cursor = db.cursor()
        sql = "INSERT INTO CONTACTS(Name , Email , Phone_No , Msg , Date) VALUES (%s, %s, %s, %s, %s)"
        print("========================")
        print(sql)
        print("========================")
        print(cursor.execute(sql, (name, email, phone, message, datetime.now())))
        db.commit()
        # mail.send_message("name    sdsdfsdfsdfsdf",
        #                   from_addr=[para['gmail_user']],
        #                   to_addrs=email,
        #                   body=message
        #                   )


        mail.send_message('New message from'+ name,
                      sender=para['gmail_sender'],
                      recipients=para['gmail_receiver'],
                      body=message + "\n" + phone)

    return render_template('contact.html', para=para)


@app.route("/home")
def index():

    return render_template('index.html', para=para)


@app.route("/index")
def ind():
    cursor = db.cursor()
    sql = "SELECT title, content, date, image_file from posts"
    cursor.execute(sql)
    post = cursor.fetchmany(10)
    blog_posts = []

    for row in post:
        post1 = {
            'date': row[2],
            'content': row[1],
            'title': row[0],
            'image_file': row[3]
        }
        blog_posts.append(post1)

    return render_template('index.html', para=para, blog_posts=blog_posts)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    cursor = db.cursor()
    sql = "SELECT title, content, date, image_file from posts where slug=%s"
    cursor.execute(sql, (post_slug))
    post = cursor.fetchone()
    post1 = {
        'date': post[2],
        'content': post[1],
        'title': post[0],
        'image_file': post[3]
    }

    print(post1)
    return render_template('post.html', para=para, post=post1)


@app.route("/sample_post",methods=['GET', 'POST'])
def sample_post():

    if (request.method == 'POST'):
        ''' Add published Post entry to the database'''
        title = request.form.get('title')
        content = request.form.get('content')
        phone = request.form.get('phone')
        subheading = request.form.get('subheading')

        '''
            Sno , title ,subheading, slug , content , date , phone
        '''

        cursor = db.cursor()
        sql = "INSERT INTO posts (title, content , phone , slug, subheading, date) VALUES (%s, %s, %s, %s, %s, %s)"
        print("========================")
        random = str(uuid.uuid1())
        print(cursor.execute(sql, (title, content, phone, title + random, subheading, datetime.now())))
        db.commit()
    return render_template('sample post.html', para=para)


app.run(debug=True)
