from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
    

app = Flask(__name__)



ENV = 'dev'

if ENV == 'prod':
    app.debug = False
   
   
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bslycyrfrrvmrz:343157231f37ee75fe0e916f0d1fe50de5653c6bda0b48b1503bdc41714ee0c0@ec2-52-207-93-32.compute-1.amazonaws.com:5432/df7fjp82tkqml2'

    
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost/citizendb'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '@G33k'

db = SQLAlchemy(app)


class Citizens(db.Model): 
    __tablename__ = "citizens"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120))
    phonenumber = db.Column(db.String(120), unique=True)
    residence = db.Column(db.String())
    district = db.Column(db.String(), unique=True)
    region = db.Column(db.String(120), unique=True)
    visitedcountry = db.Column(db.String)
    covidcontact = db.Column(db.String())
    myfever = db.Column(db.String(10))
    myheadache = db.Column(db.String(10))
    mycough = db.Column(db.String(10))
    mysorethroat = db.Column(db.String(10))
    mygeneralweakness = db.Column(db.String(10))
    mybreathing = db.Column(db.String(10))
    myothersymptoms = db.Column(db.String())
      

    def __init__(self, fullname, phonenumber, residence, district, region, visitedcountry, contactcase, myfever, myheadache, mycough, mysorethroat, mygeneralweakness, mybreathing, myothersymptoms):
        self.fullname = fullname
        self.phonenumber = phonenumber
        self.residence = residence
        self.district = district
        self.region = region
        self.visitedcountry = visitedcountry
        self.covidcontact = covidcontact
        self.myfever = myfever
        self.myheadache = myheadache
        self.mycough = mycough
        self.mysorethroat = mysorethroat
        self.mygeneralweakness = mygeneralweakness
        self.mybreathing = mybreathing
        self.myothersymptoms = myothersymptoms

class Employees(db.Model): 
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    phonenumber = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    role = db.Column(db.Integer())

    def __init__(self, firstname, lastname, email, phonenumber, password, role):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phonenumber = phonenumber
        self.password = password
        self.role = role
      
   
# Routes for the citizens
@app.route('/', methods=['GET'])
def home():
    # this is travellers page
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')

# Insert a new citizen
@app.route('/citizen', methods=['POST'])
def citizen():
    if request.method == 'POST':
        # check if the form is empty   
        myname = request.form['myname']
        myphone = request.form['myphone']
        myresidence = request.form['myresidence']
        mydistrict = request.form['mydistrict']
        myregion = request.form['myregion']
        mycountryvisit = request.form['mycountryvisit']
        mycovidcontact = request.form['mycovidcontact']
        myfever = request.form.get('myfever') 
        myheadache = request.form.get('myheadache') 
        mycough = request.form.get('mycough') 
        mysorethroat = request.form.get('mysorethroat') 
        mygeneralweakness = request.form.get('mygeneralweakness')
        mybreathing = request.form.get('mybreathing')
        myothersymptoms = request.form.get('myothersymptoms')
        #test whether we receive the entire form
        print(myname,myphone,myresidence,mydistrict,myregion,mycountryvisit,mycovidcontact,myfever,myheadache,mycough,mysorethroat,mygeneralweakness,mybreathing,myothersymptoms)
      
        if  db.session.query(Citizens).filter(Citzens.myphone == myphone).count() == 0:
            citizen = Citizens(myname,myphone,myresidence,mydistrict,myregion,mycountryvisit,mycovidcontact,myfever,myheadache,mycough,mysorethroat,mygeneralweakness,mybreathing,myothersymptoms)
            db.session.add(citizen)
            db.session.commit()
            #print
            return render_template("success.html")
        else:
            return render_template("index.html", message="You have already registered, MOH personnel will get back to you shortly")
    return render_template("index.html")
        

@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        username = request.form['username']
        userpasswd = request.form['userpasswd']
        #print user & passwd
        #print(username, userpasswd)
        #check whether empty
        if username =='' or userpasswd == '':
            return render_template("user.html")
        if db.session.query(Employees).filter(Employees.email == username and Employees.password == userpasswd).count() ==1:
            return redirect(url_for('userdash'))
    return render_template("user.html")

@app.route('/userdash', methods=['POST', 'GET'])
def userdash():
    all_data = Travellers.query.all()   
    return render_template('userdash.html', travellers = all_data)

if __name__ == "__main__":
    app.debug = True
    app.run()
