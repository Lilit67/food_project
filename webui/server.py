from flask import Flask, request, url_for
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine, exc
from flask import jsonify
import sqlite3

"""
1. API to list content 
2. API to search content
3. API get a specific content by id/any identifier

sqlite - get columns listing
PRAGMA table_info(table_name);

"""
# TODO get the hard coded names from outside
# TODO missing api, proper error processing


db_connect = create_engine('sqlite:///../db/recipe.db')
app = Flask(__name__)
api = Api(app)


@app.route("/find/<string:newid>/", methods=['GET'])
def find(newid):
    """
    Find by newid
    :param newid:
    :return:
    """
    conn = db_connect.connect()
    query = conn.execute("select * from documents where newid=%d " % int(newid))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return jsonify(result)


@app.route("/search", methods=['GET'])
def searchby():
    """
    Get content by key:value

    :return:
    """
    sqkey = request.args.get('key', '')
    sqval = request.args.get('val', '')
    conn = db_connect.connect()

    t = (sqval,)

    query = conn.execute('SELECT * FROM documents WHERE {}=?'.format(sqkey), t)
    print(query)
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return jsonify(result)


if __name__ == '__main__':
    app.run(port='5003', debug=True)

