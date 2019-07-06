'''
COMP9321 2019 Term 1 Assignment Two Code Template
Student Name:Fengting YANG
Student ID:z5089358
'''
import sqlite3
import sqlalchemy
import urllib.request
import pandas as pd
import json
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api, reqparse, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)
db = SQLAlchemy(app)
parser = reqparse.RequestParser()

parser.add_argument('q', type=str, location='args')

model = api.model("payload", {'indicator_id': fields.String})


class RawData(db.Model):
    __tablename__ = 'rawdata'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    iid = db.Column(db.String(100))
    country = db.Column(db.String(100))
    date = db.Column(db.Integer)
    value = db.Column(db.Float)

    def __init__(self, iid, country, date, value):
        self.iid = iid
        self.country = country
        self.date = date
        self.value = value

    def __repr__(self):
        return 'RawData'


class Collections(db.Model):
    __tablename__ = 'Collections'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creation_time = db.Column(db.DateTime)
    indicator = db.Column(db.String(200))
    indicator_v = db.Column(db.String(200))

    def __init__(self, creation_time, indicator, indicator_v):
        self.creation_time = creation_time
        self.indicator = indicator
        self.indicator_v = indicator_v

    def __repr__(self):
        return 'Collections'

@api.route('/collections', endpoint='ac')
class all_collections(Resource):
    @api.expect(model)
    def post(self):
        iid = request.json['indicator_id']
        if db.session.query(db.exists().where(Collections.indicator == iid)).first()[0]:
            location = db.session.query(Collections.id) \
                .filter_by(indicator=iid).first()
            return {"message": "indicator already exists" \
                       , "location": f"/collections/{location[0]}"}, 200
        data = urllib.request.urlopen(
            f'http://api.worldbank.org/v2/countries/all/indicators/{iid}?date=2013:2018&format=json&per_page=100') \
            .read().decode('utf-8')

        try:
            df = pd.DataFrame(json.loads(data)[1])
        except IndexError:
            return "Indicator does not exist", 404
        df = df[['indicator', 'country', 'date', 'value']]
        df['indicator_v'] = df['indicator'].map(lambda x: x['value'])[0]
        df['indicator'] = df['indicator'].map(lambda x: x['id'])

        df['country'] = df['country'].map(lambda x: x['value'])
        df.index = range(len(df))
        for i in range(len(df)):
            datum = RawData(df['indicator'][i], df['country'][i], int(df['date'][i]), df['value'][i])
            db.session.add(datum)

        creation_time = datetime.datetime.now()
        cdata = Collections(creation_time, iid, df['indicator_v'][0])
        try:
            db.session.add(cdata)
            db.session.flush()
            cid = cdata.id
            db.session.commit()
        except:
            db.session.rollback()
        return {"location": f"/collections/{cid}", \
                "collection_id": cid, \
                "creation_time": str(creation_time), \
                "indicator": iid}, 201

    def get(self):
        result = db.session.query(Collections.id, Collections.creation_time, Collections.indicator) \
            .all()
        df = pd.DataFrame(result)

        return [{"location": f"/collections/{df['id'][e]}", \
                 "collection_id": int(df['id'][e]), \
                 "creation_time": str(df['creation_time'][e]), \
                 "indicator": df['indicator'][e]} for e in df.index], 200


@api.route('/collections/<int:collection_id>', endpoint='oc')
class one_collection(Resource):
    def get(self, collection_id):
        if not db.session.query(db.exists().where(Collections.id == collection_id)).scalar():
            return "Collection does not exist", 404
        collection_record = Collections.query.filter_by(id=collection_id).first()
        data_record = RawData.query.filter_by(iid=collection_record.indicator).all()

        return {"collection_id": collection_record.id, \
                "indicator": collection_record.indicator, \
                "indicator_value": collection_record.indicator_v, \
                "creation_time": str(collection_record.creation_time), \
                "entries": [{"country": e.country, \
                             "date": e.date, \
                             "value": e.value} for e in data_record]}

    def delete(self, collection_id):
        if not db.session.query(db.exists().where(Collections.id == collection_id)).scalar():
            return "Collection does not exist", 404
        collection_record = Collections.query.filter_by(id=collection_id)
        data_record = RawData.query.filter_by(iid=collection_record.first().indicator)
        try:
            data_record.delete()
            collection_record.delete()
            db.session.commit()
        except:
            db.session.rollback()
        return {"message":f"Collection = {collection_id} is removed from the database!"}


@api.route('/collections/<int:collection_id>/<int:year>/<string:country>', endpoint='oy')
class one_year(Resource):
    def get(self, collection_id, year, country):
        if not db.session.query(db.exists().where(Collections.id == collection_id)).scalar():
            return "Collection does not exist", 404
        if not db.session.query(db.exists().where(RawData.date == year)).scalar():
            return "Year does not exist", 404
        if not db.session.query(db.exists().where(RawData.country == country)).scalar():
            return "Country does not exist", 404

        collection_record = Collections.query.filter_by(id=collection_id).first()
        data_record = RawData.query.filter_by(iid=collection_record.indicator) \
            .filter_by(date=year) \
            .filter_by(country=country).first()

        return {"collection_id": collection_id, \
                "indicator": collection_record.indicator, \
                "country": data_record.country, \
                "year": data_record.date, \
                "value": data_record.value}


@api.route('/collections/<int:collection_id>/<int:year>', endpoint='tb')
class top_bottom(Resource):
    def validate(self, q):
        if (not q.startswith('top')) and (not q.startswith('bottom')):
            return False
        try:
            num = int(q.replace("top", "").replace("bottom", ""))
            if num < 1 or num > 100:
                raise ValueError
            return num
        except ValueError:
            return False

    @api.expect(parser)
    def get(self, collection_id, year):
        query_string = parser.parse_args()
        if query_string['q'] == None:
            collection_record = Collections.query.filter_by(id=collection_id).first()
            data_record = RawData.query.filter_by(iid=collection_record.indicator) \
                .filter_by(date=year) \
                .all()
            return {"indicator": collection_record.indicator, \
                    "indicator_value": collection_record.indicator_v, \
                    "entries": [{"country": e.country, \
                                 "date": e.date, \
                                 "value": e.value} for e in data_record]}

        if not self.validate(query_string['q']):
            return "Query string invalid", 404
        num = self.validate(query_string['q'])
        reverse = True if query_string['q'].startswith('bottom') else False
        collection_record = Collections.query.filter_by(id=collection_id).first()
        if not reverse:
            data_record = RawData.query.filter_by(iid=collection_record.indicator) \
                .filter_by(date=year) \
                .order_by("-value").limit(num).all()
        else:
            data_record = RawData.query.filter_by(iid=collection_record.indicator) \
                .filter_by(date=year) \
                .order_by("value").limit(num).all()
        return {"indicator": collection_record.indicator, \
                "indicator_value": collection_record.indicator_v, \
                "entries": [{"country": e.country, \
                             "date": e.date, \
                             "value": e.value} for e in data_record]}


def create_db(db_file):
    '''
    uase this function to create a db, don't change the name of this function.
    db_file: Your database's name.
    '''
    try:
        conn = sqlite3.connect("data.db")
        db.create_all()
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    create_db('foo.db')
    app.run(debug=True)
