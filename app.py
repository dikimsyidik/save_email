import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class Email(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_id = db.Column(db.Integer,unique=True)
  subject = db.Column(db.String(100), unique=True)
  email_content = db.Column(db.String(500))
  time_stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


  def __init__(self,event_id,subject,email_content,time_stamp):
  	self.event_id = event_id
  	self.subject = subject
  	self.email_content = email_content
  	self.time_stamp = time_stamp

class EmailSchema(ma.Schema):
  class Meta:
    fields = ('id','event_id', 'subject', 'email_content', 'time_stamp')

email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)
format = '%d %b %Y %H:%M'

# Post a Product
@app.route('/save_emails', methods=['POST'])
def add_product():
  event_id = request.json['event_id']
  subject = request.json['subject']
  email_content = request.json['email_content']
  time_stamp = datetime.datetime.strptime(request.json['time_stamp'],format)

  new_email = Email(event_id, subject, email_content, time_stamp)

  db.session.add(new_email)
  db.session.commit()

  return email_schema.jsonify(new_email)

if __name__ == '__main__':
	app.run(debug=True)
	pass