from flask import Flask, request, abort
from sqlalchemy import create_engine

APP = Flask(__name__)
DB_ENG = create_engine('mysql+pymysql://srv:yellowDwarf142@localhost/sqrt',
                        pool_recycle=3600)

@APP.route('/')
def index():
    return '<div style="text-align: center;"> <h1>HALLOU!!1 </h1></div> '

@APP.route('/api/getgraph.json')
def getgraph_json():
    with DB_ENG.connect() as con:

        # rs = con.execute('SELECT * FROM users WHERE UserID=' +
        #    request.args.get('user'))

        #data = rs.fetchall()

        print(request)