from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from datetime import datetime
app = Flask (__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cipher.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Model for storing data (on requirement)
class Cipher(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

#Encyption key, used both for encryption and decryption
def encyptKey(myString):
    my=list(myString)
    b=[]
    for i in range(0,len(myString)):
        c=ord(my[i])
        print(chr(95+26-(c-95)))
        b.append(chr(95+26-(c-95)))
    b="".join(b)
    return b

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
   
    #variable i for making decision and input for encipher and decipher
    i=-1 
    return render_template("home.html",  i=i)

#Encrpt the input text
@app.route('/encipher', methods=['GET', 'POST'])
def encipher():
    if(request.method=="POST"):
        text = request.form['text1']
        etext = encyptKey(text)
        myCipher = Cipher(title=text, desc = etext)
        i=1
        return render_template("home.html", myCipher = myCipher, i=i)
    return redirect("/")

#Decrypt the input text
@app.route('/decipher', methods=['GET', 'POST'])
def decipher():
    if(request.method=="POST"):
        etext = request.form['text2']
        text = encyptKey(etext)
        myCipher = Cipher(title=text, desc = etext)
        i=0
        return render_template("home.html", myCipher = myCipher, i=0)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)