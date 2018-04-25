import pandas as pd
import psycopg2 as pg
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from flask import Flask
import pandas.io.sql as psql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, JSONB
import CreditEvalInquiries
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:peacebro@localhost:5432/frauddb'
db = SQLAlchemy(app)

def get_current_ist_time():
    return maya.now().datetime(to_timezone='Asia/Kolkata', naive=True)

class AuditMixin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.TIMESTAMP, default=get_current_ist_time, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=get_current_ist_time, onupdate=get_current_ist_time, nullable=False)
    # performed_by = db.Column(db.Integer, nullable=True)


class CreditEvalInquiries(AuditMixin):
    __tablename__ = "v3_credit_eval_inquiries_test"

    id =  db.Column(db.Integer,primary_key=True)
    score = db.Column(db.Integer)
    agent_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    model_name = db.Column(db.String())
    policy_codebase = db.Column(db.String())
    scoring_codebase = db.Column(db.String())
    input_data = db.Column(JSONB)
    policy_data = db.Column(JSONB)

db.create_all()

src=create_engine('postgresql://david_reader:iU9oB4DbZy@readonly-mammoth.cej4egpcwxj3.ap-south-1.rds.amazonaws.com:5432/production')
dest=create_engine('postgresql://postgres:peacebro@localhost:5432/frauddb')

query = '''SELECT * FROM "v3_credit_eval_inquiries" LIMIT 10 '''
df=pd.read_sql(query,src)
df.to_sql("v3_credit_eval_inquiries_test",dest, index=False, if_exists='append',dtype = {'input_data':sqlalchemy.types.JSON,'policy_data':sqlalchemy.types.JSON})

#from marvin_oms.templates.models import CreditEvalInquiries
#from marvin_oms.tests.datadict import ddict,



#class dkj(CreditEvalInquiries):
 #   def generate_dummy_property(self):




