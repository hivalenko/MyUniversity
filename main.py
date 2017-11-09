import json
from flask import *
from sqlalchemy import create_engine

APP = Flask(__name__)
DB_ENG = create_engine('mysql+pymysql://srv:yellowDwarf142@localhost/sqrt',
                       pool_recycle=3600)


@APP.route('/')
def index():
    return redirect('/static/MyUniversity.html')


def need_user():
    def wrapper():
        try:
            if not request.args.get('user'):
                raise ValueError
            int(request.args.get('user'))
        except ValueError:
            abort(400)



@APP.route('/api/getGraph.json')
def getgraph_json():
    with DB_ENG.connect() as con:
        uid = int(request.args.get('user'))

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


@APP.route('/api/getCompletedCourses.json')
def getcompletedcourses_json():
    pass



if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
