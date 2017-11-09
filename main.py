import json
from flask import *
from sqlalchemy import create_engine
import ml
from random import choice

APP = Flask(__name__, static_folder='web', static_url_path='')
DB_ENG = create_engine('mysql+pymysql://srv:yellowDwarf142@localhost/sqrt',
                       pool_recycle=3600)

@APP.route('/')
@APP.route('/index.html')
def index():
    return render_template('index.html')


@APP.route('/graph')
def graph():
    return render_template('graph.html')


def get_user_from_qstring():
    try:
        if not request.args.get('user'):
            raise ValueError
        return int(request.args.get('user'))
    except ValueError:
        return -1


@APP.route('/api/getGraph')
def get_graph():
    uid = get_user_from_qstring()
    with DB_ENG.connect() as con:
        if uid == -1:
            abort(400)

        rs = con.execute('SELECT * FROM personal_graphs '
                         'WHERE `userID`=%s', uid)

        links = []
        nodeids = set()
        for row in rs.fetchall():
            links.append({'source': row['node1'], 'target': row['node2'],
                          'value': row['node1'] % 6 + 1})
            nodeids.add(row['node1'])
            nodeids.add(row['node2'])

        if len(nodeids) == 0:
            abort(400)

        rs = con.execute('SELECT NodeID, name FROM nodes '
                         'WHERE `NodeID` in ' + str(tuple(nodeids)) +
                         'ORDER BY NodeID ASC;')
        nodes = []
        for row in rs.fetchall():
            nodes.append({'name': row['name'],
                          'group': row['NodeID'] % 6 + 1})

        return json.dumps({'nodes': nodes, 'links': links})


@APP.route('/api/getAdvices')
def get_advices():
    uid = get_user_from_qstring()
    with DB_ENG.connect() as con:
        rsf = con.execute('SELECT NodeID FROM personal_progress '
                          'WHERE `UserID`=%s AND isCompleted=1', uid).fetchall()
        completed_cources = list(set([x['NodeID'] for x in rsf]))

        data = []
        for i in range(4):
            data.append(choice(completed_cources))
        num = request.args.get('number')
        if not num:
            num = 1

        adv = ml.advice(data, completed_cources, num)

        rsf = con.execute('SELECT name FROM nodes '
                          'WHERE `NodeID` in ' + str(tuple(adv))).fetchall()
        resp = []
        for row in rsf:
            resp.append(row['name'])
        return json.dumps(resp)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
