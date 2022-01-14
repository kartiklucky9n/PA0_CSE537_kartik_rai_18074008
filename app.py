from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from datetime import datetime
app = Flask (__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cipher.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cipher(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    '''
    cipher = Cipher(title = "code", desc="now")
    db.session.add(cipher)
    db.session.commit()
    '''
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        title  = Cipher(title = title, desc = desc)
        db.session.add(title)
        db.session.commit()

    allCiphers = Cipher.query.all()

    return render_template("home.html", allCiphers=allCiphers)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if(request.method=="POST"):
        title = request.form['title']
        desc = request.form['desc']
        allCiphers = Cipher.query.filter_by(sno=sno).first()
        allCiphers.title = title
        allCiphers.desc = desc
        db.session.add(allCiphers)
        db.session.commit()
        return redirect("/")
        
    allCiphers = Cipher.query.filter_by(sno=sno).first()
    return render_template("update.html", allCiphers=allCiphers)

@app.route('/delete/<int:sno>')
def delete(sno):
    allCiphers = Cipher.query.get(sno)
    db.session.delete(allCiphers)
    db.session.commit()
    return redirect("/")
    
@app.route("/show")
def crpyto():
    allCiphers = Cipher.query.all()
    print(allCiphers)
    return "chal gaya"
if __name__ == "__main__":
    app.run(debug=True)