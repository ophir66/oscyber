#pip install flasks
#pip install flask-sqlalchemy

from flask import Flask, render_template,request,redirect,send_from_directory
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import time, os, hashlib

SHORT_SECRET_WORD   = "4641864"
SECRET_WORD         = "CyB3raTH3rz0g"               # Cyber At Herzog
SECRET_WORD2        = "CyB3raT15h5h4l0m"		    # Cyber At Ish Shalom
SECRET_WORD3        = "CyB3rYud4l3f15h5h4l0m"       # Cyber Yud Alef Ish Shalom

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

time1 = 0.1
time2 = 0.07

# http://osmlist.pythonanywhere.com/set_time1/0.1
# http://osmlist.pythonanywhere.com/set_time2/0.07


class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id 
    

@app.route('/index',methods=['POST','GET'])
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['passwd']
        return user + ", Dont give ur password with no reason. "  + "*" * len( passwd)
    else:
        return render_template("index.html")


@app.route('/todo',methods=['POST','GET'])
def todo():
    #print("In Todo" + request.method)
    if request.method == 'POST':
        content_task = request.form['content']
        new_task = Todo(content=content_task)
        if new_task.content.strip() == '':
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template("todo.html",tasks=tasks)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except Exception as e:
            return "Error while deal wit db  " + str(e)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("todo.html",tasks=tasks)


@app.route('/galery')
def galery():
    return render_template("galery.html")

 

@app.route('/delete')
def delete_row():
   
    id_to_del = str(request.args.get('id'))
    obj = Todo.query.filter_by(id=id_to_del).one()
    db.session.delete(obj)
    db.session.commit()

    #_to_del = str(request.query_string['id']
   
    return redirect('/todo')

@app.route('/ver')
def ver():
    return "2.2"

@app.route('/set_time1/<val>')
def set_time1(val= ''):
    global time1
    try:
        time1 = float(val)
        return "time1 set"
    except:
        return "FALIED to set time1"

@app.route('/set_time2/<val>')
def set_time2(val= ''):
    global time2
    try:
        time2 = float(val)
        return "time2 set"
    except:
        return "FALIED to set time2"

def check_pass(val, pass_checked):
    if len(val) == 0 or len(val) != len(pass_checked):
        return "0"
    else:
        time.sleep(time1)
        
        for i in range(len(val)):
            time.sleep(time2)
            if pass_checked[i] != val[i]:
                return "0" 
        return "1"

@app.route('/sod/<val>')
def sod(val= ''):
    return check_pass(val, SHORT_SECRET_WORD)

@app.route('/secret/<val>')
def secret(val= ''):
    return check_pass(val, SECRET_WORD)

@app.route('/secret30/<val>')
def secret30(val= ''):
    return check_pass(val, SECRET_WORD2)


@app.route('/bigsecret/<val>')
def bigsecret(val= ''):
    return check_pass(val, SECRET_WORD3)


@app.route('/PassCheck1/<val>')
def PassCheck1(val= ''):
    res = "1"
    SECRET = "112358132134"
    long_pad = '                        '
    pad_in = (long_pad + val)[-len(long_pad):]
    pad_secret = (long_pad + SECRET)[-len(long_pad):]

    for i in range(len(pad_secret)):
        if pad_secret[i] != pad_in[i]:
            time.sleep(0.15)
            res = "0" 
    return res

@app.route('/PassCheck2/<val>')
def PassCheck2(val= ''):
    res = "1"
    SECRET = "223344".encode()
    m1 = hashlib.sha256()
    m1.update(SECRET)
    hashed_pass = m1.digest()
    m2 = hashlib.sha256()
    m2.update(val.encode())
    hashed_in = m2.digest()
    for i in range(len(hashed_pass)):
        if hashed_pass[i] != hashed_in[i]:
            time.sleep(0.15)
            res = "0" 
    return res


'''
@app.route('/sod/<val>')
def sod(val= ''):

    if len(val) == 0 or len(val) != len(SHORT_SECRET_WORD):
        return "0"
    else:
        time.sleep(0.5)
        
        for i in range(len(val)):
            time.sleep(0.2)
            if SHORT_SECRET_WORD[i] != val[i]:
                return "0" 
        return "1"
'''
    

@app.route('/PassCheck1/')
@app.route('/PassCheck2/')
@app.route('/secret/')
@app.route('/sod/')
def secret2():
    return '0'
 

@app.route('/update',methods=['POST','GET'])
def update_row():
    #print ("In UPDATE ----")
    if request.method == 'POST':
        #print ("In POST UPDATE ----")
        new_content_task = request.form['content']
        if new_content_task.strip() == '':
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template("todo.html",tasks=tasks)

        id = str(request.args.get('id'))
        task = Todo.query.filter_by(id=id).one()
        #print ("In POST UPDATE ----")
        task.content = new_content_task
        db.session.commit()
        return redirect('/todo')

    else:
        id = str(request.args.get('id'))
        
        task = Todo.query.filter_by(id=id).one()
        
        #_to_del = str(request.query_string['id']
        #print ("updated id:" + id)
        return render_template("update.html",task=task)


if __name__ == "__main__":
    app.run()
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

