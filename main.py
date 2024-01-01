from flask import request
from flask import Flask,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy import create_engine
from flask import render_template
from sqlalchemy import or_,and_

app = Flask(__name__)
app.secret_key = "abc" 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

class College(db.Model):
  __tablename__='college'
  cid=db.Column(db.Integer,primary_key=True)
  college_code=db.Column(db.String)
  college_name=db.Column(db.String)
  
class Branch(db.Model):
  __tablename__='branch'
  bid=db.Column(db.Integer,primary_key=True)
  branch_code=db.Column(db.String)
  branch_name=db.Column(db.String)

class Allotment(db.Model):
  __tablename__='allotment'
  aid=db.Column(db.Integer,primary_key=True)
  college_code=db.Column(db.String)
  branch_code=db.Column(db.String)
  category=db.Column(db.String)
  rank=db.Column(db.Integer)
engine= create_engine("sqlite:///database.db")
db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():   
    return render_template("home.html")

@app.route("/result",methods=["GET","POST"])
def result():
    if request.method=='POST':
      rank=request.form.get('rank')
      category=request.form.get('cat')
      college_details=College.query.all()
      branch_details=Branch.query.all()
      res=Allotment.query.filter(and_(Allotment.rank>=rank,Allotment.category==category)).all()
      a=request.form.get('any')
      if int(rank)<=0:
        flash("Rank should be greater than 0",'error')  
        return redirect(url_for('home'))
      if category==None:
        flash("Provide your category",'error')  
        return redirect(url_for('home'))
      
      if a=='Y': 
        branch=request.form.getlist('bcode')
        fres=[]
        for b in branch:
          for r in res:
              if r.branch_code==b:
                fres.append(r)
        return render_template("result.html",result=fres,cdetails=college_details,bdetails=branch_details,rank=rank,category=category)
      
      return render_template("result.html",result=res,cdetails=college_details,bdetails=branch_details,rank=rank,category=category)
    return render_template("home.html")
if __name__ == '__main__':
  app.run(host='0.0.0.0')
